from flask import jsonify
from .dao.basketball_event_dao import BasketballEventDAO
#from .dao.event import EventDAO
#from .dao.team import TeamDAO
from .dao.athlete import AthleteDAO

#CONSTANTS: 
BASKETBALL_ID = 1

#TODO: Remove this later, it's just so that it compiles while the other DAOs arent finished
class EventDAO:
    def something(self):
        return

class TeamDAO:
    def something(self):
        return

class BasketballEventHandler:
    
# getAllStatisticsByBasketballEventID(eID)//Instantiates a Basketball Event DAO in order to complete the desired get request and it returns a JSON with the desired information or with an error message.
# getAllAthleteStatisticsByBasketballEventId(eID,aID)//Instantiates a Basketball Event DAO in order to complete the desired get request and it returns a JSON with the desired information or with an error message
# addStatistics(eID, aID, attributes)//Instantiates a Basketball Event DAO in order to complete the desired post request and it returns a JSON with either a confirmation or error message.
# editStatistics(eID, aID,attributes)//Instantiates a Basketball Event DAO in order to complete the desired put request and it returns a JSON with either a confirmation or error message.
# removesStatistics(eID, aID)//Instantiates a Basketball Event DAO in order to complete the desired put request and it returns a JSON with either a confirmation or error message.
# mapBasketballEventToDict(record)//Maps a Basketball Event record to a dictionary and returns it.


#===========================//DICTIONARY MAPPERS//==================================
    #TODO: need to label somehow the jsonify/request in the route so that it has the sport?
    def mapBasketballEventCollectionToDict(self,record):
        athlete_info = {}
        stat_info = {}

        athlete_info['athlete_id'] = record[0]
        athlete_info['first_name'] = record[1]
        athlete_info['middle_name'] = record[2]
        athlete_info['last_names'] = record[3]      
        athlete_info['number'] = record[4]
        athlete_info['profile_image_link'] = record[5]

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

        result = dict(Athlete = athlete_info, Event_Statistics = stat_info)
        return result

        
    def mapBasketballEventToDict(self,record):
        stat_info = {}

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

        #result = dict(Event_Statistics = stat_info)
        return stat_info
    
    def mapBasketballEventCollectionToDict(self,record):
        event_info = {}
        stat_info = {}
        
        event_info['event_id'] = record[0] 
        event_info['event_date'] = record[1]

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


#========/PROGRESS SO FAR/============
#
#TODO: Progress So Far
#
#[1][X]Added the basic handlers with basic functions
#[2][X] Need to add the extra handlers (get all athlete stats per season)
#[3][*] Need to add validation of parameters (like correct event/team for athlete)
#[4][*] Need to add routes for all
#[5][ ] Need to add handler documentation
#
#=====================================

#===========================//HANDLERS//==================================

