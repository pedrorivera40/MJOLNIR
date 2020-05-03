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
        response = self.client.delete('/pbp/Voleibol/roster?event_id=99999&athlete_id=12&team=opponent', data=json.dumps(
            {}), content_type='application/json', follow_redirects=True)
        expected_msg = "El ID del evento es inválido."
        self.assertEqual(response.status_code, 403)
        self.assertMultiLineEqual(expected_msg, response.json["ERROR"])

    def test_opp_roster_remove_invalid2(self):
        response = self.client.delete('/pbp/Voleibol/roster?event_id=28&athlete_id=99999&team=opponent', data=json.dumps(
            {}), content_type='application/json', follow_redirects=True)
        expected_msg = "El atleta no existe."
        self.assertEqual(response.status_code, 404)
        self.assertMultiLineEqual(expected_msg, response.json["ERROR"])
