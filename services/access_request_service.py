from database_models import AccessRequest, db


def log_access_request(user_id, associated_permission, outcome, associated_facial_data):
    new_request = AccessRequest(user_profile_id=user_id, associated_permission=associated_permission, outcome=outcome,
                                associated_facial_data=associated_facial_data)
    db.session.add(new_request)
    db.session.commit()
    return new_request.id


def get_access_requests(user_id):
    return AccessRequest.query.filter_by(user_profile_id=user_id).order_by(AccessRequest.timestamp.desc()).all()


if __name__ == "__main__":
    log_access_request(1, "Admin", "Granted", associated_facial_data=None)
    requests = get_access_requests(1)
    for request in requests:
        print(f"Access Request at {request.timestamp} was {request.outcome}")
