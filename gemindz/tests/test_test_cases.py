import unittest
from flask import Flask
from flask_jwt_extended import JWTManager
from models import db, User
from routes.auth import auth_bp
from routes.test_cases import test_cases_bp


class TestEndpoints(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app.config['JWT_SECRET_KEY'] = '34kt0OC79E9_vAgP7NkeRgqhiChiVCVT0MpDlzM_JI0'
        self.app.config['JWT_TOKEN_LOCATION'] = ['headers', 'cookies']

        db.init_app(self.app)
        JWTManager(self.app)

        self.app.register_blueprint(auth_bp)
        self.app.register_blueprint(test_cases_bp)

        self.client = self.app.test_client()

        with self.app.app_context():
            db.create_all()
            user = User(username='test_user', password='password', role="admin")
            db.session.add(user)
            db.session.commit()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def get_token(self, username, password):
        response = self.client.post('/auth/login', json={'username': username, 'password': password})
        data = response.get_json()
        return data['access_token']

    def test_get_all_test_cases(self):
        token = self.get_token('test_user', 'password')
        headers = {'Authorization': 'Bearer ' + token}
        response = self.client.get('/testcases/', headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, [])  # Assuming no test cases initially

    def test_create_test_case(self):
        token = self.get_token('test_user', 'password')
        headers = {'Authorization': 'Bearer ' + token}
        new_test_case_data = {
            "name": "New Test Case",
            "description": "This is a new test case."
        }
        response = self.client.post('/testcases/', headers=headers, json=new_test_case_data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json, {
            "message": "Test case created successfully",
            "test_case": {
                "id": 1,
                "name": "New Test Case",
                "description": "This is a new test case."
            }
        })

    def test_get_single_test_case(self):
        token = self.get_token('test_user', 'password')
        headers = {'Authorization': 'Bearer ' + token}

        # Create a new test case
        response = self.client.post('/testcases/', headers=headers, json={"name": "Test Case"})
        self.assertEqual(response.status_code, 201)
        test_case_id = response.json.get('test_case').get('id')

        # Retrieve the created test case
        response = self.client.get(f'/testcases/{test_case_id}', headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {
            "id": test_case_id,
            "name": "Test Case",
            "description": ""
        })

    def test_update_test_case(self):
        token = self.get_token('test_user', 'password')
        headers = {'Authorization': 'Bearer ' + token}

        # Create a new test case
        response = self.client.post('/testcases/', headers=headers, json={"name": "Test Case"})
        self.assertEqual(response.status_code, 201)
        test_case_id = response.json.get('test_case').get('id')

        # Update the created test case
        updated_test_case_data = {
            "name": "Updated Test Case",
            "description": "This is an updated test case."
        }
        response = self.client.put(f'/testcases/{test_case_id}', headers=headers, json=updated_test_case_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {
            "message": "Test case updated successfully"
        })

    def test_delete_test_case(self):
        token = self.get_token('test_user', 'password')
        headers = {'Authorization': 'Bearer ' + token}

        # Create a new test case
        response = self.client.post('/testcases/', headers=headers, json={"name": "Test Case"})
        self.assertEqual(response.status_code, 201)
        test_case_id = response.json.get('test_case').get('id')

        # Delete the test case
        response = self.client.delete(f'/testcases/{test_case_id}', headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {
            "message": "Test case deleted successfully"
        })


if __name__ == '__main__':
    unittest.main()
