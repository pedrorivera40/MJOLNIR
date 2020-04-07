from .config.sqlconfig import db_config
from flask import jsonify
import psycopg2

class TeamDAO:


#Methods:
# getAllTeams()#Returns a list of all teams.
# getTeams(sID,tBranch) #Returns a Team, given a sport id and branch (M or F).
# getTeamById(tID) # Returns a Team record by its id.
# getTeamByYear(sID,tBranch,tYear) #Returns a team from a given branch for a specific year.
# addTeam(sID,tBranch, tRoster, tYear,tImageLink) #Adds a new Team record with the information given as parameters, and returns the id of the inserted record.
# editTeam(tID,sID,tRoster,tYear,tImageLink) #Edits a team record identified by tID and returns the updated record.
# removeTeam(tID,sID) #Invalidates a team record given the team ID and returns the invalidated record.
# commitChanges()#Commits changes on the database after an insertion or update query.

#NEW: 
# getTeamSportByID(tID): #helper for event result handlers
# getTeamMemberByIDs(aID,tID): # validates if an athlete belongs to a team. returns info.
# addTeamMember(aID,tID): # adds someone to ateam
# editTeamMember(aID,tID): 
# removeTeamMember(aID,tID):
# getTeamMembersByID(tID):

#TODO: Check how this ties to statistics :)
#TODO: queries first, formatting later

    def __init__(self):
        connection_url = "dbname={} user={} password={} host ={} ".format(
        db_config['database'],
        db_config['username'],
        db_config['password'],
        db_config['host']
        )
        self.conn = psycopg2.connect(connection_url)

#=============================//HELPERS//====================

    def getTeamSportByID(self,tID):
        """
        """
        cursor = self.conn.cursor()
        query = """
                SELECT sport_id 
                FROM team
                WHERE team_id = %s
                (is_invalid == false or is_invalid is Null);
                """
        cursor.execute(query,(int(tID),))
        result = cursor.fetchone()
        return result
