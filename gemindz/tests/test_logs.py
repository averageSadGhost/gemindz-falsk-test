import unittest
from flask import Flask
from models import db, Log
from routes.logs import logs_bp


class LogsRouteTestCase(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app.register_blueprint(logs_bp)
        db.init_app(self.app)
        self.client = self.app.test_client()

        # Create application context
        self.app_context = self.app.app_context()
        self.app_context.push()

        # Create all tables in the database
        with self.app_context:
            db.create_all()

    def tearDown(self):
        # Remove application context
        self.app_context.pop()

    def test_get_logs_filter_endpoint_name(self):
        # Create a log entry
        with self.app_context:
            Log.log_request(endpoint='/test', method='GET', status_code=500, error=None)
        response = self.client.get('/logs?endpoint_name=/test', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        data = response.json
        self.assertEqual(len(data), 1)  # There should be one log with endpoint_name = '/test'

    def test_get_logs_filter_status_code(self):
        # Create a log entry
        with self.app_context:
            Log.log_request(endpoint='/test', method='GET', status_code=500, error=None)
        response = self.client.get('/logs?status_code=500', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        data = response.json
        self.assertEqual(len(data), 1)  # There should be one log with status_code = 500


if __name__ == '__main__':
    unittest.main()
