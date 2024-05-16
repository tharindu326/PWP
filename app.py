import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from flask import Flask, request, jsonify, render_template, Response
from config import cfg
from services.access_log_service import add_access_log, get_user_access_logs, get_access_log
from services.access_request_service import log_access_request, get_user_access_requests, get_access_request
from services.permission_service import add_permission_to_user, validate_access_for_user, get_user_permissions
from services.user_service import delete_user_profile, get_user_profile, update_user_facial_data, \
    get_users_by_name, update_user_name
import numpy as np
import cv2
from face_engine.classifier import Classifier
from utils import *
from flask_caching import Cache
from flasgger import Swagger
from database_models import db
from mason import IdentityBuilder, create_error_response, MASON
import json

classifier = Classifier()


def create_app():
    """
    Create and configure the Flask application.
    Configures the database, caching, URL converters, and Swagger for API documentation.
    Returns:
        app (Flask): The configured Flask application.
    """
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = cfg.db.SQLALCHEMY_DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = cfg.db.SQLALCHEMY_TRACK_MODIFICATIONS
    app.config['UPLOAD_FOLDER'] = cfg.db.database
    app.config['CACHE_TYPE'] = 'FileSystemCache'
    app.config['CACHE_DIR'] = 'cache_data'
    app.config['CACHE_DEFAULT_TIMEOUT'] = 0
    app.url_map.converters['name'] = NameConverter

    app.config['SWAGGER'] = {
        "openapi": "3.0.3",
        "uiversion": 3,
        "specs_route": "/apidocs/",
        "doc_dir": "docs/",
    }
    db.init_app(app)
    return app


app = create_app()
swagger = Swagger(app, template_file='docs/FacePass.yaml')
cache = Cache(app)
os.makedirs(app.config['CACHE_DIR'], exist_ok=True)
LINK_RELATIONS_URL = "/face_pass/link-relations#"
PROFILE_URL = '/face_pass/profile'


@app.route('/identities', methods=['POST'], endpoint='register')
@require_api_key
def register_person():
    """
    Register a new user by uploading an image and assigning permissions.
    Request Form Parameters:
        - name (str): The name of the user.
        - image (file): The image file of the user.
        - permission (list): List of permission levels for the user.
    Returns:
        Response: A JSON response with the user registration status and details.
    """
    
    name = request.form.get('name')
    files = request.files.getlist('image') if 'image' in request.files else []
    permissions_list = request.form.getlist('permission')

    try:
        result = register_new_user(name, files, permissions_list)
    except Exception as e:
        db.session.rollback()
        return create_error_response(500, title="ServerError", message=f'An error occurred: {str(e)}')
    if isinstance(result, Response):
        return result

    name = result['name']
    user_id = result['user_id']

    builder = IdentityBuilder()
    builder.add_namespace("FacePass", LINK_RELATIONS_URL)
    builder.add_control("self", href=request.path)
    builder.add_control("profile", href=PROFILE_URL)
    builder.add_control_get(user_id=user_id)
    builder.add_control_update(user_id=user_id)
    builder.add_control_delete(user_id=user_id)
    builder.add_control_access_request(user_id=user_id)
    builder.add_control_permissions(user_id=user_id)
    builder.add_control_access_logs(user_id=user_id)
    builder['message'] = f'User {name} registered successfully with ID {user_id}'
    return Response(json.dumps(builder), status=201, mimetype=MASON)


