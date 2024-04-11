import pytest
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import app, add_access_log, log_access_request
from werkzeug.datastructures import FileStorage
from config import cfg
from database_models import db


API_KEY = '2b723b784e95601787f9a821461f4d35'
base_url = ''


@pytest.fixture
def client():
    app.config.update({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': cfg.db.SQLALCHEMY_DATABASE_URI,
        'SQLALCHEMY_TRACK_MODIFICATIONS': cfg.db.SQLALCHEMY_TRACK_MODIFICATIONS
    })
    with app.app_context():
        db.create_all()
    yield app.test_client()


def register_identity(data, images_folder, client, api_key, enable_apikey=True, no_image=False):
    if enable_apikey:
        headers = {"Authorization": api_key}
    else:
        headers = {}
    url = "/identities/register"
    if not no_image:
        for filename in os.listdir(images_folder):
            file_path = os.path.join(images_folder, filename)
            image_file = FileStorage(stream=open(file_path, 'rb'), filename=filename, content_type='image/jpeg')
            if 'image' not in data:
                data['image'] = [image_file]
            else:
                data['image'].append(image_file)
    response = client.post(url, headers=headers, data=data, content_type='multipart/form-data')
    if not no_image:
        for image_file in data['image']:
            image_file.stream.close()
    return response


def test_successful_registration(client):
    data = {
        "name": 'Biden',
        "permission": "admin"
    }
    images_folder = os.path.join(os.path.dirname(__file__), '..', 'test_images', 'Biden')
    response = register_identity(data, images_folder, client, api_key=API_KEY)
    assert response.status_code == 201

    data = {
        "name": 'Obama',
        "permission": "admin"
    }
    images_folder = os.path.join(os.path.dirname(__file__), '..', 'test_images', 'Obama')
    response = register_identity(data, images_folder, client, api_key=API_KEY)
    assert response.status_code == 201


def test_registration_without_api_key(client):
    data = {
            "name": 'Biden',
            "permission": "admin"
        }
    images_folder = os.path.join(os.path.dirname(__file__), '..', 'test_images', 'Biden')
    response = register_identity(data, images_folder, client, api_key=API_KEY, enable_apikey=False)
    assert response.status_code == 400


def test_registration_invalid1(client):
    data = {
            "name": 1,
            "permission": "admin"
        }
    images_folder = os.path.join(os.path.dirname(__file__), '..', 'test_images', 'Biden')
    response = register_identity(data, images_folder, client, api_key=API_KEY)
    assert response.status_code == 400


def test_registration_missingdata1(client):
    data = {
            "name": 'Biden',
        }
    images_folder = os.path.join(os.path.dirname(__file__), '..', 'test_images', 'Biden')
    response = register_identity(data, images_folder, client, api_key=API_KEY)
    assert response.status_code == 400


def test_registration_missingdata2(client):
    data = {
            "name": 'Biden',
            "permission": "admin"
        }
    images_folder = os.path.join(os.path.dirname(__file__), '..', 'test_images', 'Biden')
    response = register_identity(data, images_folder, client, api_key=API_KEY, no_image=True)
    assert response.status_code == 400


def test_registration_invalid2(client):
    data = {
            "name": 'Biden',
            "permission": ["XXX", 'admin']
        }
    images_folder = os.path.join(os.path.dirname(__file__), '..', 'test_images', 'Biden')
    response = register_identity(data, images_folder, client, api_key=API_KEY)
    assert response.status_code == 400


def test_registration_invalid3(client):
    data = {
            "name": 'Biden',
            "permission": "XXX"
        }
    images_folder = os.path.join(os.path.dirname(__file__), '..', 'test_images', 'Biden')
    response = register_identity(data, images_folder, client, api_key=API_KEY)
    assert response.status_code == 400


def test_registration_with_invalid_api_key(client):
    data = {
        "name": 'Biden',
        "permission": "admin"
    }
    images_folder = os.path.join(os.path.dirname(__file__), '..', 'test_images', 'Biden')
    response = register_identity(data, images_folder, client, api_key='INVALIDAPIKEY')
    assert response.status_code == 401


def test_registration_with_missing_data(client):
    data = {
        "permission": "admin"
    }
    images_folder = os.path.join(os.path.dirname(__file__), '..', 'test_images', 'Biden')
    response = register_identity(data, images_folder, client, api_key=API_KEY)
    assert response.status_code == 400
    # assert "Name is required" in response.json()["error"]


