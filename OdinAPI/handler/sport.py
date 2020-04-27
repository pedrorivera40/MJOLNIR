from flask import jsonify
from .dao.sport_dao import SportDAO


class SportHandler:
    '''
    SportHandler - This class handles incomming requests from Odin API's gateway
                   by interacting with the SportDAO. It is responsible for read
                   operations corresponding to sports information including 
                   sport names, branches, categories, and positions.
    @author Pedro Luis Rivera Gomez
    '''

    def _build_sport_row_dict(self, sport_row):
        '''
        Internal method for building a dictionary per sport row obtained from DAO.
        '''

        if len(sport_row) != 4:
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
        """
        Gets all sports supported within the system.
        This function fetches sport records from the DAO.

        Returns:
            A JSON object that contains a list of sport entries.
            Each sport entry follows the following format:
                {
                    "sport_id": SPORT_ID_VALUE,
                    "sport_name": SPORT_NAME_VALUE,
                    "sport_image_url": SPORT_IMAGE_URL_VALUE,
                    "branch_name": BRANCH_NAME_VALUE
                }
        """

        sports = []
        try:
            sport_rows = SportDAO().getAllSports()
            sports = self._build_sport_dict(sport_rows)

            if len(sports) == 0:
                return jsonify(ERROR="SportHandler.getAllSports - sport data not found."), 400
        except:
            return jsonify(ERROR="SportHandler.getAllSports - unable to obtain sports from DAO."), 500

        return jsonify(SPORTS=sports), 200

    def getSportsByBranch(self, branch):
        """
        Gets all sports supported within the system filtered by branch.
        This function fetches sport records corresponding to a given branch from the DAO.

        Args
            branch: string corresponging to the sport branch

        Returns:
            A JSON object that contains a list of sport entries.
            Each sport entry follows the following format:
                {
                    "sport_id": SPORT_ID_VALUE,
                    "sport_name": SPORT_NAME_VALUE,
                    "sport_image_url": SPORT_IMAGE_URL_VALUE,
                    "branch_name": BRANCH_NAME_VALUE
                }
        """

        sports = []
        try:
            sport_rows = SportDAO().getSportsByBranch(branch)
            sports = self._build_sport_dict(sport_rows)

            if len(sports) == 0:
                return jsonify(ERROR="SportHandler.getSportsByBranch - sport data not found."), 400

        except:
            return jsonify(ERROR="SportHandler.getSportsByBranch - unable to obtain sports from DAO."), 500

        return jsonify(SPORTS=sports), 200

    def getSportById(self, sport_id):
        """
        Gets sport entry for a given sport id.
        This function fetches the sport record corresponding to a given sport id from the DAO.

        Args
            sport_id: integer corresponding to a sport id in the system

        Returns:
            A JSON object with a list of sport entries.
            Each entry follows the following format:
                {
                    "sport_id": SPORT_ID_VALUE,
                    "sport_name": SPORT_NAME_VALUE,
                    "sport_image_url": SPORT_IMAGE_URL_VALUE,
                    "branch_name": BRANCH_NAME_VALUE
                }
        """
        sport = {}
        try:
            sport_row = SportDAO().getSportById(sport_id)
            sport = self._build_sport_row_dict(sport_row)
            if len(sport) == 0:
                return jsonify(ERROR="SportHandler.getSportById - sport not found."), 400
        except:
            return jsonify(ERROR="SportHandler.getSportById - unable to obtain sport from DAO."), 500

        return jsonify(SPORT=sport), 200

    def getSportByName(self, sport_name):
        """
        Gets the sports within the system that correspond to a given names.
        This function fetches sport records corresponding to a given branch from the DAO.

        Args
            sport_name: string corresponding to the sport name of interest

        Returns:
            A JSON object that contains a list of sport entries.
            Each sport entry follows the following format:
                {
                    "sport_id": SPORT_ID_VALUE,
                    "sport_name": SPORT_NAME_VALUE,
                    "sport_image_url": SPORT_IMAGE_URL_VALUE,
                    "branch_name": BRANCH_NAME_VALUE
                }
        """

        sports = {}
        try:
            sport_rows = SportDAO().getSportByName(sport_name)
            sports = self._build_sport_dict(sport_rows)
            if len(sports) == 0:
                return jsonify(ERROR="SportHandler.getSportByName - sport not found."), 400
        except:
            return jsonify(ERROR="SportHandler.getSportByName - unable to obtain sports from DAO."), 500

        return jsonify(SPORTS=sports), 200

    def getSportCategoriesPositions(self):
        """
        Get sports and their respective categories and positions if any.
        This function obtains sports, categories, and positions from the DAO.

        Returns:
            A JSON object that follows the following structure:
                {
                    SPORT_NAME_1 : 
                    {
                        "sport_id" [SPORT_ID_1, SPORT_ID_2, ...],
                        "sport_image_url": [SPORT_IMAGE_URL_1, SPORT_IMAGE_URL_2, ...],
                        "position": [POSITION_NAME_1, POSITION_NAME_2, ...],
                        "category": [CATEGORY_NAME_1, CATEGORY_NAME_2, ...]
                    },
                    ...
                }
        """

        sports = {}
        try:
            sport_rows = SportDAO().getSportCategoriesPositions()
            sports = self._build_sport_category_position(sport_rows)
            if len(sports) == 0:
                return jsonify(ERROR="SportHandler.getSportCategoriesPositions - sport data not found."), 400
        except:
            return jsonify(ERROR="SportHandler.getSportCategoriesPositions - unable to obtain sports from DAO."), 500

        return jsonify(SPORTS=sports), 200
