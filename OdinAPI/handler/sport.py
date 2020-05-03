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
            raise Exception(
                "El valor obtenido de la basede datos es inválido.")

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

        mapped_records = []

        for row in sport_rows:
            result = {}
            # Extract record attributes.
            sport_id = row[0]
            sport_name = row[1]
            sport_branch = row[2]
            position_name = row[3]
            category_name = row[4]
            # print(row)
            # Case: sport not already considered.
            if not mapped_records:
                if sport_id not in result:

                    result['sport_id'] = sport_id
                    result['sport_name'] = sport_name
                    result['branch_name'] = sport_branch if sport_branch else ''
                    result['positions'] = [
                        position_name] if position_name else []
                    result['categories'] = [
                        category_name] if category_name else []
                    mapped_records.append(result)
                    continue
            else:
                foundMatch = False
                for record in mapped_records:
                    # print(record)
                    if sport_id == record['sport_id']:
                        #print('match found')
                        if position_name and position_name not in record['positions']:
                            record['positions'].append(position_name)

                        if category_name and category_name not in record['categories']:
                            # print(record['categories'])
                            record['categories'].append(category_name)

                        foundMatch = True
                        break

                if foundMatch:
                    continue

                else:
                    result['sport_id'] = sport_id
                    result['sport_name'] = sport_name
                    result['branch_name'] = sport_branch if sport_branch else ''
                    result['positions'] = [
                        position_name] if position_name else []
                    result['categories'] = [
                        category_name] if category_name else []
                    mapped_records.append(result)
                    continue

        return mapped_records

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
                return jsonify(ERROR="No se encontró información sobre ese deporte."), 400
        except:
            return jsonify(ERROR="Problemas internos relacionados al DAO."), 500

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
                return jsonify(ERROR="No se encontró información sobre ese deporte."), 400

        except:
            return jsonify(ERROR="Problemas internos relacionados al DAO."), 500

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
                return jsonify(ERROR="No se encontró información sobre ese deporte."), 400
        except:
            return jsonify(ERROR="Problemas internos relacionados al DAO."), 500

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
                return jsonify(ERROR="No se encontró información sobre ese deporte."), 400
        except:
            return jsonify(ERROR="Problemas internos relacionados al DAO."), 500

        return jsonify(SPORTS=sports), 200

    def getSportCategoriesPositions(self):
        """
        Get sports and their respective categories and positions if any.
        This function obtains sports, categories, and positions from the DAO.

        Returns:
            A JSON object that follows the following structure:
                {                 
                    {
                        "sport_id" : SPORT_ID,
                        "sport_name": 'SPORT_NAME',
                        "branch_name": 'BRANCH_NAME',
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
                return jsonify(ERROR="No se encontró información sobre ese deporte."), 400
        except:
            return jsonify(ERROR="Problemas internos relacionados al DAO."), 500

        return jsonify(SPORTS=sports), 200
