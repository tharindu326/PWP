from database_models import AccessPermission, db


def add_permission_to_user(user_id, permission_level):
    existing_permission = AccessPermission.query.filter_by(user_profile_id=user_id,
                                                           permission_level=permission_level).first()
    if not existing_permission:
        new_permission = AccessPermission(user_profile_id=user_id, permission_level=permission_level)
        db.session.add(new_permission)
        db.session.commit()


def get_user_permissions(user_id):
    return AccessPermission.query.filter_by(user_profile_id=user_id).all()


def validate_access_for_user(user_id, required_permission_level):
    user_permissions = AccessPermission.query.filter_by(user_profile_id=user_id).all()
    print('user_permissions', user_permissions)
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
