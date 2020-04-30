import unittest
import json
from main import app
from tests.pbp_tests.uprm_roster.uprm_roster_data import data


class TestRemoveUPRMRosterVolleyballPBP(unittest.TestCase):

    # Setup mock client.
    def setUp(self):
        app.config['DEBUG'] = True
        self.client = app.test_client()

    def test_uprm_roster_remove_invalid1(self):
        response = self.client.delete('/pbp/Voleibol/roster', data=json.dumps(
            data["invalid_to_remove1"]), content_type='application/json', follow_redirects=True)
        expected_msg = "El ID del evento es inválido."
        self.assertEqual(response.status_code, 403)
        self.assertMultiLineEqual(expected_msg, response.json["ERROR"])

    def test_uprm_roster_remove_invalid2(self):
        response = self.client.delete('/pbp/Voleibol/roster', data=json.dumps(
            data["invalid_to_remove2"]), content_type='application/json', follow_redirects=True)
        expected_msg = "El atleta no existe."
        self.assertEqual(response.status_code, 404)
        self.assertMultiLineEqual(expected_msg, response.json["ERROR"])
