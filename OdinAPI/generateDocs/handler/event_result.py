from flask import jsonify
# from .dao.event import EventDAO
# from .dao.team import TeamDAO
# from .dao.athlete import AthleteDAO
from .dao.final_score_dao import FinalScoreDAO


# THE FOLLOWING THREE ARE MOCK CLASSES FOR TESTING
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
        if eID == 6:
            return ('2020-04-20',True,'Espada',1)
        return None
    def getEventTeamByID(self,eID):
        team1events =[3,4,5,6]
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
        if aID in valid_list:
            # We dont care about value here, just that it returns
            # something to prove it exists
            return True
        return False

class EventResultHandler:
#===========================//DICTIONARY MAPPERS//==================================
    def mapEventToDict(self,record):
        pass


    #For Specific Athlete Event Info
    def mapEventAthleteStatsToDict(self,record):
        pass

    # for team statistics
    def mapEventTeamStatsToDict(self,record):
        pass

    # for final score
    def mapFinalScoreToDict(self,final_record):
        score = dict(uprm_score = final_record[0], opponent_score = final_record[1])
        event_info = dict(event_id=final_record[2],final_score_id=final_record[3])
        return dict(event_info = event_info, score = score)

    def mapEventSeasonCollectionToDict(self,record):
        pass

    def mapEventAllStatsToDict(self,team_record,athlete_records,final_record):
        pass

#===========================//HANDLERS//==================================
#===========================//I.GETS//====================================

    ## @brief         Gets all the statistics for a given event and athlete.
    #
    #
    # @param		eID	The ID of the event of which statistics need to be fetched.
    # @param		aID	The ID of the athlete of which statistics need to be fetched
    #
    # @return
    #            A JSON containing all the statistics in the system for the specified event and athlete.
    #

    def getAllAthleteStatisticsByEventId(self,eID,aID):

        pass

    ## @brief         Gets all the statistics for a given event.
    #
    #
    # @param		eID	The ID of the event of which team statistics need to be fetched.
    #
    # @return
    #            A JSON containing all the team statistics in the system for the specified event.
    #

    def getAllTeamStatisticsByEventId(self,eID):

        pass

    #New: get the final score only
    ## @brief         Gets the final score a given event.
    #
    #        Calls the  Final Score DAO to get event final score and maps the result to
    #        to a JSON that contains the final score for that event in the system. That
    #        JSON object is then returned.
    #
    #
    # @param		eID	The ID of the event of whichthe final score need to be fetched.
    #
    # @return
    #            A JSON containing the final score in the system for the specified event.
    #

    def getFinalScore(self,eID):

        #validate existing event
        e_dao = EventDAO()
        try:
            event = e_dao.getEventByID(eID)
            if not event:
                return jsonify(Error = "Event for ID:{} not found.".format(eID)),400
        except:
            return jsonify(ERROR="Unable to verify event from DAO."), 500

        dao = FinalScoreDAO()
        #get final score
        try:
            final_score_result = dao.getFinalScore(eID)
            if not final_score_result:
                return jsonify(Error = "Event Final Score not found for the event: {}.".format(eID)),404
            mappedResult = self.mapFinalScoreToDict(final_score_result)
        except:
            return jsonify(ERROR="Unable to verify final score from DAO."), 500

        return jsonify(Event_Final_Score = mappedResult),200



    ## @brief         Gets all the statistics for a given athlete during a given season.
    #
    #
    # @param		seasonYear	the season year of which statistics need to be fetched
    # @param		aID	The ID of the athlete of which statistics need to be fetched
    #
    # @return
    #            A JSON containing all the statistics in the system for the specified athlete and season year.
    #

    def getAllAthleteStatisticsPerSeason(self,aID,seasonYear):

        pass

    #NEW
    ## @brief         Gets the aggregated statistics for a given athlete and season.
    #
    #        This function uses and ID and a year number to perform a query to the database
    #        that gets the aggregated statistics in the system that match the given ID and season year.
    #
    #
    # @param		aID	The ID of the athlete of which statistics need to be fetched.
    # @param		seasonYear	the season year of which statistics need to be fetched.
    #
    #
    # @return
    #            A list containing the response to the database query
    #            containing the aggregated statistics in the system containing
    #            the matching record for the given ID and season year.
    #

    def getAggregatedAthleteStatisticsPerSeason(self,aID,seasonYear):
        pass
    #NEW
    ## @brief         Gets all the aggregated statistics for a given athlete and season.
    #
    #        This function uses and ID and a year number to perform a query to the database
    #        that gets the aggregated statistics in the system that match the given ID and season year.
    #
    #
    # @param		sID	the sport id for the basketball branch of which statistics need to be fetched
    # @param		seasonYear	the season year of which statistics need to be fetched.
    #
    #
    # @return
    #            A list containing the response to the database query
    #            containing all the aggregated statistics in the system containing
    #            the matching record for the season year.
    #

    def getAllAggregatedAthleteStatisticsPerSeason(self,sID,seasonYear):
        pass

    #NEW
    ## @brief         Gets the aggregated team statistics for a given athlete and season.
    #
    #        This function uses and ID and a year number to perform a query to the database
    #        that gets the aggregated statistics in the system that match the given ID and season year.
    #
    #
    # @param		sID	The ID of the sport of which statistics need to be fetched.
    # @param		seasonYear	the season year of which statistics need to be fetched.
    #
    #
    # @return
    #            A list containing the response to the database query
    #            containing the aggregated team statistics in the system containing
    #            the matching record for the given ID and season year.
    #

    def getAggregatedTeamStatisticsPerSeason(self,sID,seasonYear):
        pass

    #NEW get ALL the statistics for a given event be it team or individual
    ## @brief         Gets all the team and individual statistics for a given event.
    #
    #
    # @param		eID	The ID of the event of which statistics need to be fetched
    #
    # @return
    #            A JSON containing all the statistics in the system for the specified event.
    #

    def getAllStatisticsByEventID(self,eID):

        pass

