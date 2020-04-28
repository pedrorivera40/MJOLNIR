import unittest
import json
from main import app
from tests.pbp_tests.game_actions.actions_data import data

"""
Primarily testing invalid action_id, event_id, or wrong format in body.
This is agnostic to the game actions because these validations are performed before checking action_type.
"""


class TestEditValidVolleyballPBP(unittest.TestCase):

    # Setup mock client.
    def setUp(self):
        app.config['DEBUG'] = True
        self.client = app.test_client()

    def test_edit_invalid_notification1(self):
        # Try to edit notification with invalid event_id.
        response = self.client.put('/pbp/Voleibol/actions', data=json.dumps(
            data["edit_invalid_notification1"]), content_type='application/json', follow_redirects=True)
        expected_msg = "PBP Sequence does not exist."
        self.assertEqual(response.status_code, 403)
        self.assertMultiLineEqual(expected_msg, response.json["ERROR"])

    def test_edit_invalid_notification2(self):
        # Try to edit notification with invalid action_id.
        response = self.client.put('/pbp/Voleibol/actions', data=json.dumps(
            data["edit_invalid_notification2"]), content_type='application/json', follow_redirects=True)
        expected_msg = "Action does not exist."
        self.assertEqual(response.status_code, 500)
        self.assertMultiLineEqual(expected_msg, response.json["ERROR"])
