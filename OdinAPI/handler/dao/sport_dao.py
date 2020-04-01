from config.sqlconfig import db_config
from flask import jsonify
import psycopg2


# TODO -> Add class documentation.
class SportDAO:

    def __init__(self):
        '''
        Initialize postgreSQL db connection with psycopg2.
        '''
        connection_url = "dbname={} user={} password={} host ={} ".format(
            db_config['database'],
            db_config['username'],
            db_config['password'],
            db_config['host']
        )
        print(connection_url)
        self.conn = psycopg2.connect(connection_url)

    def _build_result(self, cursor):
        '''
        Internal method for building the list of rows from a given query.
        '''
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getAllSports(self):
        """
        Gets all sports supported within the system.
        This function queries sports from the relational database.
        Returns:
            A list of tuples which represent the response to the database query.
            Each sport tuple follows the following structure:
                (id, name, sport_image_url, branch).
        """
        cursor = self.conn.cursor()
        query = '''
                select S.id, S.name, S.sport_image_url, B.name
                from sport as S inner join branch as B on S.branch_id = B.id
                where S.is_invalid = false;
                '''
        cursor.execute(query)
        return self._build_result(cursor)

    def getSportsByBranch(self, branch):
        """
        Gets all sports supported within the system filtered by branch.
        This function queries sports by branch from the relational database.
        Returns:
            A list of tuples which represent the response to the database query.
            Each sport tuple follows the following structure:
                (id, name, sport_image_url, branch).
        """
        cursor = self.conn.cursor()

        # Get all valid sport names and images for all valid sports given its branch.
        query = '''
                select S.id, S.name, S.sport_image_url, B.name
                from (sport as S inner join branch as B on S.branch_id = B.id)
                where S.is_invalid = false
                and B.name = %s;
                '''

        cursor.execute(query, (branch,))
        return self._build_result(cursor)

    def getSportById(self, sport_id):
        """
        Fetches at most one sport record in the database corresponding to a given id.
        This function queries a sport given its id from the relational database.
        Returns:
            A sport tuple follows the following structure:
                (id, name, sport_image_url, branch).
        """
        
        cursor = self.conn.cursor()
        query = '''
                select S.id, S.name, S.sport_image_url, B.name
                from sport as S inner join branch as B on S.branch_id = B.id
                where S.is_invalid = false
                and S.id = %s;
                '''

        cursor.execute(query, (sport_id,))
        return cursor.fetchone()

    def getSportByName(self, sport_name):
        """
        Fetches sport records from the database corresponding to a given sport name.
        This function queries sports given a sport name from the relational database.
        Returns:
            A list of tuples which represent the response to the database query.
            Each sport tuple follows the following structure:
                (id, name, sport_image_url, branch).
        """

        cursor = self.conn.cursor()
        query = '''
                select S.id, S.name, S.sport_image_url, B.name
                from sport as S inner join branch as B on S.branch_id = B.id
                where S.is_invalid = false
                and S.name = %s;
                '''

        cursor.execute(query, (sport_name,))
        return cursor.fetchone()


if __name__ == '__main__':
    sport_dao = SportDAO()

    print(sport_dao.getAllSports())
    print(sport_dao.getSportById("1"))
    print(sport_dao.getSportByName("soccer"))
    print(sport_dao.getSportsByBranch("male"))
