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

  ###########################################
  #-------- Remove User From System --------#
  ###########################################

  def test_remove_user(self):
    #  TODO ADD a check to check if trying to remove an already removed user.
    # TODO Make user inactive when removing the user.
    response = self.client.patch(f'/users/{newUserID}/remove',follow_redirects=True)
    self.assertEqual(response.status_code, 201)
    self.assertEqual(response.json['User']['email'], self.data['email'])
    self.assertEqual(response.json['User']['full_name'], self.data['full_name'])
    self.assertEqual(response.json['User']['id'], newUserID)
    self.assertEqual(response.json['User']['is_active'], False)
    self.assertEqual(response.json['User']['is_invalid'], False)
    self.assertEqual(response.json['User']['username'], self.data['username'])

  ###########################################################
  # -------- Test Performing Actions on Removed Users --------#
  ###########################################################
  
  def test_get_user_by_id_of_removed_user(self):
      response = self.client.get(f'/users/{newUserID}', follow_redirects=True)
      self.assertEqual(response.status_code, 404)
      self.assertEqual(response.json['Error'], 'No user found in the system with that id.') # TODO add corresponding error message

  def test_get_user_by_username_of_removed_user(self):
    response = self.client.post('/users/username/', data=json.dumps({'username': self.data['username']}),content_type='application/json',  follow_redirects=True)
    self.assertEqual(response.status_code, 404)
    self.assertEqual(response.json['Error'], 'No user found in the system with that username.') # TODO add corresponding error message