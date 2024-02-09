from flask import Flask
from database_models import *
from config import cfg
from services.access_log_service import *
from services.access_request_service import *
from services.permission_service import *
from services.user_service import *


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = cfg.db.SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = cfg.db.SQLALCHEMY_TRACK_MODIFICATIONS

db.init_app(app)


def main():
    with app.app_context():
        # create user
        face_image = 'data/out.jpg'
        with open(face_image, 'rb') as file:
            blobData_face = file.read()

        # USER SERVICES
        add_user("Obama", blobData_face)
        # Fetch and print user profile
        user = get_user_profile(1)
        print(f"User: {user.name}")
        # Update user facial data
        update_user_facial_data(1, blobData_face)
        # Delete a user profile
        delete_user_profile(1)

        # PERMISSION SERVICES
        add_permission_to_user(1, "Admin")
        # Get and print permissions for a user
        permissions = get_user_permissions(1)
        for permission in permissions:
            print(f"Permission: {permission.permission_level}")
        # Revoke a specific permission
        revoke_user_permissions(1, "Admin")
        # Revoke all permissions
        revoke_user_permissions(1)

        # ACCESS REQUEST SERVICES
        log_access_request(1, "Granted")
        requests = get_access_requests(1)
        for request in requests:
            print(f"Access Reqest at {request.timestamp} was {request.outcome}")

        # ACCESS LOG SERVICE
        add_access_log(1, "Door opened successfully")
        # fetch and print access logs for a user's access requests
        logs = get_user_access_logs(1)
        for log in logs:
            print(f"Log: {log.details} for Request ID {log.access_request_id}")


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        main()
    # app.run(debug=True)

