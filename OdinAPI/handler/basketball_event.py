from flask import jsonify
from .dao.basketball_event_dao import BasketballEventDAO
#from .dao.event import EventDAO
#from .dao.team import TeamDAO
from .dao.athlete import AthleteDAO

#CONSTANTS: 
BASKETBALL_IDM = 1
BASKETBALL_IDF = 10

# THESE ARE MOCK CLASSES FOR EVENT AND TEAM
#TODO: Remove this later, it's just so that it compiles while the other DAOs arent finished
class EventDAO:
    def getEventByID(self,eID):
        #   id  date            is_local|venue      team_id
        #   3	"2020-03-30"	true	"Mangual"	1
        #   4	"2020-03-14"	true	"Espada"	1
        if eID == 3:
            return ('2020-03-30',True,'Mangual',1)
        if eID == 4:
            return ('2020-03-14',True,'Espada',1)
        if eID == 5:
            return ('2020-04-01',True,'Mangual',1)
        return None
    def getEventTeamByID(self,eID):
        team1events =[3,4,5]
        if eID in team1events:
            return 1
        else:
            return None

class TeamDAO:
    def getTeamSportByID(self,tID) :
        # Sport ID distribution
        # Team 1 is Volleyball M (1)
        # Team 2 is Volleyball M (2)
        # Team 3 is Basketball M (10)
        # Teams 4 and 5 is Volleyball F (12)
        if tID == 1:
            return 1
        if tID == 2:
            return 2
        if tID == 3:
            return 10
        if tID == 4:
            return 12
        else:
            return None
        return
    def getTeamMemberByIDs(self,aID,tID):
        # Team 1 has Athletes 1,3,4,8
        #returnable = dict(athlete_id = 8,team_id = 1)
        if tID == 1:
            if aID == 1 or aID == 3 or aID == 4 or aID == 8:
                return (aID,tID)
        return None
            

class AthleteDAO:
    def getAthleteByID(self,aID):
        # Many Athletes in system, gonna only demo a few.
        valid_list = [1,3,4,5,7,8,9,10,11,12,13,15,16]
        print("The aID is pretty cool: ",aID)
        if aID in valid_list:
            print("it's true. all of it.")
            # We dont care about value here, just that it returns 
            # something to prove it exists
            return True
        return False

class BasketballEventHandler:
    
# getAllStatisticsByBasketballEventID(eID)//Instantiates a Basketball Event DAO in order to complete the desired get request and it returns a JSON with the desired information or with an error message.
# getAllAthleteStatisticsByBasketballEventId(eID,aID)//Instantiates a Basketball Event DAO in order to complete the desired get request and it returns a JSON with the desired information or with an error message
# addStatistics(eID, aID, attributes)//Instantiates a Basketball Event DAO in order to complete the desired post request and it returns a JSON with either a confirmation or error message.
# editStatistics(eID, aID,attributes)//Instantiates a Basketball Event DAO in order to complete the desired put request and it returns a JSON with either a confirmation or error message.
# removesStatistics(eID, aID)//Instantiates a Basketball Event DAO in order to complete the desired put request and it returns a JSON with either a confirmation or error message.
# mapBasketballEventToDict(record)//Maps a Basketball Event record to a dictionary and returns it.


