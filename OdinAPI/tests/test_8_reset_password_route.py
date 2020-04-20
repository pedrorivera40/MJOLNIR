import os
import unittest
import json
from main import app
from tests.newUserData import newUser, newUserID

class TestUserRoutes(unittest.TestCase):
  # executed prior to each test
  def setUp(self):
      app.config['DEBUG'] = True
      self.data = newUser
      self.client = app.test_client()

  ######################################
  #-------- Resetting Password --------#
  ######################################

  def test_reset_password(self):
    response = self.client.patch(f'/users/{newUserID}/reset', data=json.dumps({'password' : 'newPaswordlololol1!'}), content_type='application/json',  follow_redirects=True)
    self.assertEqual(response.status_code, 201)
    self.assertEqual(response.json['User']['email'], self.data['email'])
    self.assertEqual(response.json['User']['full_name'], self.data['full_name'])
    self.assertEqual(response.json['User']['id'], newUserID)
    self.assertEqual(response.json['User']['is_active'], False)
    self.assertEqual(response.json['User']['is_invalid'], False)
    self.assertEqual(response.json['User']['username'], self.data['username'])

  def test_reset_password_unexisten_user(self):
    response = self.client.patch(f'/users/8999/reset', data=json.dumps({'password' : 'newPaswordlololol1!'}), content_type='application/json',  follow_redirects=True)
    self.assertEqual(response.status_code, 404)
    self.assertEqual(response.json['Error'], 'No user found in the system with that id.')
