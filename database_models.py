from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class UserProfile(db.Model):
    __tablename__ = 'user_profiles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    facial_data = db.Column(db.LargeBinary)
    access_permissions = db.relationship('AccessPermission', backref='user_profile', lazy=True)
    access_requests = db.relationship('AccessRequest', backref='user_profile', lazy=True)


class AccessPermission(db.Model):
    __tablename__ = 'access_permissions'
    id = db.Column(db.Integer, primary_key=True)
    user_profile_id = db.Column(db.Integer, db.ForeignKey('user_profiles.id'))
    permission_level = db.Column(db.String(50))


class AccessRequest(db.Model):
    __tablename__ = 'access_requests'
    id = db.Column(db.Integer, primary_key=True)
    user_profile_id = db.Column(db.Integer, db.ForeignKey('user_profiles.id'))
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())
    outcome = db.Column(db.String(50))
    access_logs = db.relationship('AccessLog', backref='access_request', lazy=True)


class AccessLog(db.Model):
    __tablename__ = 'access_logs'
    id = db.Column(db.Integer, primary_key=True)
    access_request_id = db.Column(db.Integer, db.ForeignKey('access_requests.id'))
    details = db.Column(db.String(255))


if __name__ == '__main__':
    db.drop_all()
    db.create_all()

    # create user
    user1 = UserProfile(name="Tharindu", facial_data=b'SampleFacialData')
    db.session.add(user1)

    # create permission for the user
    permission1 = AccessPermission(permission_level="Admin", user_profile=user1)
    db.session.add(permission1)

    # create access request for the user
    access_request1 = AccessRequest(outcome="Granted", user_profile=user1)
    db.session.add(access_request1)

    # create access log for the request
    access_log1 = AccessLog(details="Entry door accessed", access_request=access_request1)
    db.session.add(access_log1)

    db.session.commit()
