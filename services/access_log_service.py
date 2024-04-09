from database_models import AccessLog, AccessRequest, db
# from sqlalchemy import func


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


# def generate_access_report(start_date, end_date):
#     access_summary = db.session.query(AccessLog.details, func.count(AccessLog.id).label('access_count')).\
#         filter(AccessLog.timestamp >= start_date, AccessLog.timestamp <= end_date).group_by(AccessLog.details).all()
#
#     return [{"details": log.details, "access_count": log.access_count} for log in access_summary]


if __name__ == "__main__":
    add_access_log(1, "Door opened successfully")
    # fetch and print access logs for a user's access requests
    logs = get_user_access_logs(1)
    for log in logs:
        print(f"Log: {log.details} for Request ID {log.access_request_id}")
