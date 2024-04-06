import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import time
from flask import Flask, request, jsonify, make_response, render_template
from config import cfg
from services.access_log_service import add_access_log, get_user_access_logs
from services.access_request_service import log_access_request
from services.permission_service import add_permission_to_user, validate_access_for_user
from services.user_service import delete_user_profile, get_user_profile, update_user_facial_data, add_user, \
    get_users_by_name, update_user_name
import numpy as np
import cv2
from face_engine.detector import Inference
from face_engine.classifier import Classifier
from werkzeug.routing import BaseConverter, ValidationError
import re
from flask_caching import Cache
from functools import wraps
from flasgger import Swagger, swag_from
from database_models import db

inference = Inference()
classifier = Classifier()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = cfg.db.SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = cfg.db.SQLALCHEMY_TRACK_MODIFICATIONS
app.config['UPLOAD_FOLDER'] = cfg.db.database
app.config['CACHE_TYPE'] = 'FileSystemCache'
app.config['CACHE_DIR'] = 'cache_data'
app.config['CACHE_DEFAULT_TIMEOUT'] = 0
app.config["SWAGGER"] = {
                            "openapi": "3.0.3",
                            "uiversion": 3,
                            "specs_route": "/apidocs/",
                            "doc_dir": "docs/",
                            'info': {
                                    'title': 'FacePass',
                                    'version': '1.0',
                                    'description': 'Access management API',
                                },
                            'components': {
                                    'securitySchemes': {
                                        'ApiKeyAuth': {
                                            'type': 'apiKey',
                                            'in': 'header',
                                            'name': 'Authorization'
                                        }
                                    }
                                }
                        }
swagger = Swagger(app)

cache = Cache(app)
db.init_app(app)
os.makedirs(app.config['CACHE_DIR'], exist_ok=True)

VALID_API_KEYS = cfg.app.VALID_API_KEYS


def require_api_key(function):
    @wraps(function)
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get('Authorization')
        if not api_key:
            return jsonify({"error": "API Key is missing"}), 400
        elif api_key not in VALID_API_KEYS:
            return jsonify({"error": "Invalid API Key."}), 401
        return function(*args, **kwargs)
    return decorated_function


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in cfg.app.allowed_extensions


def not_string(string):
    return bool(re.search(r'[^a-zA-Z\s]', string))


def format_name(name):
    name_parts = name.split()
    capitalized_name_parts = [part.capitalize() for part in name_parts]
    capitalized_name = ' '.join(capitalized_name_parts)

    return capitalized_name


def query_key(*args, **kwargs):
    return request.full_path


class NameConverter(BaseConverter):
    def to_python(self, user_name):
        if '/' in user_name or '?' in user_name:
            raise ValidationError
        if not_string(user_name):
            return jsonify({'error': 'Numbers and special characters are not allowed in name'}), 400
        user_name = format_name(user_name)
        return user_name

    def to_url(self, user_name):
        return user_name


@app.route('/identities/register', methods=['POST'])
@require_api_key
@swag_from("docs/register.yaml")
def register_person():
    name = request.form.get('name')
    if not name:
        return jsonify({'error': 'Name is required'}), 400
    if not_string(name):
        return jsonify({'error': 'Numbers and special characters are not allowed in name'}), 400
    else:
        name = format_name(name)

    if 'image' not in request.files:
        return jsonify({'error': 'No image part in the request'}), 400

    files = request.files.getlist('image')
    if not files or any(file.filename == '' for file in files):
        return jsonify({'error': 'No image file/files provided'}), 400
    else:
        for file in files:
            if not file or not allowed_file(file.filename):
                return jsonify(
                    {'error': f'File type: {file.filename} is not allowed. Allowed types are: png, jpg, jpeg'}), 400

    permissions_list = request.form.getlist('permission')

    if not permissions_list:
        return jsonify({'error': 'please provide associated permission levels for the user'}), 400
    else:
        if not isinstance(permissions_list, list):
            return jsonify({'error': 'permissions needed to be a list'}), 400
        else:
            for user_permission in permissions_list:
                if user_permission.lower() not in cfg.permission.user_permission_levels:
                    return jsonify({'error': f'Invalid permission level: {user_permission.lower()}. Use valid permission levels: '
                                             f'{cfg.permission.user_permission_levels}'}), 400
    user_id = None
    for i, file in enumerate(files):
        blobData = file.read()
        try:
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
                cropped_face_path = os.path.join(app.config['UPLOAD_FOLDER'], str(user_id), f'face_{i}_{idx}.jpg')
                os.makedirs(os.path.dirname(cropped_face_path), exist_ok=True)
                cv2.imwrite(cropped_face_path, cropped_face)
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': f'An error occurred: {str(e)}'}), 500

    # add permissions
    for user_permission in permissions_list:
        add_permission_to_user(user_id, user_permission.lower())
    # update model with new user
    classifier.get_user_embeddings(user_id)
    classifier.save_embeddings()
    classifier.train()
    return jsonify({'message': f'User {name} registered successfully with ID {user_id}'}), 201


