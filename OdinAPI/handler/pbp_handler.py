from re import search
from flask import jsonify
from .dao.pbp_dao import PBPDao as VolleyballPBPDao
from handler.event import EventHandler
from handler.team import TeamHandler


class VolleyballPBPHandler:
    '''
    VolleyballPBPHandler - This class handles incomming requests from Odin API's gateway
                 by interacting with the PBPDAO. It is responsible for modifying
                 the state of content stored in the non-relational database,
                 especially information regarding Volleyball PBP sequences.
    @author Pedro Luis Rivera Gomez
    '''

    def __init__(self):
        """
        Default constructor - initialize keywords that apply to Volleyball PBP sequences.
        """

        self._sport_keywords = {
            "score-val": {
                "set1-opponent": 0,
                "set1-uprm": 0,
                "set2-opponent": 0,
                "set2-uprm": 0,
                "set3-opponent": 0,
                "set3-uprm": 0,
                "set4-opponent": 0,
                "set4-uprm": 0,
                "set5-opponent": 0,
                "set5-uprm": 0
            },
            "uprm-sets": ["/set1-uprm", "/set2-uprm", "/set3-uprm", "/set4-uprm", "/set5-uprm"],
            "opp-sets": ["/set1-opponent", "/set2-opponent", "/set3-opponent", "/set4-opponent", "/set5-opponent"],
            "sport": "Voleibol",
            "scoring_actions": [
                "KillPoint",
                "Ace",
                "BlockPoint",
            ],
            "personal_actions": [
                "Assist",
                "Block",
                "Dig",
            ],
            "adjust": "ScoreAdjust",
            "error_actions": [
                "AttackError",
                "ServiceError",
                "BlockingError",
                "ReceptionError"
            ],
            "notification": "Notification",
            "teams": ["uprm", "opponent"],
            # Color format regex adapted from: https://www.regextester.com/93589
            "color-format": "^((0x){0,1}|#{0,1})([0-9A-F]{8}|[0-9A-F]{6})$",
            "athlete_prefix": "athlete-"
        }

    def _get_direct_set_path(self, team, event_id, dao):
        """
        Internal method to determine set path directly depending on the action team.
        """

        # Validate team value is specified correctly.
        if team not in self._sport_keywords["teams"]:
            raise Exception("Nombre de equipo es inválido.")

        current_set = int(dao.get_current_set(event_id))
        set_path = ""

        # Determine proper set path value based on the team that needs the adjust.
        if team == self._sport_keywords["teams"][0]:
            set_path = self._sport_keywords["uprm-sets"][current_set - 1]
        else:
            set_path = self._sport_keywords["opp-sets"][current_set - 1]

        return set_path

    def _get_indirect_set_path(self, team, event_id, dao):
        """
        Internal method to obtain the indirect set path. It is the complement of the direct set path.
        """

        # Validate team value is specified correctly.
        if team not in self._sport_keywords["teams"]:
            raise Exception("Nombre de equipo es inválido.")

        current_set = int(dao.get_current_set(event_id))
        set_path = ""

        # Determine proper set path value based on the team value (returns the opposite team set path).
        if team == self._sport_keywords["teams"][0]:
            set_path = self._sport_keywords["opp-sets"][current_set - 1]
        else:
            set_path = self._sport_keywords["uprm-sets"][current_set - 1]

        return set_path

    def _handle_pbp_action(self, event_id, action, dao):
        """
        Internal method for handling Volleyball PBP Actions via a PBPDao.
        """

        # Initial validations.

        if not isinstance(action, dict):
            raise Exception(
                "Información de la acción (data) debe proveerse en formato JSONs.")

        if len(action) < 2 or len(action) > 3:
            raise Exception(
                "Información de la acción (data) debe tener 2 parámetros para una notificación y 3 para una acción de jugada.")

        if not "action_type" in action:
            raise Exception(
                "La jugada enviada no está cubierta por el PBP de Voleibol.")

        action_type = action["action_type"]

        # Notifications are only posted. No score or set value needs to be modified from a notification.
        if action_type == self._sport_keywords["notification"]:
            if len(action) != 2:
                raise Exception(
                    "Las notificaciones solo deben tener tipo de acción y mensaje.")

            if "message" not in action:
                raise Exception("No se encontró valor para el mensaje.")

            if not isinstance(action["message"], str):
                raise Exception(
                    "El tipo de mensaje es incorrecto (debe ser una secuencia de caracteres).")

            if len(action["message"]) < 1 or len(action["message"]) > 100:
                raise Exception(
                    "El mensaje debe debe tener entre 1 y 100 caracteres.")

            dao.add_pbp_game_action(event_id, action)
            return

        # At this point, the remaining valid actions must have 3 arguments.
        if len(action) != 3:
            raise Exception(
                "El número de argumentos esperado es 3.")

        # Adjust game actions modify the score of the direct team indicated in action["team"].
        # These are not added to the notifications feed (non-relational database).
        if action_type == self._sport_keywords["adjust"]:
            # Validate team value is present.
            if "team" not in action:
                raise Exception(
                    "No se ha encontrado el valor de equipo en data.")

            set_path = self._get_direct_set_path(action["team"], event_id, dao)
            # Validate difference value is present.
            if "difference" not in action:
                raise Exception(
                    "No se ha enviado el valor de diferencia en data.")

            difference = int(action["difference"])

            # Adding volleyball rules for scoring:
            indirect_path = self._get_indirect_set_path(
                action["team"], event_id, dao)
            current_set = dao.get_current_set(event_id)
            current_direct_score = dao.get_score_by_set(event_id, set_path)
            current_indirect_score = dao.get_score_by_set(
                event_id, indirect_path)

            # Finding score limit based on current set.
            limit = 25
            if current_set == 5:
                limit = 15

            potential_score = current_direct_score + difference
            if potential_score < 0:
                raise Exception(
                    "Error actualizando puntuación. La puntuación no puede ser negativa.")

            # If limit was reached and more than 2 points difference is attempted.
            if (current_indirect_score > limit or potential_score > limit) and abs(potential_score - current_indirect_score) > 2:
                raise Exception(
                    "Error actualizando puntuación. Si el límite de puntuación se excede, la diferencia de puntos debe ser menor de 3.")

            dao.set_score_by_set(event_id, set_path, potential_score)
            return

        is_valid_athlete = (self._sport_keywords["athlete_prefix"] + str(action["athlete_id"]) in dao.get_uprm_roster(event_id)
                            or (self._sport_keywords["athlete_prefix"] + str(action["athlete_id"])) in dao.get_opponent_roster(event_id))
        print(is_valid_athlete)
        # Scoring game actions modify athlete statistics and team score.
        if action_type in self._sport_keywords["scoring_actions"]:

            if is_valid_athlete:
                set_path = self._get_direct_set_path(
                    action["team"], event_id, dao)

                dao.add_scoring_pbp_game_action(event_id, action, set_path, 1)
                return

            else:
                raise Exception("Información del atleta es inválida.")

        # Personal actions only modify athlete statistics.
        # The only action to do is add to Feed and let clients compute statistics.
        if action_type in self._sport_keywords["personal_actions"]:

            if is_valid_athlete:
                dao.add_pbp_game_action(event_id, action)
                return

            else:
                raise Exception("Información del atleta es inválida.")

        if action_type in self._sport_keywords["error_actions"]:

            if is_valid_athlete:
                set_path = self._get_indirect_set_path(
                    action["team"], event_id, dao)

                dao.add_scoring_pbp_game_action(event_id, action, set_path, 1)
                return

            else:
                raise Exception("Información del atleta es inválida.")

        raise Exception(
            "La acción indicada no está cubierta por PBP de Voleibol.")

    def _handle_pbp_edit_action(self, event_id, action_id, new_action, dao):
        """
        Internal method for handling editting previously added game actions in a PBP sequence.
        """

        if not dao.pbp_game_action_exists(event_id, action_id):
            raise Exception("No existe esta acción en el sistema.")

        if len(new_action) < 2 or len(new_action) > 3:
            raise Exception(
                "La acción debe tener dos parámetros para notificación o 3 para cualquier otra acción.")

        # Every action must have a type.
        prev_action = dao.get_pbp_action(event_id, action_id)

        if prev_action == new_action:
            raise Exception("No hubo un cambio en la acción.")

        if not "action_type" in new_action:
            raise Exception("La acción nueva no tiene tipo.")

        prev_type = prev_action["action_type"]
        new_type = new_action["action_type"]

        # Variables to be used depending on the edit type.
        are_same_type = (
            prev_type in self._sport_keywords["scoring_actions"] and new_type in self._sport_keywords["scoring_actions"]
            or prev_type in self._sport_keywords["personal_actions"] and new_type in self._sport_keywords["personal_actions"]
            or prev_type in self._sport_keywords["error_actions"] and new_type in self._sport_keywords["error_actions"]
            or prev_type == "Notification" and new_type == "Notification")

        # Notifications are only posted. No score or set value needs to be modified from a notification.
        if are_same_type and prev_type == self._sport_keywords["notification"]:
            if len(new_action) != 2 or "message" not in new_action or not isinstance(new_action["message"], str) or len(new_action["message"]) < 1 or len(new_action["message"]) > 100:
                raise Exception(
                    "El formato de nueva notificación es inválido.")
            dao.edit_pbp_game_action(event_id, action_id, new_action)
            return

        # If actions are not the same and one of them is notification. This operation is not allowed.
        if prev_type == self._sport_keywords["notification"] or new_type == self._sport_keywords["notification"]:
            raise Exception(
                "Las notificaciones no pueden cambiar de tipo.")

        if len(new_action) != 3:
            raise Exception("Las jugadas deben tener 3 parámetros.")

        # From now on, the remaining game actions involve game plays.
        # Plays require values for team and athlete_id.
        # Validate team and athlete_id are valid.
        if not "team" in new_action:
            raise Exception(
                "No se encontró valor de equipo en la acción nueva.")

        if not "athlete_id" in new_action:
            raise Exception(
                "No se encontró valor de ID de atleta en la acción nueva.")

        new_team = new_action["team"]
        athlete_id = new_action["athlete_id"]

        if new_team not in self._sport_keywords["teams"]:
            raise Exception("El valor de equipo es inválido.")

        if new_team == self._sport_keywords["teams"][0] and (self._sport_keywords["athlete_prefix"] + str(int(athlete_id))) not in dao.get_uprm_roster(event_id):
            raise Exception("Atleta de UPRM no existe en el roster.")

        if new_team == self._sport_keywords["teams"][1] and (self._sport_keywords["athlete_prefix"] + str(int(athlete_id))) not in dao.get_opponent_roster(event_id):
            raise Exception("Atleta oponente no está en el roster.")

        # *** Case same type of play (scoring action), but a change is present. ***
        if are_same_type and prev_type in self._sport_keywords["scoring_actions"]:
            # Different team means we need to re-attribute the point to the proper team.
            if new_team != prev_action["team"]:
                inc_path = self._get_direct_set_path(new_team, event_id, dao)
                dec_path = self._get_indirect_set_path(new_team, event_id, dao)
                dao.adjust_score_by_play_edit(
                    event_id, dec_path, inc_path, 1, action_id, new_action)

            # Update action.
            else:
                dao.edit_pbp_game_action(event_id, action_id, new_action)
            return

        # *** Case same play type (personal action), but a change is present. ***
        if are_same_type and prev_type in self._sport_keywords["personal_actions"]:
            # Just update action.
            dao.edit_pbp_game_action(event_id, action_id, new_action)
            return

        # *** Case same type of play (error action), but a change is present. ***
        if are_same_type and prev_type in self._sport_keywords["error_actions"]:
            # Different team means we need to re-attribute the point to the proper team.
            if new_team != prev_action["team"]:
                inc_path = self._get_indirect_set_path(new_team, event_id, dao)
                dec_path = self._get_direct_set_path(new_team, event_id, dao)
                dao.adjust_score_by_play_edit(
                    event_id, dec_path, inc_path, 1, action_id, new_action)

            # Update action.
            else:
                dao.edit_pbp_game_action(event_id, action_id, new_action)
            return

        # At this point, cases in which same play type were considered.
        # The following cases represent when a different action type is found (except for notifications).

        # *** Case previously considered scoring action, but changed into an error action. ***
        if prev_type in self._sport_keywords["scoring_actions"] and new_type in self._sport_keywords["error_actions"]:
            # If different action but same team, point must be attributed to the other team. Otherwise just update the action.
            if new_team == prev_action["team"]:
                dec_path = self._get_direct_set_path(new_team, event_id, dao)
                inc_path = self._get_indirect_set_path(new_team, event_id, dao)
                dao.adjust_score_by_play_edit(
                    event_id, dec_path, inc_path, 1, action_id, new_action)

            # Update action.
            else:
                dao.edit_pbp_game_action(event_id, action_id, new_action)
            return

        # *** Case previously considered scoring action, but changed into a personal action. ***
        if prev_type in self._sport_keywords["scoring_actions"] and new_type in self._sport_keywords["personal_actions"]:
            # If different action but same team, score must decrease for current team. Otherwise just update the action.
            dec_path = self._get_direct_set_path(new_team, event_id, dao)
            if new_team != prev_action["team"]:
                dec_path = self._get_indirect_set_path(new_team, event_id, dao)

            # Update action.
            dao.adjust_score_by_play_edit_inc(
                event_id, dec_path, -1, action_id, new_action)
            return

        # *** Case previously considered error action, but changed into a scoring action. ***
        if prev_type in self._sport_keywords["error_actions"] and new_type in self._sport_keywords["scoring_actions"]:
            # If different action but same team, point must be attributed to the other team. Otherwise just update the action.
            if new_team == prev_action["team"]:
                dec_path = self._get_indirect_set_path(new_team, event_id, dao)
                inc_path = self._get_direct_set_path(new_team, event_id, dao)
                dao.adjust_score_by_play_edit(
                    event_id, dec_path, inc_path, 1, action_id, new_action)

            # Update action.
            else:
                dao.edit_pbp_game_action(event_id, action_id, new_action)
            return

        # *** Case previously considered error action, but changed into a personal action. ***
        if prev_type in self._sport_keywords["error_actions"] and new_type in self._sport_keywords["personal_actions"]:
            # If different action but same team, score must decrease for current team. Otherwise just update the action.
            dec_path = self._get_indirect_set_path(new_team, event_id, dao)
            if new_team != prev_action["team"]:
                dec_path = self._get_direct_set_path(new_team, event_id, dao)

            # Update action.
            dao.adjust_score_by_play_edit_inc(
                event_id, dec_path, -1, action_id, new_action)
            return

        # *** Case previously considered personal action, but changed into a scoring action. ***
        if prev_type in self._sport_keywords["personal_actions"] and new_type in self._sport_keywords["scoring_actions"]:
            # Update action + increase a point to current team.
            inc_path = self._get_direct_set_path(new_team, event_id, dao)

            # Update action.
            dao.adjust_score_by_play_edit_inc(
                event_id, inc_path, 1, action_id, new_action)
            return

        # *** Case previously considered personal action, but changed into a error action. ***
        if prev_type in self._sport_keywords["personal_actions"] and new_type in self._sport_keywords["error_actions"]:
            # Add a point to indirect team.
            inc_path = self._get_indirect_set_path(new_team, event_id, dao)

            # Update action.
            dao.adjust_score_by_play_edit_inc(
                event_id, inc_path, 1, action_id, new_action)
            return

        raise Exception(
            "La jugada enviada no está cubierta por el PBP de Voleibol.")

    def _handle_remove_pbp_action(self, event_id, action_id, dao):
        """
        Internal method for handling PBP actions removal and its effects over current score.
        """

        if not dao.pbp_game_action_exists(event_id, action_id):
            raise Exception("La acción no existe.")

        action = dao.get_pbp_action(event_id, action_id)

        # If it is a scoring action, direct team score must decrease by 1.
        if action["action_type"] in self._sport_keywords["scoring_actions"]:
            path = self._get_direct_set_path(action["team"], event_id, dao)
            dao.adjust_score_by_set(event_id, path, -1)

        # If it is an error action, indirect score must decrease by 1.
        elif action["action_type"] in self._sport_keywords["error_actions"]:
            path = self._get_indirect_set_path(action["team"], event_id, dao)
            dao.adjust_score_by_set(event_id, path, -1)

        dao.remove_pbp_game_action(event_id, action_id)

    def startPBPSequence(self, event_id):
        """
        Starts a PBP sequence.
        This function interacts with the PBP DAO to create a new PBP sequence.

        Args
            event_id: integer corresponding to an event id.

        Returns:
            Response containing a MSG in case of success, or Error message in case of failure.
        """

        try:
            # Validate event id is positive integer.
            if not str(event_id).isdigit():
                return jsonify(Error="El ID de evento es inválido (debe ser un entero)."), 400

            event_info, resp_code = EventHandler().getEventByID(event_id)
            event_info = event_info.json

            print(event_info)

            if not event_info.get("Event"):
                return jsonify(Error="El evento no existe."), 400

            event_info = event_info.get("Event")

            if event_info.get("sport_name") != self._sport_keywords["sport"]:
                return jsonify(Error="El evento seleccionado no es de Voleibol."), 403

            pbp_dao = VolleyballPBPDao()
            if pbp_dao.pbp_exists(event_id):
                return jsonify(Error="Ya se había creado una secuencia PBP."), 403

            # At this point, the event exists and does not have a PBP sequence.
            game_metadata = {
                "game-over": {"answer": "No"},
                "sport": self._sport_keywords["sport"],
                "current-set": 1,
                "opp-color": ""
            }

            pbp_dao.create_pbp_seq(
                event_id, game_metadata, self._sport_keywords["score-val"])

            return jsonify(MSG="La secuencia PBP para " + str(event_id) + " se ha creado exitosamente."), 200

        except Exception as e:
            print(str(e))
            return jsonify(Error=str(e)), 500

    def removePBPSequence(self, event_id):
        """
        Remove a PBP sequence.
        This function interacts with the PBP DAO to remove a new PBP sequence.

        Args
            event_id: integer corresponding to an event id.

        Returns:
            Response containing a MSG in case of success, or Error message in case of failure.
        """

        try:
            # Validate event id is positive integer.
            if not str(event_id).isdigit():
                return jsonify(Error="El ID de evento es inválido (debe ser un entero)."), 400

            pbp_dao = VolleyballPBPDao()
            if not pbp_dao.pbp_exists(event_id):
                return jsonify(Error="No existe una secuencia PBP para este evento."), 403

            meta = pbp_dao.get_pbp_meta(event_id)
            if self._sport_keywords["sport"] != meta["sport"]:
                return jsonify(Error="Esta secuencia PBP no corresponde a Voleibol."), 403

            pbp_dao.remove_pbp_seq(event_id)
            return jsonify(MSG="La secuencia PBP ha sido removida."), 200

        except Exception as e:
            print(str(e))
            return jsonify(Error=str(e))

    def adjustCurrentSet(self, event_id, adjust):
        """
        Modifies the current set by a delta value.
        This function updates the current set value of a valid event by a difference (adjust).

        Args:
            event_id: integer corresponding to an event id.
            adjust: integer value corresponding to the increment/decrement of the current set.

        Returns:
            Response containing a MSG in case of success, or Error message in case of failure.
        """
        try:
            if not isinstance(event_id, int) and not isinstance(adjust, int):
                return jsonify(Error="Los valores de ID del evento y adjust deben ser enteros."), 400

            pbp_dao = VolleyballPBPDao()

            if not pbp_dao.pbp_exists(event_id):
                return jsonify(Error="No existe una secuencia PBP para este evento."), 400

            meta = pbp_dao.get_pbp_meta(event_id)
            if self._sport_keywords["sport"] != meta["sport"]:
                return jsonify(Error="Esta secuencia PBP no corresponde a Voleibol."), 403

            if pbp_dao.is_game_over(event_id):
                return jsonify(Error="El partido de Voleibol ya ha finalizado."), 403

            current_set = pbp_dao.get_current_set(event_id)
            potential_set = current_set + adjust
            if potential_set > 5 or potential_set < 1:
                return jsonify(Error="El ajuste es inválido. El valor resultante debe estar entre 1 y 5."), 403

            pbp_dao.set_current_set(event_id, potential_set)
            return jsonify(MSG="El parcial ha sido actualizado."), 200

        except Exception as e:
            print(str(e))
            return jsonify(Error=str(e)), 500

    def setOpponentColor(self, event_id, color):
        """
        Sets the opponent color.
        This function sets the opponent color of a particular PBP sequence. This is mainly for UI purposes on the client side.

        Args:
            event_id: integer corresponding to an event id.
            color: string corresponding to a hex-formatted color.

        Returns:
            Response containing a MSG in case of success, or Error message in case of failure.
        """

        try:
            if not isinstance(color, str):
                return jsonify(Error="El color debe estar dado como una secuencia de caracteres que representan un valor HEX (# + 8 valores HEX)."), 400

            # Validate a hex formatted color is provided.
            if not search(self._sport_keywords["color-format"], color):
                return jsonify(Error="El formato de color debe ser HEX."), 400

            # Validate event id is positive integer.
            if not str(event_id).isdigit():
                return jsonify(Error="El ID de evento es inválido (debe ser un entero)."), 400

            pbp_dao = VolleyballPBPDao()
            if not pbp_dao.pbp_exists(event_id):
                return jsonify(Error="No existe una secuencia PBP para este evento."), 403

            if pbp_dao.is_game_over(event_id):
                return jsonify(Error="El partido de Voleibol ya ha finalizado."), 403

            meta = pbp_dao.get_pbp_meta(event_id)
            if self._sport_keywords["sport"] != meta["sport"]:
                return jsonify(Error="Esta secuencia PBP no corresponde a Voleibol."), 403

            if color == pbp_dao.get_opponent_color(event_id):
                return jsonify(MSG="No se encontraron cambios en el color."), 200

            pbp_dao.set_opponent_color(event_id, color)
            return jsonify(MSG="El color se ha actualizado."), 200

        except Exception as e:
            print(str(e))
            return jsonify(Error=str(e)), 500

    def setUPRMPlayer(self, event_id, athlete_id):
        """
        Add an athlete to UPRM roster in the system.
        This function adds an athlete to UPRM roster given it's event_id.

        Args
            event_id: integer corresponding to an event id.
            athlete_id: integer corresponding to an event id.

        Returns:
            Response containing a MSG in case of success, or Error message in case of failure.
        """

        try:

            if not isinstance(event_id, int) or not isinstance(athlete_id, int):
                return jsonify(Error="Valores de ID del evento y ID del atleta deben ser enteros."), 400

            event_info = EventHandler().getEventByID(event_id)
            event_info = event_info[0].json

            if not event_info.get("Event"):
                return jsonify(Error="El evento no existe."), 400

            event_info = event_info.get("Event")
            team_roster = TeamHandler().getTeamMembersByID(
                event_info["team_id"])

            team_roster = team_roster[0].json

            if not team_roster.get("Team") or not team_roster.get("Team").get("team_members"):
                return jsonify(Error="No se encontró información del roster."), 400

            team_roster = team_roster.get("Team").get("team_members")
            athlete_info = None

            for athlete in team_roster:
                if athlete["athlete_id"] == athlete_id:
                    athlete_info = athlete
                    break

            if not athlete_info:
                return jsonify(Error="No se encontró información del atleta."), 400

            pbp_dao = VolleyballPBPDao()

            if not pbp_dao.pbp_exists(event_id):
                return jsonify(Error="No existe una secuencia PBP para este evento."), 400

            if pbp_dao.is_game_over(event_id):
                return jsonify(Error="El partido de Voleibol ha finalizado."), 403

            meta = pbp_dao.get_pbp_meta(event_id)
            if self._sport_keywords["sport"] != meta["sport"]:
                return jsonify(Error="Esta secuencia PBP no corresponde a Voleibol."), 403

            uprm_roster = pbp_dao.get_uprm_roster(event_id)
            if uprm_roster and (self._sport_keywords["athlete_prefix"] + str(athlete_id)) in uprm_roster:
                return jsonify(Error="El atleta ya existe en el roster de UPRM."), 403

            player_info = {
                "athlete_id": athlete_id,
                "number": athlete_info["number"],
                "first_name": athlete_info["first_name"],
                "middle_name": athlete_info["middle_name"],
                "last_names": athlete_info["last_names"],
                "profile_image_link": athlete_info["profile_image_link"]
            }

            pbp_dao.set_uprm_athlete(event_id, player_info)
            return jsonify(MSG="Se ha actualizado la información de atletas UPRM."), 200

        except Exception as e:
            print(str(e))
            return jsonify(Error=str(e)), 500

    def addOppPlayer(self, event_id, player_info):
        """
        Add an athlete to opponent roster to the system.
        This function adds an athlete to opponent roster given it's event_id.

        Args
            event_id: integer corresponding to an event id.
            player_info: JSON object containing information about the athlete (number and name).

        Returns:
            Response containing a MSG in case of success, or Error message in case of failure.
        """
        try:

            if not isinstance(event_id, int):
                return jsonify(Error="El valor para ID del evento tiene que ser un entero."), 400

            if not isinstance(player_info, dict) or len(player_info) != 2 or not "name" in player_info or not "number" in player_info:
                return jsonify(Error="Información del atleta oponente debe darse en formato JSON y debe contener el nombre y número del atleta."), 400

            if not isinstance(player_info["name"], str) or not isinstance(player_info["number"], int):
                return jsonify(Error="La información del oponente debe darse en el siguiente formato: nombre (secuencia de caracteres) y número (entero)."), 400

            pbp_dao = VolleyballPBPDao()

            if not pbp_dao.pbp_exists(event_id):
                return jsonify(Error="No existe una secuencia PBP para este evento."), 400

            if pbp_dao.is_game_over(event_id):
                return jsonify(Error="El partido de Voleibol ha finalizado."), 403

            meta = pbp_dao.get_pbp_meta(event_id)
            if self._sport_keywords["sport"] != meta["sport"]:
                return jsonify(Error="Esta secuencia PBP no corresponde a Voleibol."), 403

            # Validate the athlete number has not been used.
            opponent_roster = pbp_dao.get_opponent_roster(event_id)

            if opponent_roster and (self._sport_keywords["athlete_prefix"] + str(player_info["number"])) in opponent_roster:
                return jsonify(Error="Ya existe un atleta oponente con este número."), 403

            pbp_dao.set_opponent_athlete(event_id, player_info)
            return jsonify(MSG="La información del atleta se agregado al sistema."), 200

        except Exception as e:
            print(str(e))
            return jsonify(Error=str(e)), 500

    def updateOppPlayer(self, event_id, player_info):
        """
        Updates an athlete within opponent roster.
        This function edits the name of an athlete from opponent roster given the event_id, and new name.

        Args
            event_id: integer corresponding to an event id.
            player_info: JSON object containing information about the athlete (number and new name).

        Returns:
            Response containing a MSG in case of success, or Error message in case of failure.
        """

        try:

            if not isinstance(event_id, int):
                return jsonify(Error="El valor para ID del evento tiene que ser un entero."), 400

            if not isinstance(player_info, dict) or len(player_info) != 2 or not "name" in player_info or not "number" in player_info:
                return jsonify(Error="Información del atleta oponente debe darse en formato JSON y debe contener el nombre y número del atleta."), 400

            if not isinstance(player_info["name"], str) or not isinstance(player_info["number"], int):
                print(player_info)
                return jsonify(Error="La información del oponente debe darse en el siguiente formato: nombre (secuencia de caracteres) y número (entero)."), 400

            pbp_dao = VolleyballPBPDao()

            if not pbp_dao.pbp_exists(event_id):
                return jsonify(Error="No existe una secuencia PBP para este evento."), 400

            if pbp_dao.is_game_over(event_id):
                return jsonify(Error="El partido de Voleibol ha finalizado."), 403

            meta = pbp_dao.get_pbp_meta(event_id)
            if self._sport_keywords["sport"] != meta["sport"]:
                return jsonify(Error="Esta secuencia PBP no corresponde a Voleibol."), 403

            # Validate the athlete number has not been used.
            opponent_roster = pbp_dao.get_opponent_roster(event_id)
            print(opponent_roster)

            if not opponent_roster or (self._sport_keywords["athlete_prefix"] + str(player_info["number"])) not in opponent_roster:
                return jsonify(Error="El atleta no existe en el sistema."), 403

            # Validate the name changes.
            prev_name = opponent_roster[self._sport_keywords["athlete_prefix"] + str(
                player_info["number"])]["name"]

            if player_info["name"] == prev_name:
                return jsonify(MSG="No se encontraron cambios en el nombre del atleta."), 200

            pbp_dao.set_opponent_athlete(event_id, player_info)
            return jsonify(MSG="La información del atleta se modificado en el sistema."), 200

        except Exception as e:
            return jsonify(Error=str(e)), 500

    def setOppPlayer(self, event_id,  player_info):
        """
        Add an athlete to opponent roster or updates its value if exists in the system.
        This function adds an athlete to opponent roster given the event_id and athlete information.
        If the athlete exists, it updates its information.

        Args
            event_id: integer corresponding to an event id.
            player_info: JSON object containing information about the athlete (number and name).

        Returns:
            Response containing a MSG in case of success, or Error message in case of failure.
        """

        try:

            if not isinstance(event_id, int):
                return jsonify(Error="El valor para ID del evento tiene que ser un entero."), 400

            if not isinstance(player_info, dict) or len(player_info) != 2 or not "name" in player_info or not "number" in player_info:
                return jsonify(Error="Información del atleta oponente debe darse en formato JSON y debe contener el nombre y número del atleta."), 400

            if not isinstance(player_info["name"], str) or not isinstance(player_info["number"], int):
                return jsonify(Error="La información del oponente debe darse en el siguiente formato: nombre (secuencia de caracteres) y número (entero)."), 400

            pbp_dao = VolleyballPBPDao()

            if not pbp_dao.pbp_exists(event_id):
                return jsonify(Error="No existe una secuencia PBP para este evento."), 400

            if pbp_dao.is_game_over(event_id):
                return jsonify(Error="El partido de Voleibol ha finalizado."), 403

            meta = pbp_dao.get_pbp_meta(event_id)
            if self._sport_keywords["sport"] != meta["sport"]:
                return jsonify(Error="Esta secuencia PBP no corresponde a Voleibol."), 403

            opponent_roster = pbp_dao.get_opponent_roster(event_id)

            if (self._sport_keywords["athlete_prefix"] + str(player_info["number"])) not in opponent_roster:
                return jsonify(Error="El atleta no existe."), 404

            # Validate the name changes.
            prev_name = opponent_roster[self._sport_keywords["athlete_prefix"] + str(
                player_info["number"])]["name"]

            if player_info["name"] == prev_name:
                return jsonify(MSG="No se encontraron cambios en el nombre del atleta."), 200

            pbp_dao.set_opponent_athlete(event_id, player_info)
            return jsonify(MSG="La información mas reciente del atleta se agregado al sistema."), 200

        except Exception as e:
            print(str(e))
            return jsonify(Error=str(e)), 500

    def removeUPRMPlayer(self, event_id,  player_id):
        """
        Removes a UPRM athlete from the PBP sequence.
        This function deletes a particular UPRM athlete from PBP sequence via the PBP DAO.

        Args
            event_id: integer corresponding to an event id.
            athlete_id: integer corresponding to the athlete to remove.

        Returns:
            Response containing a MSG in case of success, or Error message in case of failure.
        """

        try:

            pbp_dao = VolleyballPBPDao()

            if not pbp_dao.pbp_exists(event_id):
                return jsonify(Error="El ID del evento es inválido."), 403

            if pbp_dao.is_game_over(event_id):
                return jsonify(Error="El partido de Voleibol ha finalizado."), 403

            meta = pbp_dao.get_pbp_meta(event_id)
            if self._sport_keywords["sport"] != meta["sport"]:
                return jsonify(Error="Esta secuencia PBP no corresponde a Voleibol."), 403

            opp_roster = pbp_dao.get_uprm_roster(event_id)

            if opp_roster and not (self._sport_keywords["athlete_prefix"] + str(player_id)) in opp_roster:
                return jsonify(Error="El atleta no existe."), 404

            pbp_dao.remove_uprm_athlete(event_id, player_id)
            return jsonify(MSG="Se ha actualizado la información de atletas UPRM."), 200

        except Exception as e:
            print(str(e))
            return jsonify(Error=str(e)), 500

    def removeOppPlayer(self, event_id,  player_id):
        """
        Removes an opponent athlete from the PBP sequence.
        This function deletes a particular opponent athlete from PBP sequence via the PBP DAO.

        Args
            event_id: integer corresponding to an event id.
            athlete_id: integer corresponding to the athlete to remove.

        Returns:
            Response containing a MSG in case of success, or Error message in case of failure.
        """

        try:

            pbp_dao = VolleyballPBPDao()

            if not pbp_dao.pbp_exists(event_id):
                return jsonify(Error="El ID del evento es inválido."), 403

            if pbp_dao.is_game_over(event_id):
                return jsonify(Error="El partido de Voleibol ha finalizado."), 403

            meta = pbp_dao.get_pbp_meta(event_id)
            if self._sport_keywords["sport"] != meta["sport"]:
                return jsonify(Error="Esta secuencia PBP no corresponde a Voleibol."), 403

            if (self._sport_keywords["athlete_prefix"] + str(player_id)) not in pbp_dao.get_opponent_roster(event_id):
                return jsonify(Error="El atleta no existe."), 404

            pbp_dao.remove_opponent_athlete(event_id, player_id)
            return jsonify(MSG="La información del atleta se ha removido del sistema."), 200

        except Exception as e:
            print(str(e))
            return jsonify(Error=str(e)), 500

    def addPBPAction(self, event_id, action_data):
        """
        Adds a PBP game action into the feed.
        This function interacts with the PBP DAO to insert a Volleyball game action.

        Args
            event_id: integer corresponding to an event id.
            action_data: JSON object containing the new game action's value.

        Returns:
            Response containing a MSG in case of success, or Error message in case of failure.
        """

        try:
            # Validate event id is positive integer.
            if not str(event_id).isdigit():
                return jsonify(Error="El ID de evento es inválido (debe ser un entero)."), 400

            # Validate action data has proper format. (TODO -> CHECK THIS!!!)
            if not action_data:
                return jsonify(Error="La información referente a data no ha sido especificada."), 403

            # Validate event
            pbp_dao = VolleyballPBPDao()
            if not pbp_dao.pbp_exists(event_id):
                return jsonify(Error="No existe una secuencia PBP para este evento."), 403

            if pbp_dao.is_game_over(event_id):
                return jsonify(Error="El partido de Voleibol ha finalizado."), 403

            self._handle_pbp_action(event_id, action_data, pbp_dao)
            return jsonify(MSG="La acción se ha añadido al sistema."), 200

        except Exception as e:
            print(str(e))
            return jsonify(Error=str(e)), 500

    def editPBPAction(self, event_id, action_id, new_action):
        """
        Edits a PBP game action from the feed.
        This function interacts with the PBP DAO to edit a Volleyball game action
        by replacing its previous value with a new one.

        Args
            event_id: integer corresponding to an event id.
            action_id: string corresponding to a game action id.
            new_action: JSON object containing the new game action's value.

        Returns:
            Response containing a MSG in case of success, or Error message in case of failure.
        """
        try:
            # Validate event id is positive integer.
            if not str(event_id).isdigit() and str(event_id).isdigit():
                return jsonify(Error="Valores de ID del evento y ID de la acción deben ser enteros."), 400

            # Validate action data has proper format. (TODO -> CHECK THIS!!!)
            if not new_action:
                return jsonify(Error="Información sobre la nueva acción debe ser especificada (data)."), 403

            # Validate event
            pbp_dao = VolleyballPBPDao()
            if not pbp_dao.pbp_exists(event_id):
                return jsonify(Error="No existe una secuencia PBP para este evento."), 403.

            if pbp_dao.is_game_over(event_id):
                return jsonify(Error="El partido de Voleibol ha finalizado."), 403

            self._handle_pbp_edit_action(
                event_id, action_id, new_action, pbp_dao)
            return jsonify(MSG="Se ha editado la acción exitosamente."), 200

        except Exception as e:
            print(str(e))

            # In case the 'error' is due to no chance in game action, notify the user but don't return as error.
            if str(e) == "No hubo un cambio en la acción.":
                return jsonify(MSG=str(e)), 200

            return jsonify(Error=str(e)), 500

    def removePlayPBPAction(self, event_id, game_action_id):
        """
        Removes a PBP game action from the feed.
        This function interacts with the PBP DAO to remove a Volleyball game action.

        Args
            event_id: integer corresponding to an event id.

        Returns:
            Response containing a MSG in case of success, or Error message in case of failure.
        """

        try:
            # Validate event id is positive integer.
            print("ID", event_id, "action_id", game_action_id)
            if not str(event_id).isdigit() or not str(game_action_id).isdigit():
                return jsonify(Error="Valores para el ID del evento y ID de acción deben ser enteros."), 400

            # Validate event
            pbp_dao = VolleyballPBPDao()
            if not pbp_dao.pbp_exists(event_id):
                return jsonify(Error="No existe una secuencia PBP para este evento."), 403

            if pbp_dao.is_game_over(event_id):
                return jsonify(Error="El partido de Voleibol ha finalizado."), 403

            self._handle_remove_pbp_action(event_id, game_action_id, pbp_dao)
            return jsonify(MSG="Se ha removido la acción exitosamente."), 200
        except Exception as e:
            print(str(e))
            return jsonify(Error=str(e)), 500

    def setPBPSequenceOver(self, event_id):
        """
        Marks a PBP sequence state as over.
        This function interacts with the PBP DAO to modify the game-ended status of a Volleyball
        PBP sequence to true.

        Args
            event_id: integer corresponding to an event id.

        Returns:
            Response containing a MSG in case of success, or Error message in case of failure.
        """

        try:
            # Validate event id is positive integer.
            if not str(event_id).isdigit():
                return jsonify(Error="El ID de evento es inválido (debe ser un entero)."), 400

            pbp_dao = VolleyballPBPDao()
            if not pbp_dao.pbp_exists(event_id):
                return jsonify(Error="No existe una secuencia PBP para este evento."), 403

            meta = pbp_dao.get_pbp_meta(event_id)
            if self._sport_keywords["sport"] != meta["sport"]:
                return jsonify(Error="Esta secuencia PBP no corresponde a Voleibol."), 403

            if pbp_dao.is_game_over(event_id):
                return jsonify(Error="El partido de Voleibol ha finalizado."), 403

            pbp_dao.set_pbp_game_over(event_id)
            return jsonify(MSG="Se marcó el partido de Voleibol como finalizado."), 200

        except Exception as e:
            print(str(e))
            return jsonify(Error=str(e)), 500
