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

  ##########################################
  #-------- Adding Existent Users --------#
  #########################################

  # Error handling for add new user.
  
  def test_add_existent_user_email(self):
    response = self.client.post('/users/',data=json.dumps(self.data),content_type='application/json', follow_redirects=True)
    self.assertEqual(response.json['Error'], 'Email has been registered.') 

  def test_add_existent_user_username(self):
    response = self.client.post('/users/',data=json.dumps({
        'username': self.data['username'],
        'email': 'rellyDiffEmailLol@email.com',
        'full_name': self.data['full_name'],
        'password':'someR4nd0mP455woRd!',
      }),content_type='application/json', follow_redirects=True)
    self.assertEqual(response.json['Error'], 'Username is already taken.') 




if __name__ == "__main__":
    unittest.main()