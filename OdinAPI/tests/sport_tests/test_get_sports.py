import unittest
import json
from main import app

class TestGetAllSports(unittest.TestCase):

    # Setup mock client.
    def setUp(self):
        app.config['DEBUG'] = True
        self.client = app.test_client()

    def test_get_all_sports_good(self):
        response = self.client.get('/sports',data=json.dumps({}),content_type='application/json', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        print(response.json)

    def test_get_all_sports_bad(self):
        response = self.client.get('/sports',data=json.dumps({"SOMETHING_BAD": "SOMETHING_WORSE"}),content_type='application/json', follow_redirects=True)
        expected_msg = "Odin/sports: Malformed request, either branch or name is allowed."
        self.assertEqual(response.status_code, 400)
        self.assertMultiLineEqual(expected_msg, response.json["ERROR"])
        print(response.json)

    def test_get_all_sports_by_branch(self):
        response = self.client.get('/sports',data=json.dumps({"branch": "femenino"}),content_type='application/json', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        print(response.json)

    def test_get_all_sports_by_name_good(self):
        response = self.client.get('/sports',data=json.dumps({"sport_name": "Baloncesto"}),content_type='application/json', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        print(response.json)

    def test_get_all_sports_by_name_bad(self):
        response = self.client.get('/sports',data=json.dumps({"sport_name": "Tiro al blanco"}),content_type='application/json', follow_redirects=True)
        self.assertEqual(response.status_code, 400)
        print(response.json)

    def test_get_sport_by_id_good(self):
        response = self.client.get('/sports',data=json.dumps({"sport_id": 7}),content_type='application/json', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        print(response.json)

    def test_get_sport_by_id_bad(self):
        response = self.client.get('/sports',data=json.dumps({"sport_id": 999999}),content_type='application/json', follow_redirects=True)
        self.assertEqual(response.status_code, 500)
        print(response.json)

