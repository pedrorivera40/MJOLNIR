import os
import unittest
import json
from main import app
from tests.newUserData import newUser, newUserID

class TestUserRoutes(unittest.TestCase):
    # executed prior to each test
    def setUp(self):
        self.default_permissions = {"permissions": [
                {
                    "13": True,
                },
                {
                    "14": False,
                },
                {
                    "15": False,
                },
                {
                    "16": True,
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
                    "21": False,
                },
                {
                    "22": False,
                },
                {
                    "23": False,
                },
                {
                    "24": False,
                },
                {
                    "25": False,
                },
                {
                    "26": False,
                },
                {
                    "27": True,
                }]}
        app.config['DEBUG'] = True
        self.data = newUser
        self.client = app.test_client()

    #######################################################
    #-------- Set User Permissiona fot the System --------#
    #######################################################

    def test_set_user_permissions(self):
        response = self.client.patch(f'/users/{newUserID}/permissions', data=json.dumps(self.default_permissions), content_type='application/json',  follow_redirects=True)
        self.assertEqual(response.status_code, 201)
        for permission in response.json['Permissions']:
            dkey = ''
            for key in permission.keys():
                dkey = key
                if dkey == "13":
                    self.assertEqual(permission[dkey], True)
                elif dkey == "16":
                    self.assertEqual(permission[dkey], True)
                elif dkey == "27":
                    self.assertEqual(permission[dkey], True)
                else:
                    self.assertEqual(permission[dkey], False)

    def test_set_user_permissions_inexistent_user(self):
        response = self.client.patch(f'/users/89238/permissions', data=json.dumps(self.default_permissions), content_type='application/json',  follow_redirects=True)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json['Error'], 'No se encontró ningún usuario en el sistema con ese id.')


    def test_set_user_permissions_empty_permissions(self):
        response = self.client.patch(f'/users/{newUserID}/permissions', data=json.dumps({'permissions': None}), content_type='application/json',  follow_redirects=True)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['Error'], 'Permissions cant be empty.')

    def test_set_user_permissions_invalid_format(self):
        response = self.client.patch(f'/users/{newUserID}/permissions', data=json.dumps({"permissions": [
                {
                    "8": True,
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
                    "0": False,
                },
                {
                    "23": False,
                },
                {
                    "24": False,
                },
                {
                    "25": False,
                },
                {
                    "26": False,
                },
                {
                    "27": True,
                }]}), content_type='application/json',  follow_redirects=True)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['Error'], 'Bad Request.')


