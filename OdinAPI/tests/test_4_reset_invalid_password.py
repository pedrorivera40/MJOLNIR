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

  ###############################################
  #-------- Resetting Invalid Passwords --------#
  ###############################################
  def test_reset_password_8_chars(self):
    response = self.client.patch(f'/users/{newUserID}/reset', data=json.dumps({'password' : 'Pasword1'}), content_type='application/json',  follow_redirects=True)
    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.json['Error'], """Password should contain At least 1 upercase letter,
            1 lowecase letter, at least 1 number, at least 1 symbol, and is between 
            10 and 64 characters long.""")

  def test_reset_password_64_chars(self):
    response = self.client.patch(f'/users/{newUserID}/reset', data=json.dumps({'password' : 'newPaswordlololollololollololollololollololollololollololollol1!'}), content_type='application/json',  follow_redirects=True)
    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.json['Error'], """Password should contain At least 1 upercase letter,
            1 lowecase letter, at least 1 number, at least 1 symbol, and is between 
            10 and 64 characters long.""")

  def test_reset_password_shorter_than_8_chars(self):
    response = self.client.patch(f'/users/{newUserID}/reset', data=json.dumps({'password' : 'new!'}), content_type='application/json',  follow_redirects=True)
    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.json['Error'], """Password should contain At least 1 upercase letter,
            1 lowecase letter, at least 1 number, at least 1 symbol, and is between 
            10 and 64 characters long.""")

  def test_reset_password_longer_than_64_chars(self):
    response = self.client.patch(f'/users/{newUserID}/reset', data=json.dumps({'password' : 'newPaswordlololollololollololollololollololollololollololollol1!111'}), content_type='application/json',  follow_redirects=True)
    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.json['Error'], """Password should contain At least 1 upercase letter,
            1 lowecase letter, at least 1 number, at least 1 symbol, and is between 
            10 and 64 characters long.""")

  def test_reset_password_no_upper_case(self):
    response = self.client.patch(f'/users/{newUserID}/reset', data=json.dumps({'password' : 'newpassword1!'}), content_type='application/json',  follow_redirects=True)
    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.json['Error'], """Password should contain At least 1 upercase letter,
            1 lowecase letter, at least 1 number, at least 1 symbol, and is between 
            10 and 64 characters long.""")

  def test_reset_password_no_lower_case(self):
    response = self.client.patch(f'/users/{newUserID}/reset', data=json.dumps({'password' : 'NEWPASSWORD1!'}), content_type='application/json',  follow_redirects=True)
    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.json['Error'], """Password should contain At least 1 upercase letter,
            1 lowecase letter, at least 1 number, at least 1 symbol, and is between 
            10 and 64 characters long.""")

  def test_reset_password_no_numbers(self):
    response = self.client.patch(f'/users/{newUserID}/reset', data=json.dumps({'password' : 'newPassword!!'}), content_type='application/json',  follow_redirects=True)
    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.json['Error'], """Password should contain At least 1 upercase letter,
            1 lowecase letter, at least 1 number, at least 1 symbol, and is between 
            10 and 64 characters long.""")

  def test_reset_password_no_special_characters(self):
    response = self.client.patch(f'/users/{newUserID}/reset', data=json.dumps({'password' : 'newPasword11'}), content_type='application/json',  follow_redirects=True)
    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.json['Error'], """Password should contain At least 1 upercase letter,
            1 lowecase letter, at least 1 number, at least 1 symbol, and is between 
            10 and 64 characters long.""")