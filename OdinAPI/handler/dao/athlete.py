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


    def getAthletesBySport(self,sID):
        cursor = self.conn.cursor()
        query = """select A.id,A.first_name,A.middle_name,A.last_names,A.short_bio,A.height_inches,A.study_program,A.date_of_birth,A.school_of_precedence,A.number,A.profile_image_link,S.name as sport_name,P.name as position_name,C.name as category_name
                   from ((athlete as A inner join sport as S on A.sport_id=S.id) full outer join (athlete_position as AP inner join position as P on AP.position_id=P.id) on AP.athlete_id=A.id) full outer join (athlete_category as AC inner join category as C on AC.category_id=C.id) on A.id=AC.athlete_id
                   where S.id = %s
                   and A.is_invalid=false
                """
        cursor.execute(query,(sID,))        
        result = []
        for row in cursor:            
            result.append(row)
        return result       
    
    def getAthleteByID(self,aID):
        cursor = self.conn.cursor()
        query = """select A.id,A.first_name,A.middle_name,A.last_names,A.short_bio,A.height_inches,A.study_program,A.date_of_birth,A.school_of_precedence,A.number,A.profile_image_link,S.name as sport_name,P.name as position_name,C.name as category_name 
                   from ((athlete as A inner join sport as S on A.sport_id=S.id) full outer join (athlete_position as AP inner join position as P on AP.position_id=P.id) on AP.athlete_id=A.id) full outer join (athlete_category as AC inner join category as C on AC.category_id=C.id) on A.id=AC.athlete_id
                   where A.id=%s
                   and A.is_invalid=false
                """
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

    def addAthlete(self,sID,aFName, aMName, aLName, aBio, aHeight,aStudyProgram,aDateOfBirth, aSchoolOfPrecedence,aNumber,aProfilePictureLink,aPositions,aCategories):
        cursor = self.conn.cursor()                
        query = "insert into athlete(first_name,middle_name,last_names,short_bio,height_inches,study_program,date_of_birth,school_of_precedence,number,profile_image_link,sport_id,is_invalid) "\
                "values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,'false') returning id;"
        cursor.execute(query,(aFName, aMName, aLName, aBio, aHeight,aStudyProgram,aDateOfBirth, aSchoolOfPrecedence,aNumber,aProfilePictureLink,sID,))
        
        
        aID = cursor.fetchone()[0]
        if not aID:
            return []#Empty
        
        
        if aPositions != None and aCategories == None:
            query = """select P.id, P.name
                       from position as P
                       where P.sport_id = %s                                          
                    """
            cursor.execute(query,(sID,))            
            
            if not cursor:
                return []

            positions = []            
            for row in cursor:
                positions.append(row)
            if len(positions) != len(aPositions):
                return []

            apIDs = []
            try:
                for position in positions:
                    query = """insert into athlete_position(position_id,athlete_id,is_invalid)
                            values(%s,%s,%s) returning id
                            """
                    cursor.execute(query,(position[0],aID,aPositions[position[1]],))
                    apID = cursor.fetchone()[0]
                    if not apID:
                        return []
                    apIDs.append(apID)
            except:                
                if len(apIDs) != len(positions):
                    return []
            
            
        if aCategories != None and aPositions == None:
            query = """select C.id,C.name
                       from  category as C inner join sport as S on C.sport_id=S.id
                       where S.id = %s                       
                    """
            cursor.execute(query,(sID,))
            
            if not cursor:
                return []
            
            categories = []
            for row in cursor:
                categories.append(row)
            
            if len(categories) != len(aCategories):
                return []
            
            acIDs = []

            try:   
                for category in categories:            
                    query = """insert into athlete_category(athlete_id,category_id,is_invalid)
                            values(%s,%s,%s) returning id
                            """
                    cursor.execute(query,(aID,category[0],aCategories[category[1]],))
                    acID = cursor.fetchone()[0]
                    if not acID:
                        return []
                    acIDs.append(acID)
            except:
                if len(acIDs) != len(categories):
                    return []

        self.commitChanges()
        return aID

    def editAthlete(self,aID,aFName, aMName, aLName, aBio, aHeight,aStudyProgram,aDateOfBirth, aSchoolOfPrecedence,aNumber,aProfilePictureLink,sID,aPositions,aCategories):
        cursor = self.conn.cursor()
        query = """update athlete
                   set first_name = %s,
                       middle_name = %s,
                       last_names = %s,
                       short_bio = %s,
                       height_inches = %s,
                       study_program = %s,
                       date_of_birth = %s,
                       school_of_precedence = %s,
                       number = %s,
                       profile_image_link = %s,
                       sport_id = %s
                   where id = %s 
                   returning first_name,
                        middle_name,
                        last_names,
                        short_bio,
                        height_inches,
                        study_program,
                        date_of_birth,
                        school_of_precedence,
                        number,
                        profile_image_link,
                        sport_id
                """
        cursor.execute(query,(aFName, aMName, aLName, aBio, aHeight,aStudyProgram,aDateOfBirth, aSchoolOfPrecedence,aNumber,aProfilePictureLink,sID,aID,))
        result = cursor.fetchone()
        if not result:
            return []

        if aPositions != None:
            query = """select P.id
                       from position as P inner join sport as S on P.sport_id=S.id
                       where S.id = %s
                       and P.name = %s                    
                    """
            cursor.execute(query,(sID,aPositions,))
            pID = cursor.fetchone()
            print(pID)
            if not pID:
                return []
            
            query = """select AP.id
                       from athlete_position as AP inner join athlete as A on AP.athlete_id=A.id
                       where AP.athlete_id = %s
                    """
            apID = cursor.execute(query,(aID,))
            
            query = """update athlete_position
                       set position_id=%s
                       where id = %s
                       returning id
                    """
            cursor.execute(query,(pID,apID,))
            newPosition = cursor.fetchone()[0]
            if not newPosition:
                return []

        if aCategories != None:
            query = """select C.id
                       from  category as C inner join sport as S on C.sport_id=S.id
                       where S.id = %s
                       and C.name = %s
                    """
            cursor.execute(query,(sID,aCategories,))
            cID = cursor.fetchone()
            if not cID:
                return []

            query = """select AC.id
                       from athlete_category as AC inner join athlete as A on AC.athlete_id=A.id
                       where AC.athlete_id = %s
                    """
            acID = cursor.execute(query,(aID,))
            if not acID:
                return []
            
            query = """update athlete_category
                       set category_id=%s
                       where id=%s returning id
                    """
            cursor.execute(query,(cID,acID,))
            newCategory = cursor.fetchone()[0]
            if not newCategory:
                return []
            
        
        self.commitChanges()
        return result
                
    
    def removeAthlete(self,aID):
        """
        Invalidates an athlete on the database.

        This method accepts the id of the athlete in order
        to set the is_invalid field to true in the database.
        This effectively acts as a removal of the athlete in 
        from the system.
        """
        cursor = self.conn.cursor()
        query = "update athlete "\
                "set is_invalid = 'true' "\
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