#===========================//I.GETS//====================================

    #TODO: Validation - For add/updates, validate the len(attributes), same as previous len(form)
    #TODO: Validation Overkill - Remove Unnecesary Validation methods, while still keeping constraint of is_valid values

    def getAllStatisticsByBasketballEventID(self,eID):
        """
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
            mappedResult.append(self.mapBasketballEventCollectionToDict(athlete_statistics))
        return jsonify(Basketball_Event = mappedResult), 200

    def getAllAthleteStatisticsByBasketballEventId(self,eID,aID):
        """
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
        print("HELLO HELLO THERE, the ath id is",athlete)
        
        #validate existing basketball_event entry and format returnable
        dao = BasketballEventDAO()
        result = dao.getAllAthleteStatisticsByEventID(eID,aID)
        if not result:
            return jsonify(Error = "Basketball Event Statistics not found for the event: {} and the id: {}.".format(eID,aID)),404
        mappedResult = self.mapBasketballEventToDict(result)
        return jsonify(Basketball_Event_Athlete_Statistics = mappedResult),200

    def getAllAthleteStatisticsPerSeason(self,aID,seasonYear):
        """
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
            mappedResult.append(self.mapBasketballEventCollectionToDict(athlete_statistics))
        #print(mappedResult)
        return jsonify(Basketball_Event_Season_Athlete_Statistics = mappedResult), 200

#===========================//II.POSTS//====================================
    def addStatistics(self,eID,aID,attributes): # Instantiates a Basketball Event DAO in order to complete the desired post request and it returns a JSON with either a confirmation or error message.
        """
        """
        
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
        if sID != BASKETBALL_ID:
            return jsonify(Error = "Malformed Query, Event ID:{} does not belong to Sport ID:{}.".format(eID,BASKETBALL_ID)),400

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
        dao = BasketballEventDAO()
        result = dao.addStatistics(eID,aID,attributes[0],attributes[1],attributes[2],attributes[3],
        attributes[4],attributes[5],attributes[6],attributes[7],attributes[8],attributes[9],
        attributes[10],attributes[11])
        if not result:
            return jsonify(Error = "Problem inserting new statistics record."),500
        #TODO: should I mention the sport in this part? like, "basketball statistics record" or so
        return jsonify(Basketball_Event_Athlete_Statistics = "Added new statistics record with id:{} for athlete id:{} in event id:{}.".format(result,aID,eID)),201

   
    def addTeamStatistics(self,eID,attributes): # Instantiates a Basketball Event DAO in order to complete the desired post request and it returns a JSON with either a confirmation or error message.
        """
        """
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
        if sID != BASKETBALL_ID:
            return jsonify(Error = "Malformed Query, Event ID:{} does not belong to Sport ID:{}.".format(eID,BASKETBALL_ID)),400

        # Create and Validate new Basketball_Event team stats
        dao = BasketballEventDAO()
        result = dao.addTeamStatistics(eID,attributes[0],attributes[1],attributes[2],attributes[3],
        attributes[4],attributes[5],attributes[6],attributes[7],attributes[8],attributes[9],
        attributes[10],attributes[11])
        if not result:
            return jsonify(Error = "Problem inserting new team statistics record."),500
        return jsonify(Basketball_Event_Team_Stats = "Added new team statistics record with id:{} for event id:{}.".format(result,eID)),201

    def addTeamStatisticsAuto(self,eID): # Instantiates a Basketball Event DAO in order to complete the desired post request and it returns a JSON with either a confirmation or error message.
        """
        """

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
        if sID != BASKETBALL_ID:
            return jsonify(Error = "Malformed Query, Event ID:{} does not belong to Sport ID:{}.".format(eID,BASKETBALL_ID)),400

        # Create and Validate new Basketball_Event team stats
        dao = BasketballEventDAO()
        result = dao.addTeamStatistics(eID)
        if not result:
            return jsonify(Error = "Problem inserting new team statistics record."),500
        return jsonify(Basketball_Event_Team_Stats = "Added new team statistics record with id:{} for event id:{}.".format(result,eID)),201
#===========================//III.PUTS//====================================
    #TODO: Need to call the update team statistics call
    def editStatistics(self,eID,aID,attributes): # Instantiates a Basketball Event DAO in order to complete the desired put request and it returns a JSON with either a confirmation or error message.
        """
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
        result = dao.editStatistics(aID,attributes[0],attributes[1],attributes[2],attributes[3],
        attributes[4],attributes[5],attributes[6],attributes[7],attributes[8],attributes[9],
        attributes[10])
        if not result:
            return jsonify(Error = "Statistics Record not found for athlete id:{} in event id:{}.".format(aID,eID)),404
        mappedResult = self.mapBasketballEventToDict(result)
        return jsonify(Basketball_Event_Athlete_Statistics = mappedResult),200

    def editTeamStatistics(self,eID): # Instantiates a Basketball Event DAO in order to complete the desired put request and it returns a JSON with either a confirmation or error message.
        """
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

        # Update and Validate Basketball event team stats, format returnable
        dao = BasketballEventDAO()
        result = dao.editTeamStatistics(eID)
        if not result:
            return jsonify(Error = "Team Statistics Record not found for event id:{}.".format(eID)),404
        mappedResult = self.mapBasketballEventToDict(result)
        return jsonify(Basketball_Event_Team_Stats = mappedResult),200
#===========================//IV.PATCH//====================================
    #TODO: need to add the update team statistics call
    def removeStatistics(self,eID,aID): # Instantiates a Basketball Event DAO in order to complete the desired put request and it returns a JSON with either a confirmation or error message.
        """
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
        return jsonify(Basketball_Event_Athlete_Statistics = "Removed statistics record with id:{} for athlete id:{} in event id:{}.".format(result,aID,eID)),200

    def removeTeamStatistics(self,eID): # Instantiates a Basketball Event DAO in order to complete the desired put request and it returns a JSON with either a confirmation or error message.
        """
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

        # Remove Basketball_Event Team Statistics and format returnabe
        dao = BasketballEventDAO()
        result = dao.removeTeamStatistics(eID)
        if not result:
            return jsonify(Error = "Team Statistics Record not found with event id:{}.".format(eID)),404
        return jsonify(Basketball_Event_Team_Statistics = "Removed team statistics record with id:{} for event id:{}.".format(result,eID)),200