#===========================//II.POSTS//====================================
    ## @brief         Adds a new statistics record with the provided information.
    #
    #
    # @param		eID	the ID of the event for which the statistics record will be added.
    # @param		aID	the ID of the athlete for which the statistics record will be added.
    # @param		attributes	sports specific statistics
    # @return
    #            A JSON containing the id for the new Sport Event record.
    #

    def addStatistics(self,eID,aID,attributes): # Instantiates a sports-specific Event DAO in order to complete the desired post request and it returns a JSON with either a confirmation or error message.

        pass

    #NEW
    ## @brief         Adds a new team statistics record with the provided information.
    #
    #
    # @param		eID	the ID of the event for which the statistics record will be added.
    #
    ## @property		points
    # number of points scored by the athlete in the event.
    ## @property		rebounds
    # number of rebounds attained by the athlete in the event.
    ## @property		assists
    # number of assists attained by the athlete in the event.
    ## @property		steals
    # number of steals attained by the athlete in the event.
    ## @property		blocks
    # number of blocks attained by the athlete in the event.
    ## @property		turnovers
    # number of turnovers attained by the athlete in the event.
    ## @property		fieldGoalAttempt
    # number of field goal attempts attained by the athlete in the event.
    ## @property		successfulFieldGoal
    # number of successful field goals attained by the athlete in the event.
    ## @property		threePointAttempt
    # number of three point attempts attained by the athlete in the event.
    ## @property		successfulThreePoint
    # number of successful three point shots attained by the athlete in the event.
    ## @property		freeThrowAttempt
    # number of free throw attempts attained by the athlete in the event.
    ## @property		successfulFreeThrow
    # number of successful free throws attained by the athlete in the event.
    #
    # @return
    #            A JSON containing the id for the new Sport Event team statistics record.
    #

    def addTeamStatistics(self,eID,attributes): # Instantiates a sports-specific Event DAO in order to complete the desired post request and it returns a JSON with either a confirmation or error message.

        pass

    #NEW
    ## @brief         Adds a new team statistics record with the provided information and an aggregate of existing information.
    #
    #
    # @param		eID	the ID of the event for which the statistics record will be added.
    #
    # @return
    #            A JSON containing  the id for the new Sport Event team statistics record.
    #

    def addTeamStatisticsAuto(self,eID): # Instantiates a sports-specific Event DAO in order to complete the desired post request and it returns a JSON with either a confirmation or error message.

        pass

    #NEW
    ## @brief         Adds a new final score record with the provided information.
    #
    #        Calls the FinalScoreDAO to add a final score record and maps the result to
    #        to a JSON that contains the desired record. That JSON object
    #        is then returned.
    #
    #
    # @param		eID	the ID of the event for which the final score will be added.
    #
    ## @property		uprm_score
    # the final score of the local uprm team
    ## @property		opponent_Score
    # the final score of the opponent
    #
    #
    # @return
    #            A JSON containing the final score id for the new Final Score entry
    #

    def addFinalScore(self,eID,attributes): # Instantiates a sports-specific Event DAO in order to complete the desired post request and it returns a JSON with either a confirmation or error message.

        # Validate Avoid Duplication
        dao = FinalScoreDAO()
        try:
            if dao.getFinalScore(eID):
                return jsonify(Error = "Event Final Score Entry already exists for Event ID:{}".format(eID)),400
        except:
            return jsonify(ERROR="Unable to verify final score from DAO."), 500

        # Validate existing event
        e_dao = EventDAO()
        try:
            event = e_dao.getEventByID(eID)
            if not event:
                return jsonify(Error = "Event for ID:{} not found.".format(eID)),400
        except:
            return jsonify(ERROR="Unable to verify event from DAO."), 500

        invalid_duplicate = False
        try:
            if dao.getFinalScoreInvalid(eID):
                invalid_duplicate = True
        except:
            return jsonify(ERROR="Unable to verify final score from DAO."), 500

        #case with previously existing invalid entry, in that case update that entry
        if invalid_duplicate:
            try:
                result = dao.editFinalScore(eID,attributes['uprm_score'],attributes['opponent_score'])
                if not result:
                    return jsonify(Error = "Final Score Record not found for event id:{}.".format(eID)),404
                mappedResult = self.mapFinalScoreToDict(result)
            except:
                return jsonify(ERROR="Unable to verify final score from DAO."), 500

            dao.commitChanges()
            return jsonify(Event_Final_Score = mappedResult),200
        else:
        # Create and Validate new Final Score entry final score
            try:
                result = dao.addFinalScore(eID,attributes['uprm_score'],attributes['opponent_score'])
                if not result:
                    return jsonify(Error = "Problem inserting new final score record."),500
            except:
                return jsonify(ERROR="Unable to verify final score from DAO."), 500
            dao.commitChanges()
            return jsonify(Event_Final_Score = "Added new final score record with id:{} for event id:{}.".format(result,eID)),201

    #NEW: the mega query
    ## @brief         Adds new statistics records with the provided information.
    #
    #
    # @param		eID	the ID of the event for which the statistics record will be added.
    # @param		team_statistics	the IDs of the athletes for which the statistics record will be added.
    #
    # @par Athlete Statistics
    # 	athlete_id	the id for which the athlete statistics will be added for
    #                    sport-specific stats
    # 	team_statistis	sports-specific stats
    # 	uprm_score	the final score for the local uprm team
    # 	opponent_score	the final score for the opponent team
    #
    #
    # @return
    #            A JSON the id for the new Sport Event record.
    #

    def addAllEventStatistics(self,eID,attributes):
        pass


