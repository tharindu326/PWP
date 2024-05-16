
from werkzeug.routing import BaseConverter
import re
from functools import wraps
from config import cfg
import numpy as np
import cv2 
import os
import time
from face_engine.detector import Inference
from flask import request
from services.access_log_service import add_access_log
from services.access_request_service import log_access_request
from mason import create_error_response
from face_engine.classifier import Classifier
from services.user_service import get_user_profile, update_user_name, update_user_facial_data, add_user
from services.permission_service import add_permission_to_user, validate_access_for_user


inference = Inference()
VALID_API_KEYS = cfg.app.VALID_API_KEYS
classifier = Classifier()


class NameConverter(BaseConverter):
    def to_python(self, user_name):
        # if '/' in user_name or '?' in user_name:
        #     return ValueError('Special characters (?, /) cannot be included in the input data')
        # if not_string(user_name):
        #     return ValueError('Numbers and special characters are not allowed in name')
        user_name = format_name(user_name)
        return user_name
    def to_url(self, user_name):
        return user_name
    
    
def format_name(name):
    """
    Format a name to have capitalized words.
    Args:
        name (str): The name to format.
    Returns:
        str: The formatted name with capitalized words.
    """
    name_parts = name.split()
    capitalized_name_parts = [part.capitalize() for part in name_parts]
    capitalized_name = ' '.join(capitalized_name_parts)
    return capitalized_name

def require_api_key(function):
    """
    Decorator that requires an API key to access the wrapped function.
    Args:
        function (callable): The function to be decorated.
    Returns:
        callable: The decorated function with API key requirement.
    """
    @wraps(function)
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get('Authorization')
        if not api_key:
            return create_error_response(400, title="MissingAPIKey",
                                         message='API Key is missing')

        elif api_key not in VALID_API_KEYS:
            return create_error_response(401, title="Unauthorized",
                                         message='Invalid API Key')
        return function(*args, **kwargs)
    return decorated_function


def allowed_file(filename):
    """
    Check if the filename has an allowed extension.
    Args:
        filename (str): The name of the file to check.
    Returns:
        bool: True if the file has an allowed extension, False otherwise.
    """
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in cfg.app.allowed_extensions


def not_string(string):
    """
    Check if the string contains only alphabetic characters and spaces.
    Args:
        string (str): The string to check.
    Returns:
        bool: True if the string contains non-alphabetic characters, False otherwise.
    """
    return bool(re.search(r'[^a-zA-Z\s]', string))


def query_key(*args, **kwargs):
    """
    Generate a cache key based on the request's full path.
    Args:
        *args: Additional arguments.
        **kwargs: Additional keyword arguments.
    Returns:
        str: The cache key based on the request's full path.
    """
    return request.full_path

def process_access_request(file, associated_permission):
    """
    Handle an access request by verifying the user identity and permissions.
    Args:
        files (werkzeug.datastructures.FileStorage): The file storage object containing the uploaded image file.
        associated_permission (str): The permission level required for access.
    Returns:
        dict: A dictionary containing 'access', 'user_id', and 'access_request_id' if successful.
        Response: A Flask Response object containing an error message if any error occurs.
    """
    if 'image' not in file:
        return create_error_response(400, title="MissingData", message='No image part in the request')

    file = file['image']
    if file.filename == '':
        return create_error_response(400, title="MissingData", message='No selected image file')

    if not allowed_file(file.filename):
        return create_error_response(415, title="UnsupportedMediaType", message=f'file type: {file.filename.split(".")[-1]} not allowed')

    if not associated_permission:
        return create_error_response(400, title="MissingData", message='Associated permission is required')

    if associated_permission.lower() not in cfg.permission.user_permission_levels:
        return create_error_response(400, title="InvalidInputData", message=f'Invalid permission level: {associated_permission.lower()}. Use valid permission levels: {cfg.permission.user_permission_levels}')
    
    blobData = file.read()
    img = cv2.imdecode(np.frombuffer(blobData, np.uint8), cv2.IMREAD_COLOR)
    frame_out, boxes, _, _ = inference.infer(img)
    if len(boxes) == 0:
        return create_error_response(500, title="NotFound", message='No face detected from the image')

    x, y, w, h = [int(item) for item in boxes[0]]
    cropped_face = frame_out[y: y + h, x: x + w]
    face_encode = classifier.reco.encode(cropped_face)
    user_id = int(classifier.clf.predict([face_encode])[0])
    probability = classifier.clf.predict_proba([face_encode])[0][int(user_id) - 1]

    print(f'Recognized user: {user_id} | probability: {probability} | required minimal permission: {associated_permission} | prob_threshold: {cfg.recognizer.threshold}')
    if not probability > cfg.recognizer.threshold:
        return create_error_response(401, title="NotRecognized", message='user not recognized. Access denied')

    access = validate_access_for_user(user_id, associated_permission)
    access_request_id = log_access_request(user_id, associated_permission, associated_facial_data=blobData, outcome=access)
    add_access_log(access_request_id, details=None)

    return {
        'access': access,
        'user_id': user_id,
        'access_request_id': access_request_id
    }
            
            
