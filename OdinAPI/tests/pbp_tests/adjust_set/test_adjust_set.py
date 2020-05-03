import unittest
import json
from main import app


class TestAdjustSetVolleyballPBP(unittest.TestCase):

    # Setup mock client.
    def setUp(self):
        app.config['DEBUG'] = True
        self.client = app.test_client()

    def test_adjust_set_valid(self):
        response = self.client.put('/pbp/Voleibol/set', data=json.dumps(
            {"event_id": 28, "adjust": 1}), content_type='application/json', follow_redirects=True)
        expected_msg = "El parcial ha sido actualizado."
        self.assertEqual(response.status_code, 200)
        self.assertMultiLineEqual(expected_msg, response.json["MSG"])

    def test_adjust_set_non_existing_pbp(self):
        response = self.client.put('/pbp/Voleibol/set', data=json.dumps(
            {"event_id": 999999, "adjust": 1}), content_type='application/json', follow_redirects=True)
        expected_msg = "No existe una secuencia PBP para este evento."
        self.assertEqual(response.status_code, 400)
        self.assertMultiLineEqual(expected_msg, response.json["ERROR"])


if __name__ == "__main__":
    unittest.main()
