import unittest
import json
from main import app
from tests.pbp_tests.game_actions.actions_data import data
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from handler.dao.config.fb_config import serv_path, rtdb_config


class TestRemoveValidVolleyballPBP(unittest.TestCase):

    # Setup mock client.
    def setUp(self):
        app.config['DEBUG'] = True
        self.client = app.test_client()
        if not firebase_admin._apps:
            firebase_admin.initialize_app(
                credentials.Certificate(serv_path), rtdb_config)
        self._rtdb = db

    def test_remove_valid_notification(self):
        # Insert a notification straight into the database.
        self._rtdb.reference(data["content_to_valid_edit"]["path"]).set(
            data["content_to_valid_edit"]["data"])
        # Try to remove it.
        response = self.client.delete('/pbp/Voleibol/actions', data=json.dumps(
            data["valid_to_remove"]), content_type='application/json', follow_redirects=True)
        expected_msg = "Removed game action"
        self.assertEqual(response.status_code, 200)
        self.assertMultiLineEqual(expected_msg, response.json["MSG"])