#=============================//GETS//=======================
   
    def getAllTeams(self):
        """
        Gets all the teams in the system.
            
        Returns:
            A list containing the response to the database query
            containing all the teams in the system.
        """
        cursor = self.conn.cursor()
        query = """
                SELECT team.id as team_id, team.sport_id, team.season_year, team.team_image_url, sport.name as sport_name,
                branch.id as branch_id, branch.name as branch_name
                FROM team
                INNER JOIN sport on team.sport_id = sport.id
                INNER JOIN branch on sport.branch_id = branch.id
                WHERE (team.is_invalid = false or team.is_invalid is Null);
                """
        cursor.execute(query)        
        result = []
        for row in cursor:
            result.append(row)
        return result 

    #EDIT: no longer need branch parameter, part of Sport now. 
    def getTeams(self,sID): 
        """
        Gets all the teams per sport and branch. 

        This function uses an ID to perform a query to the database
        that gets all the teams in the system that match the given ID.

        Args:
            sID: The ID of the sport of which teams need to be fetched.
            
        Returns:
            A list containing the response to the database query
            containing all the teams in the system containing 
            the matching record for the given ID.
        """
        cursor = self.conn.cursor()
        query = """
                SELECT team.id as team_id, team.sport_id, team.season_year, team.team_image_url, sport.name as sport_name,
                branch.id as branch_id, branch.name as branch_name
                FROM team
                INNER JOIN sport on team.sport_id = sport.id
                INNER JOIN branch on sport.branch_id = branch.id
                WHERE sport.id = %s and
                (team.is_invalid = false or team.is_invalid is Null);
                """
        cursor.execute(query,(int(sID),))        
        result = []
        for row in cursor:
            result.append(row)
        return result 

    def getTeamById(self,tID): # Returns a Team record by its id.
        """
        Gets a specific team.

        This function uses an ID to perform a query to the database
        that gets the team in the system that matches the given ID.

        Args:
            tID: The ID of the team which needs to be fetched.
            
        Returns:
            The response to the database query
            containing the teams in the system containing 
            the matching record for the given ID.
        """
        cursor = self.conn.cursor()
        query = """
                SELECT team.id as team_id, team.sport_id, team.season_year, team.team_image_url, sport.name as sport_name,
                branch.id as branch_id, branch.name as branch_name
                FROM team
                INNER JOIN sport on team.sport_id = sport.id
                INNER JOIN branch on sport.branch_id = branch.id
                WHERE team.id = %s and
                (team.is_invalid = false or team.is_invalid is Null);
                """
        cursor.execute(query,(int(tID),))
        result = cursor.fetchone()
        return result

    # EDIT - no longer need branch id
    def getTeamByYear(self,sID,tYear): 
        """
        Gets all the teams per season and sport. 

        This function uses an ID and a season year to perform a query to the database
        that gets the team in the system that matches the given ID and year.

        Args:
            sID: The ID of the sport of which the  team need to be fetched.
            tYear: the season year of which the the team needs to be fetched
        Returns:
            the response to the database query
            containing all the team in the system containing 
            the matching record for the given ID and season year.
        """
        cursor = self.conn.cursor()
        query = """
                SELECT team.id as team_id, team.sport_id, team.season_year, team.team_image_url, sport.name as sport_name,
                branch.id as branch_id, branch.name as branch_name
                FROM team
                INNER JOIN sport on team.sport_id = sport.id
                INNER JOIN branch on sport.branch_id = branch.id
                WHERE sport.id = %s and team.season_year = %s
                (team.is_invalid = false or team.is_invalid is Null);
                """
        cursor.execute(query,(int(sID),int(tYear),))        
        result = cursor.fetchone()
        return result

    #NEW
    def getTeamMemberByIDs(self,aID,tID): 
        """
        Gets a specific team member entry

        This function uses IDs to perform a query to the database
        that gets the team member that matches the given IDs.

        Args:
            aID: The ID of the athlete of which the record needs to be fetched.
            tID: The ID of the team of which the record needs to be fetched.
            
        Returns:
            the response to the database query
            containing the team member in the system containing 
            the matching record for the given ID.
        """
        cursor = self.conn.cursor()
        query = """
                SELECT id as team_member_id, team_id, athlete_id
                FROM team_members
                WHERE team_id = %s and athlete_id = %s and
                (is_invalid = false or is_invalid is Null);
                """
        cursor.execute(query,(int(aID),int(tID),))        
        result = cursor.fetchone()
        return result
    
    # NEW
    def getTeamMembersByID(self,tID):
        """
        Gets a team members for a specific team

        This function uses an ID to perform a query to the database
        that gets the team members that match the given ID.

        Args:
            tID: The ID of the team of which the records needs to be fetched.
            
        Returns:
            A list containing the response to the database query
            containing all the team members in the system containing 
            the matching record for the given ID.
        """
        cursor = self.conn.cursor()
        query = """
                SELECT team_members.id as team_members_id, team_members.team_id, team_members.athlete_id, 
                athlete.id,athlete.first_name,athlete.middle_name,athlete.last_names 
                FROM team_members
                INNER JOIN athlete on team_members.athlete_id = athlete.id
                WHERE team_id = %s and
                (team_members.is_invalid = false or team_members.is_invalid is Null);
                """
        cursor.execute(query,(int(tID),))        
        result = cursor.fetchone()
        return result
#=============================//POST//=======================
    
    #UPDATED: removed branch parameter. removed tRoster. whatever that was.
    def addTeam(self,sID, tYear,tImageLink): #Adds a new Team record with the information given as parameters, and returns the id of the inserted record.
        """
        Adds a new team record with the provided information.

        This function accepts an ID, season year and image link 
        to perform a query to the database that adds a new team record 
        to the system with the provided information.

        Args:
            sID: the id of the team to be added
            tYear: the season year of the team to be added
            tImageLink: the image link of the team to be added
            
        Returns:
            the id of the added team. 
        """
        cursor = self.conn.cursor()
        query = """
                INSERT INTO team(sport_id,season_year,team_image_url,is_invalid)
                VALUES(%s,%s,%s,false) returning id;
                """
        cursor.execute(query,(int(sID),int(tYear),str(tImageLink),))
        tID = cursor.fetchone()[0]
        if not tID:
            return tID
        #self.commitChanges()
        return tID

    #NEW
    def addTeamMember(self,aID,tID): # adds someone to ateam
        """
        Adds a new team member record with the provided information.

        This function accepts two IDs 
        to perform a query to the database that adds a new team member record 
        to the system with the provided information.

        Args:
            aID: the id of the athlete to be added
            tID: the id of the team where the member will belong
            
        Returns:
            the id of the added team. 
        """
        cursor = self.conn.cursor()
        query = """
                INSERT INTO team_members(athlete_id,team_id,is_invalid)
                VALUES(%s,%s,false) returning id;
                """
        cursor.execute(query,(int(aID),int(tID),))
        tmID = cursor.fetchone()[0]
        if not tmID:
            return tmID
        #self.commitChanges()
        return tmID