@app.route('/identities/<int:user_id>/profile', methods=['GET'])
@require_api_key
@swag_from("docs/get_by_id.yaml")
def get_profile(user_id):
    cache_key = f"user_profile_{user_id}"
    cached_response = cache.get(cache_key)
    if cached_response:
        response = make_response(cached_response)
        response.headers['Cache'] = 'HIT'
    else:
        user_profile = get_user_profile(user_id)
        if not user_profile:
            return jsonify({'error': 'User not found'}), 404
        # user_permissions = get_user_permissions(user_id)
        # permission_list = [user_permission.permission_level for user_permission in user_permissions]
        #
        # return jsonify({
        #     'name': user_profile.name,
        #     'permissions': permission_list
        # })
        response_data = jsonify(user_profile.to_dict())
        response = make_response(response_data)
        response.headers['Cache'] = 'MISS'
        cache.set(cache_key, response_data)
    return response, 200


@app.route('/identities/<int:user_id>/update', methods=['PUT'])
@require_api_key
@swag_from("docs/update.yaml")
def update_user(user_id):
    is_name = False
    is_permission = False
    is_file = False
    files = []
    name = request.form.get('name')
    if name:
        if not_string(name):
            return jsonify({'error': 'Numbers and special characters are not allowed in name'}), 400
        else:
            name = format_name(name)
            is_name = True

    permissions_list = request.form.getlist('permission')

    if permissions_list:
        if not isinstance(permissions_list, list):
            return jsonify({'error': 'permissions needed to be a list'}), 400
        else:
            for user_permission in permissions_list:
                if user_permission.lower() not in cfg.permission.user_permission_levels:
                    return jsonify(
                        {'error': f'Invalid permission level: {user_permission.lower()}. Use valid permission levels: '
                                  f'{cfg.permission.user_permission_levels}'}), 400
            is_permission = True

    if 'image' in request.files:
        files = request.files.getlist('image')
        if not any(file.filename == '' for file in files):
            for file in files:
                if not allowed_file(file.filename):
                    return jsonify(
                        {'error': f'File type: {file.filename} is not allowed. Allowed types are: png, jpg, jpeg'}), 400
        else:
            return jsonify({'error': 'No image file/files provided'}), 400
        user = get_user_profile(user_id)
        if not user:
            return jsonify({f'error': f'User: {user_id} not found'}), 404
        is_file = True

    # update permissions
    # revoke_user_permissions(user_id)  # this will revoke all since no specific permission provided
    if is_permission:
        for user_permission in permissions_list:
            add_permission_to_user(user_id, user_permission.lower())

    if is_name:
        _ = update_user_name(user_id, name)

    if is_file:
        update_user_blob = False
        user_folder = os.path.join(app.config['UPLOAD_FOLDER'], str(user_id))
        for i, file in enumerate(files):
            blobData = file.read()
            if not update_user_blob:
                update_user_facial_data(user_id, blobData)
                update_user_blob = True
            try:
                img = cv2.imdecode(np.frombuffer(blobData, np.uint8), cv2.IMREAD_COLOR)
                frame_out, boxes, _, _ = inference.infer(img)
                for idx, box in enumerate(boxes):
                    x, y, w, h = [int(item) for item in box]
                    cropped_face = frame_out[y: y + h, x: x + w]
                    cropped_face_path = os.path.join(user_folder,
                                                     f'face_{i + len(os.listdir(user_folder)) + 1}_{idx}.jpg')
                    os.makedirs(os.path.dirname(cropped_face_path), exist_ok=True)
                    cv2.imwrite(cropped_face_path, cropped_face)
            except Exception as e:
                db.session.rollback()
                return jsonify({'error': f'An error occurred: {str(e)}'}), 500

        # Clear cache for the updated user profile
        cache.delete(f"user_profile_{user_id}")
        return jsonify({'message': f'User:{user_id} updated successfully'}), 200

    else:
        if not is_name and not is_permission:
            return jsonify({'error': f'No data for user:{user_id} to updated'}), 404


