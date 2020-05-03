import unittest
import json
from main import app
from tests.pbp_tests.opp_roster.opp_roster_data import data


class TestRemoveOppRosterVolleyballPBP(unittest.TestCase):

    # Setup mock client.
    def setUp(self):
        app.config['DEBUG'] = True
        self.client = app.test_client()

    def test_opp_roster_remove_valid1(self):
        response = self.client.delete('/pbp/Voleibol/roster?event_id=28&athlete_id=15&team=opponent', data=json.dumps(
            {}), content_type='application/json', follow_redirects=True)
        expected_msg = "La información del atleta se ha removido del sistema."
        self.assertEqual(response.status_code, 200)
        self.assertMultiLineEqual(expected_msg, response.json["MSG"])
