from database_models import AccessLog, AccessRequest, db


def add_access_log(access_request_id, details):
    """
    Adds a new access log entry to the database.
    Args:
        access_request_id (int): The ID of the associated access request.
        details (str): Additional details about the access log.
    """
    access_log = AccessLog(access_request_id=access_request_id, details=details)
    db.session.add(access_log)
    db.session.commit()


def get_user_access_logs(user_id):
    """
    Retrieves all access logs for a specific user, ordered by timestamp in descending order.
    Args:
        user_id (int): The ID of the user whose access logs are to be retrieved.
    Returns:
        list: A list of AccessLog objects associated with the user.
    """
    return db.session.query(AccessLog)\
        .join(AccessRequest, AccessLog.access_request_id == AccessRequest.id)\
        .filter(AccessRequest.user_profile_id == user_id)\
        .order_by(AccessRequest.timestamp.desc()).all()


def get_access_log(log_id):
    """
    Retrieves a specific access log entry by its ID.
    Args:
        log_id (int): The ID of the access log to retrieve.
    Returns:
        AccessLog: The AccessLog object corresponding to the specified log ID, or None if not found.
    """
    return AccessLog.query.get(log_id)

