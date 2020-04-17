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

        self.conn = psycopg2.connect(connection_url)#Establish a connection with the relational database.


    def getAllAthletes(self):
        """
        Returns all the athletes that are valid in the database.

        Performs a query on the database in order to get all
        valid atheletes in the database. It returns a list of 
        the athletes with their information.

        Returns:
            A list containing all the valid athletes and 
            their information.
        """
        cursor = self.conn.cursor()
        query = """select A.id,A.first_name,A.middle_name,A.last_names,A.short_bio,A.height_inches,A.study_program,A.date_of_birth,A.school_of_precedence,A.number,A.year_of_study,A.years_of_participation,A.profile_image_link,S.name as sport_name,B.name
                   from athlete as A inner join sport as S on A.sport_id=S.id inner join branch as B on S.branch_id = B.id
                   where A.is_invalid=false
                """

        try:
            cursor.execute(query)
            result = []
            for row in cursor:
                result.append(row)
            return result
        except:
            return [] 

    
    def getAthletesBySport(self,sID):
        """
        Returns all the athletes that participate in a sport by
        the id given.

        Performs a query on the database in order to get all
        valid atheletes in the database by using the id of the 
        sport given. It returns a list of the athletes with their 
        information including their positions and categories if
        they have them in the sport being fetched for.

        Args:
            sID: The id of the sport that has participant athletes.
        Returns:
            A list containing all the athletes and their  
            information that participate in the sport given
            identified by the sport's id.

        """
        cursor = self.conn.cursor()
        if not self.sportExists(cursor,sID):
            return []

        query = """select A.id
                   from athlete as A inner join sport as S on A.sport_id=S.id
                   where S.id = %s
                   and A.is_invalid=false
                """
        try:
            cursor.execute(query,(sID,))        
            result = []#Will hold the list with athlete records.
            aids = []#List of the ids of the athletes fetched in the query above.
            for row in cursor:
                aids.append(row[0])#Add the ids of the participant athletes in the sport
            for aid in aids:
                result.append(self.getAthleteByID(aid)) #Call this function in order to get the information of the athletes.                       
            return result
        except:
            return "A problem ocurred when fetching the athletes of a sport."
    
    def getAthleteByID(self,aID):
        """
        Gets a single athlete in the database by the 
        id of the athlete given.

        Performs a query on the database in order to fetch
        a valid athlete in the database by the id given.

        Args:
            aID: The id of the athlete to be fetched.
        Returns:
            A list containing the information of the athlete in 
            the database that has the id given.
        """

        cursor = self.conn.cursor()
        query = """select A.id,A.first_name,A.middle_name,A.last_names,A.short_bio,A.height_inches,A.study_program,A.date_of_birth,A.school_of_precedence,A.number,A.year_of_study,A.years_of_participation,A.profile_image_link,S.name as sport_name,B.name,P.name as position_name,AP.is_invalid,C.name as category_name,AC.is_invalid
                   from ((athlete as A inner join sport as S on A.sport_id=S.id inner join branch as B on S.branch_id=B.id) full outer join (athlete_position as AP inner join position as P on AP.position_id=P.id) on AP.athlete_id=A.id) full outer join (athlete_category as AC inner join category as C on AC.category_id=C.id) on A.id=AC.athlete_id
                   where A.id=%s
                   and A.is_invalid=false
                """
        try:
            cursor.execute(query,(aID,))
            result = cursor.fetchall()            
            return result
        except:
            return "A problem ocurred when fethching the athlete."    
  

    def addAthlete(self,sID,aFName, aMName, aLName, aBio, aHeight,aStudyProgram,aDateOfBirth, aSchoolOfPrecedence,aNumber,aYearOfStudy,aYearsOfParticipation,aProfilePictureLink):
        """
        Adds a new athlete into the database with the information given.

        Uses the arguments given in order to perform an insert query on 
        the database.Then it returns the id of the newly added athlete in
        the datase.

        Args:
            sID: The id of the sport in which the athlete will participate.
            aFName: First name of the athlete
            aMName: Middle name of the athlete
            aLName: Last name of the athlete
            aBio: Short bio of the athlete
            aHeight:Height of the athlete in inches
            aStudyProgram: Study Program of the athlete
            aDateOfBirth: Data of birth of the athlete.
            aSchoolOfPrecedence:School of Precedence of the athlete.
            aNumber: Number of the athlete in the sport.
            aYearOfStudy: Number of years the athlete has been studying.
            aYearsOfParticipation: Number of years the athlete has participated in the sport.
            aProfilePictureLink: Link for the image of the athlete profile
        Returns:
            The id of the newly added athlete.
        """
        
        cursor = self.conn.cursor() 
        if not self.sportExists(cursor,sID):
            return 'Sport does not exist'
    
        query = "insert into athlete(first_name,middle_name,last_names,short_bio,height_inches,study_program,date_of_birth,school_of_precedence,number,year_of_study,years_of_participation,profile_image_link,sport_id,is_invalid) "\
                "values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,'false') returning id;"
        try:
            cursor.execute(query,(aFName, aMName, aLName, aBio, aHeight,aStudyProgram,aDateOfBirth, aSchoolOfPrecedence,aNumber,aYearOfStudy,aYearsOfParticipation,aProfilePictureLink,sID,))       
            
            aID = cursor.fetchone()[0]
            if not aID:
                return 'Insert query failed'           
            
            self.commitChanges()
            return aID
        except:
            return "A problem ocurred when inserting the athlete."

    def addAthleteWithPosition(self,sID,aFName, aMName, aLName, aBio, aHeight,aStudyProgram,aDateOfBirth, aSchoolOfPrecedence,aNumber,aYearOfStudy,aYearsOfParticipation,aProfilePictureLink,aPositions):
        """
        Add a new athlete with their positions in a sport
        into the database with the information given.

        Uses the arguments given in order to perform an insert query on 
        the database.Then it returns the id of the newly added athlete in
        the datase.

        Args:
            sID: The id of the sport in which the athlete will participate.
            aFName: First name of the athlete
            aMName: Middle name of the athlete
            aLName: Last name of the athlete
            aBio: Short bio of the athlete
            aHeight:Height of the athlete in inches
            aStudyProgram: Study Program of the athlete
            aDateOfBirth: Data of birth of the athlete.
            aSchoolOfPrecedence:School of Precedence of the athlete.
            aNumber: Number of the athlete in the sport.
            aYearOfStudy: Number of years the athlete has been studying.
            aYearsOfParticipation: Number of years the athlete has participated in the sport.
            aProfilePictureLink: Link for the image of the athlete profile.
            aPositions: A dictionary containing the positions of the athelete in 
                        a sport given.
        Returns:
            The id of the newly added athlete.
        """
        cursor = self.conn.cursor() 
        if not self.sportExists(cursor,sID):
            return 'Sport does not exist'
        
        query = """insert into athlete(first_name,middle_name,last_names,short_bio,height_inches,study_program,date_of_birth,school_of_precedence,number,year_of_study,years_of_participation,profile_image_link,sport_id,is_invalid)
                   values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,'false') returning id;
                """
        cursor.execute(query,(aFName, aMName, aLName, aBio, aHeight,aStudyProgram,aDateOfBirth, aSchoolOfPrecedence,aNumber,aYearOfStudy,aYearsOfParticipation,aProfilePictureLink,sID,))
        
        
        aID = cursor.fetchone()[0]
        if not aID:
            return 'The insert query failed'
        
        
        #Get all positions for a given sport.
        query = """select P.id, P.name
                    from position as P
                    where P.sport_id = %s                                          
                """
        cursor.execute(query,(sID,))             
        

        positions = []#List of the positions for a sport         
        for row in cursor:
            positions.append(row)
        if not positions:
            return 'This sport does not have positions.'

        if len(positions) != len(aPositions):
            return 'Not all positions for the sport where given.'
        
        try:
            #This query is used to insert the athlete position in the database.
            query = """insert into athlete_position(position_id,athlete_id,is_invalid)
                        values(%s,%s,%s) returning id
                        """
            for position in positions:                                  
                cursor.execute(query,(position[0],aID,aPositions[position[1]],))
                apID = cursor.fetchone()[0]
                if not apID:
                    return 'Insertion query for athlete position failed.'                
        except:                
            return 'The names of the positions given are incorrect.'

        self.commitChanges()
        return aID

    def addAthleteWithCategory(self,sID,aFName, aMName, aLName, aBio, aHeight,aStudyProgram,aDateOfBirth, aSchoolOfPrecedence,aNumber,aYearOfStudy,aYearsOfParticipation,aProfilePictureLink,aCategories):
        """
        Add a new athlete with their categories in a sport
        into the database with the information given.

        Uses the arguments given in order to perform an insert query on 
        the database.Then it returns the id of the newly added athlete in
        the datase.

        Args:
            sID: The id of the sport in which the athlete will participate.
            aFName: First name of the athlete
            aMName: Middle name of the athlete
            aLName: Last name of the athlete
            aBio: Short bio of the athlete
            aHeight:Height of the athlete in inches
            aStudyProgram: Study Program of the athlete
            aDateOfBirth: Data of birth of the athlete.
            aSchoolOfPrecedence:School of Precedence of the athlete.
            aNumber: Number of the athlete in the sport.
            aYearOfStudy: Number of years the athlete has been studying.
            aYearsOfParticipation: Number of years the athlete has participated in the sport.
            aProfilePictureLink: Link for the image of the athlete profile.
            aCategories: A dictionary containing the categories of the athelete in 
                        a sport given.
        Returns:
            The id of the newly added athlete.
        """

        cursor = self.conn.cursor() 
        
        if not self.sportExists(cursor,sID):
            return 'Sport does not exist'
        
        query = """insert into athlete(first_name,middle_name,last_names,short_bio,height_inches,study_program,date_of_birth,school_of_precedence,number,year_of_study,years_of_participation,profile_image_link,sport_id,is_invalid) 
                   values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,'false') returning id;
                """   
        cursor.execute(query,(aFName, aMName, aLName, aBio, aHeight,aStudyProgram,aDateOfBirth, aSchoolOfPrecedence,aNumber,aYearOfStudy,aYearsOfParticipation,aProfilePictureLink,sID,))
        
        
        aID = cursor.fetchone()[0]
        if not aID:
            return 'The insert query failed'
        
        #Get the categories of a sport
        query = """select C.id,C.name
                   from  category as C inner join sport as S on C.sport_id=S.id
                   where S.id = %s                       
                """
        cursor.execute(query,(sID,))            
        
        categories = []#List containing the categories of a sport.
        for row in cursor:
            categories.append(row)

        if not categories:
            return 'This sport does not have categories.'
        
        if len(categories) != len(aCategories):
            return "Not all the categories for the sport where given."           

        try:   
            for category in categories:            
                query = """insert into athlete_category(athlete_id,category_id,is_invalid)
                           values(%s,%s,%s) returning id
                        """
                cursor.execute(query,(aID,category[0],aCategories[category[1]],))
                acID = cursor.fetchone()[0]
                if not acID:
                    return 'Insert query for the athlete category failed.'                    
        except:
            return 'The names of the categories given for the sport are incorrect.'

        self.commitChanges()
        return aID


    def editAthlete(self,aID,aFName, aMName, aLName, aBio, aHeight,aStudyProgram,aDateOfBirth, aSchoolOfPrecedence,aNumber,aYearOfStudy,aYearsOfParticipation,aProfilePictureLink,aPositions,aCategories):
        """
        Updates an existing athlete in the database
        including their positions and categories in
        the sport they participate with the arguments
        given.

        Uses the arguments given in order to perform an update query on 
        the database with the id of the athlete given.Then it returns
        the id of the newly updated athlete in the datase.

        Args:
            aID: The id of athlete to be updated.
            aFName: First name of the athlete
            aMName: Middle name of the athlete
            aLName: Last name of the athlete
            aBio: Short bio of the athlete
            aHeight:Height of the athlete in inches
            aStudyProgram: Study Program of the athlete
            aDateOfBirth: Data of birth of the athlete.
            aSchoolOfPrecedence:School of Precedence of the athlete.
            aNumber: Number of the athlete in the sport.
            aYearOfStudy: Number of years the athlete has been studying.
            aYearsOfParticipation: Number of years the athlete has participated in the sport.
            aProfilePictureLink: Link for the image of the athlete profile.
            aPositions: A dictionary containing the positions of the athelete in 
                        a sport given.
            aCategories: A dictionary containing the categories of the athelete in 
                         a sport given.
        Returns:
            The id of the newly updated athlete.
        """
        
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
                       year_of_study = %s,
                       years_of_participation = %s,
                       profile_image_link = %s                       
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
                        year_of_study,
                        years_of_participation,
                        profile_image_link,
                        sport_id
                """
        cursor.execute(query,(aFName, aMName, aLName, aBio, aHeight,aStudyProgram,aDateOfBirth, aSchoolOfPrecedence,aNumber,aYearOfStudy,aYearsOfParticipation,aProfilePictureLink,aID,))
        result = cursor.fetchone()
        if not result:
            return "Athlete update failed"

        #If the positions were given then the positions will be updated.
        if aPositions and not aCategories:

            #Get all positions for a given sport.
            query = """select P.id, P.name
                        from position as P
                        where P.sport_id = %s                                          
                    """
            cursor.execute(query,(result[12],))             
            

            positions = []#List of positions in a sport.            
            for row in cursor:
                positions.append(row)

            if not positions:
                return 'This sport does not have positions.'

            if len(positions) != len(aPositions):
                return 'Not all positions for the sport where given.'         

            try:            
                query = """update athlete_position
                        set is_invalid=%s
                        where position_id=%s
                        and athlete_id=%s
                        returning id
                        """
                for position in positions:
                    cursor.execute(query,(aPositions[position[1]],position[0],aID))
                    apID = cursor.fetchone()[0]
                if not apID:
                    return 'Athlete position update failed.' 
            except:
                return 'Was given wrong names for the positions.'
                
        #If the categories were given then the categories of the athlete will be udpated.
        if aCategories and not aPositions:

            #Get all categories of a given sport.
            query = """select C.id,C.name
                       from  category as C inner join sport as S on C.sport_id=S.id
                       where S.id = %s                       
                    """
            cursor.execute(query,(result[10],))            
        
            categories = []#List containing the categories of a sport
            for row in cursor:
                categories.append(row)

            if not categories:
                return 'This sport does not have categories.'
            
            if len(categories) != len(aCategories):
                return "Not all the categories for the sport where given." 
                
            try:
                query = """update athlete_category
                        set is_invalid=%s
                        where category_id=%s
                        and athlete_id=%s
                        returning id
                        """
                for category in categories:
                    print(category[0])
                    print(aCategories[category[1]])
                    cursor.execute(query,(aCategories[category[1]],category[0],aID,))
                    acID = cursor.fetchone()[0]
                    if not acID:
                        return "Athlete category update failed."        
            except:
                return "The name of the categories given for the sport are incorrect."
            
        
        self.commitChanges()
        return aID
                
    
    def removeAthlete(self,aID):
        """
        Invalidates an athlete on the database.

        This method accepts the id of the athlete in order
        to set the is_invalid field to true in the database.
        This effectively acts as a removal of the athlete in 
        from the system.

        Args:
            aID: The id of the athlete to invalidate.

        Returns:
            The id of the updated athlete record
        """
        
        cursor = self.conn.cursor()
        query = """update athlete
                   set is_invalid=true 
                   where id=%s
                   returning id;
                """
        cursor.execute(query,(aID,))
        aid = cursor.fetchone()[0]
        if not aid:
            return aid
        self.commitChanges()
        return aid

    def sportExists(self,cursor,sID):
        """
        Confirms the existance of a sport by the sport id
        given.

        Performs a simple fetch query to determine if 
        the sport given exists.

        Args:
            cursor: Cursor of the connection
            sID: The id of the sport being confirmed
        Returns:
            True if the sport exists in the database, 
            false otherwise.
        """
        exists = True
        query = """select id
                   from sport 
                   where id=%s
                """
        try:
            cursor.execute(query,(sID,))
            if not cursor.fetchone():
                exists = False
            return exists
        except:
            return "A problem ocurred when verifying the sport."

    #This function migh be used later.
    def _athleteExists(self,cursor,aID):
        exists = True
        query = """select id
                   from athlete
                   where id=%s
                   and is_invalid=false
                """
        cursor.execute(query,(aID,))
        if not cursor.fetchone():
            exists = False
        return exists
    
    def getAthleteSportByID(self,aID):
        """
        Returns the id of the sport in which the 
        athlete participates.

        Performs a simple fetch query to return the id
        of the sport in which the athlete participates.

        Args:
            aID: The id of the athlete.
        Returns:
            The id of the sport in which the athlete
            participates.
        """
        cursor = self.conn.cursor()
        query = """select sport_id
                   from athlete
                   where id=%s
                   and is_invalid=false
                """
        try:
            cursor.execute(query,(aID,))
            result = cursor.fetchone()
            return result
        except Exception as e:
            return "Problem ocurred when fetching the sport id of an athlete." + str(e) 

    def commitChanges(self):
        """
        Commits the changes done on the database after
        insertion and update queries have been done on the
        database.
        
        Uses the connection created when this AthleteDAO was
        instantiated to commit the changes performed on the datasase
        after insertion and update queries. 
        """
        self.conn.commit()
