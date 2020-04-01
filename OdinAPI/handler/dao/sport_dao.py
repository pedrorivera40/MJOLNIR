from config.sqlconfig import db_config
from flask import jsonify
import psycopg2


# TODO -> Add class documentation.
class SportDAO:

    # Initialize postgreSQL db connection with psycopg2.
    def __init__(self):
        connection_url = "dbname={} user={} password={} host ={} ".format(
            db_config['database'],
            db_config['username'],
            db_config['password'],
            db_config['host']
        )
        print(connection_url)
        self.conn = psycopg2.connect(connection_url)

    # Returns a list of all the Sport records in the database.
    def getAllSports(self):
        cursor = self.conn.cursor()

        # Get sport names and images for all valid sports.
        query = '''
                    select S.id, S.name, S.sport_image_url
                    from sport as S
                    where S.is_invalid = false;
                '''
        cursor.execute(query)

        result = []
        for row in cursor:
            result.append(row)

        return result

    # def getSportsByBranch(self, branch):
    #     cursor = self.conn.cursor()

    #     # Get all valid sport names and images for all valid sports given its branch.
    #     query = '''
    #                 select S.id, S.name, S.sport_image_url
    #                 from (sport as S) natural inner join
    #                 where S.is_invalid = false
    #                 and branch = %s;
    #             '''

    #     cursor.execute(query, (branch,))

    #     result = []
    #     for row in cursor:
    #         print(row)
    #         result.append(row)

    #     return result

    # Returns a specific Sport record that matches the sID given as parameter.
    def getSportById(self, sport_id):
        cursor = self.conn.cursor()

        # Get a sport name and image url given its id.
        query = '''
                    select S.id, S.name, S.sport_image_url
                    from sport as S
                    where S.is_invalid = false
                    and S.id = %s;
                '''

        cursor.execute(query, (sport_id,))

        return cursor.fetchone()

    # Returns a specific Sport record that matches the name of the sport given as parameter.
    def getSportByName(self, sport_name):
        cursor = self.conn.cursor()

        # Get a sport name and image url given its sport name.
        query = '''
                    select S.id, S.name, S.sport_image_url
                    from sport as S
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
    # print(sport_dao.getSportsByBranch("Masculino"))
