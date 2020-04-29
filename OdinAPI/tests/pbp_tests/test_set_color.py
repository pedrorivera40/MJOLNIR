import unittest
import json
from main import app
from tests.pbp_tests.pbp_data import data


class TestSetColorVolleyballPBP(unittest.TestCase):

    # Setup mock client.
    def setUp(self):
        app.config['DEBUG'] = True
        self.client = app.test_client()

    def test_set_valid_color(self):
        response = self.client.put('/pbp/Voleibol/color', data=json.dumps(
            data["valid_color"]), content_type='application/json', follow_redirects=True)
        expected_msg = "Odin: El color se ha actualizado."
        self.assertEqual(response.status_code, 200)
        self.assertMultiLineEqual(expected_msg, response.json["MSG"])

    def test_set_invalid_color(self):
        response = self.client.put('/pbp/Voleibol/color', data=json.dumps(
            data["invalid_color"]), content_type='application/json', follow_redirects=True)
        expected_msg = "Odin: El formato de color debe ser HEX."
        self.assertEqual(response.status_code, 400)
        self.assertMultiLineEqual(expected_msg, response.json["ERROR"])


if __name__ == "__main__":
    unittest.main()