def test_registration_with_invalid_data(client):
    url = f"{base_url}/identities/register"
    headers = {"Authorization": API_KEY}
    data = {"name": 'Hohn', "permission": ["admin"]}  # Invalid name
    image_file = FileStorage(stream=open('tests/data/invalid_image.txt', 'rb'), filename='testim.txt',
                             content_type='image/jpeg')
    data['image'] = image_file
    response = client.post(url, headers=headers, data=data)
    assert response.status_code == 400
    # assert "File type: invalid_image.txt is not allowed. Allowed types are: png, jpg, jpeg" in response.json()["error"]


def test_registration_with_invalid_permission_data(client):
    url = f"{base_url}/identities/register"
    headers = {"Authorization": API_KEY}
    data = {"name": 'Hohn', "permission": {"admin":1}}  # Invalid name
    image_file = FileStorage(stream=open('tests/data/invalid_image.txt', 'rb'), filename='testim.txt',
                             content_type='image/jpeg')
    data['image'] = image_file
    response = client.post(url, headers=headers, data=data)
    assert response.status_code == 400


def test_successful_profile_retrieval(client):
    user_id = 1
    url = f"{base_url}/identities/{user_id}/profile"
    headers = {"Authorization": API_KEY}

    response = client.get(url, headers=headers)
    assert response.status_code == 200

    # for cache hit
    user_id = 1
    url = f"{base_url}/identities/{user_id}/profile"
    headers = {"Authorization": API_KEY}

    response = client.get(url, headers=headers)
    assert response.status_code == 200
    # assert "id" in response.json()
    # assert "name" in response.json()
    # assert "access_permissions" in response.json()


def test_retrieval_with_invalid_user_id(client):
    # non-existent user ID for testing
    user_id = 9999
    url = f"{base_url}/identities/{user_id}/profile"
    headers = {"Authorization": API_KEY}
    response = client.get(url, headers=headers)
    assert response.status_code == 404
    # assert "User not found" in response.json()["error"]


def test_retrieval_without_api_key(client):
    # user ID for testing
    user_id = 1
    url = f"{base_url}/identities/{user_id}/profile"
    response = client.get(url)
    assert response.status_code == 400
    # assert "API Key is missing" in response.json()["error"]


def test_retrieval_with_invalid_api_key(client):
    user_id = 1
    url = f"{base_url}/identities/{user_id}/profile"
    headers = {"Authorization": "InvalidAPIKey"}
    response = client.get(url, headers=headers)
    assert response.status_code == 401
    # assert "Invalid API Key." in response.json()["error"]


def test_successful_user_update(client):
    # Test updating the details of an existing user
    user_id = 2
    url = f"{base_url}/identities/{user_id}/update"
    headers = {"Authorization": API_KEY}
    updated_name = "Barak"
    data = {"name": updated_name, "permission": ["intern", "admin"]}
    image_file = FileStorage(stream=open('test_images/Obama/O1.jpg', 'rb'), filename='O1.jpg',
                             content_type='image/jpeg')
    data['image'] = image_file
    response = client.put(url, headers=headers, data=data)
    assert response.status_code == 200
    # assert f"User details updated successfully" in response.json()["message"]


def test_update_with_invalid_permissions(client):
    user_id = 1
    url = f"{base_url}/identities/{user_id}/update"
    headers = {"Authorization": API_KEY}
    invalid_permissions = ["superuser"]
    data = {"permission": invalid_permissions}
    response = client.put(url, headers=headers, data=data)
    assert response.status_code == 400
    # assert "Invalid permission level" in response.json()["error"]


def test_update_with_invalid_name(client):
    user_id = 1
    url = f"{base_url}/identities/{user_id}/update"
    headers = {"Authorization": API_KEY}
    valid_permissions = ["admin"]
    data = {"permission": valid_permissions, 'name': 2}
    response = client.put(url, headers=headers, data=data)
    assert response.status_code == 400
    # assert "Invalid permission level" in response.json()["error"]


def test_update_with_invalid_permission(client):
    user_id = 1
    url = f"{base_url}/identities/{user_id}/update"
    headers = {"Authorization": API_KEY}
    valid_permissions = {"admin":3}
    data = {"permission": valid_permissions, 'name': 2}
    response = client.put(url, headers=headers, data=data)
    assert response.status_code == 400


