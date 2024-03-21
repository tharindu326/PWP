import pytest
from services.user_service import (
    add_user, 
    get_users_by_name, 
    get_user_profile, 
    update_user_facial_data, 
    delete_user_profile, 
    update_user_name
)
from services.access_log_service import (
    add_access_log,
    get_user_access_logs
)
from services.access_request_service import (
    log_access_request,
    get_access_requests
)
from services.permission_service import (
    add_permission_to_user,
    get_user_permissions,
    validate_access_for_user,
    revoke_user_permissions,
)
from services.access_request_service import (
    log_access_request, 
    get_access_requests
)
from services.permission_service import add_permission_to_user, get_user_permissions, validate_access_for_user, revoke_user_permissions
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import scoped_session, sessionmaker
from app import create_app  # Make sure this import matches your Flask app structure
from database_models import db as _db
from database_models import UserProfile, AccessLog, AccessRequest, AccessPermission
import threading 

@pytest.fixture(scope='session')
def app():
    """Configure and create a Flask app instance for testing."""
    app = create_app()  # Adjust as necessary
    app.config.update({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
        'SQLALCHEMY_TRACK_MODIFICATIONS': False
    })
    with app.app_context():
        _db.create_all()
        yield app
        _db.drop_all()

@pytest.fixture(scope='function')
def session(app):
    """Creates a scoped session for a test."""
    # Bind a session factory to the connection
    connection = _db.engine.connect()
    transaction = connection.begin()
    factory = sessionmaker(bind=connection)
    Session = scoped_session(factory)

    _db.session = Session

    yield _db.session

    _db.session.remove()  # Remove the session, returning connection to the pool
    transaction.rollback()  # Roll back any changes made during the test
    connection.close()

# Define your test functions here, using the `session` fixture as needed.


# Test case example remains the same

# Example Test: Add and Retrieve a User
def test_add_user(session):
    user_id = add_user("Test User", b"test_facial_data")
    assert user_id is not None
    user = UserProfile.query.get(user_id)
    assert user is not None
    assert user.name == "Test User"
    assert user.facial_data == b"test_facial_data"


def test_get_users_by_name(session):
    add_user("Duplicate Name", b"facial_data_1")
    add_user("Duplicate Name", b"facial_data_2")
    users = get_users_by_name("Duplicate Name")
    assert len(users) == 2
    assert all(user.name == "Duplicate Name" for user in users)


def test_get_user_profile(session):
    user_id = add_user("Profile Test", b"profile_facial_data")
    user = get_user_profile(user_id)
    assert user is not None
    assert user.name == "Profile Test"
    assert user.facial_data == b"profile_facial_data"

def test_update_user_facial_data(session):
    user_id = add_user("Update Test", b"original_facial_data")
    success = update_user_facial_data(user_id, b"updated_facial_data")
    assert success is True
    user = UserProfile.query.get(user_id)
    assert user.facial_data == b"updated_facial_data"


def test_delete_user_profile(session):
    user_id = add_user("Delete Test", b"delete_facial_data")
    success = delete_user_profile(user_id)
    assert success is True
    user = UserProfile.query.get(user_id)
    assert user is None

def test_update_user_name(session):
    user_id = add_user("Name Update", b"name_facial_data")
    success = update_user_name(user_id, "New Name")
    assert success is True
    user = UserProfile.query.get(user_id)
    assert user.name == "New Name"

def test_add_access_log(session):
    user_id = add_user("Access Log User", b"access_log_facial_data")
    # Use the actual `log_access_request` function to add an access request
    request_id = log_access_request(user_id, "Admin", True, b"facial_data")

    add_access_log(access_request_id=request_id, details="Access granted.")
    logs = get_user_access_logs(user_id)
    
    assert len(logs) == 1
    assert logs[0].details == "Access granted."
    assert logs[0].access_request_id == request_id


