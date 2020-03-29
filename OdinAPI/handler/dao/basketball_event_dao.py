from .config.sqlconfig import db_config
from flask import jsonify
import psycopg2

class BasketballEventDAO:

# getAllStatisticsByEventID(eID)//Return all statistics of a Basketball Event event.
# getAllAthleteStatisticsByEventId(eID,aID)//Returns all of an Athlete statistics of a Basketball Event for a given id.
# addStatistics(eID,aID,points,rebounds,assists,steals,blocks,turnovers,fieldGoalPe rcentage,threePointPercentage,freeThrowPercentage)//Adds a Basketball Event record in the database and returns the id of the inserted record.
# editStatistics(eID,aID,points,rebounds,assists,steals,blocks,turnovers,fieldGoalPe rcentage,threePointPercentage,freeThrowPercentage)//Edits a Basketball record in the database for a specific Athlete during an Event by the ids given and returns the updated record.
# removesStatistics(eID, aID)//Invalidates a Basketball Event record on a database and it returns the invalidated record.
# commitChanges()//Commits changes on the database after an insertion or update query.


    def __init__(self):
        connection_url = "dbname={} user={} password={} host ={} ".format(
        db_config['database'],
        db_config['username'],
        db_config['password'],
        db_config['host']
        )
        self.conn = psycopg2.connect(connection_url)


    def getAllStatisticsByEventID(self,eID):
        cursor = self.conn.cursor()
        query = "select A.id,A.first_name,A.middle_name,A.last_names,A.short_bio,A.height_inches,A.study_program,A.date_of_birth,A.school_of_precedence,A.number,A.profile_image_link "\
                "from athlete as A inner join(sport as S inner join(team as T inner join branch as B on T.branch_id = B.id) on S.id = T.sport_id) on A.sport_id = S.id "\
                "where S.id = %s "\
                "and B.name = %s"
        cursor.execute(query,(sID,aBranch,))        
        result = []
        for row in cursor:
            #print(row)
            result.append(row)
        return result       
    
    def getAllAthleteStatisticsByEventID(self,eID,aID):
        cursor = self.conn.cursor()
        query = ""
        cursor.execute(query,(aID,))
        result = cursor.fetchone()
        return result

    #NEW: given an event, get aggregate of team statistics
    def getAllTeamStatisticsByEventID(self,eID):
        cursor = self.conn.cursor()
        query = ""
        cursor.execute(query,(aID,))
        result = cursor.fetchone()
        return result

    #NEW : given team and athlete, return all statistics
    def getAllAthleteStatisticsPerSeason(self,aID,tID):
        cursor = self.conn.cursor()
        query = ""
        cursor.execute(query,(sID,aBranch,))        
        result = []
        for row in cursor:
            #print(row)
            result.append(row)
        return result  
    

    # Need to validate: event exists. athlete belongs to team  that is tied to the event. 
    # needless to say, a bunch changes since these are more complex statistics...
    def addStatistics(self,eID,aID,points,rebounds,assists,steals,blocks,turnovers,fieldGoalPercentage,threePointPercentage,freeThrowPercentage):
        cursor = self.conn.cursor()
        query = ""
        cursor.execute(query,(aFName, aMName, aLName, aBio, aHeight,aStudyProgram,aDateOfBirth, aSchoolOfPrecedence,aNumber,aProfilePictureLink,sID,))
        aID = cursor.fetchone()[0]
        if not aID:
            return aID
        self.commitChanges()
        return aID

    #NEW: add team statistics aggregate passed by parameter
    def addTeamStatistics(self,eID,points,rebounds,assists,steals,blocks,turnovers,fieldGoalPercentage,threePointPercentage,freeThrowPercentage):
        cursor = self.conn.cursor()
        query = ""
        cursor.execute(query,(aFName, aMName, aLName, aBio, aHeight,aStudyProgram,aDateOfBirth, aSchoolOfPrecedence,aNumber,aProfilePictureLink,sID,))
        aID = cursor.fetchone()[0]
        if not aID:
            return aID
        self.commitChanges()
        return aID

    #NEW : aggregate statistics automatically and update
    def addTeamStatistics(self,eid):
        cursor = self.conn.cursor()
        query = ""
        cursor.execute(query,(aFName, aMName, aLName, aBio, aHeight,aStudyProgram,aDateOfBirth, aSchoolOfPrecedence,aNumber,aProfilePictureLink,sID,))
        aID = cursor.fetchone()[0]
        if not aID:
            return aID
        self.commitChanges()
        return aID

    def editStatistics(self,eID,aID,points,rebounds,assists,steals,blocks,turnovers,fieldGoalPercentage,threePointPercentage,freeThrowPercentage):
        #NEW: will also have to update the team statistics
        cursor = self.conn.cursor()
        query = ""
        cursor.execute(query,(aFName, aMName, aLName, aBio, aHeight,aStudyProgram,aDateOfBirth, aSchoolOfPrecedence,aNumber,aProfilePictureLink,sID,aID,))
        result = cursor.fetchone()
        if not result:
            return result
        self.commitChanges()
        return result

    #NEW: edit team statistics. automatically update based on aggregate. 
    def updateTeamStatistics(self,eID):
        cursor = self.conn.cursor()
        query = ""
        cursor.execute(query,(aFName, aMName, aLName, aBio, aHeight,aStudyProgram,aDateOfBirth, aSchoolOfPrecedence,aNumber,aProfilePictureLink,sID,aID,))
        result = cursor.fetchone()
        if not result:
            return result
        self.commitChanges()
        return result
                
    
    def removeStatistics(self,eID,aID):
        cursor = self.conn.cursor()
        query = ""
        cursor.execute(query,(aID,))
        result = cursor.fetchone()[0]
        if not result:
            return result
        self.commitChanges()
        return result

    #NEW : remove team statistics
    def removeTeamStatistics(self,eID,aID):
        cursor = self.conn.cursor()
        query = ""
        cursor.execute(query,(aID,))
        result = cursor.fetchone()[0]
        if not result:
            return result
        self.commitChanges()
        return result

    def commitChanges(self):
        self.conn.commit()