@app.route('/identities/<int:user_id>', methods=['GET'], endpoint='get_by_id')
@require_api_key
def get_profile(user_id):
    """
    Retrieve the profile of an existing user.
    URL Parameters:
        - user_id (int): The ID of the user to retrieve the profile for.
    Returns:
        Response: A JSON response with the user profile details.
    """
    
    cache_key = f"user_profile_{user_id}"
    cached_response = cache.get(cache_key)
    if cached_response:
        response = cached_response.data.decode("utf-8")
        cached = 'HIT'
    else:
        user_profile = get_user_profile(user_id)
        if user_profile is None:
            return create_error_response(404, title="NotFound", message='User not found')
        # user_permissions = get_user_permissions(user_id)
        # permission_list = [user_permission.permission_level for user_permission in user_permissions]
        #
        # return jsonify({
        #     'name': user_profile.name,
        #     'permissions': permission_list
        # })
        response = user_profile.to_dict()
        cached = "MISS"
        cache.set(cache_key, jsonify(response))

    builder = IdentityBuilder()
    builder.add_namespace("FacePass", LINK_RELATIONS_URL)
    builder.add_control("self", href=request.path)
    builder.add_control("profile", href=PROFILE_URL)
    builder.add_control_update(user_id=user_id)
    builder.add_control_delete(user_id=user_id)
    builder.add_control_access_request(user_id=user_id)
    builder.add_control_permissions(user_id=user_id)
    builder.add_control_access_logs(user_id=user_id)
    builder['message'] = response  # json.loads(response)
    return Response(json.dumps(builder), status=200, mimetype=MASON, headers={'Cache': cached})


@app.route('/identities/<int:user_id>', methods=['PUT'], endpoint='update')
@require_api_key
def update_user(user_id):
    """
    Partially update the details of an existing user.
    URL Parameters:
        - user_id (int): The ID of the user to update.
    Request Form Parameters (optional):
        - name (str): The new name of the user.
        - image (file): The new image file of the user.
        - permission (list): List of new permission levels for the user.
    Returns:
        Response: A JSON response with the user partial update status and details.
    """
    name = request.form.get('name')
    permissions_list = request.form.getlist('permission')
    files = request.files.getlist('image') if 'image' in request.files else []

    try:
        result = update_user_details(user_id, name, permissions_list, files, cache)
    except Exception as e:
        db.session.rollback()
        return create_error_response(500, title="ServerError", message=f'An error occurred: {str(e)}')
    if isinstance(result, Response):
        return result

    is_name = result['is_name']
    is_permission = result['is_permission']
    is_file = result['is_file']

    if is_name or is_permission or is_file:
        builder = IdentityBuilder()
        builder.add_namespace("FacePass", LINK_RELATIONS_URL)
        builder.add_control("self", href=request.path)
        builder.add_control("profile", href=PROFILE_URL)
        builder.add_control_delete(user_id=user_id)
        builder.add_control_update(user_id=user_id)
        builder.add_control_access_request(user_id=user_id)
        builder.add_control_permissions(user_id=user_id)
        builder.add_control_access_logs(user_id=user_id)
        builder['message'] = f'User:{user_id} partially updated successfully'
        return Response(json.dumps(builder), status=200, mimetype=MASON)
    else:
        return create_error_response(404, title="NotFound", message=f'No data for user:{user_id} to update')

@app.route('/identities/access-request', methods=['POST'], endpoint='access_request')
@require_api_key
def handle_access_request():
    """
    Handle an access request by verifying the user identity and permissions.
    Request Form Parameters:
        - image (file): The image file of the user.
        - associated_permission (str): The permission level required for access.
    Returns:
        Response: A JSON response with the access request status and details.
    """
    file = request.files
    associated_permission = request.form.get('associated_permission')

    try:
        result = process_access_request(file, associated_permission)
    except Exception as e:
        db.session.rollback()
        return create_error_response(500, title="ServerError", message=f'An error occurred: {str(e)}')
    if isinstance(result, Response):
        return result

    access = result['access']
    user_id = result['user_id']
    access_request_id = result['access_request_id']

    if access:
        builder = IdentityBuilder()
        builder.add_namespace("FacePass", LINK_RELATIONS_URL)
        builder.add_control("self", href=request.path)
        builder.add_control("profile", href=PROFILE_URL)
        builder.add_control_access_by(user_id=user_id)
        builder.add_control_log(log_id=access_request_id)
        builder['message'] = f'User {user_id} access granted successfully'
        return Response(json.dumps(builder), status=201, mimetype=MASON)
    else:
        return create_error_response(403, title="NotAuthorized", message=f'user: {user_id} does not have permission. Access declined')
    
