import unittest
import json
from main import app
from tests.pbp_tests.game_actions.actions_data import data


class TestRemoveInvalidVolleyballPBP(unittest.TestCase):

    # Setup mock client.
    def setUp(self):
        app.config['DEBUG'] = True
        self.client = app.test_client()

    def test_invalid_pbp_to_remove1(self):
        response = self.client.delete('/pbp/Voleibol/actions?event_id=99999&action_id=25', data=json.dumps(
            {}), content_type='application/json', follow_redirects=True)
        expected_msg = "No existe una secuencia PBP para este evento."
        self.assertEqual(response.status_code, 403)
        self.assertMultiLineEqual(expected_msg, response.json["ERROR"])

    def test_invalid_pbp_to_remove2(self):
        response = self.client.delete('/pbp/Voleibol/actions?event_id=28&action_id=99999', data=json.dumps(
            {}), content_type='application/json', follow_redirects=True)
        expected_msg = "La acción no existe."
        self.assertEqual(response.status_code, 500)
        self.assertMultiLineEqual(expected_msg, response.json["ERROR"])