#===========================//III.PUTS//====================================

    ## @brief         Updates the statistics for the Sport event with the given IDs.
    #
    #
    # @param		eID	the ID of the event for which the statistics record will be updated.
    # @param		aID	the ID of the athlete for which the statistics record will be updated.
    # @param		attributes	sports-specific statistics
    #
    # @return
    #            A JSON containing all the user with the updated entry.
    #

    def editStatistics(self,eID,aID,attributes): # Instantiates a sports-specific Event DAO in order to complete the desired put request and it returns a JSON with either a confirmation or error message.

        pass

    ## @brief         Updates the team statistics for the Sport event with the given ID and aggregates of existing data.
    #
    #
    # @param		eID	the ID of the event for which the statistics record will be updated.
    #
    #
    # @return
    #            A JSON containing all the user with the updated entry.
    #

    def editTeamStatistics(self,eID): # Instantiates a sports-specific Event DAO in order to complete the desired put request and it returns a JSON with either a confirmation or error message.

    #NEW
    ## @brief         Updates the final score  the basketball event with the given ID .
    #
    #        Calls the FinalScoreDAO to update the final score of a basketball event. It then
    #        maps the result to a JSON that contains the desired record. That JSON
    #        object is then returned.
    #
    #
    # @param		eID	the ID of the event for which the final score record will be updated.
    #
    ## @property		uprm_score
    # the score of the local uprm team
    ## @property		opponent_score
    # the score of the opponent team
    #
    #
    # @return
    #            A JSON containing the final score with the updated entry.
    #

    def editFinalScore(self, eID, attributes): # Instantiates a sport-specific Event DAO in order to complete the desired put request and it returns a JSON with either a confirmation or error message.
        # Validate Exists so can update
        dao = FinalScoreDAO()
        try:
            if not dao.getFinalScore(eID):
                return jsonify(Error = "Event Final Score Entry does not exist for Event ID:{}".format(eID)),400
        except:
            return jsonify(ERROR="Unable to verify final score from DAO."), 500

        # Validate existing event
        e_dao = EventDAO()
        try:
            event = e_dao.getEventByID(eID)
            if not event:
                return jsonify(Error = "Event for ID:{} not found.".format(eID)),400
        except:
            return jsonify(ERROR="Unable to verify event from DAO."), 500


        # Update and Validate event final score, format returnable
        try:
            result = dao.editFinalScore(eID,attributes['uprm_score'],attributes['opponent_score'])
            if not result:
                return jsonify(Error = "Final Score Record not found for event id:{}.".format(eID)),404
            mappedResult = self.mapFinalScoreToDict(result)
        except:
            return jsonify(ERROR="Unable to verify final score from DAO."), 500

        dao.commitChanges()
        return jsonify(Event_Final_Score = mappedResult),200

