from flask import jsonify

from .dao.team_dao import TeamDAO
from .dao.athlete_dao import AthleteDAO

class BaseballEventHandler(EventResultHandler):
    
    # getAllTeams()//Instantiates a Team DAO in order to complete the desired get request and it returns a JSON with the desired information or with an error message.

    # getTeam(sID,tBranch) //Instantiates a Team DAO in order to complete the desired get request and it returns a JSON with the desired information or with an error message.

    # getTeamById(tID) //Instantiates a Team DAO in order to complete the desired get request and it returns a JSON with the desired information or with an error message.

    # getTeamByYear(sID,tBranch,tYear) //Instantiates a Team DAO in order to complete the desired get information or with an error message.

    # addTeam(sID,tBranch, tRoster, tYear) //Instantiates a Team DAO in order to complete the desired post request and it returns a JSON with either a confirmation or error message.

    # editTeam(tID,sID,tRoster,tYear)//Instantiates a Team DAO in order to complete the desired put request and it returns a JSON with either a confirmation or error message.

    # removeTeam(tID,sID)//Instantiates a Team DAO in order to complete the desired put request and it returns a JSON with either a confirmation or error message.

    # mapTeamToDict(record)//Maps a Team record to a dictionary and returns it.

    #NEW:
    # def getTeamSportByID(self, tID): #helper for event result handlers (NOT NEEDED)

    # def getTeamMemberByIDs(self, aID,tID): # validates if an athlete belongs to a team. returns info.
    # def addTeamMember(self, aID,tID): # adds someone to ateam
    # def editTeamMember(self, aID,tID): 
    # def removeTeamMember(self, aID,tID):
    # def getTeamMembersByID(self, tID):