def update_user_details(user_id, name, permissions_list, files, cache):
    """
    Partially update the details of an existing user.
    Args:
        user_id (int): The ID of the user to update.
        name (str, optional): The new name of the user.
        permissions_list (list, optional): List of new permission levels for the user.
        files (werkzeug.datastructures.FileStorage, optional): The file storage object containing the uploaded image files.
    Returns:
        dict: A dictionary containing flags 'is_name', 'is_permission', and 'is_file' indicating what was updated.
        Response: A Flask Response object containing an error message if any error occurs.
    """
    is_name = False
    is_permission = False
    is_file = False

    if name:
        if not_string(name):
            return create_error_response(400, title="InvalidInputData", message='Numbers and special characters are not allowed in name')
        name = format_name(name)
        is_name = True

    if permissions_list:
        if not isinstance(permissions_list, list):
            return create_error_response(400, title="InvalidInputData", message='Permissions need to be a list')
        for user_permission in permissions_list:
            if user_permission.lower() not in cfg.permission.user_permission_levels:
                return create_error_response(400, title="InvalidInputData", message=f'Invalid permission level: {user_permission.lower()}. Use valid permission levels: {cfg.permission.user_permission_levels}')
        is_permission = True

    if files:
        if not any(file.filename == '' for file in files):
            for file in files:
                if not allowed_file(file.filename):
                    return create_error_response(415, title="UnsupportedMediaType", message=f'File type: {file.filename} is not allowed. Allowed types are: png, jpg, jpeg')
        user = get_user_profile(user_id)
        if user is None:
            return create_error_response(404, title="NotFound", message=f'User: {user_id} not found')
        is_file = True

    if is_permission:
        for user_permission in permissions_list:
            add_permission_to_user(user_id, user_permission.lower())

    if is_name:
        _ = update_user_name(user_id, name)

    if is_file:
        update_user_blob = False
        user_folder = os.path.join(cfg.db.database, str(user_id))
        for i, file in enumerate(files):
            blobData = file.read()
            if not update_user_blob:
                update_user_facial_data(user_id, blobData)
                update_user_blob = True
    
            img = cv2.imdecode(np.frombuffer(blobData, np.uint8), cv2.IMREAD_COLOR)
            frame_out, boxes, _, _ = inference.infer(img)
            for idx, box in enumerate(boxes):
                x, y, w, h = [int(item) for item in box]
                cropped_face = frame_out[y: y + h, x: x + w]
                cropped_face_path = os.path.join(user_folder, f'face_{i + len(os.listdir(user_folder)) + 1}_{idx}.jpg')
                os.makedirs(os.path.dirname(cropped_face_path), exist_ok=True)
                cv2.imwrite(cropped_face_path, cropped_face)
        
        # Clear cache for the updated user profile
        cache.delete(f"user_profile_{user_id}")

    return {
        'is_name': is_name,
        'is_permission': is_permission,
        'is_file': is_file
    }
            
            
def register_new_user(name, files, permissions_list):
    """
    Register a new user by uploading an image and assigning permissions.

    Args:
        name (str): The name of the user.
        files (werkzeug.datastructures.FileStorage): The file storage object containing the uploaded image files.
        permissions_list (list): List of permission levels for the user.

    Returns:
        dict: A dictionary containing 'name' and 'user_id' if successful.
        Response: A Flask Response object containing an error message if any error occurs.
    """
    if not name:
        return create_error_response(400, title="MissingData", message='Name is required')
    if not_string(name):
        return create_error_response(400, title="InvalidInputData", message='Numbers and special characters are not allowed in name')
    
    name = format_name(name)
    
    if not files:
        return create_error_response(400, title="MissingData", message='No image part in the request')

    for file in files:
        if not allowed_file(file.filename):
            return create_error_response(415, title="UnsupportedMediaType", message=f'File type: {file.filename} is not allowed. Allowed types are: png, jpg, jpeg')

    if not permissions_list:
        return create_error_response(400, title="InvalidInputData", message='Please provide associated permission levels for the user')
    
    if not isinstance(permissions_list, list):
        return create_error_response(400, title="InvalidInputData", message='Permissions need to be a list')

    for user_permission in permissions_list:
        if user_permission.lower() not in cfg.permission.user_permission_levels:
            return create_error_response(400, title="InvalidInputData", message=f'Invalid permission level: {user_permission.lower()}. Use valid permission levels: {cfg.permission.user_permission_levels}')

    user_id = None
    for i, file in enumerate(files):
        blobData = file.read()
        img = cv2.imdecode(np.frombuffer(blobData, np.uint8), cv2.IMREAD_COLOR)
        frame_out, boxes, _, _ = inference.infer(img)
        for idx, box in enumerate(boxes):
            x, y, w, h = [int(item) for item in box]
            cropped_face = frame_out[y: y + h, x: x + w]
            if user_id is None:
                os.makedirs('temp/', exist_ok=True)
                temp_im = f'temp/{time.monotonic()}.jpg'
                cv2.imwrite(temp_im, cropped_face)
                with open(temp_im, 'rb') as f:
                    Bim = f.read()
                    user_id = add_user(name, Bim)
                os.remove(temp_im)
            cropped_face_path = os.path.join(cfg.db.database, str(user_id), f'face_{i}_{idx}.jpg')
            os.makedirs(os.path.dirname(cropped_face_path), exist_ok=True)
            cv2.imwrite(cropped_face_path, cropped_face)

    for user_permission in permissions_list:
        add_permission_to_user(user_id, user_permission.lower())

    classifier.get_user_embeddings(user_id)
    classifier.save_embeddings()
    if len(os.listdir(cfg.db.database)) > 1:
        classifier.train()

    return {
        'name': name,
        'user_id': user_id
    }