import os
import unittest
import json
from main import app
from tests.newUserData import newUser, newUserID


class TestUserRoutes(unittest.TestCase):
    # executed prior to each test
    def setUp(self):
        app.config['DEBUG'] = True
        self.userBadParams = {
            'usrname': 'newUser37',
            'emaicl': 'newuser37@email.com',
            'fcull_name': 'New User37',
            'pasord': 'N3wP4ssword!',
        }
        self.userEmptyParams = {
            'username': None,
            'email': None,
            'full_name': None,
            'password': None,
        }
        self.client = app.test_client()

    ################################
    #-------- Adding users --------#
    ################################

    def test_add_new_user_empty_request(self):
        response = self.client.post('/users/', data=json.dumps({}),
                                    content_type='application/json', follow_redirects=True)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['Error'], 'Bad Request.')

    def test_add_new_user_bad_params(self):
        response = self.client.post('/users/', data=json.dumps(self.userBadParams),
                                    content_type='application/json', follow_redirects=True)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['Error'], 'Bad Request.')

    def test_add_new_user_empty_params(self):
        response = self.client.post('/users/', data=json.dumps(self.userEmptyParams),content_type='application/json', follow_redirects=True)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['Error'],'Request Parameters Undefined.')

    #################################
    #-------- Getting users --------#
    #################################

    def test_get_user_by_username_empty_request(self):
        response = self.client.post('/users/username/', data=json.dumps(
            {}), content_type='application/json', follow_redirects=True)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['Error'], 'Bad Request.')

    def test_get_user_by_username_bad_params(self):
        response = self.client.post('/users/username/', data=json.dumps(
            self.userBadParams), content_type='application/json', follow_redirects=True)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['Error'], 'Bad Request.')

    def test_get_user_by_username_empty_params(self):
        response = self.client.post('/users/username/', data=json.dumps(
            self.userEmptyParams), content_type='application/json', follow_redirects=True)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['Error'],'Request Parameters Undefined.')

    def test_get_user_by_email_empty_request(self):
        response = self.client.post('/users/email/', data=json.dumps({}),
                                    content_type='application/json',  follow_redirects=True)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['Error'], 'Bad Request.')

    def test_get_user_by_email_bad_params(self):
        response = self.client.post('/users/email/', data=json.dumps(
            self.userBadParams), content_type='application/json',  follow_redirects=True)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['Error'], 'Bad Request.')

    def test_get_user_by_email_empty_params(self):
        response = self.client.post('/users/email/', data=json.dumps(
            self.userEmptyParams), content_type='application/json',  follow_redirects=True)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['Error'],'Request Parameters Undefined.')

    #########################################
    #-------- Activate User Account --------#
    #########################################

    def test_account_activation_empty_request(self):
        response = self.client.patch('/users/activate', data=json.dumps({}), content_type='application/json',  follow_redirects=True)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['Error'],'Bad Request.')

    def test_account_activation_bad_parameters(self):
        loginInfo = {
          'useame': None,
          'paword': None,
          'newassword': None
        }
        response = self.client.patch('/users/activate', data=json.dumps(loginInfo), content_type='application/json',  follow_redirects=True)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['Error'],'Bad Request.')

    def test_account_activation_empty_parameters(self):
        loginInfo = {
          'username': None,
          'password': None,
          'new_password': None
        }
        response = self.client.patch('/users/activate', data=json.dumps(loginInfo), content_type='application/json',  follow_redirects=True)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['Error'],'Request Parameters Undefined.')

    #########################
    #-------- Login --------#
    #########################

    def test_login_empty_request(self):
        response = self.client.post('/auth/', data=json.dumps({}), content_type='application/json',  follow_redirects=True)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['Error'],'Bad Request.')

    def test_login_bad_parameters(self):
        loginInfo = {
          'usersdsdname': 'iujhasviun',
          'passssword': 'ninjaTurtles1!'
        }
        response = self.client.post('/auth/', data=json.dumps(loginInfo), content_type='application/json',  follow_redirects=True)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['Error'],'Bad Request.')

    def test_login_empty_parameters(self):
        loginInfo = {
          'username': None,
          'password': None
        }
        response = self.client.post('/auth/', data=json.dumps(loginInfo), content_type='application/json',  follow_redirects=True)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['Error'],'Request Parameters Undefined.')

  ######################################
  #-------- Resetting Password --------#
  ######################################

    def test_reset_password_empty_request(self):
      response = self.client.patch(f'/users/21/reset', data=json.dumps({}), content_type='application/json',  follow_redirects=True)
      self.assertEqual(response.status_code, 400)
      self.assertEqual(response.json['Error'],'Bad Request.')

    def test_reset_password_bad_parameters(self):
      response = self.client.patch(f'/users/21/reset', data=json.dumps({'passsssword' : 'newPaswordlololol1!'}), content_type='application/json',  follow_redirects=True)
      self.assertEqual(response.status_code, 400)
      self.assertEqual(response.json['Error'],'Bad Request.')

    def test_reset_password_empty_parameter(self):
      response = self.client.patch(f'/users/21/reset', data=json.dumps({'password' : None}), content_type='application/json',  follow_redirects=True)
      self.assertEqual(response.status_code, 400)
      self.assertEqual(response.json['Error'],'Request Parameters Undefined.')

    # #######################################################
    # #-------- Set User Permissions fot the System --------#
    # #######################################################

    def test_set_user_permissions_empty_request(self):
        response = self.client.patch(f'/users/21/permissions', data=json.dumps({}), content_type='application/json',  follow_redirects=True)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['Error'], 'Bad Request.')

    def test_set_user_permissions_bad_parameters(self):
        default_permissions = {"pissions": [
                {
                    "is_invalid": True,
                    "permission_id": 13
                },
                {
                    "is_invalid": False,
                    "permission_id": 14
                },
                {
                    "is_invalid": False,
                    "permission_id": 15
                },
                {
                    "is_invalid": True,
                    "permission_id": 16
                },
                {
                    "is_invalid": False,
                    "permission_id": 17
                },
                {
                    "is_invalid": False,
                    "permission_id": 18
                },
                {
                    "is_invalid": False,
                    "permission_id": 19
                },
                {
                    "is_invalid": False,
                    "permission_id": 20
                },
                {
                    "is_invalid": False,
                    "permission_id": 21
                },
                {
                    "is_invalid": False,
                    "permission_id": 22
                },
                {
                    "is_invalid": False,
                    "permission_id": 23
                },
                {
                    "is_invalid": False,
                    "permission_id": 24
                },
                {
                    "is_invalid": False,
                    "permission_id": 25
                },
                {
                    "is_invalid": False,
                    "permission_id": 26
                },
                {
                    "is_invalid": True,
                    "permission_id": 27
                }]}
        response = self.client.patch(f'/users/21/permissions', data=json.dumps(default_permissions), content_type='application/json',  follow_redirects=True)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['Error'], 'Bad Request.')
        
    def test_set_user_permissions_empty_parameters(self):
        default_permissions = {"permissions": None}
        response = self.client.patch(f'/users/21/permissions', data=json.dumps(default_permissions), content_type='application/json',  follow_redirects=None)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['Error'], 'Permissions cant be empty.')

    def test_set_user_permissions_bad_parameters_inside_list(self):
        default_permissions = {"permissions": [
                {
                    8: True,
                },
                {
                    "14": False,
                },
                {
                    "lolo": False,
                },
                {
                    "45": True,
                },
                {
                    "17": False,
                },
                {
                    "18": False,
                },
                {
                    "19": False,
                },
                {
                    "20": False,
                },
                {
                    "1": False,
                },
                {
                    0: False,
                },
                {
                    23: False,
                },
                {
                    24: False,
                },
                {
                    25: False,
                },
                {
                    "26": False,
                },
                {
                    27: True,
                }]}
        response = self.client.patch(f'/users/21/permissions', data=json.dumps(default_permissions), content_type='application/json',  follow_redirects=True)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['Error'], 'Bad Request.')
        
    def test_set_user_permissions_empty_parameters_inside_list(self):
        default_permissions = {"permissions": [
                {
                    "13": None,
                },
                {
                    "14": None,
                },
                {
                    "15": None,
                },
                {
                    "16": None,
                },
                {
                    "17": None,
                },
                {
                    "18": None,
                },
                {
                    "19": None,
                },
                {
                    "20": None,
                },
                {
                    "21": None,
                },
                {
                    "22": None,
                },
                {
                    "23": None,
                },
                {
                    "24": None,
                },
                {
                    "25": None,
                },
                {
                    "26": None,
                },
                {
                    "27": None,
                }]}
        response = self.client.patch(f'/users/125/permissions', data=json.dumps(default_permissions), content_type='application/json',  follow_redirects=None)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['Error'], 'Request Parameters Undefined.')


