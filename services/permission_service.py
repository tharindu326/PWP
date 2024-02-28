from database_models import AccessPermission, db


def add_permission_to_user(user_id, permission_level):
    new_permission = AccessPermission(user_profile_id=user_id, permission_level=permission_level)
    db.session.add(new_permission)
    db.session.commit()


def get_user_permissions(user_id):
    return AccessPermission.query.filter_by(user_profile_id=user_id).all()


def validate_access_for_user(user_id, required_permission_level):
    user_permissions = AccessPermission.query.filter_by(user_profile_id=user_id).all()
    for user_permission in user_permissions:
        if user_permission.permission_level == required_permission_level:
            return True
    return False


def revoke_user_permissions(user_id, permission_level=None):
    if permission_level:
        # Revoke specific permission
        AccessPermission.query.filter_by(user_profile_id=user_id, permission_level=permission_level).delete()
    else:
        # Revoke all permissions
        # also if no specific level is provided it will also revoke all
        AccessPermission.query.filter_by(user_profile_id=user_id).delete()
    db.session.commit()


if __name__ == "__main__":
    add_permission_to_user(1, "Admin")
    # Get and print permissions for a user
    permissions = get_user_permissions(1)
    for permission in permissions:
        print(f"Permission: {permission.permission_level}")
    # Revoke a specific permission
    revoke_user_permissions(1, "Admin")
    # Revoke all permissions
    revoke_user_permissions(1)
