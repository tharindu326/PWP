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
        face_image = 'data/Obama.jpg'
        with open(face_image, 'rb') as file:
            blobData_face_Obama = file.read()

        face_image = 'data/Biden.jpg'
        with open(face_image, 'rb') as file:
            blobData_face_Biden = file.read()

        face_image = 'data/Trump.jpg'
        with open(face_image, 'rb') as file:
            blobData_face_Trump = file.read()

        # USER SERVICES
        add_user("Biden", blobData_face_Biden)
        add_user("Trump", blobData_face_Trump)
        add_user("Obama", blobData_face_Obama)

        # Fetch and print user profile
        user = get_user_profile(1)
        print(f"User: {user.name}")

        # Update user facial data
        face_image = 'data/Biden2.jpg'
        with open(face_image, 'rb') as file:
            blobData_face_Biden2 = file.read()
        update_user_facial_data(1, blobData_face_Biden2)

        # Delete a user profile
        # delete_user_profile(3)

        # PERMISSION SERVICES
        # the access group can have different properties and they are managed by the client side
        add_permission_to_user(1, "Admin")  # Visitor, Employee, Supervisor, Security, Maintenance, Admin
        add_permission_to_user(1, "Employee")
        add_permission_to_user(2, "Supervisor")
        add_permission_to_user(2, "Employee")
        add_permission_to_user(3, "Security")
        add_permission_to_user(3, "Employee")

        # Get and print permissions for a user
        permissions = get_user_permissions(2)
        for permission in permissions:
            print(f"Permission: {permission.permission_level}")

        # Revoke a specific permission
        revoke_user_permissions(1, "Admin")

        # Revoke all permissions for user 3
        revoke_user_permissions(3)

        # ACCESS REQUEST SERVICES
        # for every incoming access requests with their required permission/permission list
        # clint will send face and the minimum access group for the access
        log_access_request(1, associated_permission="Admin", outcome="Granted")  # since 1 has admin permissions access granted

        requests = get_access_requests(1)
        for request in requests:
            print(f"Access Request at {request.timestamp} was {request.outcome}")

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