#===========================//DICTIONARY MAPPERS//==================================
    #TODO: need to label somehow the jsonify/request in the route so that it has the sport?
    def mapBasketballEventToDict(self,record):
        athlete_info = {}
        stat_info = {}
        event_info = {}

        athlete_info['athlete_id'] = record[0]
        athlete_info['first_name'] = record[1]
        athlete_info['middle_name'] = record[2]
        athlete_info['last_names'] = record[3]      
        athlete_info['number'] = record[4]
        athlete_info['profile_image_link'] = record[5]

        event_info['event_id'] = record[21]
        event_info['basketball_event_id'] = record[22]

        stat_info['points'] = record[6]
        stat_info['rebounds'] = record[7]
        stat_info['assists'] = record[8]
        stat_info['steals'] = record[9]
        stat_info['blocks'] = record[10]
        stat_info['turnovers'] = record[11]
        stat_info['field_goal_attempt'] = record[12]
        stat_info['successful_field_goal'] = record[13]
        stat_info['three_point_attempt'] = record[14]
        stat_info['successful_three_point'] = record[15]
        stat_info['free_throw_attempt'] = record[16]
        stat_info['successful_free_throw'] = record[17]
        stat_info['field_goal_percentage'] = float(record[18])
        stat_info['free_throw_percentage'] = float(record[19])
        stat_info['three_point_percentage'] = float(record[20])

        result = dict(Athlete = athlete_info, Event_Info = event_info, Event_Statistics = stat_info)
        return result

        
    #For Specific Athlete Event Info
    def mapBasketballEventAthleteStatsToDict(self,record):
        stat_info = {}
        event_info = {}

        stat_info['points'] = record[0]
        stat_info['rebounds'] = record[1]
        stat_info['assists'] = record[2]
        stat_info['steals'] = record[3]
        stat_info['blocks'] = record[4]
        stat_info['turnovers'] = record[5]
        stat_info['field_goal_attempt'] = record[6]
        stat_info['successful_field_goal'] = record[7]
        stat_info['three_point_attempt'] = record[8]
        stat_info['successful_three_point'] = record[9]
        stat_info['free_throw_attempt'] = record[10]
        stat_info['successful_free_throw'] = record[11]
        stat_info['field_goal_percentage'] = float(record[12])
        stat_info['free_throw_percentage'] = float(record[13])
        stat_info['three_point_percentage'] = float(record[14])

        event_info['event_id'] = record[15]
        event_info['basketball_event_id'] = record[16]
        event_info['athlete_id'] = record[17]

        #result = dict(Event_Statistics = stat_info)
        return dict(Event_Info= event_info, Event_Statistics = stat_info)

    # for team statistics
    def mapBasketballEventTeamStatsToDict(self,record):
        stat_info = {}
        event_info = {}

        stat_info['points'] = record[0]
        stat_info['rebounds'] = record[1]
        stat_info['assists'] = record[2]
        stat_info['steals'] = record[3]
        stat_info['blocks'] = record[4]
        stat_info['turnovers'] = record[5]
        stat_info['field_goal_attempt'] = record[6]
        stat_info['successful_field_goal'] = record[7]
        stat_info['three_point_attempt'] = record[8]
        stat_info['successful_three_point'] = record[9]
        stat_info['free_throw_attempt'] = record[10]
        stat_info['successful_free_throw'] = record[11]
        stat_info['field_goal_percentage'] = float(record[12])
        stat_info['free_throw_percentage'] = float(record[13])
        stat_info['three_point_percentage'] = float(record[14])

        event_info['event_id'] = record[15]
        event_info['basketball_event_team_stats_id'] = record[16]

        #result = dict(Event_Statistics = stat_info)
        return dict(Event_Info= event_info, Event_Statistics = stat_info)
    
    def mapBasketballEventSeasonCollectionToDict(self,record):
        event_info = {}
        stat_info = {}
        
        event_info['event_id'] = record[0] 
        event_info['event_date'] = record[1]
        event_info['basketball_event_id'] = record[17]
        event_info['athlete_id'] = record[18]

        stat_info['points'] = record[2]
        stat_info['rebounds'] = record[3]
        stat_info['assists'] = record[4]
        stat_info['steals'] = record[5]
        stat_info['blocks'] = record[6]
        stat_info['turnovers'] = record[7]
        stat_info['field_goal_attempt'] = record[8]
        stat_info['successful_field_goal'] = record[9]
        stat_info['three_point_attempt'] = record[10]
        stat_info['successful_three_point'] = record[11]
        stat_info['free_throw_attempt'] = record[12]
        stat_info['successful_free_throw'] = record[13]
        stat_info['field_goal_percentage'] = float(record[14])
        stat_info['free_throw_percentage'] = float(record[15])
        stat_info['three_point_percentage'] = float(record[16])

        result = dict(Event = event_info, Event_Statistics = stat_info)
        return result



# { "event_id": 5,
#   "team_statistics": 
#    { "basketball_statistics": 
#       { "points":500,
# 		"rebounds":500,
# 		"assists":500,
# 		"steals":500,
# 		"blocks":500,
# 		"turnovers":500,
# 		"field_goal_attempt":500,
# 		"successful_field_goal":500,
# 		"three_point_attempt":500,
# 		"successful_three_point":500,
# 		"free_throw_attempt":500,
# 		"successful_free_throw":500
#       } 
#    },
#   "athlete_statistics": 
#   [
#   	{"athlete_id":4,
#   	"statistics":
# 	  	{"basketball_statistics":
# 		  	{"points":2,
# 			"rebounds":2,
# 			"assists":2,
# 			"steals":2,
# 			"blocks":2,
# 			"turnovers":2,
# 			"field_goal_attempt":2,
# 			"successful_field_goal":2,
# 			"three_point_attempt":2,
# 			"successful_three_point":2,
# 			"free_throw_attempt":2,
# 			"successful_free_throw":2
# 		  	}
# 	  	}
#   	},

    def mapBasketballEventAllStatsToDict(self,team_record,athlete_records):
        event_info = dict(
            event_id = team_record[15],
            basketball_event_team_stats_id = team_record[16]
            # event_date = team_record[17]  
        )
        basketball_statistics = dict(
            points = team_record[0],
            rebounds = team_record[1],
            assists = team_record[2],
            steals = team_record[3],
            blocks = team_record[4],
            turnovers = team_record[5],
            field_goal_attempt = team_record[6],
            successful_field_goal = team_record[7],
            three_point_attempt = team_record[8],
            successful_three_point = team_record[9],
            free_throw_attempt = team_record[10],
            successful_free_throw = team_record[11],
            field_goal_percentage = float(team_record[12]),
            free_throw_percentage = float(team_record[13]),
            three_point_percentage = float(team_record[14]),
        )
        team_statistics = dict(basketball_statistics = basketball_statistics)

        # mappedResult = []
        # for athlete_statistics in result:                        
        #     mappedResult.append(self.mapBasketballEventToDict(athlete_statistics))
        # return jsonify(Basketball_Event = mappedResult), 200

        athlete_statistics = []

        for athlete_record in athlete_records:
            athlete_info = dict(
                athlete_id = athlete_record[0],
                first_name = athlete_record[1],
                middle_name = athlete_record[2],
                last_names = athlete_record[3],    
                number = athlete_record[4],
                profile_image_link = athlete_record[5],
                basketball_event_id = athlete_record[22]
            )
            statistics = dict(
                points = athlete_record[6],
                rebounds = athlete_record[7],
                assists = athlete_record[8],
                steals = athlete_record[9],
                blocks = athlete_record[10],
                turnovers = athlete_record[11],
                field_goal_attempt = athlete_record[12],
                successful_field_goal = athlete_record[13],
                three_point_attempt = athlete_record[14],
                successful_three_point = athlete_record[15],
                free_throw_attempt = athlete_record[16],
                successful_free_throw = athlete_record[17],
                field_goal_percentage = float(athlete_record[18]),
                free_throw_percentage = float(athlete_record[19]),
                three_point_percentage = float(athlete_record[20])
            )

            athlete_statistics.append(dict(athlete_info = athlete_info, statistics = statistics))
        
        result = dict(event_info = event_info, team_statistics = team_statistics, athlete_statistic = athlete_statistics)
        return result


