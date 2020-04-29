import unittest
import json
from main import app
from tests.pbp_tests.game_actions.actions_data import data
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from handler.dao.config.fb_config import serv_path, rtdb_config


class TestEditValidVolleyballPBP(unittest.TestCase):

    # Setup mock client.
    def setUp(self):
        app.config['DEBUG'] = True
        self.client = app.test_client()
        if not firebase_admin._apps:
            firebase_admin.initialize_app(
                credentials.Certificate(serv_path), rtdb_config)
        self._rtdb = db

    # Notification to Notification.
    def test_edit_valid_notification(self):
        # Insert a notification straight into the database.
        self._rtdb.reference(data["content_to_valid_edit"]["path"]).set(
            data["content_to_valid_edit"]["data"])
        # Try to edit it.
        response = self.client.put('/pbp/Voleibol/actions', data=json.dumps(
            data["edit_valid_notification"]), content_type='application/json', follow_redirects=True)
        expected_msg = "Odin: Se ha editado la acción exitosamente."
        self.assertEqual(response.status_code, 200)
        self.assertMultiLineEqual(expected_msg, response.json["MSG"])

    # Score to Score.
    def test_edit_valid_score_to_score_opp(self):
        # Insert a score action straight into the database.
        self._rtdb.reference(data["path_to_score_to_score"]).set(
            data["score_to_be_changed2"]["data"])
        # Try to edit it.
        response = self.client.put('/pbp/Voleibol/actions', data=json.dumps(
            data["edit_valid_score_to_score_opp"]), content_type='application/json', follow_redirects=True)
        expected_msg = "Odin: Se ha editado la acción exitosamente."
        self.assertEqual(response.status_code, 200)
        self.assertMultiLineEqual(expected_msg, response.json["MSG"])

    def test_edit_valid_score_to_score_uprm(self):
        # Insert a score action straight into the database.
        self._rtdb.reference(data["path_to_score_to_score"]).set(
            data["score_to_be_changed2"]["data"])
        # Try to edit it.
        response = self.client.put('/pbp/Voleibol/actions', data=json.dumps(
            data["edit_valid_score_to_score_uprm"]), content_type='application/json', follow_redirects=True)
        expected_msg = "Odin: Se ha editado la acción exitosamente."
        self.assertEqual(response.status_code, 200)
        self.assertMultiLineEqual(expected_msg, response.json["MSG"])

    # Personal to Personal.
    def test_edit_valid_personal_to_personal_opp(self):
        # Insert a personal action straight into the database.
        self._rtdb.reference(data["path_to_personal_to_personal"]).set(
            data["personal_to_be_changed2"]["data"])
        # Try to edit it.
        response = self.client.put('/pbp/Voleibol/actions', data=json.dumps(
            data["edit_valid_personal_to_personal_opp"]), content_type='application/json', follow_redirects=True)
        expected_msg = "Odin: Se ha editado la acción exitosamente."
        self.assertEqual(response.status_code, 200)
        self.assertMultiLineEqual(expected_msg, response.json["MSG"])

    def test_edit_valid_personal_to_personal_uprm(self):
        # Insert a personal action straight into the database.
        self._rtdb.reference(data["path_to_personal_to_personal"]).set(
            data["personal_to_be_changed2"]["data"])
        # Try to edit it.
        response = self.client.put('/pbp/Voleibol/actions', data=json.dumps(
            data["edit_valid_personal_to_personal_uprm"]), content_type='application/json', follow_redirects=True)
        expected_msg = "Odin: Se ha editado la acción exitosamente."
        self.assertEqual(response.status_code, 200)
        self.assertMultiLineEqual(expected_msg, response.json["MSG"])

    # Error to Error.
    def test_edit_valid_error_to_error_opp(self):
        # Insert a error action straight into the database.
        self._rtdb.reference(data["path_to_error_to_error"]).set(
            data["error_to_be_changed2"]["data"])
        # Try to edit it.
        response = self.client.put('/pbp/Voleibol/actions', data=json.dumps(
            data["edit_valid_error_to_error_opp"]), content_type='application/json', follow_redirects=True)
        expected_msg = "Odin: Se ha editado la acción exitosamente."
        self.assertEqual(response.status_code, 200)
        self.assertMultiLineEqual(expected_msg, response.json["MSG"])

    def test_edit_valid_error_to_error_uprm(self):
        # Insert a error action straight into the database.
        self._rtdb.reference(data["path_to_error_to_error"]).set(
            data["error_to_be_changed2"]["data"])
        # Try to edit it.
        response = self.client.put('/pbp/Voleibol/actions', data=json.dumps(
            data["edit_valid_error_to_error_uprm"]), content_type='application/json', follow_redirects=True)
        expected_msg = "Odin: Se ha editado la acción exitosamente."
        self.assertEqual(response.status_code, 200)
        self.assertMultiLineEqual(expected_msg, response.json["MSG"])

    # Score to Error.
    def test_edit_valid_score_to_error_opp(self):
        # Insert a score action straight into the database.
        self._rtdb.reference(data["path_to_score_to_error"]).set(
            data["score_to_be_changed1"]["data"])
        # Try to edit it.
        response = self.client.put('/pbp/Voleibol/actions', data=json.dumps(
            data["edit_valid_score_to_error_opp"]), content_type='application/json', follow_redirects=True)
        expected_msg = "Odin: Se ha editado la acción exitosamente."
        self.assertEqual(response.status_code, 200)
        self.assertMultiLineEqual(expected_msg, response.json["MSG"])

    def test_edit_valid_score_to_error_uprm(self):
        # Insert a score action straight into the database.
        self._rtdb.reference(data["path_to_score_to_error"]).set(
            data["score_to_be_changed1"]["data"])
        # Try to edit it.
        response = self.client.put('/pbp/Voleibol/actions', data=json.dumps(
            data["edit_valid_score_to_error_uprm"]), content_type='application/json', follow_redirects=True)
        expected_msg = "Odin: Se ha editado la acción exitosamente."
        self.assertEqual(response.status_code, 200)
        self.assertMultiLineEqual(expected_msg, response.json["MSG"])

    # Scoring to Personal.
    def test_edit_valid_score_to_personal_opp(self):
        # Insert a score action straight into the database.
        self._rtdb.reference(data["path_to_score_to_personal"]).set(
            data["score_to_be_changed5"]["data"])
        # Try to edit it.
        response = self.client.put('/pbp/Voleibol/actions', data=json.dumps(
            data["edit_valid_score_to_personal_opp1"]), content_type='application/json', follow_redirects=True)
        expected_msg = "Odin: Se ha editado la acción exitosamente."
        self.assertEqual(response.status_code, 200)
        self.assertMultiLineEqual(expected_msg, response.json["MSG"])

    def test_edit_valid_score_to_personal_uprm(self):
        # Insert a score action straight into the database.
        self._rtdb.reference(data["path_to_score_to_error"]).set(
            data["score_to_be_changed5"]["data"])
        # Try to edit it.
        response = self.client.put('/pbp/Voleibol/actions', data=json.dumps(
            data["edit_valid_score_to_personal_uprm1"]), content_type='application/json', follow_redirects=True)
        expected_msg = "Odin: Se ha editado la acción exitosamente."
        self.assertEqual(response.status_code, 200)
        self.assertMultiLineEqual(expected_msg, response.json["MSG"])

    # Error to Score.
    def test_edit_valid_error_to_score_opp(self):
        # Insert a error action straight into the database.
        self._rtdb.reference(data["path_to_error_to_score"]).set(
            data["error_to_be_changed4"]["data"])
        # Try to edit it.
        response = self.client.put('/pbp/Voleibol/actions', data=json.dumps(
            data["edit_valid_error_to_score_opp"]), content_type='application/json', follow_redirects=True)
        expected_msg = "Odin: Se ha editado la acción exitosamente."
        self.assertEqual(response.status_code, 200)
        self.assertMultiLineEqual(expected_msg, response.json["MSG"])

    def test_edit_valid_error_to_score_uprm(self):
        # Insert a error action straight into the database.
        self._rtdb.reference(data["path_to_error_to_score"]).set(
            data["error_to_be_changed4"]["data"])
        # Try to edit it.
        response = self.client.put('/pbp/Voleibol/actions', data=json.dumps(
            data["edit_valid_error_to_score_uprm"]), content_type='application/json', follow_redirects=True)
        expected_msg = "Odin: Se ha editado la acción exitosamente."
        self.assertEqual(response.status_code, 200)
        self.assertMultiLineEqual(expected_msg, response.json["MSG"])

    # Error to Personal.
    def test_edit_valid_error_to_personal_opp(self):
        # Insert a error action straight into the database.
        self._rtdb.reference(data["path_to_error_to_personal"]).set(
            data["error_to_be_changed3"]["data"])
        # Try to edit it.
        response = self.client.put('/pbp/Voleibol/actions', data=json.dumps(
            data["edit_valid_error_to_personal_opp"]), content_type='application/json', follow_redirects=True)
        expected_msg = "Odin: Se ha editado la acción exitosamente."
        self.assertEqual(response.status_code, 200)
        self.assertMultiLineEqual(expected_msg, response.json["MSG"])

    def test_edit_valid_error_to_personal_uprm(self):
        # Insert a error action straight into the database.
        self._rtdb.reference(data["path_to_error_to_personal"]).set(
            data["error_to_be_changed3"]["data"])
        # Try to edit it.
        response = self.client.put('/pbp/Voleibol/actions', data=json.dumps(
            data["edit_valid_error_to_personal_uprm"]), content_type='application/json', follow_redirects=True)
        expected_msg = "Odin: Se ha editado la acción exitosamente."
        self.assertEqual(response.status_code, 200)
        self.assertMultiLineEqual(expected_msg, response.json["MSG"])

    # Personal to Score.
    def test_edit_valid_personal_to_score_opp(self):
        # Insert a error action straight into the database.
        self._rtdb.reference(data["path_to_personal_to_score"]).set(
            data["personal_to_be_changed24"]["data"])
        # Try to edit it.
        response = self.client.put('/pbp/Voleibol/actions', data=json.dumps(
            data["edit_valid_personal_to_score_opp"]), content_type='application/json', follow_redirects=True)
        expected_msg = "Odin: Se ha editado la acción exitosamente."
        self.assertEqual(response.status_code, 200)
        self.assertMultiLineEqual(expected_msg, response.json["MSG"])

    def test_edit_valid_personal_to_score_uprm(self):
        # Insert a error action straight into the database.
        self._rtdb.reference(data["path_to_personal_to_score"]).set(
            data["personal_to_be_changed24"]["data"])
        # Try to edit it.
        response = self.client.put('/pbp/Voleibol/actions', data=json.dumps(
            data["edit_valid_personal_to_score_uprm"]), content_type='application/json', follow_redirects=True)
        expected_msg = "Odin: Se ha editado la acción exitosamente."
        self.assertEqual(response.status_code, 200)
        self.assertMultiLineEqual(expected_msg, response.json["MSG"])

    # Personal to Error.
    def test_edit_valid_personal_to_error_opp(self):
        # Insert a personal action straight into the database.
        self._rtdb.reference(data["path_to_personal_to_error"]).set(
            data["personal_to_be_changed3"]["data"])
        # Try to edit it.
        response = self.client.put('/pbp/Voleibol/actions', data=json.dumps(
            data["edit_valid_personal_to_error_opp"]), content_type='application/json', follow_redirects=True)
        expected_msg = "Odin: Se ha editado la acción exitosamente."
        self.assertEqual(response.status_code, 200)
        self.assertMultiLineEqual(expected_msg, response.json["MSG"])

    def test_edit_valid_personal_to_error_uprm(self):
        # Insert a personal action straight into the database.
        self._rtdb.reference(data["path_to_personal_to_error"]).set(
            data["personal_to_be_changed3"]["data"])
        # Try to edit it.
        response = self.client.put('/pbp/Voleibol/actions', data=json.dumps(
            data["edit_valid_personal_to_error_uprm"]), content_type='application/json', follow_redirects=True)
        expected_msg = "Odin: Se ha editado la acción exitosamente."
        self.assertEqual(response.status_code, 200)
        self.assertMultiLineEqual(expected_msg, response.json["MSG"])
