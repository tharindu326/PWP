from faker import Faker
import requests
from tests.utils import get_api_key

fake = Faker()


def generate_random_name():
    return fake.name()


def test_successful_registration(base_url):
    url = f"{base_url}/identities/register"
    headers = {"Authorization": get_api_key()}
    name = generate_random_name()
    data = {"name": name, "permission": ["admin"]}
    files = {"image": open("./tests/data/president_1.jpeg", "rb")}

    response = requests.post(url, headers=headers, data=data, files=files)
    assert response.status_code == 201
    assert f"User {name} registered successfully" in response.json()["message"]


def test_registration_without_api_key(base_url):
    url = f"{base_url}/identities/register"
    # No Authorization header included
    data = {"name": "John Doe", "permission": ["admin"]}
    files = {"image": open("./tests/data/president_1.jpeg", "rb")}

    response = requests.post(url, data=data, files=files)
    assert response.status_code == 400
    assert "API Key is missing" in response.json()["error"]


def test_registration_with_invalid_api_key(base_url):
    url = f"{base_url}/identities/register"
    headers = {"Authorization": "invalid_api_key"}
    name = generate_random_name()
    data = {"name": name, "permission": ["admin"]}
    files = {"image": open("./tests/data/president_1.jpeg", "rb")}

    response = requests.post(url, headers=headers, data=data, files=files)
    assert response.status_code == 401
    assert "Invalid API Key" in response.json()["error"]


def test_registration_with_missing_data(base_url):
    url = f"{base_url}/identities/register"
    headers = {"Authorization": get_api_key()}
    # Missing name in the data
    data = {"permission": ["admin"]}
    files = {"image": open("./tests/data/president_1.jpeg", "rb")}

    response = requests.post(url, headers=headers, data=data, files=files)
    assert response.status_code == 400
    assert "Name is required" in response.json()["error"]


def test_registration_with_invalid_data(base_url):
    url = f"{base_url}/identities/register"
    headers = {"Authorization": get_api_key()}
    name = generate_random_name()
    data = {"name": name, "permission": ["admin"]}  # Invalid name
    files = {"image": open("./tests/data/invalid_image.txt", "rb")}  # Invalid image file format

    response = requests.post(url, headers=headers, data=data, files=files)
    assert response.status_code == 400
    assert "File type: invalid_image.txt is not allowed. Allowed types are: png, jpg, jpeg" in response.json()["error"]


def test_multiple_registrations_with_same_name(base_url):
    url = f"{base_url}/identities/register"
    headers = {"Authorization": get_api_key()}
    name = generate_random_name()
    data = {"name": name, "permission": ["admin"]}
    files = {"image": open("./tests/data/president_1.jpeg", "rb")}

    # Register the user once
    response1 = requests.post(url, headers=headers, data=data, files=files)
    assert response1.status_code == 201

    # Try registering the user again with the same name
    response2 = requests.post(url, headers=headers, data=data, files=files)
    assert response2.status_code == 400
    assert "A user with this name already exists" in response2.json()["error"]


def test_successful_profile_retrieval(base_url):
    user_id = 1
    url = f"{base_url}/identities/{user_id}/profile"
    headers = {"Authorization": get_api_key()}

    response = requests.get(url, headers=headers)
    assert response.status_code == 200
    assert "id" in response.json()
    assert "name" in response.json()
    assert "access_permissions" in response.json()


def test_retrieval_with_invalid_user_id(base_url):
    # non-existent user ID for testing
    user_id = 9999
    url = f"{base_url}/identities/{user_id}/profile"
    headers = {"Authorization": get_api_key()}

    response = requests.get(url, headers=headers)
    assert response.status_code == 404
    assert "User not found" in response.json()["error"]


def test_retrieval_without_api_key(base_url):
    # user ID for testing
    user_id = 1
    url = f"{base_url}/identities/{user_id}/profile"
    response = requests.get(url)
    assert response.status_code == 400
    assert "API Key is missing" in response.json()["error"]


def test_retrieval_with_invalid_api_key(base_url):
    user_id = 1
    url = f"{base_url}/identities/{user_id}/profile"
    headers = {"Authorization": "InvalidAPIKey"}
    response = requests.get(url, headers=headers)
    assert response.status_code == 401
    assert "Invalid API Key." in response.json()["error"]


