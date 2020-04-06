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

  #############################################################
  # -------- Test Performing Actions on Removed Users --------#
  #############################################################
  
  def test_remove_removed_user(self):
    #  TODO ADD a check to check if trying to remove an already removed user.
    # TODO Make user inactive when removing the user.
    response = self.client.patch(f'/users/{newUserID}/remove',follow_redirects=True)
    self.assertEqual(response.status_code, 404)
    self.assertEqual(response.json['Error'], 'No user found in the system with that id.')
  
  def test_get_user_by_id_of_removed_user(self):
      response = self.client.get(f'/users/{newUserID}', follow_redirects=True)
      self.assertEqual(response.status_code, 404)
      self.assertEqual(response.json['Error'], 'No user found in the system with that id.') # TODO add corresponding error message

  def test_get_user_by_username_of_removed_user(self):
    # Make sure to put data of a removed user
    response = self.client.post('/users/username/', data=json.dumps({'username': 'toriko'}),content_type='application/json',  follow_redirects=True)
    self.assertEqual(response.status_code, 404)
    self.assertEqual(response.json['Error'], 'No user found in the system with that username.') # TODO add corresponding error message

  def test_toggle_active_on_removed_user(self):
    response = self.client.patch(f'/users/{newUserID}/toggleActive',follow_redirects=True)
    self.assertEqual(response.status_code, 404)
    self.assertEqual(response.json['Error'], 'No user found in the system with that id.') 

  def test_add_new_user_with_username_of_removed_user(self):
    newUserOldUsername = {
          'email' : 'iklo9@email.com',
          'full_name' : 'Barbell Bayron',
          'username' : self.data['username'],
          'password' : 'ninjaTurtles'
    }
    id = newUserID + 1
    response = self.client.post('/users/', data=json.dumps(newUserOldUsername),content_type='application/json', follow_redirects=True)
    self.assertEqual(response.status_code, 201)
    self.assertEqual(response.json['User']['email'], newUserOldUsername['email'])
    self.assertEqual(response.json['User']['full_name'], newUserOldUsername['full_name'])
    self.assertEqual(response.json['User']['id'], id)
    self.assertEqual(response.json['User']['is_active'], False)
    self.assertEqual(response.json['User']['is_invalid'], False)
    self.assertEqual(response.json['User']['username'], newUserOldUsername['username'])