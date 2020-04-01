import os
import unittest
import json
from main import app
from tests.newUserData import newUser

class TestUserRoutes(unittest.TestCase):
  # executed prior to each test
  def setUp(self):
      app.config['DEBUG'] = True
      self.data = newUser
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




if __name__ == "__main__":
    unittest.main()