def test_retrieve_access_logs_by_user(session):
    user_id = add_user("Log Retrieval User", b"log_retrieval_facial_data")
    request_id_1 = log_access_request(user_id, "Permission 1", True, b"facial_data_1")
    request_id_2 = log_access_request(user_id, "Permission 2", False, b"facial_data_2")

    add_access_log(access_request_id=request_id_1, details="Access 1 granted.")
    add_access_log(access_request_id=request_id_2, details="Access 2 denied.")
    logs = get_user_access_logs(user_id)

    assert len(logs) == 2
    assert any(log.details == "Access 1 granted." for log in logs)
    assert any(log.details == "Access 2 denied." for log in logs)

def test_log_access_request(session):
    user_id = add_user("Request Log User", b"request_log_facial_data")
    request_id = log_access_request(user_id, "Test Permission", True, b"test_facial_data")
    
    assert request_id is not None
    # Verify the access request details
    request = AccessRequest.query.get(request_id)
    assert request is not None
    assert request.user_profile_id == user_id
    assert request.associated_permission == "Test Permission"
    assert request.outcome == '1'
    assert request.associated_facial_data == b"test_facial_data"

def test_retrieve_access_requests_for_user(session):
    user_id = add_user("Multiple Requests User", b"multiple_requests_facial_data")
    # Log multiple access requests
    log_access_request(user_id, "Permission 1", True, b"facial_data_1")
    log_access_request(user_id, "Permission 2", False, b"facial_data_2")

    requests = get_access_requests(user_id)
    assert len(requests) >= 2  # Assuming there could be existing requests for the user
    # Check the details of the first request
    assert requests[0].user_profile_id == user_id
    assert requests[0].associated_permission in ["Permission 1", "Permission 2"]
    assert requests[0].associated_facial_data in [b"facial_data_1", b"facial_data_2"]
    # Ensure requests are ordered by timestamp desc
    assert requests[0].timestamp >= requests[1].timestamp

def test_add_permission_to_user(session):
    user_id = add_user("Permission User", b"permission_facial_data")
    add_permission_to_user(user_id, "admin")
    permissions = get_user_permissions(user_id)
    assert len(permissions) == 1
    assert permissions[0].permission_level == "admin"

def test_get_user_permissions(session):
    user_id = add_user("Permissions User", b"permissions_facial_data")
    add_permission_to_user(user_id, "edit")
    add_permission_to_user(user_id, "view")
    permissions = get_user_permissions(user_id)
    assert len(permissions) == 2
    assert set(perm.permission_level for perm in permissions) == {"edit", "view"}

def test_validate_access_for_user(session):
    user_id = add_user("Access Validation User", b"access_validation_facial_data")
    add_permission_to_user(user_id, "edit")
    is_valid = validate_access_for_user(user_id, "edit")
    assert is_valid is True
    is_valid = validate_access_for_user(user_id, "admin")
    assert is_valid is False

def test_revoke_user_permissions_specific(session):
    user_id = add_user("Revoke Specific Permission User", b"revoke_specific_facial_data")
    add_permission_to_user(user_id, "delete")
    add_permission_to_user(user_id, "edit")
    revoke_user_permissions(user_id, "delete")
    permissions = get_user_permissions(user_id)
    assert len(permissions) == 1
    assert permissions[0].permission_level != "delete"

def test_revoke_user_permissions_all(session):
    user_id = add_user("Revoke All Permissions User", b"revoke_all_facial_data")
    add_permission_to_user(user_id, "delete")
    add_permission_to_user(user_id, "edit")
    revoke_user_permissions(user_id)
    permissions = get_user_permissions(user_id)
    assert len(permissions) == 0

# def test_permission_service_with_invalid_user_id(session):
#     # Attempt to add a permission for a non-existent user
#     add_permission_to_user(user_id=99999, permission_level="Test")
#     permissions = get_user_permissions(user_id=99999)
#     # Assuming the application should not allow adding permissions for non-existent users
#     assert len(permissions) == 0  
    
