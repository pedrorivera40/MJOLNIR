import unittest
import json
from main import app
from tests.pbp_tests.game_actions.actions_data import data

class TestRemoveValidVolleyballPBP(unittest.TestCase):

    # Setup mock client.
    def setUp(self):
        app.config['DEBUG'] = True
        self.client = app.test_client()

    def test_remove_valid_notification(self):
        response = self.client.delete('/pbp/actions',data=json.dumps(data["valid_to_remove"]),content_type='application/json', follow_redirects=True)
        expected_msg = "Removed game action"
        self.assertEqual(response.status_code, 200)
        self.assertMultiLineEqual(expected_msg, response.json["MSG"])