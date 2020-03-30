from .config.sqlconfig import db_config
import psycopg2

class PositionDAO:
    def __init__(self):
        connection_url = "dbname={} user={} password={} host ={} ".format(
            db_config['database'],
            db_config['username'],
            db_config['password'],
            db_config['host']
        )
        self.conn = psycopg2.connect(connection_url)

    def getPositions(self,sID):
        cursor = self.conn.cursor()
        query = """select P.id, P.name
                   from position as P inner join sport as S on P.sport_id = S.id
                   where S.id = %s
                """
        cursor.execute(query,(sID,))
        result = []
        for row in cursor:
            print(row)
            result.append(row)
        return result       
    
    def getPositionByName(self,psName):
        cursor = self.conn.cursor()
        query = """select P.id, P.name
                   from position as P inner join sport as S on P.sport_id = S.id
                   where P.name = %s
                """
        cursor.execute(query,(psName,))
        result = cursor.fetchone()
        return result
    
    def getAthletePositionInSport(self,sID,aID):
        cursor = self.conn.cursor()
        query = """select AP.id,P.id,P.name
                   from athlete_position as AP inner join (position as P inner join sport as S on P.sport_id = S.id) on AP.position_id = P.id
                   where S.id = %s
                   and AP.athlete_id = %s
                """
        cursor.execute(query,(sID,aID,))
        result = cursor.fetchone()
        return result

    def addAthletePosition(self,psID,aID):
        cursor = self.conn.cursor()
        query = """insert into athlete_position(position_id,athlete_id,is_invalid)
                   values (%s,%s,'false') returning id
                """
        cursor.execute(query,(psID,aID,))
        apID = cursor.fetchone()[0]
        if not apID:
            return apID
        self.commitChanges()
        return apID
    
    def editAthletePosition(self,apID,pID,aID):
        cursor = self.conn.cursor()
        query = """update athlete_position
                   set position_id = %s,
                       athlete_id = %s
                   where id = %s
                   returning id,
                             position_id,
                             athlete_id
                """
        cursor.execute(query,(pID,aID,apID,))
        result = cursor.fetchone()
        if not result:
            return result
        self.commitChanges()
        return result
    
    def removeAthletePosition(self,apID):
        cursor = self.conn.cursor()
        query = """update athlete_position
                   set is_invalid = 'true'
                   where id = %s
                   returning id
                """
        cursor.execute(query,(apID,))
        result = cursor.fetchone()[0]
        if not result:
            return result
        self.commitChanges()
        return result
    
    def commitChanges(self):
        self.conn.commit()




