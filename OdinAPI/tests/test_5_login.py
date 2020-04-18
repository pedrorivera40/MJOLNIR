import os
import unittest
import json
from main import app
from tests.newUserData import newUser, newUserID
from auth import verifyToken

class TestUserRoutes(unittest.TestCase):
    # executed prior to each test
    def setUp(self):
        app.config['DEBUG'] = True
        self.data = newUser
        self.client = app.test_client()

    #######################################################
    #-------- Set User Permissiona fot the System --------#
    #######################################################

    def test_sucessful_login(self):
        loginInfo = {
          'username': self.data['username'],
          'password': 'ninjaTurtles1!'
        }
        response = self.client.post('/auth/', data=json.dumps(loginInfo), content_type='application/json',  follow_redirects=True)
        token = response.json['auth']['token'].split(' ')[1]
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['auth']['user'], self.data['username'])
        self.assertEqual(verifyToken(token), True)

    def test_wrong_password_login(self):
        loginInfo = {
          'username': self.data['username'],
          'password': 'piljnvdijn'
        }
        response = self.client.post('/auth/', data=json.dumps(loginInfo), content_type='application/json',  follow_redirects=True)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['Error'], 'Username or Password are incorrect.')

    def test_invalid_username_login(self):
        loginInfo = {
          'username': 'newUseriohihih20',
          'password': 'ninjaTurtles1!'
        }
        response = self.client.post('/auth/', data=json.dumps(loginInfo), content_type='application/json',  follow_redirects=True)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['Error'], 'Username or Password are incorrect.')

    def test_invalid_username__invalid_password_login(self):
        loginInfo = {
          'username': 'newUseriohihih20',
          'password': 'piljnvdijn'
        }
        response = self.client.post('/auth/', data=json.dumps(loginInfo), content_type='application/json',  follow_redirects=True)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['Error'], 'Username or Password are incorrect.')