def test_update_nonexistent_user(client):
    # Test updating details of a user that does not exist
    user_id = 15
    url = f"{base_url}/identities/{user_id}/update"
    headers = {"Authorization": API_KEY}
    updated_name = "Barak"
    data = {"name": updated_name, "permission": ["intern", "admin"]}
    image_file = FileStorage(stream=open('test_images/Obama/O1.jpg', 'rb'), filename='O1.jpg',
                             content_type='image/jpeg')
    data['image'] = image_file
    response = client.put(url, headers=headers, data=data)
    print(response.data)
    assert response.status_code == 404
    # assert f"User details updated successfully" in response.json()["message"]


def test_update_without_api_key(client):
    user_id = 1
    url = f"{base_url}/identities/{user_id}/update"
    data = {"name": "NoKey User", "permission": ["admin"]}
    image_file = FileStorage(stream=open('test_images/Obama/O1.jpg', 'rb'), filename='O1.jpg',
                             content_type='image/jpeg')
    data['image'] = image_file
    response = client.put(url, data=data)
    assert response.status_code == 400
    # assert "API Key is missing" in response.json()["error"]


def test_update_with_invalid_api_key(client):
    user_id = 1
    url = f"{base_url}/identities/{user_id}/update"
    headers = {"Authorization": "InvalidAPIKey"}
    data = {"name": "InvalidKey User", "permission": ["admin"]}
    image_file = FileStorage(stream=open('test_images/Obama/O1.jpg', 'rb'), filename='O1.jpg',
                             content_type='image/jpeg')
    data['image'] = image_file
    response = client.put(url, headers=headers, data=data)
    assert response.status_code == 401
    # assert "Invalid API Key" in response.json()["error"]


def test_unsuccessful_access_grant(client):
    # test access granted when un recognize user face uis there
    url = f"{base_url}/identities/access-request"
    headers = {"Authorization": API_KEY}
    data = {"associated_permission": "intern"}
    image_file = FileStorage(stream=open('test_images/Biden/B1.jpg', 'rb'), filename='B1.jpg',
                             content_type='image/jpeg')
    data['image'] = image_file
    response = client.post(url, headers=headers, data=data)
    print(response.data)
    assert response.status_code == 403
    # assert "user: 2 does not have permission. Access declined" in response.json()["@error"]["@messages"]


def test_successful_access_grant(client):
    url = f"{base_url}/identities/access-request"
    headers = {"Authorization": API_KEY}
    data = {"associated_permission": "admin"}
    image_file = FileStorage(stream=open('test_images/Biden/B1.jpg', 'rb'), filename='B1.jpg',
                             content_type='image/jpeg')
    data['image'] = image_file
    response = client.post(url, headers=headers, data=data)
    print(response.data)
    assert response.status_code == 201
    # assert "user: 1 access granted successfully" in response.json()["message"]


def test_not_recognized_access_grant(client):
    url = f"{base_url}/identities/access-request"
    headers = {"Authorization": API_KEY}
    data = {"associated_permission": "admin"}
    image_file = FileStorage(stream=open('test_images/Trump/T5.jpg', 'rb'), filename='T5.jpg',
                             content_type='image/jpeg')
    data['image'] = image_file
    response = client.post(url, headers=headers, data=data)
    print(response.data)
    assert response.status_code == 401


def test_access_denial_insufficient_permissions(client):
    url = f"{base_url}/identities/access-request"
    headers = {"Authorization": API_KEY}
    data = {"associated_permission": "intern"}  # Assuming 'guest' permission is insufficient for access
    image_file = FileStorage(stream=open('test_images/Biden/B1.jpg', 'rb'), filename='B1.jpg',
                             content_type='image/jpeg')
    data['image'] = image_file

    response = client.post(url, headers=headers, data=data)
    assert response.status_code == 403
    # assert "user: 1 does not have permission. Access declined" in response.json()["message"]


def test_access_request_no_face_detected(client):
    url = f"{base_url}/identities/access-request"
    headers = {"Authorization": API_KEY}
    data = {"associated_permission": "admin"}
    image_file = FileStorage(stream=open('tests/data/no_face_image.jpg', 'rb'), filename='B1.jpg',
                             content_type='image/jpeg')
    data['image'] = image_file

    response = client.post(url, headers=headers, data=data)
    assert response.status_code == 500
    # assert "No face detected" in response.json()["error"]


