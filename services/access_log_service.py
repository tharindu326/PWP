from database_models import AccessLog, AccessRequest, db


def add_access_log(access_request_id, details):
    access_log = AccessLog(access_request_id=access_request_id, details=details)
    db.session.add(access_log)
    db.session.commit()


def get_user_access_logs(user_id):
    return db.session.query(AccessLog)\
        .join(AccessRequest, AccessLog.access_request_id == AccessRequest.id)\
        .filter(AccessRequest.user_profile_id == user_id)\
        .order_by(AccessRequest.timestamp.desc()).all()


def get_access_log(log_id):
    return AccessLog.query.get(log_id)