#=============================//PUTS//=======================

    # TODO: Updated... not sure if we should allow Sport/season year update. roster aint a thing.
    def editTeam(self,tID,tImageLink): #Edits a team record identified by tID and returns the updated record.  
        """
        Updates the entry for the team with the given information.

        This function accepts an ID, season year and image link and uses them 
        to update the team record  with the matching ID.

        Args:
            tID: the ID of the team to be edited
            tImageLink: the url for the team image
            
        Returns:
            A list containing the response to the database query
            containing the matching record for the modified team.
        """
        cursor = self.conn.cursor()
        query = """
                UPDATE team
                SET team_image_url = %s,
                    is_invalid = false
                WHERE id = %s
                RETURNING
                    id as team_id,
                    sport_id, 
                    season_year, 
                    team_image_url;
                """
        cursor.execute(query,(str(tImageLink),int(tID),))
        result = cursor.fetchone()
        if not result:
            return result
        #self.commitChanges()
        return result

    #NEW: is this even necessary?
    def editTeamMember(self,aID,tID): 
        """
        Updates the entry for the team member with the given information.

        This function accepts two IDs and uses them 
        to update the team member record  with the matching IDs.

        Args:
            aID: the athlete id of of the team member entry to be edited
            tID: the ID of the team where the athlete belongs to
            
        Returns:
            A list containing the response to the database query
            containing the matching record for the modified team member.
        """
        cursor = self.conn.cursor()
        query = """
                UPDATE team_members
                SET is_invalid = false
                WHERE athlete_id = %s and team_id = %s
                RETURNING
                    id as team_member_id,
                    athlete_id, 
                    team_id;
                """
        cursor.execute(query,(int(aID),int(tID),))
        result = cursor.fetchone()
        if not result:
            return result
        #self.commitChanges()
        return result
#=============================//DELETE//=======================
     
    #updated: removed the
    def removeTeam(self,tID): #Invalidates a team record given the team ID and returns the invalidated record.  
        """
        Invalidates a team entry in the database.

        This function accepts an ID and uses it to set the valid field
        within the database as invalid, this acts as a deletion of the 
        team entry from the system.

        Args:
            tID: The ID of the team which will be invalidated.
            
        Returns:
            the id of the invalidated team
        """
        cursor = self.conn.cursor()
        query = """
                UPDATE team
                SET is_invalid = true
                WHERE team_id = %s
                RETURNING id;
                """
        cursor.execute(query,(int(tID),))
        result = cursor.fetchone()
        if not result:
            return result
        #self.commitChanges()
        return result

    #NEW
    def removeTeamMember(self,aID,tID):
        """
        Invalidates a team member entry in the database.

        This function accepts two IDs and uses them to set the valid field
        within the database as invalid, this acts as a deletion of the 
        team member entry from the system.

        Args:
            aID: the ID of the athlete whose membership will be invalidated
            tID: The ID of the team from which the athlete will be invalidated.
            
        Returns:
            the id of the invalidated team member
        """
        cursor = self.conn.cursor()
        query = """
                UPDATE team_members
                SET is_invalid = true
                WHERE athlete_id = %s and team_id = %s
                RETURNING id;
                """
        cursor.execute(query,(int(aID),int(tID),))
        result = cursor.fetchone()
        if not result:
            return result
        #self.commitChanges()
        return result
#=============================//OTHER//=======================

    def commitChanges(self):
        self.conn.commit()