#========/PROGRESS SO FAR/============
#
#TODO: Progress So Far
#
#LEYENDA: [X] is done, [*] is WIP, [ ] is not done
#
#[1][X]Added the basic handlers with basic functions
#[2][X] Need to add the extra handlers (get all athlete stats per season)
#[3][X] Need to add validation of parameters (like correct event/team for athlete)
#[4][X] Need to add routes for all
#[5][X] Need to add handler documentation
#[6][*] Add Final Score table (handlers/dao)
#[7][X] Prepare Tests and Mock Returns for Event, Team, etc
#       -GetAllStats(eID)           --> GET[X], 
#       -GetAllStats(eID,aID)       --> GET[X], POST    [X],    PUT[X], REMOVE[X]
#       -GetTeamStats(eID)          --> GET[X], POST(x2)[X][X], PUT[X], REMOVE[X]
#       -GetSeasonStats(aID,season) --> GET[X]
#[8][ ] Error Handling (try catch all of it), and check event form length
#[9][X] Add the validation of Previously Existing on Add (avoid duplicates) and Remove (cant remove nonexisting). Maybe on update 
#[10][X]Default is_invalid to false on adds.
#[11][X]PAYLOAD MEGAQUERY ADD: Add Route to give "payload" JSON as parameter and basically upload ALL results
#[12][X]On all queries, return the id of what you are getting too. 
#[13][ ]PARAMETER VALIDATION: For validation use is_instance of the date you receive,also if null of course
#[14][X]Create a "Get ALL statistics" handlers that returns both the team and the individual statistics...
#[15][X]After removing commits from DAO, confirm are done on habdler
#[16][X]Make it so the update method for athlete statistics does the update query too, dont want to call from route. 
#[17][*]Verify test cases for the new handlers such as the ADD/GET-ALL payload thing.
#
#=====================================

#===========================//HANDLERS//==================================
    



