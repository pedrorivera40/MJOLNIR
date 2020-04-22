import unittest
import json
from main import app
from tests.pbp_tests.game_actions.actions_data import data


class TestEditValidVolleyballPBP(unittest.TestCase):

    # Setup mock client.
    def setUp(self):
        app.config['DEBUG'] = True
        self.client = app.test_client()

    def test_edit_valid_notification(self):
        response = self.client.put('/pbp/Voleibol/actions', data=json.dumps(
            data["edit_valid_notification"]), content_type='application/json', follow_redirects=True)
        expected_msg = "Edit game action success."
        self.assertEqual(response.status_code, 200)
        self.assertMultiLineEqual(expected_msg, response.json["MSG"])

    def test_edit_valid_score_to_error(self):
        response = self.client.put('/pbp/Voleibol/actions', data=json.dumps(
            data["edit_valid_score_to_error"]), content_type='application/json', follow_redirects=True)
        expected_msg = "Edit game action success."
        self.assertEqual(response.status_code, 200)
        self.assertMultiLineEqual(expected_msg, response.json["MSG"])
