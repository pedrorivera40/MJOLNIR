from flask import jsonify
from .dao.event_dao import EventDAO

class EventHandler:


    #        Converts an event record returned by the Event DAO into a dictionary
    #        and returns it.
    #
    #        Creates a result dictionary an then maps the values from the record
    #        list into the dictionary before sending it to the caller.
    #
    #
    # @param		record	An event record in the database with event information
    # @return
    #            A dictionay with the event information in the record list given
    #            mapped in it.
    #

    def mapEventToDict(self,record):
        result = {}
        result['id'] = record[0]
        result['event_date'] = record[1]
        result['is_local'] = record[2]
        result['venue'] = record[3]
        result['team_id'] = record[4]
        result['opponent_name'] = record[5]
        result['event_summary'] = record[6]
        result['sport_name'] = record[7]
        result['sport_img_url'] = record[8]
        result['branch'] = record[9]
        result['team_season_year'] = record[10]

        if 'Voleibol' in record[7]:
            result['hasPBP'] = self._pbp_exists(record[0])

        return result

    #        Converts  an event record returned by the Event DAO into a dictionary
    #        and returns it.This dictionary will dictionary will contain the local
    #        and opponent scores of an a event if they have them.
    #
    #        Creates a result dictionary an then maps the values from the record
    #        list into the dictionary before sending it to the caller. This dictonary
    #        will contain the local and opponent scores of an event if the record has
    #        them.
    #
    #
    # @param		record	An event record in the database with event information along with
    #                    local an opponent scores for an event if it exists.
    # @return
    #            A dictionay with the basic athlete information in the records list given as well
    #            as athlete positions and categories, if the records list has them, mapped in it.
    #

    def mapEventWithScoresToDict(self,record):
        result = {}
        result['id'] = record[0]
        result['event_date'] = record[1]
        result['is_local'] = record[2]
        result['venue'] = record[3]
        result['team_id'] = record[4]
        result['opponent_name'] = record[5]
        result['event_summary'] = record[6]
        result['sport_name'] = record[7]
        result['sport_img_url'] = record[8]
        result['branch'] = record[9]
        result['local_score'] = record[10]
        result['opponent_score'] = record[11]

        if 'Voleibol' in record[7]:
            result['hasPBP'] = self._pbp_exists(record[0])

        return result

    ## @brief         Gets all events in the database.
    #
    #        Calls the EventDAO to get a list of all the
    #        event records in the database and maps the result
    #        to a JSON that contains all those valid events.
    #        The JSON object is then returned to the caller.
    #
    # @return
    #            A JSON containing all the valid events in the
    # @return		            database.
    #

    def getAllEvents(self):

        try:
            result = EventDAO().getAllEvents()
            if not result:
                return jsonify(Error = "No events were found."),400
            mappedResult = []
            for event in result:
                mappedResult.append(self.mapEventWithScoresToDict(event))
            return jsonify(Events = mappedResult),200

        except:
            return jsonify(Error = "An error ocurred when fetching all the events in the system."),400


    ## @brief         Gets all athletes belonging to a specific sport.
    #
    #        Calls the EventDAO to get a list of all event records
    #        in which a specific team is a participant and maps the result
    #        to a JSON that contains all those valid events in the
    #        system. The JSON objects is then returned to the caller.
    #
    #
    # @param		tID	The id of the team that is a participant
    #                 in the events to be given.
    #
    # @return
    #            A JSON containing all valid events that have the team
    #            identified by the id given as a participant.
    #

    def getEventsByTeam(self,tID):
        if not isinstance(tID,int):
            return jsonify(Error = "Bad arguments in request"),400
        try:
            result = EventDAO().getEventsByTeam(tID)
            if isinstance(result,str):
                return jsonify(Error = result),400
            mappedResult = []
            for event in result:
                mappedResult.append(self.mapEventWithScoresToDict(event))
            return jsonify(Events = mappedResult),200
        except:
            return jsonify(Error = "A problem ocurred when getting the events of a team."),400

    ## @brief         Gets a specified event by their id.
    #
    #        Calls the EventDAO to get an event by their id
    #        and maps the result to a JSON that contains the desired
    #        record. The JSON object is then returned to the caller.
    #
    #
    # @param		eID	The id of the event that needs to be fetched.
    #
    # @return
    #            A JSON containing the event with the given id.
    #
    #

    def getEventByID(self,eID):
        if not isinstance(eID,int):
            return jsonify(Error = "Bad arguments in request"),400
        try:
            result = EventDAO().getEventByID(eID)
            if isinstance(result,str):
                return jsonify(Error = result),400
            mappedResult = self.mapEventToDict(result)

            return jsonify(Event = mappedResult),200
        except:
            return jsonify(Error = "A problem ocurred when getting an event by its id."),400


    ## @brief         Adds a new event for a team with the information given.
    #
    #        Calls a EventDAO to add a new event and maps the
    #        result to a JSON object that contains the id of the newly added
    #        event.
    #
    #
    # @param		tID	The id of the team that will participate in the event.
    # @param		attributes	A list containing the attributes of the event to
    #                        be added.
    # @return
    #            A JSON object containing the id of the newly added event.
    #
    #

    def addEvent(self,tID,attributes):
        if not isinstance(tID,int) or not isinstance(attributes,list):
            return jsonify(Error = "Bad arguments in request"),400

        try:

            attributesValidation = self.validateAttributes(attributes)

            if isinstance(attributesValidation,str):
                return jsonify(Error = attributesValidation),400

            result = EventDAO().addEvent(tID,attributes[0],attributes[1],attributes[2],attributes[3],attributes[4])

            if isinstance(result,str):
                return jsonify(Error = result),400

            return jsonify(Event = "Added event with id: {}".format(result)),201

        except:
            return jsonify("A problem ocurred when adding an event."),400

    #        Edits the attributes of an existing and valid event record with
    #        the given id.
    #
    #        Calls the EventDAO to edit the athlete record. It then maps the result
    #        to a JSON that contains the desirerd record. The JSON object created is
    #        then returned to the caller.
    #
    #
    # @param		eID	The id of the event that is going to be edited.
    # @param		attributes	The new attributes of the event to be edited.
    #
    # @return
    #            A JSON object containing the information of the edited event.
    #

    def editEvent(self,eID,attributes):
        if not isinstance(eID,int) or not isinstance(attributes,list):
            return jsonify(Error = "Bad arguments in request"),400

        try:

            attributesValidation = self.validateAttributes(attributes)

            if isinstance(attributesValidation,str):
                return jsonify(Error = attributesValidation),400

            result = EventDAO().editEvent(eID,attributes[0],attributes[1],attributes[2],attributes[3],attributes[4])

            if isinstance(result,str):
                return jsonify(Error = result),400

            return jsonify(Event = "Edited event with id: {}".format(result)),200

        except:
            return jsonify("A problem ocurred when editing an event."),400


    ## @brief         Invalidates an event in the database.
    #
    #        Call the EventDAO to invalidate the event record. It then
    #        maps the result to a JSON object that contains the id of the
    #        invalidated event. The JSON object is then returned to the caller.
    #
    #
    # @param		eID	The id of the event to be invalidated.
    #
    # @return
    #            A JSON containing the id of the invalidated event.
    #

    def removeEvent(self,eID):
        if not isinstance(eID,int):
            return jsonify(Error = "Bad arguments were given."),400
        try:
            result = EventDAO().removeEvent(eID)

            if isinstance(result,str):
                return jsonify(Error = result),400

            return jsonify(Event = "Removed event with id:{}".format(result)),200

        except:
            return jsonify("A problem ocurred when removing an event."),400

    #        Validates the attributes list given for the addEvent() and editEvent()
    #        functions.
    #
    #
    # @param		attributes	A list containing the attributes of an event to be added or
    # @param		                        edited.
    # @return
    #            A string with an error message if the validation fails an integer otherwise.
    #

    def validateAttributes(self,attributes):
        if len(attributes) != 5:
            return "Incorrect length of attributes were given."
        try:
            eventDate = attributes[0]
            isLocal = attributes[1]
            venue = attributes[2]
            opponentName = attributes[3]
            eventSummary = attributes[4]

            if not eventDate or not isinstance(eventDate,str):
                return "Invalid date given."

            if not isLocal or isinstance(isLocal,bool):
                return "Invalid locality given."

            if venue and not isinstance(venue,str):
                return "Invalid venue given."

            if opponentName and not isinstance(opponentName,str):
                return "Invalid opponent name given."

            if eventSummary and not isinstance(eventSummary,str) and len(eventSummary)>250:
                return "Invalid opponent color given."

            return 1

        except:
            return "Bad argument keys were given."

    #        Mock function of the on found in PBP DAO
    #        using it to return true if a volleyball event
    #        identified by their id has a pbp sequence.
    #
    #
    # @param		eID	The id of the volleyball event.
    # @return
    #            True if the id matches a predefined one, False otherwise
    #
    #
    # @protected

    def _pbp_exists(self,eID):

        if eID == 7:
            return True
        else:
            return False













