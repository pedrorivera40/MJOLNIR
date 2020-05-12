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

    ##########################
    #-------- Lockout--------#
    ##########################

    def test_lockout(self):
        loginInfo = {
          'username': self.data['username'],
          'password': 'piljnvdijn'
        }

        for number in [1,2,3]:
          response = self.client.post('/auth/', data=json.dumps(loginInfo), content_type='application/json',  follow_redirects=True)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json['Error'], 'La cuenta ha sido desactivada, favor de activarla.')


