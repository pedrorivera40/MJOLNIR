import unittest
import json
from main import app
from tests.pbp_tests.opp_roster.opp_roster_data import data


class TestRemoveOppRosterVolleyballPBP(unittest.TestCase):

    # Setup mock client.
    def setUp(self):
        app.config['DEBUG'] = True
        self.client = app.test_client()

    def test_opp_roster_remove_invalid1(self):
        response = self.client.delete('/pbp/Voleibol/roster', data=json.dumps(
            data["invalid_to_remove1"]), content_type='application/json', follow_redirects=True)
        expected_msg = "Invalid event id."
        self.assertEqual(response.status_code, 403)
        self.assertMultiLineEqual(expected_msg, response.json["ERROR"])

    def test_opp_roster_remove_invalid2(self):
        response = self.client.delete('/pbp/Voleibol/roster', data=json.dumps(
            data["invalid_to_remove2"]), content_type='application/json', follow_redirects=True)
        expected_msg = "Player does not exist."
        self.assertEqual(response.status_code, 404)
        self.assertMultiLineEqual(expected_msg, response.json["ERROR"])