@app.route('/identities/name/<name:user_name>', methods=['GET'], endpoint='get_by_name')
@require_api_key
@cache.cached(key_prefix=query_key)
def get_users(user_name):
    """
    Retrieve users by name.
    URL Parameters:
        - user_name (str): The name of the users to retrieve.
    Returns:
        Response: A JSON response with the list of users matching the name.
    """
    
    users = get_users_by_name(user_name)
    if len(users) == 0:
        return create_error_response(404, title="NotFound", message=f'No users in that name {user_name}')
    builder = IdentityBuilder()
    builder.add_namespace("FacePass", LINK_RELATIONS_URL)
    builder.add_control("profile", href=PROFILE_URL)
    builder.add_control("self", href=request.path)
    for user in users:
        builder.add_control_delete(user_id=user.id)
        builder.add_control_access_logs(user_id=user.id)
        builder.add_control_update(user_id=user.id)
        builder.add_control_access_request(user_id=user.id)
        builder.add_control_permissions(user_id=user.id)
    builder['message'] = [user.to_dict() for user in users]
    return Response(json.dumps(builder), status=200, mimetype=MASON)


@app.route('/identities/<int:user_id>', methods=['DELETE'], endpoint='delete')
@require_api_key
def delete_identity(user_id):
    """
    Delete an existing user.
    URL Parameters:
        - user_id (int): The ID of the user to delete.
    Returns:
        Response: A JSON response with the user deletion status.
    """
    user = get_user_profile(user_id)
    if user is None:
        return create_error_response(404, title="NotFound", message=f'User: {user_id} not found')

    if delete_user_profile(user_id):
        builder = IdentityBuilder()
        builder.add_namespace("FacePass", LINK_RELATIONS_URL)
        builder.add_control("self", href=request.path)
        builder.add_control("profile", href=PROFILE_URL)
        builder.add_control_add()
        builder.add_control_get_name(user_name='user_name')
        builder.add_control_get(user_id='user_id')
        builder['message'] = f"User {user_id} deleted successfully"
        return Response(json.dumps(builder), status=204, mimetype=MASON)


@app.route('/identities/<int:user_id>/access-logs', methods=['GET'], endpoint='access_log_by_user')
@require_api_key
def get_access_logs_user(user_id):
    """
    Retrieve access logs for a specific user.
    URL Parameters:
        - user_id (int): The ID of the user to retrieve access logs for.
    Returns:
        Response: A JSON response with the access logs of the user.
    """
    
    user = get_user_profile(user_id)
    if user is None:
        return create_error_response(404, title="NotFound", message=f'User: {user_id} not found')

    access_logs = get_user_access_logs(user_id)
    builder = IdentityBuilder()
    builder.add_namespace("FacePass", LINK_RELATIONS_URL)
    builder.add_control("self", href=request.path)
    builder.add_control("profile", href=PROFILE_URL)
    builder.add_control_logs_by(user_id=user_id)
    for access_log in access_logs:
        builder.add_control_by_access(access_request_id=access_log.access_request_id)
    builder['message'] = [access_log.to_dict() for access_log in access_logs]
    return Response(json.dumps(builder), status=200, mimetype=MASON)


@app.route('/identities/<int:user_id>/requests', methods=['GET'], endpoint='requests_by_user')
@require_api_key
def get_requests(user_id):
    """
    Retrieve access requests for a specific user.
    URL Parameters:
        - user_id (int): The ID of the user to retrieve access requests for.
    Returns:
        Response: A JSON response with the access requests of the user.
    """
    
    user = get_user_profile(user_id)
    if user is None:
        return create_error_response(404, title="NotFound", message=f'User: {user_id} not found')
    requests = get_user_access_requests(user_id)
    builder = IdentityBuilder()
    builder.add_namespace("FacePass", LINK_RELATIONS_URL)
    builder.add_control("self", href=request.path)
    builder.add_control("profile", href=PROFILE_URL)
    builder.add_control_access_by(user_id=user_id)
    builder.add_control_request_access()
    for request_ in requests:
        if len(request_.access_logs) != 0:
            builder.add_control_log(log_id=request_.access_logs[0].id)
    builder['message'] = [request_.to_dict() for request_ in requests]
    return Response(json.dumps(builder), status=200, mimetype=MASON)


