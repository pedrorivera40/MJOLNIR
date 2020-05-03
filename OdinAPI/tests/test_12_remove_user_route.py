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
    response = self.client.patch(f'/users/{newUserID}/remove',follow_redirects=True)
    self.assertEqual(response.status_code, 201)
    self.assertEqual(response.json['User']['email'], self.data['email'])
    self.assertEqual(response.json['User']['full_name'], self.data['full_name'])
    self.assertEqual(response.json['User']['id'], newUserID)
    self.assertEqual(response.json['User']['is_active'], False)
    self.assertEqual(response.json['User']['is_invalid'], True)
    self.assertEqual(response.json['User']['username'], self.data['username'])

  def test_remove_user_inexistent_user(self):
    response = self.client.patch(f'/users/666/remove',follow_redirects=True)
    self.assertEqual(response.status_code, 404)
    self.assertEqual(response.json['Error'], 'No se encontró ningún usuario en el sistema con ese id.')