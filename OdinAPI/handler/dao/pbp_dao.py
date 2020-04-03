from .config.fb_config import serv_path, rtdb_config
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db


# TODO -> Add class documentation
class PBPDao:
    '''
    PBPDao - This class implements a Data Access Object pattern to provide 
             Odin API interaction to information about sport play-by-play 
             sequences stored in the non-relational database.
    @author Pedro Luis Rivera Gomez
    '''

    # Initialize Firebase Admin SDK and set Realtime Database instance.
    def __init__(self):
        firebase_admin.initialize_app(
            credentials.Certificate(serv_path), rtdb_config)
        self._rtdb = db
        # TODO -> Move this into the a separate file such as fb_config.py.
        self._db_keywords = {
            "root": "/v1/",
            "meta": "/game-metadata",
            "uprm-roster": "/uprm-roster",
            "opp-roster": "/opponent-roster",
            "set": "/current-set",
            "score": "/score",
            "actions": "/game-actions",
            "score-key": "score",
            "over": "/game-ended",
            "answer": "/answer",
            "uprm-sets": ["/set1-uprm", "/set2-uprm", "/set3-uprm", "/set4-uprm", "/set5-uprm"],
            "opp-sets": ["/set1-opponent", "/set2-opponent", "/set3-opponent", "/set4-opponent", "/set5-opponent"]
        }

    def create_pbp_seq(self, event_id, game_metadata, score_val):
        """
        Initialize a PBP sequence for a valid sport event.
        This function creates a PBP sequence initializing its metadata and scoring system.

        Args
            event_id: integer corresponding to an event id.
            game_metadata: JSON object containing general information about a PBP sequence depending on the sport.
            score_val: JSON object containing the initial scores per period of a PBP sequence depending on the sport.

        Returns:
            void
        """

        event_node = {
            self._db_keywords["meta"]: game_metadata,
            self._db_keywords["score-key"]: score_val
        }

        path = self._db_keywords["root"] + int(event_id)
        self._rtdb.reference(path).set(event_node)

    def remove_pbp_seq(self, event_id):
        """
        Remove a PBP sequence from the non-relational database.
        This function deletes a PBP sequence's node from the non-relational database.

        Args
            event_id: integer corresponding to an event id.

        Returns:
            void
        """

        path = self._db_keywords["root"] + int(event_id)
        return self._rtdb.reference(path).delete()

    def set_pbp_metadata(self, event_id, metadata):
        return self._rtdb.reference(self._db_keywords["root"] + int(event_id) + self._db_keywords["meta"]).set(metadata)

    def set_uprm_roster(self, event_id, uprm_roster):
        return self._rtdb.reference(self._db_keywords["root"] + int(event_id) + self._db_keywords["uprm-roster"]).set(uprm_roster)

    def set_opponent_roster(self, event_id, opponent_roster):
        return self._rtdb.reference(self._db_keywords["root"] + int(event_id) + self._db_keywords["opp-roster"]).set(opponent_roster)

    def pbp_exists(self, event_id):
        return self._rtdb.reference(self._db_keywords["root"] + int(event_id)).get() != None

    def set_current_set(self, event_id, new_set):
        return self._rtdb.reference(self._db_keywords["root"] + int(event_id) + self._db_keywords["set"]).set(new_set)

    def get_current_set(self, event_id):
        return self._rtdb.reference(self._db_keywords["root"] + int(event_id) + self._db_keywords["set"]).get()

    def set_uprm_score(self, event_id, set, score):
        return self._rtdb.reference(self._db_keywords["root"] + int(event_id) + self._db_keywords["score"] + self._db_keywords["uprm-sets"][set - 1]).set(score)

    def get_uprm_score(self, event_id, set):
        return self._rtdb.reference(self._db_keywords["root"] + int(event_id) + self._db_keywords["score"] + self._db_keywords["uprm-sets"][set - 1]).get()

    def set_opponent_score(self, event_id, set, score):
        return self._rtdb.reference(self._db_keywords["root"] + int(event_id) + self._db_keywords["score"] + self._db_keywords["opp-sets"][set - 1]).set(score)

    def get_opponent_score(self, event_id, set):
        return self._rtdb.reference(self._db_keywords["root"] + int(event_id) + self._db_keywords["score"] + self._db_keywords["opp-sets"][set - 1]).get()

    def pbp_game_action_exists(self, event_id, action_id):
        return self._rtdb.reference(self._db_keywords["root"] + int(event_id) + self._db_keywords["actions"] + "/" + action_id).get() != None

    def add_pbp_game_action(self, event_id, action_content):
        return self._rtdb.reference(self._db_keywords["root"] + int(event_id) + self._db_keywords["actions"]).push(action_content)

    def edit_pbp_game_action(self, event_id, action_id, action_content):
        return self._rtdb.reference(self._db_keywords["root"] + int(event_id) + self._db_keywords["actions"] + "/" + action_id).set(action_content)

    def remove_pbp_game_action(self, event_id, action_id):
        """
        Removes a game action from PBP sequence.
        This function deletes a particular game action from PBP sequence.

        Args
            event_id: integer corresponding to an event id.
            action_id: string corresponding to the game action to remove.

        Returns:
            void
        """

        path = self._db_keywords["root"] + int(event_id) + \
            self._db_keywords["actions"] + "/" + action_id

        self._rtdb.reference(path).delete()

    def is_game_over(self, event_id):
        """
        Determines if a particular game is over.
        This function returns the game-ended status of a PBP sequence (Boolean).

        Args
            event_id: integer corresponding to an event id.

        Returns:
            Boolean result that determines if the game is over or not.
        """

        path = self._db_keywords["root"] + int(event_id) + \
            self._db_keywords["meta"] + \
            self._db_keywords["over"] + self._db_keywords["answer"]

        return self._rtdb.reference(path).get()

    def set_pbp_game_over(self, event_id):
        """
        Marks a PBP sequence state as over.
        This function modifies the game-ended status of a PBP sequence to true.

        Args
            event_id: integer corresponding to an event id.

        Returns:
            void
        """

        path = self._db_keywords["root"] + int(event_id) + \
            self._db_keywords["meta"] + self._db_keywords["over"]

        self._rtdb.reference(path).set({"answer": True})


# if __name__ == '__main__':

#     # Initialize a Play-by-Play DAO for quick testing purposes.
#     pbp_dao = PBPDao()
#     print(pbp_dao._rtdb.reference("v1").get())
#     print(pbp_dao.pbp_exists("crap"))
#     print(pbp_dao._rtdb.reference("v1/crap").delete())
#     print(pbp_dao.pbp_exists("crap"))
