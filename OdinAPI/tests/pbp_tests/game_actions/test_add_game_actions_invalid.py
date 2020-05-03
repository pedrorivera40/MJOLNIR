import unittest
import json
from main import app
from tests.pbp_tests.game_actions.actions_data import data


class TestAddInvalidActionVolleyballPBP(unittest.TestCase):

    # Setup mock client.
    def setUp(self):
        app.config['DEBUG'] = True
        self.client = app.test_client()

    def test_invalid_action_play(self):
        response = self.client.post('/pbp/Voleibol/actions', data=json.dumps(
            data["invalid_action_play"]), content_type='application/json', follow_redirects=True)
        expected_msg = "La acción indicada no está cubierta por PBP de Voleibol."
        self.assertEqual(response.status_code, 500)
        self.assertMultiLineEqual(expected_msg, response.json["ERROR"])

    def test_more_params_play(self):
        response = self.client.post('/pbp/Voleibol/actions', data=json.dumps(
            data["more_params_play"]), content_type='application/json', follow_redirects=True)
        expected_msg = "Información de la acción (data) debe tener 2 parámetros para una notificación y 3 para una acción de jugada."
        self.assertEqual(response.status_code, 500)
        self.assertMultiLineEqual(expected_msg, response.json["ERROR"])

    def test_message_limit_notification(self):
        response = self.client.post('/pbp/Voleibol/actions', data=json.dumps(
            data["message_limit_notification"]), content_type='application/json', follow_redirects=True)
        expected_msg = "El mensaje debe debe tener entre 1 y 100 caracteres."
        self.assertEqual(response.status_code, 500)
        self.assertMultiLineEqual(expected_msg, response.json["ERROR"])

    def test_more_params_notification(self):
        response = self.client.post('/pbp/Voleibol/actions', data=json.dumps(
            data["more_params_notification"]), content_type='application/json', follow_redirects=True)
        expected_msg = "Las notificaciones solo deben tener tipo de acción y mensaje."
        self.assertEqual(response.status_code, 500)
        self.assertMultiLineEqual(expected_msg, response.json["ERROR"])

    def test_non_valid_id_notification(self):
        response = self.client.post('/pbp/Voleibol/actions', data=json.dumps(
            data["non_valid_id_notification"]), content_type='application/json', follow_redirects=True)
        expected_msg = "El ID de evento es inválido (debe ser un entero)."
        self.assertEqual(response.status_code, 400)
        self.assertMultiLineEqual(expected_msg, response.json["ERROR"])

    def test_non_existing_event_notification(self):
        response = self.client.post('/pbp/Voleibol/actions', data=json.dumps(
            data["non_existing_event_notification"]), content_type='application/json', follow_redirects=True)
        expected_msg = "No existe una secuencia PBP para este evento."
        self.assertEqual(response.status_code, 403)
        self.assertMultiLineEqual(expected_msg, response.json["ERROR"])