#===========================//I.GETS//====================================

    #TODO: Validation - For add/updates, validate the len(attributes), same as previous len(form)
    #TODO: Validation Overkill - Remove Unnecesary Validation methods, while still keeping constraint of is_valid values

    def getAllStatisticsByBasketballEventID(self,eID):
        """
        Gets all the statistics for a given event. 

        Calls the BasketballEventDAO to get event statistics and maps the result to
        to a JSON that contains all the statistics for that event in the system. That
        JSON object is then returned.

        Args:
            eID: The ID of the event of which statistics need to be fetched.
            
        Returns:
            A JSON containing all the statistics in the system for the specified event.
        """

        #validate existing event
        e_dao = EventDAO()
        event = e_dao.getEventByID(eID)
        if not event:
            return jsonify(Error = "Event for ID:{} not found.".format(eID)),400
        
        #validate existing basketball_event entries and format returnable
        dao = BasketballEventDAO()
        result = dao.getAllStatisticsByEventID(eID)
        if not result:
            return jsonify(Error = "Basketball Event Statistics not found for the event: {}.".format(eID)),404
        mappedResult = []
        for athlete_statistics in result:                        
            mappedResult.append(self.mapBasketballEventToDict(athlete_statistics))
        return jsonify(Basketball_Event = mappedResult), 200

    def getAllAthleteStatisticsByBasketballEventId(self,eID,aID):
        """
        Gets all the statistics for a given event and athlete. 

        Calls the BasketballEventDAO to get event statistics and maps the result to
        to a JSON that contains all the statistics for that athlete and event in the system. That
        JSON object is then returned.

        Args:
            eID: The ID of the event of which statistics need to be fetched.
            aID: The ID of the athlete of which statistics need to be fetched
            
        Returns:
            A JSON containing all the statistics in the system for the specified event and athlete.
        """

        #validate existing event
        e_dao = EventDAO()
        event = e_dao.getEventByID(eID)
        if not event:
            return jsonify(Error = "Event for ID:{} not found.".format(eID)),400
        
        #validate existing athlete 
        a_dao = AthleteDAO()
        athlete = a_dao.getAthleteByID(aID)
        if not athlete:
            return jsonify(Error = "Athlete for ID:{} not found.".format(aID)),400
        
        #validate existing basketball_event entry and format returnable
        dao = BasketballEventDAO()
        result = dao.getAllAthleteStatisticsByEventID(eID,aID)
        if not result:
            return jsonify(Error = "Basketball Event Statistics not found for the event: {} and the athlete id: {}.".format(eID,aID)),404
        mappedResult = self.mapBasketballEventAthleteStatsToDict(result)
        return jsonify(Basketball_Event_Athlete_Statistics = mappedResult),200

    def getAllTeamStatisticsByBasketballEventId(self,eID):
        """
        Gets all the statistics for a given event. 

        Calls the BasketballEventDAO to get event team statistics and maps the result to
        to a JSON that contains all the team statistics for that event in the system. That
        JSON object is then returned.

        Args:
            eID: The ID of the event of which team statistics need to be fetched.
            
        Returns:
            A JSON containing all the team statistics in the system for the specified event.
        """

        #validate existing event
        e_dao = EventDAO()
        event = e_dao.getEventByID(eID)
        if not event:
            return jsonify(Error = "Event for ID:{} not found.".format(eID)),400
        
        #validate existing basketball_event entry and format returnable
        dao = BasketballEventDAO()
        result = dao.getAllTeamStatisticsByEventID(eID)
        if not result:
            return jsonify(Error = "Basketball Event Team Statistics not found for the event: {}".format(eID)),404
        mappedResult = self.mapBasketballEventTeamStatsToDict(result)
        return jsonify(Basketball_Event_Team_Stats = mappedResult),200

    def getAllAthleteStatisticsPerSeason(self,aID,seasonYear):
        """
        Gets all the statistics for a given athlete during a given season. 

        Calls the BasketballEventDAO to get event statistics and maps the result to
        to a JSON that contains all the statistics for that athlete during the given season
        in the system. That JSON object is then returned.

        Args:
            seasonYear: the season year of which statistics need to be fetched
            aID: The ID of the athlete of which statistics need to be fetched
            
        Returns:
            A JSON containing all the statistics in the system for the specified athlete and season year.
        """

        #validate existing athlete 
        a_dao = AthleteDAO()
        athlete = a_dao.getAthleteByID(aID)
        if not athlete:
            return jsonify(Error = "Athlete for ID:{} not found.".format(aID)),400

        # validate existing basketball_event entries and format returnable
        dao = BasketballEventDAO()
        result = dao.getAllAthleteStatisticsPerSeason(aID,seasonYear)
        if not result:
            return jsonify(Error = "Basketball Event Statistics not found for the athlete id:{} in season year:{}.".format(aID,seasonYear)),404
        mappedResult = []
        for athlete_statistics in result:                     
            mappedResult.append(self.mapBasketballEventSeasonCollectionToDict(athlete_statistics))
        #print(mappedResult)
        return jsonify(Basketball_Event_Season_Athlete_Statistics = mappedResult), 200

    #NEW get ALL the statistics for a given event be it team or individual
    def getAllStatisticsForEvent(self,eID):
        """
        Gets all the team and individual statistics for a given event. 

        Calls the BasketballEventDAO to get event statistics and maps the result to
        to a JSON that contains all the statistics for that event in the system. 
        That JSON object is then returned.

        Args:
            eID: The ID of the event of which statistics need to be fetched
            
        Returns:
            A JSON containing all the statistics in the system for the specified event.
        """

        #validate existing event
        e_dao = EventDAO()
        event = e_dao.getEventByID(eID)
        if not event:
            return jsonify(Error = "Event for ID:{} not found.".format(eID)),400

        dao = BasketballEventDAO()
        team_result = dao.getAllTeamStatisticsByEventID(eID)
        if not team_result:
            return jsonify(Error = "Basketball Event Team Statistics not found for the event: {}".format(eID)),404
        all_stats_result = dao.getAllStatisticsByEventID(eID)
        if not all_stats_result:
            return jsonify(Error = "Basketball Event Statistics not found for the event: {}.".format(eID)),404
        
        mappedResult = self.mapBasketballEventAllStatsToDict(team_result,all_stats_result)
        return jsonify(Basketball_Event_Statistics = mappedResult),200

