from flask import jsonify
from .dao.basketball_event_dao import BasketballEventDAO


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
    
#========/PROGRESS/============

# Added the basic handlers with basic functions
# Need to add validation of parameters (like correct event/team for athlete)
# Need to add the extra handlers (get all athlete stats per season)
# Need to add handler documentation
# Need to add routes for all







#==============================
#===========================//HANDLERS//==================================
#TODO: not just the basic gets, also confirm the valid parameter (does athlete belong to team? etc.)
    def getAllStatisticsByBasketballEventID(self,eID):
        """
        """
        dao = BasketballEventDAO()
        result = dao.getAllStatisticsByEventID(eID)
        if not result:
            return jsonify(Error = "Basketball Event Statistics not found for the event: {}.".format(eID)),404
        mappedResult = []
        for athlete_statistics in result:                        
            mappedResult.append(self.mapBasketballEventCollectionToDict(athlete_statistics))
        #print(mappedResult)
        return jsonify(Basketball_Event = mappedResult), 200

    def getAllAthleteStatisticsByBasketballEventId(self,eID,aID):
        """
        """
        dao = BasketballEventDAO()
        result = dao.getAllAthleteStatisticsByEventID(eID,aID)
        if not result:
            return jsonify(Error = "Basketball Event Statistics not found for the event: {} and the id: {}.".format(eID,aID)),404
        mappedResult = self.mapBasketballEventToDict(result)
        return jsonify(Basketball_Event_Athlete_Statistics = mappedResult),200
#---WORK WORK WORK WORK
    def addStatistics(self,eID,aID,attributes): # Instantiates a Basketball Event DAO in order to complete the desired post request and it returns a JSON with either a confirmation or error message.
        """
        """
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
        dao = BasketballEventDAO()
        result = dao.addTeamStatistics(eID)
        if not result:
            return jsonify(Error = "Problem inserting new team statistics record."),500
        return jsonify(Basketball_Event_Team_Stats = "Added new team statistics record with id:{} for event id:{}.".format(result,eID)),201

    #TODO: Need to call the update team statistics call
    def editStatistics(self,eID,aID,attributes): # Instantiates a Basketball Event DAO in order to complete the desired put request and it returns a JSON with either a confirmation or error message.
        """
        """
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
        dao = BasketballEventDAO()
        result = dao.editTeamStatistics(eID)
        if not result:
            return jsonify(Error = "Team Statistics Record not found for event id:{}.".format(eID)),404
        mappedResult = self.mapBasketballEventToDict(result)
        return jsonify(Basketball_Event_Team_Stats = mappedResult),200
    
    #TODO: need to add the update team statistics call
    def removeStatistics(self,eID,aID): # Instantiates a Basketball Event DAO in order to complete the desired put request and it returns a JSON with either a confirmation or error message.
        """
        """
        dao = BasketballEventDAO()
        result = dao.removeStatistics(eID,aID)
        if not result:
            return jsonify(Error = "Statistics Record not found with event id:{} for athlete id:{}.".format(eID,aID)),404
        return jsonify(Basketball_Event_Athlete_Statistics = "Removed statistics record with id:{} for athlete id:{} in event id:{}.".format(result,aID,eID)),200

    def removeTeamStatistics(self,eID): # Instantiates a Basketball Event DAO in order to complete the desired put request and it returns a JSON with either a confirmation or error message.
        """
        """
        dao = BasketballEventDAO()
        result = dao.removeTeamStatistics(eID)
        if not result:
            return jsonify(Error = "Team Statistics Record not found with event id:{}.".format(eID)),404
        return jsonify(Basketball_Event_Team_Statistics = "Removed team statistics record with id:{} for event id:{}.".format(result,eID)),200




