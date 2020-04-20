import os
import unittest
import json
import auth
import re

class TestUserRoutes(unittest.TestCase):

  def test_rules_match_password_10_chars(self):
    result = auth.rulesMatch('P4ssword!!')
    self.assertEqual(result, True)

  def test_rules_match_password_64_chars(self):
      result = auth.rulesMatch('newPaswordlololollololollololollololollololollololollololollol1!')
      self.assertEqual(result, True)

  def test_rules_match_password_shorter_than_10_chars(self):
      result = auth.rulesMatch('P4sword!')
      self.assertEqual(result, False)

  def test_rules_match_password_longer_than_64_chars(self):
      result = auth.rulesMatch('newPaswordlololollololollololollololollololollololollololollol1!111')
      self.assertEqual(result, False)

  def test_rules_match_password_no_upper_case(self):
      result = auth.rulesMatch('newpassword1!')
      self.assertEqual(result, False)

  def test_rules_match_password_no_lower_case(self):
      result = auth.rulesMatch('NEWPASSWORD1!')
      self.assertEqual(result, False)

  def test_rules_match_password_no_numbers(self):
      result = auth.rulesMatch('newPassword!!')
      self.assertEqual(result, False)

  def test_rules_match_password_no_special_characters(self):
      result = auth.rulesMatch('newPasword11')
      self.assertEqual(result, False)

  def test_password_hashing(self):
    password = 'secretPasswordHehe'
    hash = auth.createHash(password)
    self.assertEqual(auth.verifyHash(password,hash), True)

  def test_jwt_token_creation_and_verification(self):
    username = 'elCanserbero'
    permisions = {'permissions': 'somePermissions'}
    token = auth.generateToken(username,permisions)
    token = token.split(' ')[1]
    self.assertEqual(auth.verifyToken(token), True)