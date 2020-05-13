from .config.sqlconfig import db_config
from flask import jsonify
import psycopg2


class SportDAO:
    '''
    SportDAO - This class implements a Data Access Object pattern to provide 
               Odin API information regarding sports stored in the relational 
               database.
    @author Pedro Luis Rivera Gomez
    '''

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

    def getCategoriesBySportId(self, sport_id):
        """
        Get the categories of a sport given its sport_id.
        This function fetches the list of categories along 
        with their id for a particular sport record.
        This function queries categories from the relational 
        database.

        Returns:
            A list of tuples which represent the response to the database query.
            Each sport tuple follows the following structure:
                (category_id, category_name).
        """

        cursor = self.conn.cursor()
        query = '''
                select C.id, C.name from sport as S join category as C 
                on (S.id = C.sport_id) where S.id = %s;
                '''

        cursor.execute(query, (sport_id,))
        return self._build_result(cursor)

    def getAllSports(self):
        """
        Gets all sports supported within the system.
        This function queries sports from the relational database.

        Returns:
            A list of tuples which represent the response to the database query.
            Each sport tuple follows the following structure:
                (sport_id, sport_name, sport_image_url, branch_name).
        """
        cursor = self.conn.cursor()
        query = '''
                select S.id, S.name, S.sport_image_url, B.name
                from sport as S inner join branch as B on S.branch_id = B.id;
                '''
        cursor.execute(query)
        return self._build_result(cursor)

    def getSportsByBranch(self, branch):
        """
        Gets all sports supported within the system filtered by branch.
        This function queries sports by branch from the relational database.

        Args
            branch: string corresponging to the sport branch

        Returns:
            A list of tuples which represent the response to the database query.
            Each sport tuple follows the following structure:
                (sport_id, sport_name, sport_image_url, branch_name).
        """

        cursor = self.conn.cursor()
        query = '''
                select S.id, S.name, S.sport_image_url, B.name
                from (sport as S inner join branch as B on S.branch_id = B.id)
                where B.name = %s;
                '''

        cursor.execute(query, (branch,))
        return self._build_result(cursor)

    def getSportById(self, sport_id):
        """
        Fetches at most one sport record in the database corresponding to a given id.
        This function queries a sport given its id from the relational database.

        Args
            sport_id: integer corresponding to a sport id in the relational database

        Returns:
            A sport tuple follows the following structure:
                (sport_id, sport_name, sport_image_url, branch_name).
        """

        cursor = self.conn.cursor()
        query = '''
                select S.id, S.name, S.sport_image_url, B.name
                from sport as S inner join branch as B on S.branch_id = B.id
                where S.id = %s;
                '''

        cursor.execute(query, (sport_id,))
        return cursor.fetchone()

    def getSportByName(self, sport_name):
        """
        Fetches sport records from the database corresponding to a given sport name.
        This function queries sports given a sport name from the relational database.

        Args
            sport_name: string corresponding to the sport name of interest

        Returns:
            A list of tuples which represent the response to the database query.
            Each sport tuple follows the following structure:
                (sport_id, sport_name, sport_image_url, branch_name).
        """

        cursor = self.conn.cursor()
        query = '''
                select S.id, S.name, S.sport_image_url, B.name
                from sport as S inner join branch as B on S.branch_id = B.id
                where S.name = %s;
                '''

        cursor.execute(query, (sport_name,))
        return self._build_result(cursor)

    def getSportCategoriesPositions(self):
        """
        Get records from the database corresponding to sports and their 
        respective categories and positions if any.
        This function queries sport categories and positions from the relational database.

        Returns:
            A list of tuples which represent the response to the database query.
            Each sport tuple follows the following structure:
                (sport_id, sport_name, branch_name, position_name, category_name).
        """

        cursor = self.conn.cursor()
        query = '''
                select S.id, S.name, B.name, P.name as position_name, C.name as category_name
                from (sport as S inner join branch as B on S.branch_id = B.id)
                full join position as P on S.id = P.sport_id
                full join category as C on S.id = C.sport_id;
                '''

        cursor.execute(query)
        return self._build_result(cursor)


# if __name__ == '__main__':
#     sport_dao = SportDAO()

#     print(sport_dao.getAllSports())
#     print(sport_dao.getSportById("1"))
#     print(sport_dao.getSportByName("soccer"))
#     print(sport_dao.getSportsByBranch("male"))