def test_access_denial_insufficient_image(client):
    url = f"{base_url}/identities/access-request"
    headers = {"Authorization": API_KEY}
    data = {"associated_permission": "intern"}  # Assuming 'guest' permission is insufficient for access
    response = client.post(url, headers=headers, data=data)
    assert response.status_code == 400


def test_access_request_with_invalid_data(client):
    url = f"{base_url}/identities/access-request"
    headers = {"Authorization": API_KEY}
    data = {"associated_permission": "admin"}
    image_file = FileStorage(stream=open('tests/data/invalid_image.txt', 'rb'), filename='invalid_image.txt', content_type='image/jpeg')
    data['image'] = image_file
    response = client.post(url, headers=headers, data=data)
    assert response.status_code == 400
    # assert "file type: txt not allowed" in response.json()["error"]


def test_access_request_with_missing_data1(client):
    url = f"{base_url}/identities/access-request"
    headers = {"Authorization": API_KEY}
    data = {}
    image_file = FileStorage(stream=open('test_images/Biden/B1.jpg', 'rb'), filename='B1.jpg', content_type='image/jpeg')
    data['image'] = image_file
    response = client.post(url, headers=headers, data=data)
    assert response.status_code == 400


# def test_access_request_with_server_error(client):
#     url = f"{base_url}/identities/access-request"
#     headers = {"Authorization": API_KEY}
#     data = {}
#     image_file = FileStorage(stream=open('test_images/Biden/B1.jpg', 'rb'), filename='B1.jpg', content_type='image/jpeg')
#     data['image'] = image_file
#     input("Open the DB instance form DB browser to restrict the writing permissions to the DB, then server error will pop up")
#     response = client.post(url, headers=headers, data=data)
#     assert response.status_code == 400


def test_access_request_with_missing_data2(client):
    url = f"{base_url}/identities/access-request"
    headers = {"Authorization": API_KEY}
    data = {"associated_permission": "admin"}
    response = client.post(url, headers=headers, data=data)
    assert response.status_code == 400


def test_access_request_with_invalid_data1(client):
    url = f"{base_url}/identities/access-request"
    headers = {"Authorization": API_KEY}
    data = {"associated_permission": "xxxx"}
    image_file = FileStorage(stream=open('test_images/Biden/B1.jpg', 'rb'), filename='B1.jpg', content_type='image/jpeg')
    data['image'] = image_file
    response = client.post(url, headers=headers, data=data)
    assert response.status_code == 400


def test_successful_user_deletion(client):
    user_id = 2
    url = f"{base_url}/identities/{user_id}/delete"
    headers = {"Authorization": API_KEY}
    response = client.delete(url, headers=headers)
    assert response.status_code == 204
    # assert "deleted successfully" in response.json()["message"]


def test_delete_nonexistent_user(client):
    # Use an ID assumed not to exist
    user_id = 20
    url = f"{base_url}/identities/{user_id}/delete"
    headers = {"Authorization": API_KEY}
    response = client.delete(url, headers=headers)
    assert response.status_code == 404
    # assert "User not found" in response.json()["error"]


def test_delete_user_without_api_key(client):
    # Use a known user ID that can be attempted for deletion
    user_id = 3
    url = f"{base_url}/identities/{user_id}/delete"
    response = client.delete(url)
    # Verify that the API key is required
    assert response.status_code == 400
    # assert "API Key is missing" in response.json()["error"]


def test_delete_user_with_invalid_api_key(client):
    # Use a known user ID that can be attempted for deletion
    user_id = 1
    url = f"{base_url}/identities/{user_id}/delete"
    headers = {"Authorization": "InvalidAPIKey"}
    response = client.delete(url, headers=headers)
    assert response.status_code == 401
    # assert "Invalid API Key" in response.json()["error"]


def test_retrieve_access_logs_for_existing_user(client):
    with app.app_context():
        add_access_log(access_request_id=1, details='test access log')
    url = f"{base_url}identities/1/access-logs"
    headers = {"Authorization": API_KEY}
    response = client.get(url, headers=headers)
    assert response.status_code == 200


