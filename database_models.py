from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class UserProfile(db.Model):
    __tablename__ = 'user_profiles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    facial_data = db.Column(db.LargeBinary)
    access_permissions = db.relationship('AccessPermission', backref='user_profile', lazy=True)
    access_requests = db.relationship('AccessRequest', backref='user_profile', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'access_permissions': [access_permission.to_dict() for access_permission in self.access_permissions],
        }


class AccessPermission(db.Model):
    __tablename__ = 'access_permissions'
    id = db.Column(db.Integer, primary_key=True)
    user_profile_id = db.Column(db.Integer, db.ForeignKey('user_profiles.id'))
    permission_level = db.Column(db.String(50))

    def to_dict(self):
        return {
            'id': self.id,
            'user_profile_id': self.user_profile_id,
            'permission_level': self.permission_level
        }


class AccessRequest(db.Model):
    __tablename__ = 'access_requests'
    id = db.Column(db.Integer, primary_key=True)
    user_profile_id = db.Column(db.Integer, db.ForeignKey('user_profiles.id'))
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())
    outcome = db.Column(db.String(50))
    associated_permission = db.Column(db.String(50))  # minimum access/ access groups
    associated_facial_data = db.Column(db.LargeBinary)
    access_logs = db.relationship('AccessLog', backref='access_request', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'timestamp': str(self.timestamp),
            'outcome': self.outcome,
            # 'associated_facial_data': self.associated_facial_data,
            'associated_permission': self.associated_permission
        }


class AccessLog(db.Model):
    __tablename__ = 'access_logs'
    id = db.Column(db.Integer, primary_key=True)
    access_request_id = db.Column(db.Integer, db.ForeignKey('access_requests.id'))
    details = db.Column(db.String(255))

    def to_dict(self):
        return {
            "id": self.id,
            "access_request_id": self.access_request_id,
            "details": self.details,
        }

