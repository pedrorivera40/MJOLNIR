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
    #ALL NEW

    ## @brief

    def getTeamSportByID(self,tID):
        cursor = self.conn.cursor()
        query = """
                SELECT sport_id
                FROM team
                WHERE id = %s and
                (is_invalid = false or is_invalid is Null);
                """
        cursor.execute(query,(int(tID),))
        result = cursor.fetchone()
        return result

    ## @brief         Gets a specific team's id.
    #
    #        This function uses sport ID and season year to perform a query to the database
    #        that gets the team in the system that matches the given parameters.
    #
    #
    # @param		sID	The ID of the sport of which the team needs to be fetched.
    # @param		tYear	the season year of which the team needs to be fetched
    #
    # @return
    #            The response to the database query
    #            containing the team in the system containing
    #            the matching record for the given parameters
    #

    def getTeamIDByYear(self,sID,tYear): # Returns a Team id based on year
        cursor = self.conn.cursor()
        query = """
                SELECT team.id as team_id
                FROM team
                WHERE sport_id = %s and season_year = %s and
                (team.is_invalid = false or team.is_invalid is Null);
                """
        cursor.execute(query,(int(sID),int(tYear),))
        result = cursor.fetchone()
        return result

    ## @brief         Gets a specific invalid team.
    #
    #        This function uses an ID to perform a query to the database
    #        that gets the invalid team in the system that matches the given ID.
    #
    #
    # @param		tID	The ID of the invalid team which needs to be fetched.
    #
    # @return
    #            The response to the database query
    #            containing the team in the system containing
    #            the matching record for the given ID if invalid
    #

    def getTeamByIDInvalid(self,tID): # Returns a Team record by its id.
        cursor = self.conn.cursor()
        query = """
                SELECT team.id as team_id
                FROM team
                WHERE team.id = %s and
                (team.is_invalid = true);
                """
        cursor.execute(query,(int(tID),))
        result = cursor.fetchone()
        return result

    ## @brief         Gets a specific invalid team.
    #
    #        This function uses an ID to perform a query to the database
    #        that gets the invalid team in the system that matches the given ID.
    #
    #
    # @param		tID	The ID of the invalid team which needs to be fetched.
    #
    # @return
    #            The response to the database query
    #            containing the team in the system containing
    #            the matching record for the given ID if invalid
    #

    def getTeamByYearInvalid(self,sID,tYear): # Returns a Team record by its id.
        cursor = self.conn.cursor()
        query = """
                SELECT team.id as team_id
                FROM team
                WHERE team.sport_id = %s and team.season_year = %s and
                (team.is_invalid = true);
                """
        cursor.execute(query,(int(sID),int(tYear),))
        result = cursor.fetchone()
        return result

    ## @brief         Gets a specific invalid team member entry
    #
    #        This function uses IDs to perform a query to the database
    #        that gets the invalid team member that matches the given IDs.
    #
    #
    # @param		aID	The ID of the athlete of which the record needs to be fetched.
    # @param		tID	The ID of the team of which the record needs to be fetched.
    #
    # @return
    #            the response to the database query
    #            containing the team member in the system containing
    #            the matching record for the given ID if invalid
    #

    def getTeamMemberByIDsInvalid(self,aID,tID):
        cursor = self.conn.cursor()
        query = """
                SELECT team_members.id as team_members_id
                FROM team_members
                WHERE team_id = %s and athlete_id = %s and
                (team_members.is_invalid = true);
                """
        cursor.execute(query,(int(tID),int(aID),))
        result = cursor.fetchone()
        return result
