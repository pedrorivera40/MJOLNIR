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

  #################################
  #-------- Getting users --------#
  #################################

  def test_get_all_users(self):
    response = self.client.get('/users/', follow_redirects=True)
    self.assertEqual(response.status_code, 200)

  def test_get_user_by_id(self):
    response = self.client.get(f'/users/{newUserID}', follow_redirects=True) # TODO: Again ID changes depending on the id of the user being added
    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.json['User']['email'], self.data['email'])
    self.assertEqual(response.json['User']['full_name'], self.data['full_name'])
    self.assertEqual(response.json['User']['id'], newUserID)
    self.assertEqual(response.json['User']['is_active'], False)
    self.assertEqual(response.json['User']['is_invalid'], False)
    self.assertEqual(response.json['User']['username'], self.data['username'])

  def test_get_user_by_inexistent_id(self):
    response = self.client.get('/users/2200000000', follow_redirects=True)
    self.assertEqual(response.status_code, 404)
    self.assertEqual(response.json['Error'], 'No se encontró ningún usuario en el sistema con ese id.') # TODO add corresponding error message

  def test_get_user_by_username(self):
    response = self.client.post('/users/username/', data=json.dumps({'username': self.data['username']}),content_type='application/json',  follow_redirects=True)
    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.json['User']['email'], self.data['email'])
    self.assertEqual(response.json['User']['full_name'], self.data['full_name'])
    self.assertEqual(response.json['User']['id'], newUserID)
    self.assertEqual(response.json['User']['is_active'], False)
    self.assertEqual(response.json['User']['is_invalid'], False)
    self.assertEqual(response.json['User']['username'], self.data['username'])

  def test_get_user_by_inexistent_username(self):
      response = self.client.post('/users/username/', data=json.dumps({'username': 'thisDoesNotExists'}), content_type='application/json', follow_redirects=True)
      self.assertEqual(response.status_code, 404)
      self.assertEqual(response.json['Error'], 'No se encontró ningún usuario en el sistema con ese nombre de usuario.')

  def test_get_user_by_email(self):
    response = self.client.post('/users/email/', data=json.dumps({'email' : self.data['email']}), content_type='application/json',  follow_redirects=True)
    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.json['User']['email'], self.data['email'])
    self.assertEqual(response.json['User']['full_name'], self.data['full_name'])
    self.assertEqual(response.json['User']['id'], newUserID)
    self.assertEqual(response.json['User']['is_active'], False)
    self.assertEqual(response.json['User']['is_invalid'], False)
    self.assertEqual(response.json['User']['username'], self.data['username'])

  def test_get_user_by_inexistent_email(self):
        response = self.client.post('/users/email/', data=json.dumps({'email': 'thisDoesNotExists'}), content_type='application/json', follow_redirects=True)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json['Error'], 'No se encontró ningún usuario en el sistema con ese correo electrónico.')
