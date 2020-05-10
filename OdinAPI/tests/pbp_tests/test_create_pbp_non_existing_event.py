import unittest
import json
from main import app
from tests.pbp_tests.pbp_data import data


class TestCreateVolleyballPBP(unittest.TestCase):

    # Setup mock client.
    def setUp(self):
        app.config['DEBUG'] = True
        self.client = app.test_client()

    def test_create_pbp_non_existing_event(self):
        response = self.client.post('/pbp/Voleibol', data=json.dumps(
            data["non_exists_id"]), content_type='application/json', follow_redirects=True)
        expected_msg = "El evento no existe."
        self.assertEqual(response.status_code, 400)
        self.assertMultiLineEqual(expected_msg, response.json["ERROR"])


if __name__ == "__main__":
    unittest.main()