#=============================//GETS//=======================

    ## @brief         Gets all the teams in the system.
    #
    # @return
    #            A list containing the response to the database query
    #            containing all the teams in the system.
    #

    def getAllTeams(self):
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
    ## @brief         Gets all the teams per sport and branch.
    #
    #        This function uses an ID to perform a query to the database
    #        that gets all the teams in the system that match the given ID.
    #
    #
    # @param		sID	The ID of the sport of which teams need to be fetched.
    #
    # @return
    #            A list containing the response to the database query
    #            containing all the teams in the system containing
    #            the matching record for the given ID.
    #

    def getTeams(self,sID):
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

    ## @brief         Gets a specific team.
    #
    #        This function uses an ID to perform a query to the database
    #        that gets the team in the system that matches the given ID.
    #
    #
    # @param		tID	The ID of the team which needs to be fetched.
    #
    # @return
    #            The response to the database query
    #            containing the teams in the system containing
    #            the matching record for the given ID.
    #

    def getTeamByID(self,tID): # Returns a Team record by its id.
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
    ## @brief         Gets all the teams per season and sport.
    #
    #        This function uses an ID and a season year to perform a query to the database
    #        that gets the team in the system that matches the given ID and year.
    #
    #
    # @param		sID	The ID of the sport of which the  team need to be fetched.
    # @param		tYear	the season year of which the the team needs to be fetched
    # @return
    #            the response to the database query
    #            containing all the team in the system containing
    #            the matching record for the given ID and season year.
    #

    def getTeamByYear(self,sID,tYear):
        cursor = self.conn.cursor()
        query = """
                SELECT team.id as team_id, team.sport_id, team.season_year, team.team_image_url, sport.name as sport_name,
                branch.id as branch_id, branch.name as branch_name
                FROM team
                INNER JOIN sport on team.sport_id = sport.id
                INNER JOIN branch on sport.branch_id = branch.id
                WHERE sport.id = %s and team.season_year = %s and
                (team.is_invalid = false or team.is_invalid is Null);
                """
        cursor.execute(query,(int(sID),int(tYear),))
        result = cursor.fetchone()
        return result

    #NEW
    ## @brief         Gets a specific team member entry
    #
    #        This function uses IDs to perform a query to the database
    #        that gets the team member that matches the given IDs.
    #
    #
    # @param		aID	The ID of the athlete of which the record needs to be fetched.
    # @param		tID	The ID of the team of which the record needs to be fetched.
    #
    # @return
    #            the response to the database query
    #            containing the team member in the system containing
    #            the matching record for the given ID.
    #

    def getTeamMemberByIDs(self,aID,tID):
        cursor = self.conn.cursor()
        query = """
                SELECT team_members.id as team_members_id, team_members.team_id, team_members.athlete_id,
                athlete.first_name,athlete.middle_name,athlete.last_names, athlete.number, athlete.profile_image_link
                FROM team_members
                INNER JOIN athlete on team_members.athlete_id = athlete.id
                WHERE team_id = %s and athlete_id = %s and
                (team_members.is_invalid = false or team_members.is_invalid is Null);
                """
        cursor.execute(query,(int(tID),int(aID),))
        result = cursor.fetchone()
        return result

    # NEW
    ## @brief         Gets a team members for a specific team
    #
    #        This function uses an ID to perform a query to the database
    #        that gets the team members that match the given ID.
    #
    #
    # @param		tID	The ID of the team of which the records needs to be fetched.
    #
    # @return
    #            A list containing the response to the database query
    #            containing all the team members in the system containing
    #            the matching record for the given ID.
    #

    def getTeamMembersByID(self,tID):
        cursor = self.conn.cursor()
        query = """
                SELECT team_members.id as team_members_id, team_members.team_id, team_members.athlete_id,
                athlete.first_name,athlete.middle_name,athlete.last_names, athlete.number, athlete.profile_image_link
                FROM team_members
                INNER JOIN athlete on team_members.athlete_id = athlete.id
                WHERE team_id = %s and
                (team_members.is_invalid = false or team_members.is_invalid is Null);
                """
        cursor.execute(query,(int(tID),))
        result = []
        for row in cursor:
            result.append(row)
        return result
