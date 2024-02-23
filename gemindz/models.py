from database import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime


class BaseMixin(object):
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class TestCase(BaseMixin, db.Model):
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)

    # Define a relationship with ExecutionResults
    execution_results = db.relationship('ExecutionResult', backref='test_case', cascade='all, delete-orphan')

    def __init__(self, name, description):
        self.name = name
        self.description = description


class ExecutionResult(BaseMixin, db.Model):
    test_case_id = db.Column(db.Integer, db.ForeignKey('test_case.id', ondelete='CASCADE'), nullable=False)
    test_asset_id = db.Column(db.Integer, nullable=False)
    result = db.Column(db.String(50), nullable=False)

    def __init__(self, test_case_id, test_asset_id, result):
        self.test_case_id = test_case_id
        self.test_asset_id = test_asset_id
        self.result = result


class User(BaseMixin, db.Model):
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # Role: 'admin' or 'user'

    def __init__(self, username, password, role='user'):
        self.username = username
        self.password_hash = generate_password_hash(password)
        self.role = role

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Log(BaseMixin, db.Model):
    endpoint_name = db.Column(db.String(100), nullable=False)
    method = db.Column(db.String(10), nullable=False)
    status_code = db.Column(db.Integer, nullable=False)
    error = db.Column(db.Text)

    def __init__(self, endpoint_name, method, status_code, error=None):
        self.endpoint_name = endpoint_name
        self.method = method
        self.status_code = status_code
        self.error = error

    @classmethod
    def log_request(cls, endpoint, method, status_code, error=None):
        new_log = cls(
            endpoint_name=endpoint,
            method=method,
            status_code=status_code,
            error=error
        )
        db.session.add(new_log)
        db.session.commit()
