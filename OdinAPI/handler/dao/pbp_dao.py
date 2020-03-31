from config.fb_config import serv_path, rtdb_config
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db


# TODO -> Add class documentation
class VolleyballPBPDao:

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
            "opp-sets": ["/set1-opponent", "/set2-opponent", "/set3-opponent", "/set4-opponent", "/set5-opponent"]
        }

    def create_volleyball_pbp_seq(self, event_id, game_metadata, uprm_roster, opponent_roster):
        # Define basic structure of a PBP node contained in the NoSQL database.
        event_node = {
            self._db_keywords["meta"]: game_metadata,
            self._db_keywords["score-key"]: self._db_keywords["score-val"]
        }

        return self._rtdb.reference(self._db_keywords["root"] + event_id).set(event_node)

    def remove_volleyball_pbp_seq(self, event_id):
        return self._rtdb.reference(self._db_keywords["root"] + event_id).delete()

    def set_pbp_metadata(self, event_id, metadata):
        return self._rtdb.reference(self._db_keywords["root"] + event_id + self._db_keywords["meta"]).set(metadata)

    def set_uprm_roster(self, event_id, uprm_roster):
        return self._rtdb.reference(self._db_keywords["root"] + event_id + self._db_keywords["uprm-roster"]).set(uprm_roster)

    def set_opponent_roster(self, event_id, opponent_roster):
        return self._rtdb.reference(self._db_keywords["root"] + event_id + self._db_keywords["opp-roster"]).set(opponent_roster)

    def pbp_exists(self, event_id):
        return self._rtdb.reference(self._db_keywords["root"] + event_id).get() != None

    def set_current_set(self, event_id, new_set):
        return self._rtdb.reference(self._db_keywords["root"] + event_id + self._db_keywords["set"]).set(new_set)

    def get_current_set(self, event_id):
        return self._rtdb.reference(self._db_keywords["root"] + event_id + self._db_keywords["set"]).get()

    def set_uprm_score(self, event_id, set, score):
        return self._rtdb.reference(self._db_keywords["root"] + event_id + self._db_keywords["score"] + self._db_keywords["uprm-sets"][set - 1]).set(score)

    def get_uprm_score(self, event_id, set):
        return self._rtdb.reference(self._db_keywords["root"] + event_id + self._db_keywords["score"] + self._db_keywords["uprm-sets"][set - 1]).get()

    def set_opponent_score(self, event_id, set, score):
        return self._rtdb.reference(self._db_keywords["root"] + event_id + self._db_keywords["score"] + self._db_keywords["opp-sets"][set - 1]).set(score)

    def get_opponent_score(self, event_id, set):
        return self._rtdb.reference(self._db_keywords["root"] + event_id + self._db_keywords["score"] + self._db_keywords["opp-sets"][set - 1]).get()

    def add_pbp_game_action(self, event_id, action_content):
        return self._rtdb.reference(self._db_keywords["root"] + event_id + self._db_keywords["actions"]).push(action_content)

    def edit_pbp_game_action(self, event_id, action_id, action_content):
        return self._rtdb.reference(self._db_keywords["root"] + event_id + self._db_keywords["actions"] + "/" + action_id).set(action_content)

    def remove_pbp_game_action(self, event_id, action_id):
        return self._rtdb.reference(self._db_keywords["root"] + event_id + self._db_keywords["actions"] + "/" + action_id).delete()


if __name__ == '__main__':

    # Initialize a Play-by-Play DAO for quick testing purposes.
    pbp_dao = VolleyballPBPDao()
    print(pbp_dao._rtdb.reference("v1").get())
    print(pbp_dao.pbp_exists("crap"))
    print(pbp_dao._rtdb.reference("v1/crap").delete())
    print(pbp_dao.pbp_exists("crap"))
    # print(pbp_dao.get_current_set("unique-volleyball-game-id-1"))
    # pbp_dao.create_volleyball_pbp_seq(1, 1, 1, 1)
    # print(pbp_dao._rtdb.reference("/v1/caca").push({"a": "1"}))
    # print(pbp_dao._rtdb.reference(
    #     "/v1/caca/-M3iczDv5Lii5kzBT8Ms").update({"a": "3"}))