#=============================//POST//=======================

    #UPDATED: removed branch parameter. removed tRoster. whatever that was.
    ## @brief         Adds a new team record with the provided information.
    #
    #        This function accepts an ID, season year and image link
    #        to perform a query to the database that adds a new team record
    #        to the system with the provided information.
    #
    #
    # @param		sID	the id of the team to be added
    # @param		tYear	the season year of the team to be added
    # @param		tImageLink	the image link of the team to be added
    #
    # @return
    #            the id of the added team.
    #

    def addTeam(self,sID, tYear,tImageLink): #Adds a new Team record with the information given as parameters, and returns the id of the inserted record.
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
    ## @brief         Adds a new team member record with the provided information.
    #
    #        This function accepts two IDs
    #        to perform a query to the database that adds a new team member record
    #        to the system with the provided information.
    #
    #
    # @param		aID	the id of the athlete to be added
    # @param		tID	the id of the team where the member will belong
    #
    # @return
    #            the id of the added team.
    #

    def addTeamMember(self,aID,tID): # adds someone to ateam
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
    ## @brief         Updates the entry for the team with the given information.
    #
    #        This function accepts an ID, season year and image link and uses them
    #        to update the team record  with the matching ID.
    #
    #
    # @param		tID	the ID of the team to be edited
    # @param		tImageLink	the url for the team image
    #
    # @return
    #            A list containing the response to the database query
    #            containing the matching record for the modified team.
    #

    def editTeam(self,tID,tImageLink): #Edits a team record identified by tID and returns the updated record.
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

    # TODO: Updated... not sure if we should allow Sport/season year update. roster aint a thing.
    ## @brief         Updates the entry for the team with the given information.
    #
    #        This function accepts an ID, season year and image link and uses them
    #        to update the team record  with the matching ID.
    #
    #
    # @param		tID	the ID of the team to be edited
    # @param		tImageLink	the url for the team image
    #
    # @return
    #            A list containing the response to the database query
    #            containing the matching record for the modified team.
    #

    def editTeamByYear(self,sID,tYear,tImageLink): #Edits a team record identified by tID and returns the updated record.
        cursor = self.conn.cursor()
        query = """
                UPDATE team
                SET team_image_url = %s,
                    is_invalid = false
                WHERE sport_id = %s and season_year = %s
                RETURNING
                    id as team_id,
                    sport_id,
                    season_year,
                    team_image_url;
                """
        cursor.execute(query,(str(tImageLink),int(sID),int(tYear),))
        result = cursor.fetchone()
        if not result:
            return result
        #self.commitChanges()
        return result

    #NEW: is this even necessary?
    ## @brief         Updates the entry for the team member with the given information.
    #
    #        This function accepts two IDs and uses them
    #        to update the team member record  with the matching IDs.
    #
    #
    # @param		aID	the athlete id of of the team member entry to be edited
    # @param		tID	the ID of the team where the athlete belongs to
    #
    # @return
    #            A list containing the response to the database query
    #            containing the matching record for the modified team member.
    #

    def editTeamMember(self,aID,tID):
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
    ## @brief         Invalidates a team entry in the database.
    #
    #        This function accepts an ID and uses it to set the valid field
    #        within the database as invalid, this acts as a deletion of the
    #        team entry from the system.
    #
    #
    # @param		tID	The ID of the team which will be invalidated.
    #
    # @return
    #            the id of the invalidated team
    #

    def removeTeam(self,tID): #Invalidates a team record given the team ID and returns the invalidated record.
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

    #updated: removed the
    ## @brief         Invalidates a team entry in the database.
    #
    #        This function accepts an ID and uses it to set the valid field
    #        within the database as invalid, this acts as a deletion of the
    #        team entry from the system.
    #
    #
    # @param		tID	The ID of the team which will be invalidated.
    #
    # @return
    #            the id of the invalidated team
    #

    def removeTeamByYear(self,sID,tYear): #Invalidates a team record given the team ID and returns the invalidated record.
        cursor = self.conn.cursor()
        query = """
                UPDATE team
                SET is_invalid = true
                WHERE sport_id= %s and season_year = %s
                RETURNING id;
                """
        cursor.execute(query,(int(sID),int(tYear),))
        result = cursor.fetchone()
        if not result:
            return result
        #self.commitChanges()
        return result

    #NEW
    ## @brief         Invalidates a team member entry in the database.
    #
    #        This function accepts two IDs and uses them to set the valid field
    #        within the database as invalid, this acts as a deletion of the
    #        team member entry from the system.
    #
    #
    # @param		aID	the ID of the athlete whose membership will be invalidated
    # @param		tID	The ID of the team from which the athlete will be invalidated.
    #
    # @return
    #            the id of the invalidated team member
    #

    def removeTeamMember(self,aID,tID):
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
