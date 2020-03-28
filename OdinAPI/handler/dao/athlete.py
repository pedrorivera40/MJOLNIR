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
    
    def getAthleteByID(self,aID):
        cursor = self.conn.cursor()
        query = "select A.id,A.first_name,A.middle_name,A.last_names,A.short_bio,A.height_inches,A.study_program,A.date_of_birth,A.school_of_precedence,A.number,A.profile_image_link "\
                "from athlete as A "\
                "where A.id=%s"
        cursor.execute(query,(aID,))
        result = cursor.fetchone()
        return result
    
    def getAthleteByName(self,aFName,aMName,aLName):
        cursor = self.conn.cursor()
        query = None
        if aMName == None:
            query = "select A.id,A.first_name,A.middle_name,A.last_names,A.short_bio,A.height_inches,A.study_program,A.date_of_birth,A.school_of_precedence,A.number,A.profile_image_link "\
                    "from athlete as A "\
                    "where A.first_name = %s "\
                    "and A.last_names = %s"
            cursor.execute(query,(aFName,aLName,))
        else:
            query = "select A.id,A.first_name,A.middle_name,A.last_names,A.short_bio,A.height_inches,A.study_program,A.date_of_birth,A.school_of_precedence,A.number,A.profile_image_link "\
                    "from athlete as A "\
                    "where A.first_name = %s "\
                    "and A.middle_name = %s"\
                    "and A.last_names = %s"
            cursor.execute(query,(aFName,aMName,aLName,))
        result = []
        for row in cursor:
            result.append(row)
        return result

    def addAthlete(self,sID, aBranch, aFName, aMName, aLName, aBio, aHeight,aStudyProgram,aDateOfBirth, aSchoolOfPrecedence,aNumber,aProfilePictureLink):
        cursor = self.conn.cursor()
        query = "insert into athlete(first_name,middle_name,last_names,short_bio,height_inches,study_program,date_of_birth,school_of_precedence,number,profile_image_link,sport_id) "\
                "values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) returning id;"
        cursor.execute(query,(aFName, aMName, aLName, aBio, aHeight,aStudyProgram,aDateOfBirth, aSchoolOfPrecedence,aNumber,aProfilePictureLink,sID,))
        aID = cursor.fetchone()[0]
        if not aID:
            return aID
        self.commitChanges()
        return aID

    def editAthlete(self,sID,aID,aBranch, aFName, aMName, aLName, aBio, aHeight,aStudyProgram,aDateOfBirth, aSchoolOfPrecedence,aNumber,aProfilePictureLink):
        cursor = self.conn.cursor()
        query = "update athlete "\
                "set first_name = %s,"\
                "    middle_name = %s,"\
                "    last_names = %s,"\
                "    short_bio = %s,"\
                "    height_inches = %s,"\
                "    study_program = %s,"\
                "    date_of_birth = %s,"\
                "    school_of_precedence = %s,"\
                "    number = %s,"\
                "    profile_image_link = %s,"\
                "    sport_id = %s"\
                "where id = %s "\
                "returning first_name,"\
                "    middle_name,"\
                "    last_names,"\
                "    short_bio,"\
                "    height_inches,"\
                "    study_program,"\
                "    date_of_birth,"\
                "    school_of_precedence,"\
                "    number,"\
                "    profile_image_link,"\
                "    sport_id"
        cursor.execute(query,(aFName, aMName, aLName, aBio, aHeight,aStudyProgram,aDateOfBirth, aSchoolOfPrecedence,aNumber,aProfilePictureLink,sID,aID,))
        result = cursor.fetchone()
        if not result:
            return result
        self.commitChanges()
        return result
                
    
    def removeAthlete(self,sID,aID):
        cursor = self.conn.cursor()
        query = "update athlete "\
                "set school_of_precedence = 'Simulating Removal in this column' "\
                "where id = %s "\
                "returning id"
        cursor.execute(query,(aID,))
        result = cursor.fetchone()[0]
        if not result:
            return result
        self.commitChanges()
        return result

    def commitChanges(self):
        self.conn.commit()