#===========================//IV.REMOVE//====================================
    ## @brief         Invalidates a statistics record in the database based on the given IDs.
    #
    #
    # @param		eID	the ID of the event for which the statistics record will be invalidated.
    # @param		aID	the ID of the athlete for which the statistics record will be invalidated.
    #
    # @return
    #            A JSON containing the id of the invalidated record.
    #

    def removeStatistics(self,eID,aID): # Instantiates a sports-specific Event DAO in order to complete the desired put request and it returns a JSON with either a confirmation or error message.

        pass

    #NEW
    ## @brief         Invalidates a team statistics record in the database based on the given ID.
    #
    #
    # @param		eID	the ID of the event for which the statistics record will be invalidated.
    #
    # @return
    #            A JSON the id of the invalidated sports-specific Event.
    #

    def removeTeamStatistics(self,eID): # Instantiates a sports-specific Event DAO in order to complete the desired put request and it returns a JSON with either a confirmation or error message.

        pass

    # NEW
    ## @brief         Invalidates a final_score record in the database based on the given ID.
    #
    #        Calls the FinalScoreDAO to invalidate a final score record. It then
    #        maps the result to a JSON that contains the desired record. That JSON
    #        object is then returned.
    #
    #
    # @param		eID	the ID of the event for which the final score will be invalidated.
    #
    # @return
    #            A JSON containing the final score  id of the invalidated value
    #

    def removeFinalScore(self,eID): # Instantiates a Final Score DAO in order to complete the desired put request and it returns a JSON with either a confirmation or error message.

        # Validate existing event
        e_dao = EventDAO()
        try:
            event = e_dao.getEventByID(eID)
            if not event:
                return jsonify(Error = "Event for ID:{} not found.".format(eID)),400
        except:
            return jsonify(ERROR="Unable to verify event from DAO."), 500


        # Remove Basketball_Event final score and format returnabe
        dao = FinalScoreDAO()
        try:
            result = dao.removeFinalScore(eID)
            if not result:
                return jsonify(Error = "Final Score Record not found with event id:{}.".format(eID)),404
        except:
            return jsonify(ERROR="Unable to verify final score from DAO."), 500

        dao.commitChanges()
        return jsonify(Event_Final_Score = "Removed final score record with id:{} for event id:{}.".format(result,eID)),200





