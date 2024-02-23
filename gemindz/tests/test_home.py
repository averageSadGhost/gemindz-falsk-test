import unittest
from flask import Flask
from routes.home import home_bp


class HomeRouteTestCase(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.config['TESTING'] = True
        self.app.register_blueprint(home_bp)
        self.client = self.app.test_client()

    def test_home_endpoint(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        data = response.json
        self.assertTrue(data['message'].startswith('The server is up and running for'))


if __name__ == '__main__':
    unittest.main()
