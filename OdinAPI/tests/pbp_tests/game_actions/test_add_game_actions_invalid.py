import unittest
import json
from main import app
from tests.pbp_tests.game_actions.actions_data import data

class TestAddInvalidActionVolleyballPBP(unittest.TestCase):

    # Setup mock client.
    def setUp(self):
        app.config['DEBUG'] = True
        self.client = app.test_client()

    def test_invalid_action_play(self):
        response = self.client.post('/pbp/actions',data=json.dumps(data["invalid_action_play"]),content_type='application/json', follow_redirects=True)
        expected_msg = "Undefined Volleyball PBP Sequence Game Action."
        self.assertEqual(response.status_code, 500)
        self.assertMultiLineEqual(expected_msg, response.json["ERROR"])

    def test_more_params_play(self):
        response = self.client.post('/pbp/actions',data=json.dumps(data["more_params_play"]),content_type='application/json', follow_redirects=True)
        expected_msg = "Action (data) must have 2 params for notification and 3 for game action."
        self.assertEqual(response.status_code, 500)
        self.assertMultiLineEqual(expected_msg, response.json["ERROR"])

    def test_message_limit_notification(self):
        response = self.client.post('/pbp/actions',data=json.dumps(data["message_limit_notification"]),content_type='application/json', follow_redirects=True)
        expected_msg = "Invalid message length (must be within 1 and 100 characters)."
        self.assertEqual(response.status_code, 500)
        self.assertMultiLineEqual(expected_msg, response.json["ERROR"])

    def test_more_params_notification(self):
        response = self.client.post('/pbp/actions',data=json.dumps(data["more_params_notification"]),content_type='application/json', follow_redirects=True)
        expected_msg = "Notifications can only have action_type and message"
        self.assertEqual(response.status_code, 500)
        self.assertMultiLineEqual(expected_msg, response.json["ERROR"])

    def test_non_valid_id_notification(self):
        response = self.client.post('/pbp/actions',data=json.dumps(data["non_valid_id_notification"]),content_type='application/json', follow_redirects=True)
        expected_msg = "Invalid event id (must be an integer)."
        self.assertEqual(response.status_code, 400)
        self.assertMultiLineEqual(expected_msg, response.json["ERROR"])

    def test_non_existing_event_notification(self):
        response = self.client.post('/pbp/actions',data=json.dumps(data["non_existing_event_notification"]),content_type='application/json', follow_redirects=True)
        expected_msg = "PBP Sequence does not exist."
        self.assertEqual(response.status_code, 403)
        self.assertMultiLineEqual(expected_msg, response.json["ERROR"])

        