import json

from starter_code.models.user import UserModel
from starter_code.tests.base_test import BaseTest


class UserTest(BaseTest):
    def test_register_user(self):
        with self.app() as client:
            with self.app_context():
                response = client.post('/register', data = {'username': 'test', 'password': '1234'})

                self.assertEqual(response.status_code, 201)
                self.assertIsNotNone(UserModel.find_by_username('test'))
                # json.loads() used to convert json format to python dictionary
                self.assertDictEqual({"message": "User created successfully."}, json.loads(response.data))

    def test_register_and_login(self):
        with self.app() as client:
            with self.app_context():
                client.post('/register', data = {'username': 'test', 'password': '1234'})
                # json.dumps() converts the python dict to json string (as '/auth' endpoint requires the data to be in json format)
                auth_response = client.post('/auth',
                                            data = json.dumps({'username': 'test', 'password': '1234'}),
                                            headers={'content-Type': 'application/json'})
                # auth_response is going to return the dictionary that looks like this:
                # {'access_token': 'ajhscdvjsdvcjashdgcsgdcyy7'}, read more about access_token

                self.assertIn('access_token', json.loads(auth_response.data).keys())

    def test_register_duplicate_user(self):
        with self.app() as client:
            with self.app_context():
                client.post('/register', data={'username': 'test', 'password': '1234'})
                response = client.post('/register', data = {'username': 'test', 'password': '1234'})

                self.assertEqual(response.status_code, 400)
                self.assertDictEqual({"message": "A user with that username already exists"}, json.loads(response.data))

    def test_register(self):
        with self.app() as client:
            with self.app_context():
                headers = {
                    'Content-Type': "application/json",
                    'Authorization': "JWT",
                    'cache-control': "no-cache",
                    'Postman-Token': "97c26c8c-1b17-46e7-aa6b-6c1e9e309c55"
                }
                auth_response = client.post('/register',
                                            data=json.dumps({'username': 'test', 'password': '1234'}),
                                            headers=headers)

                self.assertEqual(auth_response.status_code, 201)