def test_successful_user_update(base_url):
    # Test updating the details of an existing user
    user_id = 4
    url = f"{base_url}/identities/{user_id}/update"
    headers = {"Authorization": get_api_key()}
    updated_name = "Narendra Modi"
    data = {"name": updated_name, "permission": ["intern"]}
    files = {"image": open("./tests/data/M5.jpg", "rb")}
    response = requests.put(url, headers=headers, data=data, files=files)
    print(response)
    assert response.status_code == 200
    assert f"User details updated successfully" in response.json()["message"]


def test_update_with_invalid_permissions(base_url):
    user_id = 1
    url = f"{base_url}/identities/{user_id}/update"
    headers = {"Authorization": get_api_key()}
    invalid_permissions = ["superuser"]
    data = {"permission": invalid_permissions}
    response = requests.put(url, headers=headers, data=data)
    assert response.status_code == 400
    assert "Invalid permission level" in response.json()["error"]


def test_update_nonexistent_user(base_url):
    # Test updating details of a user that does not exist
    nonexistent_user_id = 11000
    url = f"{base_url}/identities/{nonexistent_user_id}/update"
    headers = {"Authorization": get_api_key()}
    updated_name = "Pikachu"
    data = {"name": updated_name, "permission": ["admin"]}
    files = {"image": open("./tests/data/president_1.jpeg", "rb")}
    response = requests.put(url, headers=headers, data=data, files=files)
    assert response.status_code == 404


def test_update_without_api_key(base_url):
    user_id = 1
    url = f"{base_url}/identities/{user_id}/update"
    data = {"name": "NoKey User", "permission": ["admin"]}
    response = requests.put(url, data=data)
    assert response.status_code == 400
    assert "API Key is missing" in response.json()["error"]


def test_update_with_invalid_api_key(base_url):
    user_id = 1
    url = f"{base_url}/identities/{user_id}/update"
    headers = {"Authorization": "InvalidAPIKey"}
    data = {"name": "InvalidKey User", "permission": ["admin"]}
    response = requests.put(url, headers=headers, data=data)
    assert response.status_code == 401
    assert "Invalid API Key" in response.json()["error"]


def test_unsuccessful_access_grant(base_url):
    # test access granted when un recognize user face uis there
    url = f"{base_url}/identities/access-request"
    headers = {"Authorization": get_api_key()}
    data = {"associated_permission": "intern"}
    files = {"image": open("./tests/data/M5.jpg", "rb")}
    response = requests.post(url, headers=headers, data=data, files=files)
    print(response.json())
    assert response.status_code == 401
    assert "user not recognized. Access denied" in response.json()["error"]


def test_successful_access_grant(base_url):
    url = f"{base_url}/identities/access-request"
    headers = {"Authorization": get_api_key()}
    data = {"associated_permission": "admin"}
    files = {"image": open("./tests/data/B1.jpg", "rb")}
    response = requests.post(url, headers=headers, data=data, files=files)
    print(response.json())
    assert response.status_code == 201
    assert "user: 1 access granted successfully" in response.json()["message"]


def test_access_denial_insufficient_permissions(base_url):
    url = f"{base_url}/identities/access-request"
    headers = {"Authorization": get_api_key()}
    data = {"associated_permission": "intern"}  # Assuming 'guest' permission is insufficient for access
    files = {"image": open("./tests/data/B1.jpg", "rb")}  # A valid image with recognizable face

    response = requests.post(url, headers=headers, data=data, files=files)
    assert response.status_code == 403
    assert "user: 1 does not have permission. Access declined" in response.json()["message"]


# def test_access_denial_insufficient_permissions(base_url):
#     url = f"{base_url}/identities/access-request"
#     headers = {"Authorization": get_api_key()}
#     data = {"associated_permission": "guest"}  # Assuming 'guest' permission is insufficient for access
#     files = {"image": open("./tests/data/president_3.jpg", "rb")}  # A valid image with recognizable face

#     response = requests.post(url, headers=headers, data=data, files=files)
#     assert response.status_code == 403
#     assert "does not have permission" in response.json()["message"]

def test_access_request_no_face_detected(base_url):
    url = f"{base_url}/identities/access-request"
    headers = {"Authorization": get_api_key()}
    data = {"associated_permission": "admin"}
    files = {"image": open("./tests/data/no_face_image.jpg", "rb")}  # An image without a detectable face

    response = requests.post(url, headers=headers, data=data, files=files)
    assert response.status_code == 500
    assert "No face detected" in response.json()["error"]


