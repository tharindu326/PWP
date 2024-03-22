import pytest

@pytest.fixture(scope="module")
def base_url():
    return "http://127.0.0.1:5000"  # Adjust this to your Flask app's URL