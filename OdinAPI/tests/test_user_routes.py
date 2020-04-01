import os
import unittest
import json
from main import app

class TestUserRoutes(unittest.TestCase):
  # executed prior to each test
  def setUp(self):
      app.config['DEBUG'] = True
      self.data = {
        'username': 'newUser17',
        'email': 'newuser17@email.com',
        'full_name': 'New User17',
        'password':'someR4nd0mP455woRd',
      }
      self.client = app.test_client()


  ################################
  #-------- Adding users --------#
  ################################

  # def test_add_new_user(self):
  #   response = self.client.post('/users/',data=json.dumps(self.data),content_type='application/json', follow_redirects=True)
  #   self.assertEqual(response.status_code, 201)
  #   self.assertEqual(response.json['User']['email'], self.data['email'])
  #   self.assertEqual(response.json['User']['full_name'], self.data['full_name'])
  #   self.assertEqual(response.json['User']['id'], 48)
  #   self.assertEqual(response.json['User']['is_active'], False)
  #   self.assertEqual(response.json['User']['is_invalid'], False)
  #   self.assertEqual(response.json['User']['username'], self.data['username'])
    

  # Error handling
  def test_add_existent_user_email(self):
    response = self.client.post('/users/',data=json.dumps(self.data),content_type='application/json', follow_redirects=True)
    self.assertEqual(response.json['Error'], 'Email has been registered.') 

  def test_add_existent_user_username(self):
    response = self.client.post('/users/',data=json.dumps({
        'username': self.data['username'],
        'email': 'rellyDiffEmailLol@email.com',
        'full_name': self.data['full_name'],
        'password':'someR4nd0mP455woRd',
      }),content_type='application/json', follow_redirects=True)
    self.assertEqual(response.json['Error'], 'Username is already taken.') 

  #################################
  #-------- Getting users --------#
  #################################

  def test_get_all_users(self):
    response = self.client.get('/users/', follow_redirects=True)
    self.assertEqual(response.status_code, 200)

  def test_get_user_by_id(self):
    response = self.client.get('/users/48', follow_redirects=True) # TODO: Again ID changes depending on the id of the user being added
    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.json['User']['email'], self.data['email'])
    self.assertEqual(response.json['User']['full_name'], self.data['full_name'])
    self.assertEqual(response.json['User']['id'], 48)
    self.assertEqual(response.json['User']['is_active'], False)
    self.assertEqual(response.json['User']['is_invalid'], False)
    self.assertEqual(response.json['User']['username'], self.data['username'])

  def test_get_user_by_inexistent_id(self):
    response = self.client.get('/users/2200000000', follow_redirects=True)
    self.assertEqual(response.status_code, 404)
    self.assertEqual(response.json['Error'], 'No user found in the system with that id.') # TODO add corresponding error message

  def test_get_user_by_username(self):
    response = self.client.post('/users/username/', data=json.dumps({'username': self.data['username']}),content_type='application/json',  follow_redirects=True)
    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.json['User']['email'], self.data['email'])
    self.assertEqual(response.json['User']['full_name'], self.data['full_name'])
    self.assertEqual(response.json['User']['id'], 48)
    self.assertEqual(response.json['User']['is_active'], False)
    self.assertEqual(response.json['User']['is_invalid'], False)
    self.assertEqual(response.json['User']['username'], self.data['username'])

  def test_get_user_by_email(self):
    response = self.client.post('/users/email/', data=json.dumps({'email' : self.data['email']}), content_type='application/json',  follow_redirects=True)
    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.json['User']['email'], self.data['email'])
    self.assertEqual(response.json['User']['full_name'], self.data['full_name'])
    self.assertEqual(response.json['User']['id'], 48)
    self.assertEqual(response.json['User']['is_active'], False)
    self.assertEqual(response.json['User']['is_invalid'], False)
    self.assertEqual(response.json['User']['username'], self.data['username'])

  # ######################################
  # #-------- Resetting Password --------#
  # ######################################

  def test_reset_password(self):
    response = self.client.patch('/users/22/reset', data=json.dumps({'password' : 'newPaswordlololol'}), content_type='application/json',  follow_redirects=True)
    self.assertEqual(response.status_code, 201)
    self.assertEqual(response.json['User']['email'], self.data['email'])
    self.assertEqual(response.json['User']['full_name'], self.data['full_name'])
    self.assertEqual(response.json['User']['id'], 48)
    self.assertEqual(response.json['User']['is_active'], False)
    self.assertEqual(response.json['User']['is_invalid'], False)
    self.assertEqual(response.json['User']['username'], self.data['username'])

  # ############################################
  # #-------- Toggle User Active State --------#
  # ############################################

  # def test_toggle_active(self):
  #   # TODO add a check for when you are trying to activate a non existent user.
  #   response = self.client.patch('/users/22/toggleActive',follow_redirects=True)
  #   self.assertEqual(response.status_code, 201)
  #   self.assertEqual(response.json['User']['email'], self.data['email'])
  #   self.assertEqual(response.json['User']['full_name'], self.data['full_name'])
  #   self.assertEqual(response.json['User']['id'], 48)
  #   self.assertEqual(response.json['User']['is_active'], False)
  #   self.assertEqual(response.json['User']['is_invalid'], False)
  #   self.assertEqual(response.json['User']['username'], self.data['username'])

  # ###########################################
  # #-------- Remove User From System --------#
  # ###########################################

  # def test_remove_user(self):
  #   #  TODO ADD a check to check if trying to remove an already removed user.
  #   # TODO Make user inactive when removing the user.
  #   response = self.client.patch('/users/22/remove',follow_redirects=True)
  #   self.assertEqual(response.status_code, 201)
  #   self.assertEqual(response.json['User']['email'], self.data['email'])
  #   self.assertEqual(response.json['User']['full_name'], self.data['full_name'])
  #   self.assertEqual(response.json['User']['id'], 48)
  #   self.assertEqual(response.json['User']['is_active'], False)
  #   self.assertEqual(response.json['User']['is_invalid'], False)
  #   self.assertEqual(response.json['User']['username'], self.data['username'])

  ############################################################
  #-------- Test Performing Actions on Removed Users --------#
  ############################################################
  
  # def test_get_user_by_id_of_removed_user(self):
  #     response = self.client.get('/users/48', follow_redirects=True)
  #     self.assertEqual(response.status_code, 404)
  #     self.assertEqual(response.json['Error'], 'No user found in the system with that id.') # TODO add corresponding error message

  # def test_get_user_by_username_of_removed_user(self):
  #   response = self.client.post('/users/username/', data=json.dumps({'username': self.data['username']}),content_type='application/json',  follow_redirects=True)
  #   self.assertEqual(response.status_code, 404)
  #   self.assertEqual(response.json['Error'], 'No user found in the system with that username.') # TODO add corresponding error message



if __name__ == "__main__":
    unittest.main()