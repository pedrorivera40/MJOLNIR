import unittest
import json
from main import app
from tests.pbp_tests.pbp_data import data


class TestCreateVolleyballPBP(unittest.TestCase):

    # Setup mock client.
    def setUp(self):
        app.config['DEBUG'] = True
        self.client = app.test_client()

    def test_create_pbp_valid(self):
        response = self.client.post('/pbp/Voleibol', data=json.dumps(
            data["valid_id"]), content_type='application/json', follow_redirects=True)
        expected_msg = "Odin: La secuencia PBP para " + \
            str(data["valid_id"]["event_id"]) + " se ha creado exitosamente."
        self.assertEqual(response.status_code, 200)
        self.assertMultiLineEqual(expected_msg, response.json["MSG"])


if __name__ == "__main__":
    unittest.main()