def test_retrieve_access_logs_for_nonexistent_user(client):
    nonexistent_user_id = 100000000
    url = f"{base_url}/{nonexistent_user_id}/access-logs"
    headers = {"Authorization": API_KEY}
    response = client.get(url, headers=headers)
    assert response.status_code == 404
    # assert "User not found" in response.json()["error"]


def test_retrieve_access_logs_without_api_key(client):
    # Use a valid user_id for this test
    user_id = 1
    url = f"{base_url}/access-log/{user_id}"
    response = client.get(url)
    assert response.status_code == 400
    # assert "API Key is missing" in response.json()["error"]


def test_retrieve_access_logs_with_invalid_api_key(client):
    # Use a valid user_id for this test
    user_id = 1
    url = f"{base_url}/access-log/{user_id}"
    headers = {"Authorization": "InvalidAPIKey"}
    response = client.get(url, headers=headers)
    assert response.status_code == 401
    # assert "Invalid API Key" in response.json()["error"]


def test_successful_retrieval_user_by_name(client):
    user_name = 'Biden'
    url = f"{base_url}/identities/{user_name}"
    headers = {"Authorization": API_KEY}
    response = client.get(url, headers=headers)
    assert response.status_code == 200


def test_retrieval_user_by_name_with_nonexistent_user(client):
    user_name = 'XXX'
    url = f"{base_url}/identities/{user_name}"
    headers = {"Authorization": API_KEY}
    response = client.get(url, headers=headers)
    print(response.data)
    assert response.status_code == 404


def test_invalid_retrieval_user_by_name1(client):
    user_name = '?'
    url = f"{base_url}/identities/{user_name}"
    headers = {"Authorization": API_KEY}
    response = client.get(url, headers=headers)
    print(response.data)
    assert response.status_code == 404


def test_successful_retrival_requests_by_user_id(client):
    blobData = None
    with app.app_context():
        access_id = log_access_request(1, associated_permission="admin", associated_facial_data=blobData,
                           outcome=1)
    user_id = 1
    url = f"{base_url}/identities/{user_id}/requests"
    headers = {"Authorization": API_KEY}
    response = client.get(url, headers=headers)
    assert response.status_code == 200


def test_retrival_requests_by_user_id_with_nonexistent_user(client):
    user_id = 1000
    url = f"{base_url}/identities/{user_id}/requests"
    headers = {"Authorization": API_KEY}
    response = client.get(url, headers=headers)
    assert response.status_code == 404


def test_successful_retrival_permissions_by_user_id(client):
    user_id = 1
    url = f"{base_url}/identities/{user_id}/permissions"
    headers = {"Authorization": API_KEY}
    response = client.get(url, headers=headers)
    assert response.status_code == 200


def test_retrival_permissions_by_user_id_with_nonexistent_user(client):
    user_id = 1000
    url = f"{base_url}/identities/{user_id}/permissions"
    headers = {"Authorization": API_KEY}
    response = client.get(url, headers=headers)
    assert response.status_code == 404


def test_successful_retrival_logs_by_log_id(client):
    log_id = 1
    url = f"{base_url}/access-log/{log_id}"
    headers = {"Authorization": API_KEY}
    response = client.get(url, headers=headers)
    assert response.status_code == 200


def test_successful_retrival_logs_by_log_id_with_nonexistent_log_id(client):
    log_id = 1000
    url = f"{base_url}/access-log/{log_id}"
    headers = {"Authorization": API_KEY}
    response = client.get(url, headers=headers)
    assert response.status_code == 404


def test_successful_retrival_AR_by_access_request_id(client):
    access_request_id = 1
    url = f"{base_url}/access-request/{access_request_id}"
    headers = {"Authorization": API_KEY}
    response = client.get(url, headers=headers)
    assert response.status_code == 200


def test_successful_retrival_AR_by_AR_id_with_nonexistent_AR_id(client):
    access_request_id = 1000
    url = f"{base_url}/access-request/{access_request_id}"
    headers = {"Authorization": API_KEY}
    response = client.get(url, headers=headers)
    assert response.status_code == 404


def test_tos_linkRel_profile_endpoints(client):
    url = f"/face_pass/link-relations"
    response = client.get(url)
    assert response.status_code == 200

    url = f"/face_pass/profile"
    response = client.get(url)
    assert response.status_code == 200

    url = f"/face_pass/tos"
    response = client.get(url)
    assert response.status_code == 200