#     # Verify access validation correctly handles non-existent users
#     is_valid = validate_access_for_user(user_id=99999, required_permission_level="Test")
#     # Expect validation to correctly identify invalid user and return False
#     assert not is_valid
    
#     # Attempt to revoke permissions for a non-existent user should not raise an error
#     revoke_user_permissions(user_id=99999, permission_level="Test")

# def test_access_control_enforcement(session):
#     # Setup: create a user and assign a specific permission
#     user_id = add_user("Access Control User", b"access_control_data")
#     add_permission_to_user(user_id, "Limited")
    
#     # Attempt to perform an action that requires a higher permission level
#     # This step depends on your application's specific logic for enforcing access control
#     # For example:
#     # can_access = attempt_protected_action(user_id, "Admin")
#     # assert not can_access

def test_data_validation(session):
    # Create a user without validating data, assuming the application allows it
    invalid_user_id = add_user("", b"")
    assert invalid_user_id is not None
    
    # Add a user with valid data for permission testing
    user_id = add_user("Validation User", b"valid_data")
    # Attempt to add a permission with an invalid (empty) level
    add_permission_to_user(user_id, "")
    permissions = get_user_permissions(user_id)
    # Adjust expectations based on the application's current behavior
    # Assuming no validation is present and the application allows adding permissions with empty levels
    assert any(permission.permission_level == "" for permission in permissions)

def test_concurrent_access_handling(session):
    user_id = add_user("Concurrent User", b"concurrent_data")
    
    def add_permission():
        add_permission_to_user(user_id, "Concurrent")
    
    # Start multiple threads to simulate concurrent access
    threads = [threading.Thread(target=add_permission) for _ in range(10)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    
    # Verify that the correct number of permissions have been added
    # This assertion depends on how your application is supposed to handle concurrent modifications
    permissions = get_user_permissions(user_id)
    # For example, assuming the application should prevent duplicate permissions
    assert len(permissions) == 1

def test_user_lifecycle(session):
    # Create a user
    user_id = add_user("Lifecycle Test User", b"lifecycle_data")
    assert get_user_profile(user_id) is not None

    # Add a permission to the user
    add_permission_to_user(user_id, "admin")
    permissions = get_user_permissions(user_id)
    assert any(perm.permission_level == "admin" for perm in permissions)

    # Revoke the permission
    revoke_user_permissions(user_id, "admin")
    permissions = get_user_permissions(user_id)
    assert all(perm.permission_level != "admin" for perm in permissions)

    # Delete the user and check if permissions are also handled
    delete_user_profile(user_id)
    assert get_user_profile(user_id) is None
    # Assuming deleting a user also clears their permissions
    permissions = get_user_permissions(user_id)
    assert len(permissions) == 0

def test_access_request_and_logging(session):
    user_id = add_user("Access Logging User", b"access_logging_data")

    # Log an access request
    request_id = log_access_request(user_id, "read", True, b"request_facial_data")
    assert request_id is not None

    # Add an access log for the request
    add_access_log(access_request_id=request_id, details="Access granted for reading.")
    logs = get_user_access_logs(user_id)
    assert len(logs) > 0
    assert any(log.details == "Access granted for reading." for log in logs)

def test_permission_changes_impact_on_access(session):
    user_id = add_user("Permission Impact User", b"permission_impact_data")
    # Initially grant a read permission
    add_permission_to_user(user_id, "read")
    is_read_allowed = validate_access_for_user(user_id, "read")
    assert is_read_allowed is True

    # Now, revoke read permission and check access
    revoke_user_permissions(user_id, "read")
    is_read_allowed = validate_access_for_user(user_id, "read")
    assert is_read_allowed is False

    # Optionally, add a different permission and test access for a different operation
    add_permission_to_user(user_id, "write")
    is_write_allowed = validate_access_for_user(user_id, "write")
    assert is_write_allowed is True
