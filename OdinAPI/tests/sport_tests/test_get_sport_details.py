import unittest
import json
from main import app

class TestGetAllSports(unittest.TestCase):

    # Setup mock client.
    def setUp(self):
        app.config['DEBUG'] = True
        self.client = app.test_client()

    def test_get_all_sports_good(self):
        response = self.client.get('/sports/details',data=json.dumps({}),content_type='application/json', follow_redirects=True)
        self.assertEqual(response.status_code, 200)