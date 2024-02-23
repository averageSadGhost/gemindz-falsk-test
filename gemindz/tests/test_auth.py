import unittest
import logging
from flask import Flask
from flask_jwt_extended import JWTManager
from models import db, User
from routes.auth import auth_bp

logging.basicConfig(level=logging.DEBUG)  # Set logging level to DEBUG


class AuthRouteTestCase(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app.config['JWT_SECRET_KEY'] = '34kt0OC79E9_vAgP7NkeRgqhiChiVCVT0MpDlzM_JI0'  # Set JWT secret key
        self.app.register_blueprint(auth_bp)
        db.init_app(self.app)
        JWTManager(self.app)
        with self.app.app_context():
            db.create_all()
        self.client = self.app.test_client()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_register_success(self):
        # Test registering a new user
        response = self.client.post('/auth/register', json={'username': 'test_user', 'password': 'password',
                                                            'role': 'admin'})
        self.assertEqual(response.status_code, 201)

    def test_register_existing_user(self):
        # Test registering a user that already exists
        new_user = User(username='existing_user', password='password')
        with self.app.app_context():
            db.session.add(new_user)
            db.session.commit()
        response = self.client.post('/auth/register', json={'username': 'existing_user', 'password': 'password',
                                                            'role': 'admin'})
        self.assertEqual(response.status_code, 400)

    def test_register_invalid_role(self):
        response = self.client.post('/auth/register', json={'username': 'test_user', 'password': 'password',
                                                            'role': 'invalid'})
        self.assertEqual(response.status_code, 400)

    def test_login_success(self):
        new_user = User(username='test_user', password='password')
        with self.app.app_context():
            db.session.add(new_user)
            db.session.commit()
        response = self.client.post('/auth/login', json={'username': 'test_user', 'password': 'password'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('access_token', response.json)

    def test_login_invalid_credentials(self):
        new_user = User(username='test_user', password='password')
        with self.app.app_context():
            db.session.add(new_user)
            db.session.commit()
        response = self.client.post('/auth/login', json={'username': 'test_user', 'password': 'wrong_password'})
        self.assertEqual(response.status_code, 401)


if __name__ == '__main__':
    unittest.main()
