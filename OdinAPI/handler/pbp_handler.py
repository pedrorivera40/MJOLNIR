from re import search
from flask import jsonify
from .dao.pbp_dao import PBPDao as VolleyballPBPDao
from.dao.mock.event_dao import _mockEventDAO as EventDAO


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
            "color-format": "^#(?:[0-9a-fA-F]{1,2}){3}$"
        }

    def _get_direct_set_path(self, team, event_id, dao):
        """
        Internal method to determine set path directly depending on the action team.
        """

        # Validate team value is specified correctly.
        if team not in self._sport_keywords["teams"]:
            raise Exception("Invalid team value.")

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
            raise Exception("Invalid team value.")

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
        if not dao.pbp_exists(event_id):
            raise Exception("Invalid event id.")

        if dao.is_game_over(event_id):
            raise Exception("Event is over.")

        action_type = action["type"]

        if not action_type:
            raise Exception("Invalid PBP action.")

        # Notifications are only posted. No score or set value needs to be modified from a notification.
        if action_type == self._sport_keywords["notification"]:
            dao.add_pbp_game_action(event_id, action)
            return

        # Adjust game actions modify the score of the direct team indicated in action["team"].
        # These are not added to the notifications feed (non-relational database).
        if action_type == self._sport_keywords["adjust"]:
            set_path = self._get_direct_set_path(action["team"], event_id, dao)
            difference = int(action["difference"])
            dao.adjust_score_by_set(event_id, set_path, difference)
            return

        is_valid_athlete = (action["athlete_id"] in dao.get_uprm_roster(event_id)
                            or action["athlete_id"] in dao.get_opponent_roster(event_id))

        # Scoring game actions modify athlete statistics and team score.
        # TODO -> TEST THIS SECTION.
        if action_type in self._sport_keywords["scoring_actions"]:

            if is_valid_athlete:
                set_path = self._get_direct_set_path(
                    action["team"], event_id, dao)
                difference = int(action["difference"])
                dao.add_pbp_game_action(event_id, action)
                dao.adjust_score_by_set(event_id, set_path, 1)
                return

            else:
                raise Exception("Invalid athlete information.")

        # Personal actions only modify athlete statistics.
        # The only action to do is add to Feed and let clients compute statistics.
        if action_type in self._sport_keywords["personal_actions"]:

            if is_valid_athlete:
                dao.add_pbp_game_action(event_id, action)
                return

            else:
                raise Exception("Invalid athlete information.")

        if action_type in self._sport_keywords["error_actions"]:

            if is_valid_athlete:
                set_path = self._get_indirect_set_path(
                    action["team"], event_id, dao)
                difference = int(action["difference"])
                dao.add_pbp_game_action(event_id, action)
                dao.adjust_score_by_set(event_id, set_path, 1)
                return

            else:
                raise Exception("Invalid athlete information.")

        raise Exception("Undefined Volleyball PBP Sequence Game Action.")

    def _handle_pbp_edit_action(self, event_id, action_id, new_action, dao):
        """
        Internal method for handling editting previously added game actions in a PBP sequence.
        """

        if not dao.pbp_exists(event_id):
            raise Exception("Event does not exist.")

        if dao.is_game_over(event_id):
            raise Exception("Event is over.")

        if not dao.pbp_game_action_exists(event_id, action_id):
            raise Exception("Action does not exist.")

        # Every action must have a type.
        prev_action = dao.get_pbp_action(event_id, action_id)

        if prev_action == new_action:
            raise Exception("There is no change in new action.")

        prev_type = prev_action["type"]
        new_type = new_action["type"]

        # Variables to be used depending on the edit type.
        are_same_type = (prev_type == new_type)

        # Notifications are only posted. No score or set value needs to be modified from a notification.
        if are_same_type and prev_type == self._sport_keywords["notification"]:
            dao.add_pbp_game_action(event_id, new_action)
            return

        # If actions are not the same and one of them is notification. This operation is not allowed.
        if prev_type == self._sport_keywords["notification"] or new_type == self._sport_keywords["notification"]:
            raise Exception("Notifications cannot change type.")

        # From now on, the remaining game actions involve game plays.
        # Plays require values for team and athlete_id.
        # Validate team and athlete_id are valid.
        new_team = new_action["team"]
        athlete_id = new_action["athlete_id"]

        if new_team not in self._sport_keywords["teams"]:
            raise Exception("Invalid team.")

        if new_team == self._sport_keywords["teams"][0] and athlete_id not in dao.get_uprm_roster(event_id):
            raise Exception("Athlete not in UPRM roster.")

        if new_team == self._sport_keywords["teams"][1] and athlete_id not in dao.get_opponent_roster(event_id):
            raise Exception("Athlete not in opponent roster.")

        # *** Case same type of play (scoring action), but a change is present. ***
        if are_same_type and prev_type in self._sport_keywords["scoring_actions"]:
            # Different team means we need to re-attribute the point to the proper team.
            if new_team != prev_action["team"]:
                inc_path = self._get_direct_set_path(new_team, event_id, dao)
                dec_path = self._get_indirect_set_path(new_team, event_id, dao)
                dao.adjust_score_by_differential(
                    event_id, dec_path, inc_path, 1)

            # Update action.
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
                dao.adjust_score_by_differential(
                    event_id, dec_path, inc_path, 1)

            # Update action.
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
                dao.adjust_score_by_differential(
                    event_id, dec_path, inc_path, 1)

            # Update action.
            dao.edit_pbp_game_action(event_id, action_id, new_action)
            return

        # *** Case previously considered scoring action, but changed into a personal action. ***
        if prev_type in self._sport_keywords["scoring_actions"] and new_type in self._sport_keywords["personal_actions"]:
            # If different action but same team, score must decrease for current team. Otherwise just update the action.
            dec_path = self._get_direct_set_path(new_team, event_id, dao)
            if new_team != prev_action["team"]:
                dec_path = self._get_indirect_set_path(new_team, event_id, dao)

            dao.adjust_score_by_set(event_id, dec_path, -1)
            # Update action.
            dao.edit_pbp_game_action(event_id, action_id, new_action)
            return

        # *** Case previously considered error action, but changed into a scoring action. ***
        if prev_type in self._sport_keywords["error_actions"] and new_type in self._sport_keywords["scoring_actions"]:
            # If different action but same team, point must be attributed to the other team. Otherwise just update the action.
            if new_team == prev_action["team"]:
                dec_path = self._get_indirect_set_path(new_team, event_id, dao)
                inc_path = self._get_direct_set_path(new_team, event_id, dao)
                dao.adjust_score_by_differential(
                    event_id, dec_path, inc_path, 1)

            # Update action.
            dao.edit_pbp_game_action(event_id, action_id, new_action)
            return

        # *** Case previously considered error action, but changed into a personal action. ***
        if prev_type in self._sport_keywords["error_actions"] and new_type in self._sport_keywords["personal_actions"]:
            # If different action but same team, score must decrease for current team. Otherwise just update the action.
            inc_path = self._get_direct_set_path(new_team, event_id, dao)
            if new_team != prev_action["team"]:
                inc_path = self._get_indirect_set_path(new_team, event_id, dao)

            dao.adjust_score_by_set(event_id, inc_path, 1)
            # Update action.
            dao.edit_pbp_game_action(event_id, action_id, new_action)
            return

        # *** Case previously considered personal action, but changed into a scoring action. ***
        if prev_type in self._sport_keywords["personal_actions"] and new_type in self._sport_keywords["scoring_actions"]:
            # If different action but same team, score must decrease for current team. Otherwise just update the action.
            inc_path = self._get_direct_set_path(new_team, event_id, dao)
            if new_team != prev_action["team"]:
                inc_path = self._get_indirect_set_path(new_team, event_id, dao)

            dao.adjust_score_by_set(event_id, inc_path, 1)
            # Update action.
            dao.edit_pbp_game_action(event_id, action_id, new_action)
            return

        # *** Case previously considered personal action, but changed into a error action. ***
        if prev_type in self._sport_keywords["personal_actions"] and new_type in self._sport_keywords["error_actions"]:
            # If different action but same team, score must decrease for current team. Otherwise just update the action.
            dec_path = self._get_direct_set_path(new_team, event_id, dao)
            if new_team != prev_action["team"]:
                dec_path = self._get_indirect_set_path(new_team, event_id, dao)

            dao.adjust_score_by_set(event_id, dec_path, -1)
            # Update action.
            dao.edit_pbp_game_action(event_id, action_id, new_action)
            return

        raise Exception("Unexpected PBP action")

    def _handle_remove_pbp_action(self, event_id, action_id, dao):
        """
        Internal method for handling PBP actions removal and its effects over current score.
        """

        if not dao.pbp_exists(event_id):
            raise Exception("Event does not exist.")

        if dao.is_game_over(event_id):
            raise Exception("Event is over.")

        if not dao.pbp_game_action_exists(event_id, action_id):
            raise Exception("Action does not exist.")

        action = dao.get_pbp_action(event_id, action_id)

        # If it is a scoring action, direct team score must decrease by 1.
        if action["type"] in self._sport_keywords["scoring_actions"]:
            path = self._get_direct_set_path(action["team"], event_id, dao)
            dao.adjust_score_by_set(event_id, path, -1)

        # If it is an error action, indirect score must decrease by 1.
        elif action["type"] in self._sport_keywords["error_actions"]:
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
            Response containing a MSG in case of success, or ERROR message in case of failure.
        """

        try:
            event_info = EventDAO().getEventById(event_id)

            if not event_info:
                return jsonify(ERROR="Invalid event."), 400

            if len(event_info) != 7:
                return jsonify(ERROR="Invalid response from Event DAO."), 500

            if event_info["sport_name"] != self._sport_keywords["sport"]:
                return jsonify(ERROR="Sport does not match Volleyball."), 403

            pbp_dao = VolleyballPBPDao()
            if pbp_dao.pbp_exists(event_id):
                return jsonify(ERROR="PBP Sequence already created."), 403

            # At this point, the event exists and does not have a PBP sequence.
            game_metadata = {
                "game-ended": {"answer": "No"},
                "sport": event_info[4],
            }

            pbp_dao.create_pbp_seq(
                event_id, game_metadata, self._sport_keywords["score-val"])

            return jsonify(MSG="PBP Sequence for " + id + " was successfully created"), 200

        except Exception as e:
            return jsonify(ERROR=e), 500

    def removePBPSequence(self, event_id):
        try:
            pbp_dao = VolleyballPBPDao()
            if not pbp_dao.pbp_exists(event_id):
                return jsonify(ERROR="PBP sequence does not exist."), 403

            meta = pbp_dao.get_pbp_meta(event_id)
            if meta["sport"] != meta["sport"]:
                return jsonify(ERROR="Not volleyball PBP sequence"), 403

            pbp_dao.remove_pbp_seq(event_id)
            return jsonify(MSG="PBP Sequence removed."), 200

        except Exception as e:
            return jsonify(ERROR=e)

    def setOpponentColor(self, event_id, color):
        """
        Sets the opponent color.
        This function sets the opponent color of a particular PBP sequence. This is mainly for UI purposes on the client side.

        Args
            event_id: integer corresponding to an event id.
            color: string corresponding to a hex-formatted color.

        Returns:
            Response containing a MSG in case of success, or ERROR message in case of failure.
        """

        try:
            # Validate a hex formatted color is provided.
            if not search(self._sport_keywords["color-format"], color):
                return jsonify(ERROR="Invalid color format."), 400

            event_info = EventDAO().getEventById(event_id)

            if not event_info:
                return jsonify(ERROR="Invalid event."), 400

            if len(event_info) != 7:
                return jsonify(ERROR="Invalid response from Event DAO."), 500

            if event_info["sport_name"] != self._sport_keywords["sport"]:
                return jsonify(ERROR="Sport does not match Volleyball."), 403

            pbp_dao = VolleyballPBPDao()
            if not pbp_dao.pbp_exists(event_id):
                return jsonify(ERROR="PBP sequence does not exist."), 403

            pbp_dao.set_opponent_color(event_id, color)
            return jsonify(MSG="Color set."), 200

        except Exception as e:
            return jsonify(ERROR=e), 500

    def setUPRMPlayer(self, event_id, player_info):
        """
        Add an athlete to UPRM roster or updates its value if exists in the system.
        This function adds an athlete to UPRM roster given it's event_id.
        If the athlete exists, it updates its information.

        Args
            event_id: integer corresponding to an event id.

        Returns:
            Response containing a MSG in case of success, or ERROR message in case of failure.
        """
        # TODO -> Verify the player is valid...
        try:
            event_dao = EventDAO()

            # TODO -> check if it would be better adding another method in the DAO for getting sportByEventId.
            # TODO -> make sure this alligns with the output of Event DAO (contact Luis).
            if event_dao.getEventById(event_id)[4] != self._sport_keywords["sport"]:
                return jsonify(ERROR="Not a volleyball event."), 403

            pbp_dao = VolleyballPBPDao()

            if not pbp_dao.pbp_exists(event_id):
                return jsonify(ERROR="Invalid event id."), 403

            if not player_info["number"] or not player_info["name"] or not player_info["athlete_id"]:
                return jsonify(ERROR="Invalid player_info. Must contain number, name, and athlete id."), 403

            pbp_dao.set_uprm_athlete(event_id, player_info)
            return jsonify(MSG="Athlete information set in the system."), 200

        except Exception as e:
            return jsonify(ERROR=e), 500

    def setOppPlayer(self, event_id,  player_info):
        """
        Add an athlete to opponent roster or updates its value if exists in the system.
        This function adds an athlete to opponent roster given it's event_id.
        If the athlete exists, it updates its information.

        Args
            event_id: integer corresponding to an event id.

        Returns:
            Response containing a MSG in case of success, or ERROR message in case of failure.
        """
        # TODO -> Verify the player is valid...

        try:
            event_dao = EventDAO()

            # TODO -> check if it would be better adding another method in the DAO for getting sportByEventId.
            # TODO -> make sure this alligns with the output of Event DAO (contact Luis).
            if event_dao.getEventById(event_id)[4] != self._sport_keywords["sport"]:
                return jsonify(ERROR="Not a volleyball event."), 403

            pbp_dao = VolleyballPBPDao()

            if not pbp_dao.pbp_exists(event_id):
                return jsonify(ERROR="Invalid event id."), 403

            if not player_info["number"] or not player_info["name"]:
                return jsonify(ERROR="Invalid player_info. Must contain number, and name."), 403

            pbp_dao.set_opponent_athlete(event_id, player_info)
            return jsonify(MSG="Athlete information set in the system."), 200

        except Exception as e:
            return jsonify(ERROR=e), 500

    def removeUPRMPlayer(self, event_id,  player_id):
        """
        Removes a UPRM athlete from the PBP sequence.
        This function deletes a particular UPRM athlete from PBP sequence via the PBP DAO.

        Args
            event_id: integer corresponding to an event id.
            athlete_id: integer corresponding to the athlete to remove.

        Returns:
            Response containing a MSG in case of success, or ERROR message in case of failure.
        """

        try:
            event_dao = EventDAO()

            # TODO -> check if it would be better adding another method in the DAO for getting sportByEventId.
            # TODO -> make sure this alligns with the output of Event DAO (contact Luis).
            if event_dao.getEventById(event_id)[4] != self._sport_keywords["sport"]:
                return jsonify(ERROR="Not a volleyball event."), 403

            pbp_dao = VolleyballPBPDao()

            if not pbp_dao.pbp_exists(event_id):
                return jsonify(ERROR="Invalid event id."), 403

            if not player_id in pbp_dao.get_uprm_roster(event_id):
                return jsonify(ERROR="Player does not exist."), 404

            pbp_dao.remove_uprm_athlete(event_id, player_id)
            return jsonify(MSG="Athlete information removed from the system."), 200

        except Exception as e:
            return jsonify(ERROR=e), 500

    def removeOppPlayer(self, event_id,  player_id):
        """
        Removes an opponent athlete from the PBP sequence.
        This function deletes a particular opponent athlete from PBP sequence via the PBP DAO.

        Args
            event_id: integer corresponding to an event id.
            athlete_id: integer corresponding to the athlete to remove.

        Returns:
            Response containing a MSG in case of success, or ERROR message in case of failure.
        """

        try:
            event_dao = EventDAO()

            # TODO -> check if it would be better adding another method in the DAO for getting sportByEventId.
            # TODO -> make sure this alligns with the output of Event DAO (contact Luis).
            if event_dao.getEventById(event_id)[4] != self._sport_keywords["sport"]:
                return jsonify(ERROR="Not a volleyball event."), 403

            pbp_dao = VolleyballPBPDao()

            if not pbp_dao.pbp_exists(event_id):
                return jsonify(ERROR="Invalid event id."), 403

            if not player_id in pbp_dao.get_opponent_roster(event_id):
                return jsonify(ERROR="Player does not exist."), 404

            pbp_dao.remove_opponent_athlete(event_id, player_id)
            return jsonify(MSG="Athlete information removed from the system."), 200

        except Exception as e:
            return jsonify(ERROR=e), 500

    def addPBPAction(self, event_id, action_data):
        """
        Adds a PBP game action into the feed.
        This function interacts with the PBP DAO to insert a Volleyball game action.

        Args
            event_id: integer corresponding to an event id.
            action_data: JSON object containing the new game action's value.

        Returns:
            Response containing a MSG in case of success, or ERROR message in case of failure.
        """

        try:
            event_dao = EventDAO()

            # TODO -> check if it would be better adding another method in the DAO for getting sportByEventId.
            # TODO -> make sure this alligns with the output of Event DAO (contact Luis).
            if event_dao.getEventById(event_id)[4] != self._sport_keywords["sport"]:
                return jsonify(ERROR="Not a volleyball event."), 403

            pbp_dao = VolleyballPBPDao()
            self._handle_pbp_action(event_id, action_data, pbp_dao)
            return jsonify(MSG="Action added into the system."), 200

        except Exception as e:
            return jsonify(ERROR=e), 500

    # TODO -> Edit to implement a similar approach to the addPBPAction method.
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
            Response containing a MSG in case of success, or ERROR message in case of failure.
        """
        try:
            event_dao = EventDAO()

            # TODO -> check if it would be better adding another method in the DAO for getting sportByEventId.
            # TODO -> make sure this alligns with the output of Event DAO (contact Luis).
            if event_dao.getEventById(event_id)[4] != self._sport_keywords["sport"]:
                return jsonify(ERROR="Not a volleyball event."), 403

            pbp_dao = VolleyballPBPDao()

            self._handle_pbp_edit_action(
                event_id, action_id, new_action, pbp_dao)
            return jsonify(MSG="Edit game action success."), 200

        except Exception as e:
            return jsonify(ERROR=e), 500

    # TODO -> Make it work same as add action (handle scoring actions...)
    def removePlayPBPAction(self, event_id, game_action_id):
        """
        Removes a PBP game action from the feed.
        This function interacts with the PBP DAO to remove a Volleyball game action.

        Args
            event_id: integer corresponding to an event id.

        Returns:
            Response containing a MSG in case of success, or ERROR message in case of failure.
        """

        try:
            event_dao = EventDAO()

            # TODO -> check if it would be better adding another method in the DAO for getting sportByEventId.
            # TODO -> make sure this alligns with the output of Event DAO (contact Luis).
            if event_dao.getEventById(event_id)[4] != self._sport_keywords["sport"]:
                return jsonify(ERROR="Not a volleyball event."), 403

            event_dao = EventDAO()
            self._handle_remove_pbp_action(event_id, game_action_id, event_dao)

            return jsonify(MSG="Removed game action"), 200
        except Exception as e:
            return jsonify(ERROR=e), 500

    def setPBPSequenceOver(self, event_id):
        """
        Marks a PBP sequence state as over.
        This function interacts with the PBP DAO to modify the game-ended status of a Volleyball
        PBP sequence to true.

        Args
            event_id: integer corresponding to an event id.

        Returns:
            Response containing a MSG in case of success, or ERROR message in case of failure.
        """

        try:
            pbp_dao = VolleyballPBPDao()
            event_dao = EventDAO()

            # TODO -> check if it would be better adding another method in the DAO for getting sportByEventId.
            # TODO -> make sure this alligns with the output of Event DAO (contact Luis).
            if event_dao.getEventById(event_id)[4] != self._sport_keywords["sport"]:
                return jsonify(ERROR="Not a volleyball event."), 403

            if pbp_dao.pbp_exists(event_id):
                pbp_dao.set_pbp_game_over(event_id)
                return jsonify(MSG="Success."), 200

            return jsonify(ERROR="Non-existing PBP Sequence."), 403

        except Exception as e:
            return jsonify(ERROR=e), 500
