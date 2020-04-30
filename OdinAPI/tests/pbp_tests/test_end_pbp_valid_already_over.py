import unittest
import json
from main import app
from tests.pbp_tests.pbp_data import data


class TestEndVolleyballPBP(unittest.TestCase):

    # Setup mock client.
    def setUp(self):
        app.config['DEBUG'] = True
        self.client = app.test_client()

    def test_end_pbp_valid_already_over(self):
        response = self.client.post('/pbp/Voleibol/end', data=json.dumps(
            data["valid_id"]), content_type='application/json', follow_redirects=True)
        expected_msg = "El partido de Voleibol ha finalizado."
        self.assertEqual(response.status_code, 403)
        self.assertMultiLineEqual(expected_msg, response.json["ERROR"])


if __name__ == "__main__":
    unittest.main()