@app.route('/identities/<int:user_id>/permissions', methods=['GET'], endpoint='permissions_by_user')
@require_api_key
def get_requests(user_id):
    """
    Retrieve permissions for a specific user.
    URL Parameters:
        - user_id (int): The ID of the user to retrieve permissions for.
    Returns:
        Response: A JSON response with the permissions of the user.
    """
    
    user = get_user_profile(user_id)
    if user is None:
        return create_error_response(404, title="NotFound", message=f'User: {user_id} not found')
    user_permissions = get_user_permissions(user_id)
    builder = IdentityBuilder()
    builder.add_namespace("FacePass", LINK_RELATIONS_URL)
    builder.add_control("self", href=request.path)
    builder.add_control("profile", href=PROFILE_URL)
    builder.add_control_permission_by(user_id=user_id)
    builder['message'] = [user_permission.to_dict() for user_permission in user_permissions]
    return Response(json.dumps(builder), status=200, mimetype=MASON)


@app.route('/access-log/<int:log_id>', methods=['GET'], endpoint='access_log')
@require_api_key
def get_log(log_id):
    """
    Retrieve a specific access log.
    URL Parameters:
        - log_id (int): The ID of the access log to retrieve.
    Returns:
        Response: A JSON response with the details of the access log.
    """
    
    access_log = get_access_log(log_id)
    if access_log is None:
        return create_error_response(404, title="NotFound", message=f'Log {log_id} not found')

    access_request_id = access_log.access_request_id
    access_request = get_access_request(access_request_id)

    builder = IdentityBuilder()
    builder.add_namespace("FacePass", LINK_RELATIONS_URL)
    builder.add_control("self", href=request.path)
    builder.add_control("profile", href=PROFILE_URL)
    builder.add_control_logs_by(user_id=access_request.user_profile_id)
    builder.add_control_by_access(access_request_id=access_request_id)
    builder['message'] = access_log.to_dict()
    return Response(json.dumps(builder), status=200, mimetype=MASON)


@app.route('/access-request/<int:access_request_id>', methods=['GET'], endpoint='access_log_by_id')
@require_api_key
def get_access_logs(access_request_id):
    """
    Retrieve access logs for a specific access request.
    URL Parameters:
        - access_request_id (int): The ID of the access request to retrieve logs for.
    Returns:
        Response: A JSON response with the access logs of the request.
    """
    
    access_request = get_access_request(access_request_id)
    if access_request is None:
        return create_error_response(404, title="NotFound", message=f'Access request {access_request_id} not found')

    builder = IdentityBuilder()
    builder.add_namespace("FacePass", LINK_RELATIONS_URL)
    builder.add_control("self", href=request.path)
    builder.add_control("profile", href=PROFILE_URL)
    builder.add_control_access_by(user_id=access_request.user_profile_id)
    builder.add_control_request_access()
    builder.add_control_log(access_request.access_logs[0].id)
    builder['message'] = access_request.to_dict()
    return Response(json.dumps(builder), status=200, mimetype=MASON)


@app.route('/face_pass/tos')
def terms_of_service():
    """
    Render the terms of service page.
    Returns:
        Response: The rendered terms of service HTML page.
    """
    # template taken from https://www.gnu.org/licenses/gpl-3.0.en.html
    return render_template('tos.html')


@app.route("/face_pass/link-relations")
def send_link_relations_html():
    """
    Render the link relations page.
    Returns:
        Response: The rendered link relations HTML page.
    """
    return render_template('link_relations.html')


@app.route("/face_pass/profile")
def send_profile_html():
    """
    Render the profile page.
    Returns:
        Response: The rendered profile HTML page.
    """
    return render_template('profile.html')


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host=cfg.app.host, port=cfg.app.port, debug=False)
