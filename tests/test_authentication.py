from flask import Flask
from flask_io import FlaskIO, fields
from flask_io.authentication import Authentication
from unittest import TestCase


class TestAuthorization(TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.io = FlaskIO()
        self.io.init_app(self.app)
        self.client = self.app.test_client()

    def test_with_token(self):
        @self.app.route('/resource', methods=['GET'])
        @self.io.authentication(TokenAuthentication)
        def test():
            pass

        response = self.client.get('/resource', headers={'Authorization': 'token'})
        self.assertEqual(response.status_code, 204)

    def test_missing_token(self):
        @self.app.route('/resource', methods=['GET'])
        @self.io.authentication(TokenAuthentication)
        def test():
            pass
        response = self.client.get('/resource')
        self.assertEqual(response.status_code, 401)


class TokenAuthentication(Authentication):
    def authenticate(self, request):
        if request.headers.get('Authorization') is None:
            return None
        return 'user', 'auth'