#===========================//II.POSTS//====================================
    def addStatistics(self,eID,aID,attributes): # Instantiates a Basketball Event DAO in order to complete the desired post request and it returns a JSON with either a confirmation or error message.
        """
        Adds a new statistics record with the provided information.

        Calls the BastketballEventDAO to add a new statistics record and maps the result to
        to a JSON that contains the desired record. That JSON object 
        is then returned.

        Args:
            eID: the ID of the event for which the statistics record will be added.
            aID: the ID of the athlete for which the statistics record will be added.
            Attributes:
                points: number of points scored by the athlete in the event.
                rebounds: number of rebounds attained by the athlete in the event.
                assists: number of assists attained by the athlete in the event.
                steals: number of steals attained by the athlete in the event.
                blocks: number of blocks attained by the athlete in the event.
                turnovers: number of turnovers attained by the athlete in the event.
                fieldGoalAttempt: number of field goal attempts attained by the athlete in the event.
                successfulFieldGoal: number of successful field goals attained by the athlete in the event.
                threePointAttempt: number of three point attempts attained by the athlete in the event.
                successfulThreePoint: number of successful three point shots attained by the athlete in the event.
                freeThrowAttempt: number of free throw attempts attained by the athlete in the event.
                successfulFreeThrow: number of successful free throws attained by the athlete in the event.
            
        Returns:
            A JSON containing all the statistics for the new Basketball Event record.
        """

        # Validate Avoid Duplication
        dao = BasketballEventDAO()
        if dao.getBasketballEventID(eID,aID):
            return jsonify(Error = "Basketball Event Entry already exists for Event ID:{} and Athlete ID:{}".format(eID,aID)),400

        # Validate existing event
        e_dao = EventDAO()
        event = e_dao.getEventByID(eID)
        if not event:
            return jsonify(Error = "Event for ID:{} not found.".format(eID)),400
        
        # Get Event Team For Validation
        t_dao = TeamDAO()
        #TODO: (Luis) Need EventDAO method to obtain team ID
        tID = e_dao.getEventTeamByID(eID)

        # Validate that the event belongs to the correct sport.
        #TODO: (Herbert) Need TeamDAO to return sport_id of a team.
        sID = t_dao.getTeamSportByID(tID) 
        if sID != BASKETBALL_IDF and sID != BASKETBALL_IDM:
            return jsonify(Error = "Malformed Query, Event ID:{} does not belong to Basketball.".format(eID)),400

        # Validate existing athlete 
        a_dao = AthleteDAO()
        athlete = a_dao.getAthleteByID(aID)
        if not athlete:
            return jsonify(Error = "Athlete for ID:{} not found.".format(aID)),400

        # Validate athlete belongs to team playing event
        #TODO: (Herbert) Need TeamDAO method to get a team_member record to validate team membership. Could be a Boolean
        if not t_dao.getTeamMemberByIDs(aID,tID): #alternatively: t_dao.athleteBelongsToTeam(aID,tID)
            return jsonify(Error = "Malformed Query, Athlete ID:{} does not belong to Team ID:{} from Event ID:{}.".format(aID,tID,eID)),400
        
        # Create and Validate new Basketball_Event
        result = dao.addStatistics(eID,aID,attributes[0],attributes[1],attributes[2],attributes[3],
        attributes[4],attributes[5],attributes[6],attributes[7],attributes[8],attributes[9],
        attributes[10],attributes[11])
        if not result:
            return jsonify(Error = "Problem inserting new statistics record."),500
        #TODO: should I mention the sport in this part? like, "basketball statistics record" or so
        dao.commitChanges()
        return jsonify(Basketball_Event_Athlete_Statistics = "Added new statistics record with id:{} for athlete id:{} in event id:{}.".format(result,aID,eID)),201

   
    def addTeamStatistics(self,eID,attributes): # Instantiates a Basketball Event DAO in order to complete the desired post request and it returns a JSON with either a confirmation or error message.
        """
        Adds a new team statistics record with the provided information.

        Calls the BastketballEventDAO to add a new team statistics record and maps the result to
        to a JSON that contains the desired record. That JSON object 
        is then returned.

        Args:
            eID: the ID of the event for which the statistics record will be added.
            Attributes:
                points: number of points scored by the athlete in the event.
                rebounds: number of rebounds attained by the athlete in the event.
                assists: number of assists attained by the athlete in the event.
                steals: number of steals attained by the athlete in the event.
                blocks: number of blocks attained by the athlete in the event.
                turnovers: number of turnovers attained by the athlete in the event.
                fieldGoalAttempt: number of field goal attempts attained by the athlete in the event.
                successfulFieldGoal: number of successful field goals attained by the athlete in the event.
                threePointAttempt: number of three point attempts attained by the athlete in the event.
                successfulThreePoint: number of successful three point shots attained by the athlete in the event.
                freeThrowAttempt: number of free throw attempts attained by the athlete in the event.
                successfulFreeThrow: number of successful free throws attained by the athlete in the event.
            
        Returns:
            A JSON containing all the statistics for the new Basketball Event team statistics record.
        """

        # Validate Avoid Duplication
        dao = BasketballEventDAO()
        if dao.getBasketballEventTeamStatsID(eID):
            return jsonify(Error = "Basketball Event Team Stats Entry already exists for Event ID:{}".format(eID)),400

        # Validate existing event
        e_dao = EventDAO()
        event = e_dao.getEventByID(eID)
        if not event:
            return jsonify(Error = "Event for ID:{} not found.".format(eID)),400
        
        # Get Event Team For Validation
        t_dao = TeamDAO()
        #TODO: (Luis) Need EventDAO method to obtain team ID
        tID = e_dao.getEventTeamByID(eID)

        # Validate that the event belongs to the correct sport.
        #TODO: (Herbert) Need TeamDAO to return sport_id of a team.
        sID = t_dao.getTeamSportByID(tID)
        if sID != BASKETBALL_IDF and sID != BASKETBALL_IDM:
            return jsonify(Error = "Malformed Query, Event ID:{} does not belong to Basketball.".format(eID)),400

        # Create and Validate new Basketball_Event team stats
        result = dao.addTeamStatistics(eID,attributes[0],attributes[1],attributes[2],attributes[3],
        attributes[4],attributes[5],attributes[6],attributes[7],attributes[8],attributes[9],
        attributes[10],attributes[11])
        if not result:
            return jsonify(Error = "Problem inserting new team statistics record."),500
        dao.commitChanges()
        return jsonify(Basketball_Event_Team_Stats = "Added new team statistics record with id:{} for event id:{}.".format(result,eID)),201

    def addTeamStatisticsAuto(self,eID): # Instantiates a Basketball Event DAO in order to complete the desired post request and it returns a JSON with either a confirmation or error message.
        """
        Adds a new team statistics record with the provided information and an aggregate of existing information.

        Calls the BastketballEventDAO to add a new team statistics record and maps the result to
        to a JSON that contains the desired record. That JSON object 
        is then returned.

        Args:
            eID: the ID of the event for which the statistics record will be added.
            
        Returns:
            A JSON containing all the statistics for the new Basketball Event team statistics record.
        """

        # Validate Avoid Duplication
        dao = BasketballEventDAO()
        if dao.getBasketballEventTeamStatsID(eID):
            return jsonify(Error = "Basketball Event Team Stats Entry already exists for Event ID:{}".format(eID)),400

        # Validate existing event
        e_dao = EventDAO()
        event = e_dao.getEventByID(eID)
        if not event:
            return jsonify(Error = "Event for ID:{} not found.".format(eID)),400
        
        # Get Event Team For Validation
        t_dao = TeamDAO()
        #TODO: (Luis) Need EventDAO method to obtain team ID
        tID = e_dao.getEventTeamByID(eID)

        # Validate that the event belongs to the correct sport.
        #TODO: (Herbert) Need TeamDAO to return sport_id of a team.
        sID = t_dao.getTeamSportByID(tID)
        if sID != BASKETBALL_IDF and sID != BASKETBALL_IDM:
            return jsonify(Error = "Malformed Query, Event ID:{} does not belong to Basketball.".format(eID)),400

        # Create and Validate new Basketball_Event team stats
        result = dao.addTeamStatisticsAuto(eID)
        if not result:
            return jsonify(Error = "Problem inserting new team statistics record."),500
        dao.commitChanges()
        return jsonify(Basketball_Event_Team_Stats = "Added new team statistics record with id:{} for event id:{}.".format(result,eID)),201


    # THE JSON REQUEST PARAMETER FORMAT(Volleyball version, mostly the same tho...)
    # { "event_id": 5,
    # "team_statistics": 
    # { "basketball_statistics": 
    #     { "points":500,
    #         "rebounds":500,
    #         "assists":500,
    #         "steals":500,
    #         "blocks":500,
    #         "turnovers":500,
    #         "field_goal_attempt":500,
    #         "successful_field_goal":500,
    #         "three_point_attempt":500,
    #         "successful_three_point":500,
    #         "free_throw_attempt":500,
    #         "successful_free_throw":500
    #     } 
    # },
    # "athlete_statistics": 
    # [
    #     {"athlete_id":4,
    #     "statistics":
    #         {"basketball_statistics":
    #             {"points":2,
    #             "rebounds":2,
    #             "assists":2,
    #             "steals":2,
    #             "blocks":2,
    #             "turnovers":2,
    #             "field_goal_attempt":2,
    #             "successful_field_goal":2,
    #             "three_point_attempt":2,
    #             "successful_three_point":2,
    #             "free_throw_attempt":2,
    #             "successful_free_throw":2
    #             }
    #         }
    #     },
    #     {"athlete_id":8,
    #     "statistics":
    #         {"basketball_statistics":
    #             {"points":1,
    #             "rebounds":1,
    #             "assists":1,
    #             "steals":1,
    #             "blocks":1,
    #             "turnovers":1,
    #             "field_goal_attempt":1,
    #             "successful_field_goal":1,
    #             "three_point_attempt":1,
    #             "successful_three_point":1,
    #             "free_throw_attempt":1,
    #             "successful_free_throw":1
    #             }
    #         }
    #     }
    #     ],
    # "uprm_score": 0,
    # "opponent_score": 0 }

    #NEW: the mega query
    def addAllEventStatistics(self,eID,team_statistics,athlete_statistics):
        """
        Adds new statistics records with the provided information.

        Calls the BastketballEventDAO to add new statistics records and maps the result to
        to a JSON that contains the desired records. That JSON object 
        is then returned.

        Args:
            eID: the ID of the event for which the statistics record will be added.
            athlete_ids: the IDs of the athletes for which the statistics record will be added.
            Attributes:
                points: number of points scored by the athlete in the event.
                rebounds: number of rebounds attained by the athlete in the event.
                assists: number of assists attained by the athlete in the event.
                steals: number of steals attained by the athlete in the event.
                blocks: number of blocks attained by the athlete in the event.
                turnovers: number of turnovers attained by the athlete in the event.
                fieldGoalAttempt: number of field goal attempts attained by the athlete in the event.
                successfulFieldGoal: number of successful field goals attained by the athlete in the event.
                threePointAttempt: number of three point attempts attained by the athlete in the event.
                successfulThreePoint: number of successful three point shots attained by the athlete in the event.
                freeThrowAttempt: number of free throw attempts attained by the athlete in the event.
                successfulFreeThrow: number of successful free throws attained by the athlete in the event.
            
        Returns:
            A JSON containing all the statistics for the new Basketball Event record.
        """

        dao = BasketballEventDAO()

        # Validate Avoid Duplication Team Stats
        if dao.getBasketballEventTeamStatsID(eID):
            return jsonify(Error = "Basketball Event Team Stats Entry already exists for Event ID:{}".format(eID)),400

        # Validate existing event
        e_dao = EventDAO()
        event = e_dao.getEventByID(eID)
        if not event:
            return jsonify(Error = "Event for ID:{} not found.".format(eID)),400
        
        # Get Event Team For Validation
        t_dao = TeamDAO()
        #TODO: (Luis) Need EventDAO method to obtain team ID
        tID = e_dao.getEventTeamByID(eID)

        # Validate that the event belongs to the correct sport.
        #TODO: (Herbert) Need TeamDAO to return sport_id of a team.
        sID = t_dao.getTeamSportByID(tID) 
        if sID != BASKETBALL_IDF and sID != BASKETBALL_IDM:
            return jsonify(Error = "Malformed Query, Event ID:{} does not belong to Basketball.".format(eID)),400

        # Go through every set of athlete to add attributes for. 
        for attributes in athlete_statistics:

            aID = attributes['athlete_id']

            # Validate Avoid Duplication Basketball Event Entry
            if dao.getBasketballEventID(eID,aID):
                return jsonify(Error = "Basketball Event Entry already exists for Event ID:{} and Athlete ID:{}".format(eID,aID)),400

            # Validate existing athlete 
            statistics = attributes['statistics']['basketball_statistics']
            a_dao = AthleteDAO()
            athlete = a_dao.getAthleteByID(aID)
            if not athlete:
                return jsonify(Error = "Athlete for ID:{} not found.".format(aID)),400

            # Validate athlete belongs to team playing event
            #TODO: (Herbert) Need TeamDAO method to get a team_member record to validate team membership. Could be a Boolean
            if not t_dao.getTeamMemberByIDs(aID,tID): #alternatively: t_dao.athleteBelongsToTeam(aID,tID)
                return jsonify(Error = "Malformed Query, Athlete ID:{} does not belong to Team ID:{} from Event ID:{}.".format(aID,tID,eID)),400
            
            # Create and Validate new Basketball_Event
            result = dao.addStatistics(eID,aID,statistics['points'],statistics['rebounds'],statistics['assists'],
            statistics['steals'],statistics['blocks'],statistics['turnovers'],statistics['field_goal_attempt'],statistics['successful_field_goal'],statistics['three_point_attempt'],
            statistics['successful_three_point'],statistics['free_throw_attempt'],statistics['successful_free_throw'])
            if not result:
                return jsonify(Error = "Problem inserting new statistics record."),500
            #TODO: should I mention the sport in this part? like, "basketball statistics record" or so
            # SUCCESS MESSAGE
            # return jsonify(Basketball_Event_Athlete_Statistics = "Added new statistics record with id:{} for athlete id:{} in event id:{}.".format(result,aID,eID)),201

        # Create and Validate new Basketball_Event team stats
        result = dao.addTeamStatistics(eID,team_statistics['points'],team_statistics['rebounds'],team_statistics['assists'],
            team_statistics['steals'],team_statistics['blocks'],team_statistics['turnovers'],team_statistics['field_goal_attempt'],team_statistics['successful_field_goal'],team_statistics['three_point_attempt'],
            team_statistics['successful_three_point'],team_statistics['free_throw_attempt'],team_statistics['successful_free_throw'])
        if not result:
            return jsonify(Error = "Problem inserting new team statistics record."),500
        dao.commitChanges()
        return jsonify(Basketball_Event_Team_Stats = "Added new team statistics record with id:{} and individual statistics for event id:{}.".format(result,eID)),201



