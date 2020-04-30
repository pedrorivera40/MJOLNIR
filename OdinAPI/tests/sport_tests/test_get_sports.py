import unittest
import json
from main import app


class TestGetAllSports(unittest.TestCase):

    # Setup mock client.
    def setUp(self):
        app.config['DEBUG'] = True
        self.client = app.test_client()

    def test_get_all_sports_good(self):
        response = self.client.get(
            '/sports', data=json.dumps({}), content_type='application/json', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        print(response.json)

    def test_get_all_sports_bad(self):
        response = self.client.get('/sports?SOMETHING_BAD=SOMETHING_WORSE', data=json.dumps({}),
                                   content_type='application/json', follow_redirects=True)
        expected_msg = "Error en la solicitud. Debe proveerse un valor (rama deportiva o nombre del deporte) como argumento."
        self.assertEqual(response.status_code, 400)
        self.assertMultiLineEqual(expected_msg, response.json["ERROR"])
        print(response.json)

    def test_get_all_sports_by_branch(self):
        response = self.client.get('/sports?branch=Femenino', data=json.dumps(
            {}), content_type='application/json', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        print(response.json)

    def test_get_all_sports_by_name_good(self):
        response = self.client.get('/sports?sport_name=Baloncesto', data=json.dumps(
            {}), content_type='application/json', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        print(response.json)

    def test_get_all_sports_by_name_bad(self):
        response = self.client.get('/sports?sport_name=Tiro al blanco', data=json.dumps(
            {}), content_type='application/json', follow_redirects=True)
        self.assertEqual(response.status_code, 400)
        print(response.json)

    def test_get_sport_by_id_good(self):
        response = self.client.get('/sports?sport_id=7', data=json.dumps(
            {}), content_type='application/json', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        print(response.json)

    def test_get_sport_by_id_bad(self):
        response = self.client.get('/sports?sport_id=999999', data=json.dumps(
            {}), content_type='application/json', follow_redirects=True)
        self.assertEqual(response.status_code, 500)
        print(response.json)