#===========================//DICTIONARY MAPPERS//==================================
    #TODO: need to label somehow the jsonify/request in the route so that it has the sport?
    #NEW (name): basic team info
    def mapTeamToDict(self,record):

        # "team":{
        #     "team_id":1,
        #     "sport_id":1,
        #     "sport_name":"SampleSport",
        #     "season_year":"2020",
        #     "team_image_url":"www.google.com"
        #     "branch_id":2,
        #     "branch_name":"Femenina"

        team_info = {}

        team_info['team_id']=record[0]
        team_info['sport_id']=record[1]
        team_info['season_year']=record[2]
        team_info['team_image_url']=record[3]
        team_info['sport_name']=record[4]
        team_info['branch_id']=record[5]
        team_info['branch_name']=record[6]

        
        
        result = dict(team_info = team_info)
        return result

    #NEW
    def mapTeamMembersToDict(self,record):

        # {
        # "team_members":[
        #     {
        #         "team_member_id":1,
        #         "first_name"="Bruce",
        #         "middle_name"="Batman",
        #         "last_names"="Wayne",
        #         "number"=27,
        #         "profile_image_link"="www.google.com",
        #     },
        #     {
        #         "team_member_id":2,
        #         "first_name"="Clark",
        #         "middle_name"="Superman",
        #         "last_names"="Kent",
        #         "number"=3,
        #         "profile_image_link"="www.google.com",
        #     },
        #     }
        #     ]
        # }

        team_members = []

        for team_member in record:
            team_members.append(dict(
                team_members_id = record[0], 
                team_id = record[1], 
                athlete_id = record[2], 
                first_name = record[3], 
                middle_name = record[4], 
                last_names = record[5], 
                number = record[6], 
                profile_image_link = record[7]
                ))

        result = dict(team_members = team_members)
        return result


    # DEPRECATED, DONT NEED ALL TOGETHER DUE TO DIFFERENT VIEWS
    # # Updated: this will be so that it has the team AND the members
    # def mapTeamToDict(self,record):
        
    #     # This one will have the TEAM info first and then the info of each member

    #     ## WHAT IT RETURNS:
    #     # {
    #     # "team":{
    #     #     "team_id":1,
    #     #     "sport_id":1,
    #     #     "sport_name":"SampleSport",
    #     #     "season_year":"2020",
    #     #     "team_image_url":"www.google.com"
    #     #     "branch_id":2,
    #     #     "branch_name":"Femenina"
    #     # }
    #     # "team_members":[
    #     #     {
    #     #         "team_member_id":1,
    #     #         "first_name"="Bruce",
    #     #         "middle_name"="Batman",
    #     #         "last_names"="Wayne",
    #     #         "number"=27,
    #     #         "profile_image_link"="www.google.com",
    #     #     },
    #     #     {
    #     #         "team_member_id":2,
    #     #         "first_name"="Clark",
    #     #         "middle_name"="Superman",
    #     #         "last_names"="Kent",
    #     #         "number"=3,
    #     #         "profile_image_link"="www.google.com",
    #     #     },
    #     #     }
    #     #     ]
    #     # }

    #     #  SELECT team.id as team_id, team.sport_id, team.season_year, team.team_image_url, sport.name as sport_name,
    #     #         branch.id as branch_id, branch.name as branch_name
    #     # SELECT team_members.id as team_members_id, team_members.team_id, team_members.athlete_id, 
    #     #         athlete.id,athlete.first_name,athlete.middle_name,athlete.last_names, athlete.number, athlete.profile_image_link

    #     team_info = {}
    #     team_info['team_id']=record[0]
    #     team_info['sport_id']=record[1]
    #     team_info['season_year']=record[2]
    #     team_info['team_image_url']=record[3]
    #     team_info['sport_name']=record[4]
    #     team_info['branch_id']=record[5]
    #     team_info['branch_name']=record[6]
   
    #     team_members = []

    #     for team_member in record:
    #         team_members.append(dict(
    #             team_members_id = record[0], 
    #             team_id = record[1], 
    #             athlete_id = record[2], 
    #             first_name = record[3], 
    #             middle_name = record[4], 
    #             last_names = record[5], 
    #             number = record[6], 
    #             profile_image_link = record[7]
    #             ))
        
    #     result = dict()
    #     return result

    #===========================//HANDLERS//==================================
    #===========================//I.GETS//====================================

    # Is this even necessary?? Probably not, no tenemos un view que pida todos los teams del sistema....
    # gets all the information...
    def getAllTeams(self): 
        """
        Gets all the teams in the system. 

        Calls the TeamDAO to get team entries and maps the result
        to a JSON that contains all the teams in the system. That
        JSON object is then returned.
            
        Returns:
            A JSON containing all the teams in the system.
        """
        try:
            dao = TeamDAO()
            result = dao.getAllTeams()
            if not result:
                return jsonify(Error = "Teams not found."),404
            mappedResult =[]
            for team in result:
                mappedResult.append(self.mapTeamBasicToDict(team))
        except:
            return jsonify(ERROR="Unable to verify team from DAO."), 500
        
        return jsonify(Teams = mappedResult)

    # TODO: clear up this one, very confused as to what the purpose was...there is more than one team per branch and sport.
    # TODO: maybe repurpose as getTeamsBySport(self,sID)
    # I think it might just have been a typo...since there's a DAO for getTeams that does the same
    # I assume the get team also returns the members, as in, it will return ALL the team info
    #updated: branch not needed
    def getTeams(self,sID): 
        """
        Gets all the teams in the system that match the given sport id. 

        Calls the TeamDAO to get team entries and maps the result
        to a JSON that contains all the teams in the system that match the sport ID. That
        JSON object is then returned.

        Args:
            sID: the ID of the sport of which the teams will be returned
            
        Returns:
            A JSON containing all the teams in the system for that sport.
        """
        try:
            #TODO: validate sport
            pass
        except:
            return jsonify(ERROR="Unable to verify sport from DAO."), 500

        try:
            dao = TeamDAO()
            result = dao.getTeams(sID)
            if not result:
                return jsonify(Error = "Teams not found with sport id:{}.".format(sID)),404
            mappedResult =[]
            for team in result:
                mappedResult.append(self.mapTeamBasicToDict(team))
        except:
            return jsonify(ERROR="Unable to verify team from DAO."), 500
        
        return jsonify(Teams = mappedResult)

    # same info as getTeam, but different query
    def getTeamByID(self,tID): 
        """
        Gets the team in the system that matches the given team id.  

        Calls the TeamDAO to get the team entry and its team members and maps the result
        to a JSON that contains the team in the system that matches the team ID. 
        That JSON object is then returned.

        Args:
            tID: the ID of the team which will be returned
            
        Returns:
            A JSON containing the team and its members.
        """
        #it's a get, so tID validation is just if it exists as a valid entry

        #GET TEAM
        try:
            dao = TeamDAO()
            result = dao.getTeamByID(tID)
            if not result:
                return jsonify(Error = "Team not found with id:{}.".format(tID)),404
            mappedResult = self.mapTeamToDict(result)
        except:
            return jsonify(ERROR="Unable to verify team from DAO."), 500
        
        #get members
        #TODO: case of team with no members
        try:
            result_members = dao.getTeamMembersByID(tID)
            if not result_members:
                #TODO: team has no members
                pass
            mappedResult = self.mapTeamToDict(result_team,result_members)
        except:
            return jsonify(ERROR="Unable to verify team members from DAO."), 500
        return jsonify(Team = mappedResult)

    # this one would be general team information, similar to get all teams but filtered by season
    #updated: dont need branch
    def getTeamByYear(self,sID,tYear):
        """
        Gets the team in the system that matches the given sport and season year.  

        Calls the TeamDAO to get the team entry and its team members and maps the result
        to a JSON that contains the team in the system that matches the sport and season. 
        That JSON object is then returned.

        Args:
            sID: the ID of the sport of which the team will be returned
            tYear: the season year from which the team will be returned
            
        Returns:
            A JSON containing the team and its members.
        """
        #it's a get, so tID validation is just if it exists as a valid entry
        try:
            #TODO: validate sport
            #TODO: do we validate year? prob not, just an int. 
            pass
        except:
            return jsonify(ERROR="Unable to verify sport from DAO."), 500

        #get team
        try:
            dao = TeamDAO()
            result_team = dao.getTeamByYear(sID,tYear)
            if not result_team:
                return jsonify(Error = "Team not found with id:{}.".format(tID)),404
        except:
            return jsonify(ERROR="Unable to verify team from DAO."), 500

        #get members
        #TODO: case of team with no members
        try:
            tID = result_team[0]
            result_members = dao.getTeamMembersByID(tID)
            if not result_members:
                #TODO: team has no members
                pass
            mappedResult = self.mapTeamToDict(result_team,result_members)
        except:
            return jsonify(ERROR="Unable to verify team members from DAO."), 500
        return jsonify(Team = mappedResult)

    # TODO: remove, unnecesary handler
    #NEW: def not necessary, the dao is more of a helper...
    # def getTeamMemberByIDs(self, aID,tID): 
    #     """
    #     Gets the team member in the system that matches the given ids.  

    #     Calls the TeamDAO to get the team member entry and maps the result
    #     to a JSON that contains the team member in the system that matches the ids. 
    #     That JSON object is then returned.

    #     Args:
    #         aID: the ID of the athlete of which the team member entry will be returned
    #         tID: the ID of the team of which the team member entry will be returned
            
    #     Returns:
    #         A JSON containing the team member. 
    #     """
    #     #it's a get, so tID validation is just if it exists as a valid entry
    #     try:
    #         #TODO: validate athlete (?)
    #         #TODO: validate team (?)
    #         pass
    #     except:
    #         return jsonify(ERROR="Unable to verify sport from DAO."), 500

    #     try:
    #         dao = TeamDAO()
    #         result = dao.getTeamMemberByIDs(aID,tID)
    #         if not result:
    #             return jsonify(Error = "Team member not found with athlete id:{} and team id:{}.".format(aID,tID)),404
    #         mappedResult = self.mapTeamToDict(result)
    #     except:
    #         return jsonify(ERROR="Unable to verify team member from DAO."), 500
    #     return jsonify(Teams = mappedResult)
    
    # TODO: check if this is dupliacted by getTeam. most likely is. 
    #NEW: is it necessary? also part of get team...
    def getTeamMembersByID(self, tID):
        return
    #===========================//II.POSTS//====================================
    #update: image link was missing?
    def addTeam(self,sID,tYear,tImageLink,tRoster): 
        """
        creates a team and adds members to it...
        need to ge tthe id of the created team to form relationship
        """
        # Alternative:
        # sport_id = attributes['sport_id']
        # season_year = attributes['season_year']
        # team_image_url = attributes['team_image_url']
        # team_members = attributes['team_members']
        
        # Validate Avoid Duplication Team
        try:
            dao = TeamDAO()
            if dao.getTeamByYear(sID,tYear):
                return jsonify(Error = "Team already exists for Sport ID:{} and Season Year:{}".format(sID,tYear)),400
        except:
            return jsonify(ERROR="Unable to verify Team from DAO."), 500
         
        #TODO: Validate Existing Duplicate, convert to update (need to create new DAO function)
        #TODO: Validate Sport (already done by validatig the athlete?)
        #Done: Validate each athlete and their sport (same as team)
        
        try:
            team_id = dao.addTeam(sID,tYear,tImageLink)
            if not team_id:
                return jsonify(Error = "Problem inserting new team record."),500
        except:
            return jsonify(ERROR="Unable to verify Team from DAO."), 500

        for team_member in tRoster:
            aID = team_member['athlete_id']
            try:
                a_dao = AthleteDAO()
                athlete = a_dao.getAthleteByID(aID)
                if not athlete:
                    return jsonify(Error = "Athlete for ID:{} not found.".format(aID)),400
                #MOCKED METHOD TO GET ATHLETE SPORT
                athlete_sport = a_dao.getAthleteSportByID(aID)
                if athlete_sport != sID:
                    return jsonify(Error = "Athlete for ID:{} does not match team sport ID:{}.".format(aID,sID)),400
            except:
                return jsonify(ERROR="Unable to verify athlete from DAO."), 500

            try: 
                athlete_id = dao.addTeamMember(aID,team_id)
                if not athlete_id:
                    return jsonify(Error = "Problem inserting team member record."),500
            except:
                return jsonify(ERROR="Unable to verify team member from DAO."), 500
            
            dao.commitChanges()
            return jsonify(Team = "Added new team record with id:{} for Sport ID for Sport ID:{} and Season Year:{}".format(team_id,sID,tYear))

    #NEW
    def addTeamMember(self, aID,tID): 
        """
        adds someone to ateam
        """
        return
    #===========================//III.PUTS//====================================

    def editTeam(self,tID,sID,tRoster,tYear):
        """
        Instantiates a Team DAO in order to complete the desired put request and it returns a JSON with either a confirmation or error message.
        """
        return

    #NEW
    def editTeamMember(self, aID,tID): 
        return
    #===========================//IV.REMOVE//====================================

    def removeTeam(self,tID,sID): 
        """
        Instantiates a Team DAO in order to complete the desired put request and it returns a JSON with either a confirmation or error message.
        """
        return

    #NEW
    def removeTeamMember(self, aID,tID):
        return