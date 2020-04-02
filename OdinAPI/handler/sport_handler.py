from flask import jsonify
from .dao.sport_dao import SportDAO


# TODO -> Add class documentation...
class SportHandler:

    def __init__(self):
        self._dao = SportDAO()

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

    def _build_sport_dict(self, sport_rows):
        '''
        Internal method for building the list of sports into a list of dictionaries.
        '''

        result = []
        for row in sport_rows:
            result.append(self._build_sport_row_dict(row))

        return result

    def _build_sport_category_position(self, sport_rows):
        '''
        Internal method for building the result list dictionary corresponding
        to a sport name along its corresponding ids, categories, and positions if any.
        '''

        result = {}
        for row in sport_rows:

            if len(row) != 5:
                raise Exception(
                    "SportHandler Error: invalid sport row length.")

            # Extract record attributes.
            sport_id = row[0]
            sport_name = row[1]
            sport_image_url = row[2]
            position_name = row[3]
            category_name = row[4]

            # Case: sport not already considered.
            if sport_name not in result:
                result[sport_name] = {
                    "sport_id": [sport_id],
                    "sport_image_url": [sport_image_url] if sport_image_url else [],
                    "position": [position_name] if position_name else [],
                    "category": [category_name] if category_name else []
                }
                continue

            # Case: sport exist, but there is at least an attribute that changes.
            # Approach: For the remaining attributes, if its value is not present then add it into result.
            if sport_id not in result[sport_name]["sport_id"]:
                result[sport_name]["sport_id"].append(sport_id)

            if sport_image_url and sport_image_url not in result[sport_name]["sport_image_url"]:
                result[sport_name]["sport_image_url"].append(sport_image_url)

            if position_name and position_name not in result[sport_name]["position"]:
                result[sport_name]["position"].append(position_name)

            if category_name and category_name not in result[sport_name]["category"]:
                result[sport_name]["category"].append(category_name)

        return result

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

    def getSportCategoriesPositions(self):
        sports = {}
        try:
            sport_rows = self._dao.getSportCategoriesPositions()
            sports = self._build_sport_category_position(sport_rows)
        except:
            return jsonify(ERROR="SportHandler.getSportCategoriesPositions - unable to obtain sports from DAO."), 500

        return jsonify(SPORTS=sports), 200
