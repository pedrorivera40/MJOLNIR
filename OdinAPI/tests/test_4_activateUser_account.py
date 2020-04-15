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

    #########################################
    #-------- Activate User Account --------#
    #########################################

    def test_account_activation(self):
        loginInfo = {
          'username': self.data['username'],
          'password': self.data['password'],
          'new_password': 'ninjaTurtles2!'
        }
        response = self.client.patch('/users/activate', data=json.dumps(loginInfo), content_type='application/json',  follow_redirects=True)
        print(response.json)
        self.assertEqual(response.json['User']['email'], self.data['email'])
        self.assertEqual(response.json['User']['full_name'], self.data['full_name'])
        self.assertEqual(response.json['User']['id'], newUserID)
        self.assertEqual(response.json['User']['is_active'], True)
        self.assertEqual(response.json['User']['is_invalid'], False)
        self.assertEqual(response.json['User']['username'], self.data['username'])


