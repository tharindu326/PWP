from database_models import AccessPermission, db


def add_permission_to_user(user_id, permission_level):
    """
    Adds a new permission to a user if it does not already exist.
    Args:
        user_id (int): The ID of the user to add the permission to.
        permission_level (str): The level of permission to add.
    """
    existing_permission = AccessPermission.query.filter_by(user_profile_id=user_id,
                                                           permission_level=permission_level).first()
    if not existing_permission:
        new_permission = AccessPermission(user_profile_id=user_id, permission_level=permission_level)
        db.session.add(new_permission)
        db.session.commit()


def get_user_permissions(user_id):
    """
    Retrieves all permissions for a specific user.
    Args:
        user_id (int): The ID of the user whose permissions are to be retrieved.
    Returns:
        list: A list of AccessPermission objects associated with the user.
    """
    return AccessPermission.query.filter_by(user_profile_id=user_id).all()


def validate_access_for_user(user_id, required_permission_level):
    """
    Validates if a user has a specific permission level.
    Args:
        user_id (int): The ID of the user whose permissions are to be validated.
        required_permission_level (str): The required permission level to check.
    Returns:
        bool: True if the user has the required permission level, False otherwise.
    """
    user_permissions = AccessPermission.query.filter_by(user_profile_id=user_id).all()
    print('user_permissions', user_permissions)
    for user_permission in user_permissions:
        if user_permission.permission_level == required_permission_level:
            return True
    return False


def revoke_user_permissions(user_id, permission_level=None):
    """
    Revokes permissions from a user. If a specific permission level is provided, only that permission is revoked.
    Otherwise, all permissions are revoked.
    Args:
        user_id (int): The ID of the user whose permissions are to be revoked.
        permission_level (str, optional): The specific permission level to revoke. If None, all permissions are revoked.
    """
    if permission_level:
        # Revoke specific permission
        AccessPermission.query.filter_by(user_profile_id=user_id, permission_level=permission_level).delete()
    else:
        # Revoke all permissions
        # also if no specific level is provided it will also revoke all
        AccessPermission.query.filter_by(user_profile_id=user_id).delete()
    db.session.commit()
