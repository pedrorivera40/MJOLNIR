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
      

  ################################
  #-------- Adding users --------#
  ################################

  def test_add_new_user(self):
    response = self.client.post('/users/',data=json.dumps(self.data),content_type='application/json', follow_redirects=True)
    self.assertEqual(response.status_code, 201)
    self.assertEqual(response.json['User']['email'], self.data['email'])
    self.assertEqual(response.json['User']['full_name'], self.data['full_name'])
    self.assertEqual(response.json['User']['id'], newUserID)
    self.assertEqual(response.json['User']['is_active'], False)
    self.assertEqual(response.json['User']['is_invalid'], False)
    self.assertEqual(response.json['User']['username'], self.data['username'])
    
  def test_add_new_user_bad_password(self):
    self.data['password'] = 'shitPaswd'
    response = self.client.post('/users/',data=json.dumps(self.data),content_type='application/json', follow_redirects=True)
    self.assertEqual(response.status_code, 400)
    self.assertEqual(response.json['Error'], """La contraseña debe contener al menos 1 letra mayúscula, 
            1 minúscula, 1 símbolo, y debe tener entre 10 y 64 caracteres.""")
    

if __name__ == "__main__":
    unittest.main()