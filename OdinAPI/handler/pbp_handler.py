from flask import jsonify
from .dao.pbp_dao import PBPDao as VolleyballPBPDao
from.dao.mock.event_dao import _mockEventDAO as EventDAO


class PBPHandler:
    '''
    PBPHandler - This class handles incomming requests from Odin API's gateway
                 by interacting with the PBPDAO. It is responsible for modifying
                 the state of content stored in the non-relational database.
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
            "sport": "Voleibol"
        }

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
                return jsonify(ERROR="PBPHandler.startPBPSequence: Invalid event."), 400

            if len(event_info) != 7:
                return jsonify(ERROR="PBPHandler.startPBPSequence: Invalid response from Event DAO."), 500

            if event_info["sport_name"] != self._sport_keywords["sport"]:
                return jsonify(ERROR="PBPHandler.startPBPSequence: Sport does not match Volleyball."), 403

        except:
            return jsonify(ERROR="PBPHandler.startPBPSequence: Could not retrieve information from Event DAO."), 500

        try:
            pbp_dao = VolleyballPBPDao()
            if pbp_dao.pbp_exists(event_id):
                return jsonify(ERROR="PBPHandler.startPBPSequence: PBP Sequence already created."), 403

            # At this point, the event exists and does not have a PBP sequence.
            game_metadata = {
                "branch": event_info[0],
                "game-ended": {"answer": "No"},
                "location": "Home" if event_info[1] else "Away",
                "opponent-color": event_info[2],
                "opponent-name": event_info[3],
                "sport": event_info[4],
                "venue": event_info[5]
            }

            pbp_dao.create_volleyball_pbp_seq(
                event_id, game_metadata, self._sport_keyword["score-val"])

            return jsonify(CREATED="PBP Sequence for " + id + " was successfully created"), 200

        except:
            return jsonify(ERROR="PBPHandler.startPBPSequence: Could not retrieve information from PBP DAO."), 500

    def addUPRMRoster(self):
        return 1

    def addOppRoster(self):
        return 1

    def editUPRMRoster(self):
        return 1

    def editOppRoster(self):
        return 1

    def removeUPRMRoster(self):
        return 1

    def removeOppRoster(self):
        return 1

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
            if event_dao.getEventById(event_id)[4] != self._sport_keywords["sport"]:
                return jsonify(MSG="PBPHandler.setPBPSequenceOver: Not a volleyball event."), 403

            pbp_dao = VolleyballPBPDao()
            if pbp_dao.pbp_exists(event_id):

                if pbp_dao.is_game_over(event_id):
                    return jsonify(ERROR="PBPHandler.addPBPAction: PBP sequence already over."), 403
                # TODO -> validate sequence info is complete... VALIDATE SPORT == voleibol...
                return jsonify(ADDED=pbp_dao.add_pbp_game_action(event_id, {})), 200

            return jsonify(ERROR="PBPHandler.addPBPAction: Non-existing PBP sequence."), 403

        except:
            return jsonify(ERROR="PBPHandler.addPBPSequence: Could not retrieve information from PBP DAO."), 500

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

        return 0

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
            if event_dao.getEventById(event_id)[4] != self._sport_keywords["sport"]:
                return jsonify(MSG="PBPHandler.setPBPSequenceOver: Not a volleyball event."), 403

            pbp_dao = VolleyballPBPDao()
            if pbp_dao.pbp_exists(event_id):

                if pbp_dao.pbp_game_action_exists(event_id, game_action_id):
                    return jsonify(pbp_dao.remove_pbp_game_action(event_id, game_action_id)), 200

                return jsonify(ERROR="PBPHandler.setPBPSequenceOver: Non-existing game action."), 403

            return jsonify(ERROR="PBPHandler.setPBPSequenceOver: Non-existing PBP Sequence."), 403
        except:
            return jsonify(ERROR="PBPHandler.removePlayPBPSequence: Internal error from PBP DAO."), 500

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
            if event_dao.getEventById(event_id)[4] != self._sport_keywords["sport"]:
                return jsonify(MSG="PBPHandler.setPBPSequenceOver: Not a volleyball event."), 403

            if pbp_dao.pbp_exists(event_id):
                pbp_dao.set_pbp_game_over(event_id)
                return jsonify(MSG="PBPHandler.setPBPSequenceOver: Success."), 200

            return jsonify(ERROR="PBPHandler.setPBPSequenceOver: Non-existing PBP Sequence."), 403

        except:
            return jsonify(ERROR="PBPHandler.setPBPSequenceOver: Internal error from PBP DAO."), 500
