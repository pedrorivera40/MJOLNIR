import os
import unittest
import json
from main import app

class TestUserRoutes(unittest.TestCase):
  # executed prior to each test
  def setUp(self):
      app.config['DEBUG'] = True
      self.data = {
        'username': 'mhchito',
        'email': 'pesejo@email.com',
        'full_name': 'Mau Neo',
        'password':'someR4nd0mP455woRd',
      }
      self.client = app.test_client()


  def test_get_all_users(self):
    response = self.client.get('/users/', follow_redirects=True)
    self.assertEqual(response.status_code, 200)
      
  # def test_add_new_user(self):
  #   response = self.client.post('/users/',data=json.dumps(self.data),content_type='application/json', follow_redirects=True)
  #   self.assertEqual(response.status_code, 201)
  #   self.assertTrue(response.json['User']) == """ {
  #   "email": "pesejo@email.com",
  #   "full_name": "Mau Neo",
  #   "id": 22,
  #   "is_active": false,
  #   "is_invalid": false,
  #   "username": "mhchito"
  # } """

  def test_add_existent_user_email(self):
    response = self.client.post('/users/',data=json.dumps(self.data),content_type='application/json', follow_redirects=True)
    self.assertEqual(response.json['Error'], 'Email has been registered.') 

  def test_add_existent_user_username(self):
    response = self.client.post('/users/',data=json.dumps({
        'username': 'mhchito',
        'email': 'pjo@email.com',
        'full_name': 'Mau Neo',
        'password':'someR4nd0mP455woRd',
      }),content_type='application/json', follow_redirects=True)
    self.assertEqual(response.json['Error'], 'Username is already taken.') 

  def test_get_user_by_id(self):
    response = self.client.get('/users/22', follow_redirects=True)
    self.assertEqual(response.status_code, 200)
    self.assertTrue(response.json['User']) == """ {
    "email": "pesejo@email.com",
    "full_name": "Mau Neo",
    "id": 22,
    "is_active": false,
    "is_invalid": false,
    "username": "mhchito"
  } """

  def test_get_user_by_username(self):
    response = self.client.post('/users/username/', data=json.dumps({'username': self.data['username']}),content_type='application/json',  follow_redirects=True)
    self.assertEqual(response.status_code, 200)
    self.assertTrue(response.json['User']) == """ {
    "email": "pesejo@email.com",
    "full_name": "Mau Neo",
    "id": 22,
    "is_active": false,
    "is_invalid": false,
    "username": "mhchito"
  } """

  def test_get_user_by_email(self):
    response = self.client.post('/users/email/', data=json.dumps({'email' : self.data['email']}), content_type='application/json',  follow_redirects=True)
    self.assertEqual(response.status_code, 200)
    self.assertTrue(response.json['User']) == """ {
    "email": "pesejo@email.com",
    "full_name": "Mau Neo",
    "id": 22,
    "is_active": false,
    "is_invalid": false,
    "username": "mhchito"
    } """

  def test_reset_password(self):
    response = self.client.patch('/users/22/reset', data=json.dumps({'password' : 'newPaswordlololol'}), content_type='application/json',  follow_redirects=True)
    self.assertEqual(response.status_code, 201)
    self.assertTrue(response.json['User']) == """ {
    "email": "pesejo@email.com",
    "full_name": "Mau Neo",
    "id": 22,
    "is_active": false,
    "is_invalid": false,
    "username": "mhchito"
    } """

  def test_toggle_active(self):
    # TODO add a check for when you are trying to activate a non existent user.
    response = self.client.patch('/users/22/toggleActive',follow_redirects=True)
    self.assertEqual(response.status_code, 201)
    self.assertEqual(response.json['User']['is_active'], False)

  def test_remove_user(self):
    #  TODO ADD a check to check if trying to remove an already removed user.
    response = self.client.patch('/users/22/remove',follow_redirects=True)
    # self.assertEqual(response.status_code, 201)
    self.assertEqual(response.json['User']['is_invalid'], True) 



if __name__ == "__main__":
    unittest.main()