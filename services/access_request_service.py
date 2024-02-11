from database_models import AccessRequest, db


def log_access_request(user_id, outcome):
    new_request = AccessRequest(user_profile_id=user_id, user_profile=outcome)
    db.session.add(new_request)
    db.session.commit()
    return new_request.id


def get_access_requests(user_id):
    return AccessRequest.query.filter_by(user_profile_id=user_id).order_by(AccessRequest.timestamp.desc()).all()


if __name__ == "__main__":
    log_access_request(1, "Granted")
    requests = get_access_requests(1)
    for request in requests:
        print(f"Access Reqest at {request.timestamp} was {request.outcome}")