def test_access_request_with_invalid_data(base_url):
    url = f"{base_url}/identities/access-request"
    headers = {"Authorization": get_api_key()}
    data = {"associated_permission": "admin"}
    files = {"image": ("invalid_image.txt", "This is not an image.", "text/plain")}  # Unsupported image format

    response = requests.post(url, headers=headers, data=data, files=files)
    assert response.status_code == 400
    assert "file type: txt not allowed" in response.json()["error"]


# def test_unexpected_errors_handling(base_url):
#     """Test handling of unexpected errors."""
#     # Simulate database connection issue
#     with app.app_context():
#         db.drop_all()  # Simulate database connection issue by dropping all tables
#     url = f"{base_url}/identities/register"
#     headers = {"Authorization": get_api_key()}
#     data = {"name": "John Doe", "permission": json.dumps(["admin"])}
#     with open("./tests/data/president_1.jpg", "rb") as img:
#         files = {"image": (img, "president_1.jpg")}
#         response = client.post(url, headers=headers, data=data, content_type='multipart/form-data', follow_redirects=True)
#     assert response.status_code == 500
#     assert "An error occurred" in response.json["error"]
#     img.close()

# def test_successful_user_deletion(base_url):
#     # Assume you have a user with a known ID that can safely be deleted for testing.
#     user_id = 1
#     url = f"{base_url}/identities/{user_id}/delete"
#     headers = {"Authorization": get_api_key()}

#     response = requests.delete(url, headers=headers)

#     # Verify that the user was deleted successfully
#     assert response.status_code == 200
#     assert "deleted successfully" in response.json()["message"]

def test_delete_nonexistent_user(base_url):
    # Use an ID assumed not to exist
    user_id = 1
    url = f"{base_url}/identities/{user_id}/delete"
    headers = {"Authorization": get_api_key()}
    response = requests.delete(url, headers=headers)
    # Verify that the appropriate error message is returned
    assert response.status_code == 404
    assert "User not found" in response.json()["error"]


def test_delete_user_without_api_key(base_url):
    # Use a known user ID that can be attempted for deletion
    user_id = 1
    url = f"{base_url}/identities/{user_id}/delete"
    response = requests.delete(url)
    # Verify that the API key is required
    assert response.status_code == 400
    assert "API Key is missing" in response.json()["error"]


def test_delete_user_with_invalid_api_key(base_url):
    # Use a known user ID that can be attempted for deletion
    user_id = 1
    url = f"{base_url}/identities/{user_id}/delete"
    headers = {"Authorization": "InvalidAPIKey"}
    response = requests.delete(url, headers=headers)
    # Verify that the response indicates an invalid API key
    assert response.status_code == 401
    assert "Invalid API Key" in response.json()["error"]


# def test_retrieve_access_logs_for_existing_user(base_url):
#     user_id = create_test_user(base_url, "Test User", permissions=["admin"])

#     url = f"{base_url}/access-log/{user_id}"
#     headers = {"Authorization": get_api_key()}

#     response = requests.get(url, headers=headers)
#     assert response.status_code == 200
#     assert isinstance(response.json(), list)

#     delete_test_user(base_url, user_id)

# def test_retrieve_access_logs_for_nonexistent_user(base_url):
#     # Use a user_id that does not exist
#     nonexistent_user_id = 100000000
#     url = f"{base_url}/access-log/{nonexistent_user_id}"
#     headers = {"Authorization": get_api_key()}

#     response = requests.get(url, headers=headers)
#     assert response.status_code == 404
#     assert "User not found" in response.json()["error"]

def test_retrieve_access_logs_without_api_key(base_url):
    # Use a valid user_id for this test
    user_id = 1
    url = f"{base_url}/access-log/{user_id}"
    response = requests.get(url)
    assert response.status_code == 400
    assert "API Key is missing" in response.json()["error"]


def test_retrieve_access_logs_with_invalid_api_key(base_url):
    # Use a valid user_id for this test
    user_id = 1
    url = f"{base_url}/access-log/{user_id}"
    headers = {"Authorization": "InvalidAPIKey"}
    response = requests.get(url, headers=headers)
    assert response.status_code == 401
    assert "Invalid API Key" in response.json()["error"]
