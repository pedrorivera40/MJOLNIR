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
        #TODO: Implementation of function
        return None
    
    def getPositionByName(self,psName):
        #TODO: Implementation of function
        return None
    
    def getPositionByAID(self,sID,aID):
        #TODO: Implementation of function
        return None

    def addPosition(self,sID,aID,psName):
        #TODO: Implementation of function
        return None
    
    def editPosition(self,pID,sID,aID,psName):
        #TODO: Implementation of function
        return None
    
    def removePosition(self,pID,sID,aID):
        #TODO: Implementation of function
        return None
    
    def commitChanges(self):
        self.conn.commit()




