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

    #############################################################
    # -------- Test Performing Actions on Removed Users --------#
    #############################################################

    def test_remove_removed_user(self):
        #  TODO ADD a check to check if trying to remove an already removed user.
        # TODO Make user inactive when removing the user.
        response = self.client.patch(
            f'/users/{newUserID}/remove', follow_redirects=True)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            response.json['Error'], 'No se encontró ningún usuario en el sistema con ese id.')

    def test_get_user_by_id_of_removed_user(self):
        response = self.client.get(
            f'/users/{newUserID}', follow_redirects=True)
        self.assertEqual(response.status_code, 404)
        # TODO add corresponding error message
        self.assertEqual(
            response.json['Error'], 'No se encontró ningún usuario en el sistema con ese id.')

    def test_get_user_by_username_of_removed_user(self):
        # Make sure to put data of a removed user
        response = self.client.post('/users/username/', data=json.dumps(
            {'username': 'newUser19'}), content_type='application/json',  follow_redirects=True)
        self.assertEqual(response.status_code, 404)
        # TODO add corresponding error message
        self.assertEqual(
            response.json['Error'], 'No se encontró ningún usuario en el sistema con ese nombre de usuario.')

    def test_toggle_active_on_removed_user(self):
        response = self.client.patch(
            f'/users/{newUserID}/toggleActive', follow_redirects=True)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            response.json['Error'], 'No se encontró ningún usuario en el sistema con ese id.')

    def test_get_user_permissions_removed_user(self):
        """The add user permissions method is internal to the dao and is used when
        a new use is added to the system. To test that method works correctly
        we will perform a get of those permissions. Effectively testing both
        methods at the same time."""

        response = self.client.get(
            f'/users/{newUserID}/permissions', content_type='application/json',  follow_redirects=True)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            response.json['Error'], 'No se encontró ningún usuario en el sistema con ese id.')

    def test_set_user_permissions_inexistent_user(self):
        response = self.client.patch(f'/users/{newUserID}/permissions', data=json.dumps(
            self.default_permissions), content_type='application/json',  follow_redirects=True)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            response.json['Error'], 'No se encontró ningún usuario en el sistema con ese id.')

    def test_add_new_user_with_username_of_removed_user(self):
        newUserOldUsername = {
            'email': 'newnewUser45email.com',
            'full_name': 'Newnew User45',
            'username': self.data['username'],
            'password': 'ninjaTurtles1!'
        }
        id = newUserID + 1
        response = self.client.post('/users/', data=json.dumps(
            newUserOldUsername), content_type='application/json', follow_redirects=True)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['User']
                         ['email'], newUserOldUsername['email'])
        self.assertEqual(
            response.json['User']['full_name'], newUserOldUsername['full_name'])
        self.assertEqual(response.json['User']['id'], id)
        self.assertEqual(response.json['User']['is_active'], False)
        self.assertEqual(response.json['User']['is_invalid'], False)
        self.assertEqual(
            response.json['User']['username'], newUserOldUsername['username'])
