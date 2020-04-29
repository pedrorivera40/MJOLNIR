import unittest
import json
from main import app
from tests.pbp_tests.pbp_data import data


class TestEndVolleyballPBP(unittest.TestCase):

    # Setup mock client.
    def setUp(self):
        app.config['DEBUG'] = True
        self.client = app.test_client()

    def test_end_pbp_invalid(self):
        response = self.client.post('/pbp/Voleibol/end', data=json.dumps(
            data["invalid_id"]), content_type='application/json', follow_redirects=True)
        expected_msg = "Odin: El ID de evento es inválido (debe ser un entero)."
        self.assertEqual(response.status_code, 400)
        self.assertMultiLineEqual(expected_msg, response.json["ERROR"])


if __name__ == "__main__":
    unittest.main()
