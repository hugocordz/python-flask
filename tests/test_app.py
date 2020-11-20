import base64
import unittest
import json

from app import app


class SignupTest(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    def test_hello(self):
        response = self.app.get('/')

        self.assertEqual(200, response.status_code)
        self.assertIsNotNone(response.data)

    def test_exchange_401(self):
        response = self.app.get('/exchange')
        self.assertEqual(401, response.status_code)
        self.assertEqual('Unauthorized', response.json['name'])

    def test_register_user(self):
        payload = json.dumps({
            "password": "password",
            "name": "user",
            "admin": False
        })

        response = self.app.post('/register', headers={"Content-Type": "application/json"}, data=payload)

        self.assertEqual(200, response.status_code)
        self.assertEqual('registered successfully', response.json['message'])

    def test_login(self):
        response = self.app.post('/login', headers={
            "Authorization": "Basic {}".format(base64.b64encode(b"user:password").decode("utf8"))})
        self.assertEqual(200, response.status_code)
        self.assertIsNotNone(response.json['token'])

    def test_exchange(self):
        response_login = self.app.post('/login', headers={
            "Authorization": "Basic {}".format(base64.b64encode(b"user:password").decode("utf8"))})
        response = self.app.get('/exchange', headers={"x-access-token": response_login.json['token']})
        self.assertEqual(200, response.status_code)
        self.assertIsNotNone(response.json['rates'])
