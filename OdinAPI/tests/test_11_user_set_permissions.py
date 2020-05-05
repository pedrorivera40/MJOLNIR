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
                    13: True,
                },
                {
                    14: False,
                },
                {
                    15: False,
                },
                {
                    16: True,
                },
                {
                    17: False,
                },
                {
                    18: False,
                },
                {
                    19: False,
                },
                {
                    20: False,
                },
                {
                    21: False,
                },
                {
                    22: False,
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
                    26: False,
                },
                {
                    27: True,
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
                if dkey == 13:
                    self.assertEqual(permission[dkey], True)
                elif dkey == 16:
                    self.assertEqual(permission[dkey], True)
                elif dkey == 27:
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

    # def test_set_user_permissions_invalid_format(self):
    #     response = self.client.patch(f'/users/{newUserID}/permissions', data=json.dumps({"permissions": [
    #             {
    #                 "is_inlid": True,
    #                 "permison_id": 13
    #             },
    #             {
    #                 "is_invalid": False,
    #                 "permission_id": 14
    #             },
    #             {
    #                 "is_invalid": False,
    #                 "permission_id": 15
    #             },
    #             {
    #                 "is_invalid": True,
    #                 "permission_id": 16
    #             },
    #             {
    #                 "is_invalid": False,
    #                 "permission_id": 17
    #             },
    #             {
    #                 "is_invalid": False,
    #                 "permission_id": 18
    #             },
    #             {
    #                 "is_invalid": False,
    #                 "permission_id": 19
    #             },
    #             {
    #                 "is_invalid": False,
    #                 "permission_id": 20
    #             },
    #             {
    #                 "is_invalid": False,
    #                 "permission_id": 21
    #             },
    #             {
    #                 "is_invalid": False,
    #                 "permission_id": 22
    #             },
    #             {
    #                 "is_invalid": False,
    #                 "permission_id": 23
    #             },
    #             {
    #                 "is_invalid": False,
    #                 "permission_id": 24
    #             },
    #             {
    #                 "is_invalid": False,
    #                 "permission_id": 25
    #             },
    #             {
    #                 "is_invalid": False,
    #                 "permission_id": 26
    #             },
    #             {
    #                 "is_invalid": True,
    #                 "permission_id": 27
    #             }]}), content_type='application/json',  follow_redirects=True)
    #     self.assertEqual(response.status_code, 400)
    #     self.assertEqual(response.json['Error'], 'Bad Request.')


