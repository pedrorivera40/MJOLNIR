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

  ############################################
  #-------- Toggle User Active State --------#
  ############################################

  # def test_toggle_active(self):
  #   # TODO add a check for when you are trying to activate a non existent user.
  #   response = self.client.patch('/users/48/toggleActive',follow_redirects=True)
  #   self.assertEqual(response.status_code, 201)
  #   self.assertEqual(response.json['User']['email'], self.data['email'])
  #   self.assertEqual(response.json['User']['full_name'], self.data['full_name'])
  #   self.assertEqual(response.json['User']['id'], 48)
  #   self.assertEqual(response.json['User']['is_active'], True)
  #   self.assertEqual(response.json['User']['is_invalid'], False)
  #   self.assertEqual(response.json['User']['username'], self.data['username'])