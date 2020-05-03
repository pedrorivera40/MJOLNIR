import unittest
import json
from main import app
from tests.pbp_tests.game_actions.actions_data import data


class TestAddValidVolleyballPBP(unittest.TestCase):

    # Setup mock client.
    def setUp(self):
        app.config['DEBUG'] = True
        self.client = app.test_client()

    def test_add_valid_notification(self):
        response = self.client.post('/pbp/Voleibol/actions', data=json.dumps(
            data["valid_notification"]), content_type='application/json', follow_redirects=True)
        expected_msg = "La acción se ha añadido al sistema."
        self.assertEqual(response.status_code, 200)
        self.assertMultiLineEqual(expected_msg, response.json["MSG"])

    def test_add_valid_scoring_uprm(self):
        response = self.client.post('/pbp/Voleibol/actions', data=json.dumps(
            data["valid_scoring_uprm"]), content_type='application/json', follow_redirects=True)
        expected_msg = "La acción se ha añadido al sistema."
        self.assertEqual(response.status_code, 200)
        self.assertMultiLineEqual(expected_msg, response.json["MSG"])

    def test_add_valid_scoring_opp(self):
        response = self.client.post('/pbp/Voleibol/actions', data=json.dumps(
            data["valid_scoring_opp"]), content_type='application/json', follow_redirects=True)
        expected_msg = "La acción se ha añadido al sistema."
        self.assertEqual(response.status_code, 200)
        self.assertMultiLineEqual(expected_msg, response.json["MSG"])

    def test_add_valid_personal_uprm(self):
        response = self.client.post('/pbp/Voleibol/actions', data=json.dumps(
            data["valid_personal_uprm"]), content_type='application/json', follow_redirects=True)
        expected_msg = "La acción se ha añadido al sistema."
        self.assertEqual(response.status_code, 200)
        self.assertMultiLineEqual(expected_msg, response.json["MSG"])

    def test_add_valid_personal_opp(self):
        response = self.client.post('/pbp/Voleibol/actions', data=json.dumps(
            data["valid_personal_opp"]), content_type='application/json', follow_redirects=True)
        expected_msg = "La acción se ha añadido al sistema."
        self.assertEqual(response.status_code, 200)
        self.assertMultiLineEqual(expected_msg, response.json["MSG"])

    def test_add_valid_error_uprm(self):
        response = self.client.post('/pbp/Voleibol/actions', data=json.dumps(
            data["valid_error_uprm"]), content_type='application/json', follow_redirects=True)
        expected_msg = "La acción se ha añadido al sistema."
        self.assertEqual(response.status_code, 200)
        self.assertMultiLineEqual(expected_msg, response.json["MSG"])

    def test_add_valid_error_opp(self):
        response = self.client.post('/pbp/Voleibol/actions', data=json.dumps(
            data["valid_error_opp"]), content_type='application/json', follow_redirects=True)
        expected_msg = "La acción se ha añadido al sistema."
        self.assertEqual(response.status_code, 200)
        self.assertMultiLineEqual(expected_msg, response.json["MSG"])

    def test_valid_adjust(self):
        response = self.client.post('/pbp/Voleibol/actions', data=json.dumps(
            data["valid_adjust"]), content_type='application/json', follow_redirects=True)
        expected_msg = "La acción se ha añadido al sistema."
        self.assertEqual(response.status_code, 200)
        self.assertMultiLineEqual(expected_msg, response.json["MSG"])


if __name__ == "__main__":
    unittest.main()
