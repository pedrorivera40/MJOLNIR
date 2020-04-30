import unittest
import json
from main import app
from tests.pbp_tests.uprm_roster.uprm_roster_data import data


class TestRemoveUPRMRosterVolleyballPBP(unittest.TestCase):

    # Setup mock client.
    def setUp(self):
        app.config['DEBUG'] = True
        self.client = app.test_client()

    def test_uprm_roster_remove_valid(self):
        response = self.client.delete('/pbp/Voleibol/roster', data=json.dumps(
            data["valid_to_remove"]), content_type='application/json', follow_redirects=True)
        expected_msg = "La información del atleta se ha removido del sistema."
        self.assertEqual(response.status_code, 200)
        self.assertMultiLineEqual(expected_msg, response.json["MSG"])
