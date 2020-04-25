import unittest
import json
from main import app
from tests.pbp_tests.uprm_roster.uprm_roster_data import data


class TestAddUPRMRosterVolleyballPBP(unittest.TestCase):

    # Setup mock client.
    def setUp(self):
        app.config['DEBUG'] = True
        self.client = app.test_client()

    def test_uprm_roster_add_invalid1(self):
        response = self.client.post('/pbp/Voleibol/roster', data=json.dumps(
            data["invalid_uprm_roster1"]), content_type='application/json', follow_redirects=True)
        expected_msg = "Event does not exist."
        self.assertEqual(response.status_code, 400)
        self.assertMultiLineEqual(expected_msg, response.json["ERROR"])

    def test_uprm_roster_add_invalid2(self):
        response = self.client.post('/pbp/Voleibol/roster', data=json.dumps(
            data["invalid_uprm_roster2"]), content_type='application/json', follow_redirects=True)
        expected_msg = "Athlete does not exist in the event roster."
        self.assertEqual(response.status_code, 400)
        self.assertMultiLineEqual(expected_msg, response.json["MSG"])
