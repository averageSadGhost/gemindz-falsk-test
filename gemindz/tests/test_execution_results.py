import unittest
from flask import Flask
from flask_jwt_extended import JWTManager
from models import db, User, ExecutionResult
from routes.execution_results import execution_results_bp
from routes.auth import auth_bp
from routes.test_cases import test_cases_bp


class TestExecutionResultsEndpoints(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app.config['JWT_SECRET_KEY'] = '34kt0OC79E9_vAgP7NkeRgqhiChiVCVT0MpDlzM_JI0'
        self.app.config['JWT_TOKEN_LOCATION'] = ['headers', 'cookies']

        db.init_app(self.app)
        JWTManager(self.app)

        self.app.register_blueprint(execution_results_bp)
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
        if data:
            return data.get('access_token')
        else:
            print("Error getting token:", response.data)
            return None

    def test_record_execution_result(self):
        token = self.get_token('test_user', 'password')
        headers = {'Authorization': 'Bearer ' + token}
        # Create a new test case
        response = self.client.post('/testcases/', headers=headers, json={"name": "Test Case"})
        self.assertEqual(response.status_code, 201)
        test_case_id = response.json.get('test_case').get('id')
        execution_data = {
            "test_case_id": test_case_id,
            "test_asset_id": 1,
            "result": "pass"
        }
        response = self.client.post('/execution_results', json=execution_data, headers=headers)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json.get('message'), "Execution result recorded successfully")
        # Check if the execution result details are returned
        execution_result = response.json.get('execution_result')
        self.assertIsNotNone(execution_result)
        self.assertIn('id', execution_result)
        self.assertIn('test_case_id', execution_result)
        self.assertIn('test_asset_id', execution_result)
        self.assertIn('result', execution_result)

    def test_get_execution_results_for_test_asset(self):
        with self.app.app_context():
            # Create a test execution result
            execution_result = ExecutionResult(test_case_id=1, test_asset_id=1, result='pass')
            db.session.add(execution_result)
            db.session.commit()

        # Retrieve execution results for the test asset
        response = self.client.get('/execution_results/1')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.json) > 0)


if __name__ == '__main__':
    unittest.main()
