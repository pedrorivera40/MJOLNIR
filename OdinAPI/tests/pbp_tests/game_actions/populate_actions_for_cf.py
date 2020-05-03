import unittest
import json
from main import app
from tests.pbp_tests.game_actions.actions_data import data


class TestPopulateVolleyballPBP(unittest.TestCase):

    # Setup mock client.
    def setUp(self):
        app.config['DEBUG'] = True
        self.client = app.test_client()

    def test_populate_db(self):
        response = self.client.post('/pbp/Voleibol/actions', data=json.dumps(
            {
                "event_id": 28,
                "data": {
                    "action_type": "KillPoint",
                    "team": "uprm",
                    "athlete_id": 110
                }
            }), content_type='application/json', follow_redirects=True)
        expected_msg = "Action added into the system."
        self.assertEqual(response.status_code, 200)
        self.assertMultiLineEqual(expected_msg, response.json["MSG"])
        response = self.client.post('/pbp/Voleibol/actions', data=json.dumps(
            {
                "event_id": 28,
                "data": {
                    "action_type": "Ace",
                    "team": "uprm",
                    "athlete_id": 111
                }
            }), content_type='application/json', follow_redirects=True)
        expected_msg = "Action added into the system."
        self.assertEqual(response.status_code, 200)
        self.assertMultiLineEqual(expected_msg, response.json["MSG"])
        response = self.client.post('/pbp/Voleibol/actions', data=json.dumps(
            {
                "event_id": 28,
                "data": {
                    "action_type": "KillPoint",
                    "team": "opponent",
                    "athlete_id": 1587365468141
                }
            }), content_type='application/json', follow_redirects=True)
        expected_msg = "Action added into the system."
        self.assertEqual(response.status_code, 200)
        self.assertMultiLineEqual(expected_msg, response.json["MSG"])


if __name__ == "__main__":
    unittest.main()