#===========================//III.PUTS//====================================
    #TODO: Need to call the update team statistics call
    def editStatistics(self,eID,aID,attributes): # Instantiates a Basketball Event DAO in order to complete the desired put request and it returns a JSON with either a confirmation or error message.
        """
        Updates the statistics for the basketball event with the given IDs.

        Calls the BasktballEventDAO to update the statistics of a basketball event. It then
        maps the result to a JSON that contains the desired record. That JSON 
        object is then returned.

        Args:
            eID: the ID of the event for which the statistics record will be updated.
            aID: the ID of the athlete for which the statistics record will be updated.
            Attributes:
                points: number of points scored by the athlete in the event.
                rebounds: number of rebounds attained by the athlete in the event.
                assists: number of assists attained by the athlete in the event.
                steals: number of steals attained by the athlete in the event.
                blocks: number of blocks attained by the athlete in the event.
                turnovers: number of turnovers attained by the athlete in the event.
                fieldGoalAttempt: number of field goal attempts attained by the athlete in the event.
                successfulFieldGoal: number of successful field goals attained by the athlete in the event.
                threePointAttempt: number of three point attempts attained by the athlete in the event.
                successfulThreePoint: number of successful three point shots attained by the athlete in the event.
                freeThrowAttempt: number of free throw attempts attained by the athlete in the event.
                successfulFreeThrow: number of successful free throws attained by the athlete in the event.
            
        Returns:
            A JSON containing all the user with the updated dashboard user.
        """

        # Validate existing event
        e_dao = EventDAO()
        event = e_dao.getEventByID(eID)
        if not event:
            return jsonify(Error = "Event for ID:{} not found.".format(eID)),400
        
        # Validate existing athlete 
        a_dao = AthleteDAO()
        athlete = a_dao.getAthleteByID(aID)
        if not athlete:
            return jsonify(Error = "Athlete for ID:{} not found.".format(aID)),400

        # Update and Validate Basketball event, format returnable
        dao = BasketballEventDAO()
        result = dao.editStatistics(eID,aID,attributes[0],attributes[1],attributes[2],attributes[3],
        attributes[4],attributes[5],attributes[6],attributes[7],attributes[8],attributes[9],
        attributes[10],attributes[11])
        if not result:
            return jsonify(Error = "Statistics Record not found for athlete id:{} in event id:{}.".format(aID,eID)),404

        #update and validate Basketball Event Team Statistic
        team_result = dao.editTeamStatistics(eID)
        if not result:
            return jsonify(Error = "Team Statistics Record not found for event id:{}.".format(eID)),404

        
        mappedResult = self.mapBasketballEventAthleteStatsToDict(result)
        dao.commitChanges()
        return jsonify(Basketball_Event_Athlete_Statistics = mappedResult),200

    def editTeamStatistics(self,eID): # Instantiates a Basketball Event DAO in order to complete the desired put request and it returns a JSON with either a confirmation or error message.
        """
        Updates the team statistics for the basketball event with the given ID and aggregates of existing data.

        Calls the BasktballEventDAO to update the statistics of a basketball event. It then
        maps the result to a JSON that contains the desired record. That JSON 
        object is then returned.

        Args:
            eID: the ID of the event for which the statistics record will be updated.
        
            
        Returns:
            A JSON containing all the user with the updated dashboard user.
        """

        # Validate existing event
        e_dao = EventDAO()
        event = e_dao.getEventByID(eID)
        if not event:
            return jsonify(Error = "Event for ID:{} not found.".format(eID)),400

        # Update and Validate Basketball event team stats, format returnable
        dao = BasketballEventDAO()
        result = dao.editTeamStatistics(eID)
        if not result:
            return jsonify(Error = "Team Statistics Record not found for event id:{}.".format(eID)),404
        mappedResult = self.mapBasketballEventTeamStatsToDict(result)
        dao.commitChanges()
        return jsonify(Basketball_Event_Team_Stats = mappedResult),200
