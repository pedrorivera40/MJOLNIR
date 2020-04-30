import unittest
import json
from main import app
from tests.pbp_tests.pbp_data import data


class TestRemoveVolleyballPBP(unittest.TestCase):

    # Setup mock client.
    def setUp(self):
        app.config['DEBUG'] = True
        self.client = app.test_client()

    def test_remove_pbp_valid(self):
        response = self.client.delete('/pbp/Voleibol', data=json.dumps(
            data["valid_id"]), content_type='application/json', follow_redirects=True)
        expected_msg = "La secuencia PBP ha sido removida."
        self.assertEqual(response.status_code, 200)
        self.assertMultiLineEqual(expected_msg, response.json["MSG"])


if __name__ == "__main__":
    unittest.main()
