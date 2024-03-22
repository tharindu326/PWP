import requests
from tests.utils import get_api_key
from faker import Faker
import random

fake = Faker()
def generate_random_name():
    return fake.name()

def test_successful_registration(base_url):
    url = f"{base_url}/identities/register"
    headers = {"Authorization": get_api_key()}
    name = generate_random_name()
    data = {"name": name, "permission": ["admin"]}
    files = {"image": open("./tests/data/president_1.jpg", "rb")}  # Update the path to a valid image file

    response = requests.post(url, headers=headers, data=data, files=files)
    assert response.status_code == 201
    assert f"User {name} registered successfully" in response.json()["message"]

def test_registration_without_api_key(base_url):
    url = f"{base_url}/identities/register"
    # No Authorization header included
    data = {"name": "John Doe", "permission": ["admin"]}
    files = {"image": open("./tests/data/president_1.jpg", "rb")}  # Ensure the path to a valid image file is correct

    response = requests.post(url, data=data, files=files)
    assert response.status_code == 400
    assert "API Key is missing" in response.json()["error"]

def test_registration_with_invalid_api_key(base_url):
    url = f"{base_url}/identities/register"
    headers = {"Authorization": "invalid_api_key"}
    name = generate_random_name()
    data = {"name": name, "permission": ["admin"]}
    files = {"image": open("./tests/data/president_1.jpg", "rb")}  # Update the path to a valid image file

    response = requests.post(url, headers=headers, data=data, files=files)
    assert response.status_code == 401
    assert "Invalid API Key" in response.json()["error"]

def test_registration_with_missing_data(base_url):
    url = f"{base_url}/identities/register"
    headers = {"Authorization": get_api_key()}
    # Missing name in the data
    data = {"permission": ["admin"]}
    files = {"image": open("./tests/data/president_1.jpg", "rb")}  # Update the path to a valid image file

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
    files = {"image": open("./tests/data/president_1.jpg", "rb")}  # Update the path to a valid image file

    # Register the user once
    response1 = requests.post(url, headers=headers, data=data, files=files)
    assert response1.status_code == 201
    assert f"User {name} registered successfully" in response1.json()["message"]

    # Try registering the user again with the same name
    response2 = requests.post(url, headers=headers, data=data, files=files)
    assert response2.status_code == 400
    assert "A user with this name already exists" in response2.json()["error"]

import requests
from tests.utils import get_api_key

def test_successful_profile_retrieval(base_url):
    # Define a user ID for which profile retrieval will be tested
    user_id = 1
    url = f"{base_url}/identities/{user_id}/profile"
    headers = {"Authorization": get_api_key()}

    response = requests.get(url, headers=headers)
    assert response.status_code == 200
    assert "id" in response.json()  # Ensure the response contains the user ID
    assert "name" in response.json()  # Ensure the response contains the user name
    assert "access_permissions" in response.json()  # Ensure the response contains user permissions

def test_retrieval_with_invalid_user_id(base_url):
    # Define a non-existent user ID for testing
    user_id = 9999
    url = f"{base_url}/identities/{user_id}/profile"
    headers = {"Authorization": get_api_key()}

    response = requests.get(url, headers=headers)
    assert response.status_code == 404
    assert "User not found" in response.json()["error"]  # Expecting user not found error

def test_retrieval_without_api_key(base_url):
    # Define a user ID for testing
    user_id = 1
    url = f"{base_url}/identities/{user_id}/profile"

    response = requests.get(url)
    assert response.status_code == 400
    assert "API Key is missing" in response.json()["error"]  # Expecting API key missing error

def test_retrieval_with_invalid_api_key(base_url):
    # Define a user ID for testing
    user_id = 1
    url = f"{base_url}/identities/{user_id}/profile"
    headers = {"Authorization": "InvalidAPIKey"}

    response = requests.get(url, headers=headers)
    assert response.status_code == 401
    assert "Invalid API Key." in response.json()["error"]  # Expecting invalid API key error