#===========================//IV.PATCH//====================================
    #TODO: need to add the update team statistics call
    def removeStatistics(self,eID,aID): # Instantiates a Basketball Event DAO in order to complete the desired put request and it returns a JSON with either a confirmation or error message.
        """
        Invalidates a statistics record in the database based on the given IDs.

        Calls the BasketballEventDAO to invalidate a statistics record. It then
        maps the result to a JSON that contains the desired record. That JSON 
        object is then returned.

        Args:
            eID: the ID of the event for which the statistics record will be invalidated.
            aID: the ID of the athlete for which the statistics record will be invalidated.
            
        Returns:
            A JSON containing all the statistics with the updated Basketball Event.
        """

        # Validate existing event
        e_dao = EventDAO()
        event = e_dao.getEventByID(eID)
        if not event:
            return jsonify(Error = "Event for ID:{} not found.".format(eID)),400
        
        # Validate existing athlete 
        a_dao = AthleteDAO()
        athlete = a_dao.getAthleteByID(aID)
        if not athlete:
            return jsonify(Error = "Athlete for ID:{} not found.".format(aID)),400

        # Remove Basketball_Event Statistics and format returnabe
        dao = BasketballEventDAO()
        result = dao.removeStatistics(eID,aID)
        if not result:
            return jsonify(Error = "Statistics Record not found with event id:{} for athlete id:{}.".format(eID,aID)),404
        dao.commitChanges()
        return jsonify(Basketball_Event_Athlete_Statistics = "Removed statistics record with id:{} for athlete id:{} in event id:{}.".format(result,aID,eID)),200

    def removeTeamStatistics(self,eID): # Instantiates a Basketball Event DAO in order to complete the desired put request and it returns a JSON with either a confirmation or error message.
        """
        Invalidates a team statistics record in the database based on the given ID.

        Calls the BasketballEventDAO to invalidate a team statistics record. It then
        maps the result to a JSON that contains the desired record. That JSON 
        object is then returned.

        Args:
            eID: the ID of the event for which the statistics record will be invalidated.
            
        Returns:
            A JSON containing all the statistics with the updated Basketball Event.
        """

        # Validate existing event
        e_dao = EventDAO()
        event = e_dao.getEventByID(eID)
        if not event:
            return jsonify(Error = "Event for ID:{} not found.".format(eID)),400

        # Remove Basketball_Event Team Statistics and format returnabe
        dao = BasketballEventDAO()
        result = dao.removeTeamStatistics(eID)
        if not result:
            return jsonify(Error = "Team Statistics Record not found with event id:{}.".format(eID)),404
        dao.commitChanges()
        return jsonify(Basketball_Event_Team_Statistics = "Removed team statistics record with id:{} for event id:{}.".format(result,eID)),200




