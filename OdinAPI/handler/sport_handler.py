
'''
getAllSports() //Instantiates a Sport DAO in order to complete the desired get  request and it returns a JSON with the desired information or with an error message.

getSportById(sID)//Instantiates a Sport DAO in order to complete the desired get  request and it returns a JSON with the desired information or with an error message.

getSportByName(sName)//Instantiates a Sport DAO in order to complete the desired get  request and it returns a JSON with the desired information or with an error message.

mapSportToDict(record)//Maps a Sport record to a dictionary and returns it.

getAllSportCategory()//Instantiates a Sport Category DAO in order to complete the desired get  request and it returns a JSON with the desired information or with an error message.

getSportCategoryByID(scID)//Instantiates a Sport Category DAO in order to complete the desired get  request and it returns a JSON with the desired information or with an error message.

getSportCategoryByName(scName)//Instantiates a Sport Category DAO in order to complete the desired get  request and it returns a JSON with the desired information or with an error message.

mapSportCategoryToDict(record)//Maps a Sport Category record to a dictionary and returns it.

*** (sport_id, sport_name, sport_image_url, branch_id, branch_name)

'''

from flask import jsonify
from .dao.sport_dao import SportDAO


# TODO -> Add class documentation...
class SportHandler:

    def __init__(self):
        self._dao = SportDAO()

    def _build_sport_dict(self, sport_rows):
        '''
        Internal method for building the list of sports into a list of dictionaries.
        '''

        result = []
        for row in sport_rows:
            result.append(self._build_sport_row_dict(row))

        return result

    def _build_sport_row_dict(self, sport_row):
        '''
        Internal method for building a dictionary per sport row obtained from DAO.
        '''

        if len(sport_row != 4):
            raise Exception("SportHandler Error: invalid sport row length.")

        return {
            "sport_id": sport_row[0],
            "sport_name": sport_row[1],
            "sport_image_url": sport_row[2],
            "branch_name": sport_row[3]
        }

    def getAllSports(self):

        sports = []
        try:
            sport_rows = self._dao.getAllSports()
            sports = self._build_sport_dict(sport_rows)
        except:
            return jsonify(ERROR="SportHandler.getAllSports - unable to obtain sports from DAO."), 500

        return jsonify(SPORTS=sports), 200

    def getSportsByBranch(self, branch):
        sports = []
        try:
            sport_rows = self._dao.getSportsByBranch(branch)
            sports = self._build_sport_dict(sport_rows)
        except:
            return jsonify(ERROR="SportHandler.getSportsByBranch - unable to obtain sports from DAO."), 500

        return jsonify(SPORTS=sports), 200

    def getSportById(self, sport_id):
        sport = {}
        try:
            sport_row = self._dao.getSportById(sport_id)
            sport = self._build_sport_row_dict(sport_row)
        except:
            return jsonify(ERROR="SportHandler.getSportById - unable to obtain sport from DAO."), 500

        return jsonify(SPORT=sport), 200

    def getSportByName(self, sport_name):
        sports = {}
        try:
            sport_rows = self._dao.getSportByName(sport_name)
            sports = self._build_sport_dict(sport_rows)
        except:
            return jsonify(ERROR="SportHandler.getSportByName - unable to obtain sports from DAO."), 500

        return jsonify(SPORTS=sports), 200

    # def _build_sport_category_position()

    # def getSportCategoriesPositions(self):
    #     return 1
