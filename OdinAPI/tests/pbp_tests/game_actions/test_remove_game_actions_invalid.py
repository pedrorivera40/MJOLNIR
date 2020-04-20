import unittest
import json
from main import app
from tests.pbp_tests.game_actions.actions_data import data

class TestRemoveInvalidVolleyballPBP(unittest.TestCase):

    # Setup mock client.
    def setUp(self):
        app.config['DEBUG'] = True
        self.client = app.test_client()

    def test_invalid_pbp_to_remove1(self):
        response = self.client.delete('/pbp/actions',data=json.dumps(data["invalid_pbp_to_remove1"]),content_type='application/json', follow_redirects=True)
        expected_msg = "PBP Sequence does not exist."
        self.assertEqual(response.status_code, 403)
        self.assertMultiLineEqual(expected_msg, response.json["ERROR"])

    def test_invalid_pbp_to_remove2(self):
        response = self.client.delete('/pbp/actions',data=json.dumps(data["invalid_pbp_to_remove2"]),content_type='application/json', follow_redirects=True)
        expected_msg = "Action does not exist."
        self.assertEqual(response.status_code, 500)
        self.assertMultiLineEqual(expected_msg, response.json["ERROR"])