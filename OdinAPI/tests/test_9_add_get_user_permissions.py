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

    #######################################################
    #-------- Set User Permissiona fot the System --------#
    #######################################################

    def test_get_user_permissions(self):
        """The add user permissions method is internal to the dao and is used when
        a new use is added to the system. To test that method works correctly
        we will perform a get of those permissions. Effectively testing both
        methods at the same time."""

        response = self.client.get(f'/users/{newUserID}/permissions', content_type='application/json',  follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        for permission in response.json['Permissions']:
            self.assertEqual(permission['is_invalid'], False)

    def test_get_user_permissions_inexistent_user(self):
        """The add user permissions method is internal to the dao and is used when
        a new use is added to the system. To test that method works correctly
        we will perform a get of those permissions. Effectively testing both
        methods at the same time."""

        response = self.client.get(f'/users/987438348/permissions', content_type='application/json',  follow_redirects=True)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json['Error'], 'No User found in the system with that id.')


