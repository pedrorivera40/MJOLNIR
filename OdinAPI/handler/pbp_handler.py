from dao.pbp_dao import VolleyballPBPDAO


class PBPHandler:

    def __init__(self):
        self.dao = VolleyballPBPDAO()

    def startPBPSequence(self, event_id, sequence_info):
        # THIS IS JUST TO REMIND MYSELF I HAVE TO TRY/CATCH INTERACTION WITH DAO.
        # try:
        #     self.dao.startPBPSequence
        # except:
        #      return

        return 0

    def editPBPSequence(self, event_id, sequence_change):
        return 0

    def removePlayPBPSequence(self, event_id, game_action_id):
        return 0