@app.route('/identities/access-request', methods=['POST'])
@require_api_key
@swag_from("docs/access_request.yaml")
def handle_access_request():
    if 'image' not in request.files:
        return jsonify({'error': 'No image part in the request'}), 400

    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'No selected image file'}), 400
    if not allowed_file(file.filename):
        return jsonify({'error': f'file type: {file.filename.split(".")[-1]} not allowed'}), 400
    associated_permission = request.form.get('associated_permission')
    if not associated_permission:
        return jsonify({'error': 'Associated permission is required'}), 400
    if associated_permission.lower() not in cfg.permission.user_permission_levels:
        return jsonify({'error': f'Invalid permission level: {associated_permission.lower()}. Use valid permission levels: '
                                 f'{cfg.permission.user_permission_levels}'}), 400
    if file and allowed_file(file.filename):
        blobData = file.read()
        try:
            img = cv2.imdecode(np.frombuffer(blobData, np.uint8), cv2.IMREAD_COLOR)
            frame_out, boxes, _, _ = inference.infer(img)
            if len(boxes) != 0:
                x, y, w, h = [int(item) for item in boxes[0]]
                cropped_face = frame_out[y: y + h, x: x + w]
                face_encode = classifier.reco.encode(cropped_face)
                user_id = classifier.clf.predict([face_encode])[0]
                probability = classifier.clf.predict_proba([face_encode])[0][int(user_id) - 1]
                print(f'Recognized user: {user_id} | probability: {probability} | required minimal permission: '
                      f'{associated_permission} | prob_threshold: {cfg.recognizer.threshold}')
                if not probability > cfg.recognizer.threshold:
                    return jsonify(
                        {'error': f'user not recognized. Access denied'}), 401
                access = validate_access_for_user(user_id, associated_permission)
                access_request_id = log_access_request(user_id, associated_permission, associated_facial_data=blobData,
                                                       outcome=access)
                add_access_log(access_request_id, details=None)

                if access:
                    return jsonify({'message': f'user: {user_id} access granted successfully'}), 201
                else:
                    return jsonify({'message': f'user: {user_id} does not have permission. Access declined'}), 403
            else:
                return jsonify({'error': f'No face detected from the image'}), 500
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': f'An error occurred: {str(e)}'}), 500
    else:
        return jsonify({'error': f'File type: {file.filename} is not allowed. Allowed types are: png, jpg, jpeg'}), 400


app.url_map.converters['name'] = NameConverter


@app.route('/identities/<name:user_name>/profile', methods=['GET'])
@require_api_key
@cache.cached(key_prefix=query_key)
@swag_from("docs/get_by_name.yaml")
def get_users(user_name):
    users = get_users_by_name(user_name)
    if not users:
        return jsonify({'error': 'No users in that name'}), 404
    return jsonify([user.to_dict() for user in users])


@app.route('/identities/<int:user_id>/delete', methods=['DELETE'])
@require_api_key
@swag_from("docs/delete.yaml")
def delete_identity(user_id):
    user = get_user_profile(user_id)
    if user is None:
        return jsonify({"error": "User not found"}), 404

    if delete_user_profile(user_id):
        return jsonify({"message": f"User {user_id} deleted successfully"}), 200


@app.route('/access-log/<int:user_id>', methods=['GET'])
@require_api_key
@swag_from("docs/get_access_logs.yaml")
def get_access_logs(user_id):
    user = get_user_profile(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    access_logs = get_user_access_logs(user_id)
    return jsonify([access_log.to_dict() for access_log in access_logs]), 200


@app.route('/tos')
def terms_of_service():
    # template taken from https://www.gnu.org/licenses/gpl-3.0.en.html
    return render_template('tos.html')


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        # main()
    app.run(host=cfg.app.host, port=cfg.app.port, debug=False)

