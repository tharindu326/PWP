from database_models import AccessRequest, db


def log_access_request(user_id, associated_permission, outcome, associated_facial_data):
    """
    Logs a new access request in the database.
    Args:
        user_id (int): The ID of the user making the access request.
        associated_permission (str): The permission level associated with the access request.
        outcome (bool): The outcome of the access request (granted or denied).
        associated_facial_data (bytes): The facial data associated with the access request.
    Returns:
        int: The ID of the newly created access request.
    """
    new_request = AccessRequest(user_profile_id=user_id, associated_permission=associated_permission, outcome=outcome,
                                associated_facial_data=associated_facial_data)
    db.session.add(new_request)
    db.session.commit()
    return new_request.id


def get_user_access_requests(user_id):
    """
    Retrieves all access requests for a specific user, ordered by timestamp in descending order.
    Args:
        user_id (int): The ID of the user whose access requests are to be retrieved.
    Returns:
        list: A list of AccessRequest objects associated with the user.
    """
    return AccessRequest.query.filter_by(user_profile_id=user_id).order_by(AccessRequest.timestamp.desc()).all()


def get_access_request(access_request_id):
    """
    Retrieves a specific access request by its ID.
    Args:
        access_request_id (int): The ID of the access request to retrieve.
    Returns:
        AccessRequest: The AccessRequest object corresponding to the specified access request ID, or None if not found.
    """
    return AccessRequest.query.get(access_request_id)
