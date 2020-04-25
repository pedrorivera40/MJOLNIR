import unittest
import json
from main import app
from tests.pbp_tests.opp_roster.opp_roster_data import data


class TestAddOppRosterVolleyballPBP(unittest.TestCase):

    # Setup mock client.
    def setUp(self):
        app.config['DEBUG'] = True
        self.client = app.test_client()

    def test_opp_roster_add_invalid1(self):
        response = self.client.post('/pbp/Voleibol/roster', data=json.dumps(
            data["invalid_data1"]), content_type='application/json', follow_redirects=True)
        expected_msg = "PBP sequence does not exist."
        self.assertEqual(response.status_code, 400)
        self.assertMultiLineEqual(expected_msg, response.json["ERROR"])
