from .config.sqlconfig import db_config
from flask import jsonify
import psycopg2

class AthleteDAO:
    def __init__(self):
        connection_url = "dbname={} user={} password={} host ={} ".format(
        db_config['database'],
        db_config['username'],
        db_config['password'],
        db_config['host']
        )
        self.conn = psycopg2.connect(connection_url)


    def getAtheletesBySport(self,sID,aBranch):
        #TODO Still need to implement this function.
        return None
    
    def getAthleteByID(self,aID):
        #TODO Still need to implement this function.
        return None
    
    def getAthleteByName(self,aFName,aMName,aLName):
        #TODO Still need to implement this function.
        return None

    def addAthlete(self,sID, aBranch, aFName, aMname, aLname, aBio, aHeight,aStudyProgram,aDateOfBirth, aSchoolOfPrecedence,aNumber,aProfilePictureLink):
        #TODO Still need to implement this function.
        return None

    def editAthlete(self,sID,aID,aBranch, afName, aMname, aLname, aBio, aHeight,aStudyProgram,aDateOfBirth, aSchoolOfPrecedence,aNumber,aProfilePictureLink):
        #TODO Still need to implement this function.
        return None
    
    def removeAthlete(self,sID,aID):
        #TODO Still need to implement this function.
        return None

    def commitChanges(self):
        #TODO Still need to implement this function.
        return None
