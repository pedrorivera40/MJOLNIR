import unittest
import json
from main import app
from tests.pbp_tests.uprm_roster.uprm_roster_data import data


class TestAddUPRMRosterVolleyballPBP(unittest.TestCase):

    # Setup mock client.
    def setUp(self):
        app.config['DEBUG'] = True
        self.client = app.test_client()

    def test_uprm_roster_add_valid(self):
        response = self.client.post('/pbp/Voleibol/roster', data=json.dumps(
            data["valid_uprm_roster1"]), content_type='application/json', follow_redirects=True)
        expected_msg = "Odin: La información del atleta se ha agragado al sistema."
        self.assertEqual(response.status_code, 200)
        self.assertMultiLineEqual(expected_msg, response.json["MSG"])
