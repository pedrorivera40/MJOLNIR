from flask import jsonify
from .dao.event_dao import EventDAO
from dateutil.parser import parse
import re

class EventHandler:


    def mapEventToDict(self,record):
        """
        Converts an event record returned by the Event DAO into a dictionary 
        and returns it.

        Creates a result dictionary an then maps the values from the record 
        list into the dictionary before sending it to the caller.

        Args:
            record: An event record in the database with event information
        Returns:
            A dictionay with the event information in the record list given
            mapped in it.
        """
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

    def mapEventWithScoresToDict(self,record):
        """
        Converts  an event record returned by the Event DAO into a dictionary 
        and returns it.This dictionary will dictionary will contain the local
        and opponent scores of an a event if they have them.

        Creates a result dictionary an then maps the values from the record 
        list into the dictionary before sending it to the caller. This dictonary 
        will contain the local and opponent scores of an event if the record has
        them.
     
        Args:
            record: An event record in the database with event information along with
                    local an opponent scores for an event if it exists.
        Returns:
            A dictionay with the basic athlete information in the records list given as well
            as athlete positions and categories, if the records list has them, mapped in it.
        """
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

    def getAllEvents(self):
        """
        Gets all events in the database.

        Calls the EventDAO to get a list of all the
        event records in the database and maps the result
        to a JSON that contains all those valid events.
        The JSON object is then returned to the caller.

        Returns:
            A JSON containing all the valid events in the 
            database.
        """

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
        
    
    def getEventsByTeam(self,tID):
        """
        Gets all events belonging to a specific team.

        Calls the EventDAO to get a list of all event records
        in which a specific team is a participant and maps the result 
        to a JSON that contains all those valid events in the 
        system. The JSON objects is then returned to the caller.
        
        Args:
            tID: The id of the team that is a participant
                 in the events to be given.
        
        Returns:
            A JSON containing all valid events that have the team
            identified by the id given as a participant.
        """
        try:
            if not isinstance(int(tID),int) or tID < 0:
                return jsonify(Error = "Bad arguments in request"),400
        except:
            return jsonify(Error = "Bad arguments in request"),400
        try:
            dao = EventDAO()
            if not dao.teamExists(tID):
                return jsonify(Error = "Team does not exist with id:{}".format(tID)),404

            result = dao.getEventsByTeam(tID)

            if isinstance(result,str):
                return jsonify(Error = result),400
            mappedResult = []
            for event in result:
                mappedResult.append(self.mapEventWithScoresToDict(event))
            return jsonify(Events = mappedResult),200
        except:
            return jsonify(Error = "A problem ocurred when getting the events of a team."),400

    def getEventByID(self,eID):
        """
        Gets a specified event by their id.

        Calls the EventDAO to get an event by their id 
        and maps the result to a JSON that contains the desired 
        record. The JSON object is then returned to the caller.

        Args:
            eID: The id of the event that needs to be fetched.

        Returns:
            A JSON containing the event with the given id.

        """
        try:
            if not isinstance(int(eID),int) or eID < 0:
                return jsonify(Error = "Bad arguments in request"),400
        except:
            return jsonify(Error = "Bad arguments in request"),400

        try:
            dao = EventDAO()
            if not dao.eventExists(eID):
                return jsonify(Error = "Event does not exist with id:{}".format(eID)),404
            result = dao.getEventByID(eID)
            if isinstance(result,str):
                return jsonify(Error = result),400
            mappedResult = self.mapEventToDict(result)

            return jsonify(Event = mappedResult),200
        except:
            return jsonify(Error = "A problem ocurred when getting an event by its id."),400
    

    def addEvent(self,tID,attributes):
        """
        Adds a new event for a team with the information given.

        Calls a EventDAO to add a new event and maps the 
        result to a JSON object that contains the id of the newly added 
        event.

        Args:
            tID: The id of the team that will participate in the event.
            attributes: A list containing the attributes of the event to
                        be added.
        Returns:
            A JSON object containing the id of the newly added event.

        """
        try:
            if not isinstance(int(tID),int) or tID < 0 or not isinstance(attributes,dict):
                return jsonify(Error = "Bad arguments in request"),400
        except:
            return jsonify(Error = "Bad arguments in request"),400    
        try:   
            
            attributesValidation = self.validateAttributes(attributes)

            if isinstance(attributesValidation,str):
                return jsonify(Error = attributesValidation),400
            
            dao = EventDAO()
            if not dao.teamExists(tID):
                return jsonify(Error = "Team does not exist with id:{}".format(tID)),404

            result = dao.addEvent(tID,attributes['event_date'],attributes['is_local'],attributes['venue'],attributes['opponent_name'],attributes['event_summary'])

            if isinstance(result,str):
                return jsonify(Error = result),400

            return jsonify(Event = "Added event with id: {}".format(result)),201
            
        except:
            return jsonify("A problem ocurred when adding an event."),400
        
    def editEvent(self,eID,attributes):
        """
        Edits the attributes of an existing and valid event record with
        the given id.

        Calls the EventDAO to edit the athlete record. It then maps the result
        to a JSON that contains the desirerd record. The JSON object created is
        then returned to the caller.

        Args:
            eID: The id of the event that is going to be edited.
            attributes: The new attributes of the event to be edited.
        
        Returns:
            A JSON object containing the information of the edited event.
        """
        try:
            if not isinstance(int(eID),int) or eID < 0 or not isinstance(attributes,dict):
                return jsonify(Error = "Bad arguments in request"),400
        except:
            return jsonify(Error = "Bad arguments in request"),400

        try:   
            
            attributesValidation = self.validateAttributes(attributes)

            if isinstance(attributesValidation,str):
                return jsonify(Error = attributesValidation),400
            
            dao = EventDAO()
            if not dao.eventExists(eID):
                return jsonify(Error = "Event does not exist with id:{}".format(eID)),404

            result = dao.editEvent(eID,attributes['event_date'],attributes['is_local'],attributes['venue'],attributes['opponent_name'],attributes['event_summary'])

            if isinstance(result,str):
                return jsonify(Error = result),400
                
            return jsonify(Event = "Edited event with id: {}".format(result)),200
            
        except:
            return jsonify("A problem ocurred when editing an event."),400
        
    
    def removeEvent(self,eID):
        """
        Invalidates an event in the database. 

        Call the EventDAO to invalidate the event record. It then
        maps the result to a JSON object that contains the id of the 
        invalidated event. The JSON object is then returned to the caller.

        Args:
            eID: The id of the event to be invalidated.

        Returns:
            A JSON containing the id of the invalidated event.
        """
        try:
            if not isinstance(int(eID),int) or eID < 0:
                return jsonify(Error = "Bad arguments were given."),400
        except:
            return jsonify(Error = "Bad arguments in request"),400

        try:
            dao = EventDAO()
            if not dao.eventExists(eID):
                return jsonify(Error = "Event does not exist with id:{}".format(eID)),404

            result = dao.removeEvent(eID)

            if isinstance(result,str):
                return jsonify(Error = result),400

            return jsonify(Event = "Removed event with id:{}".format(result)),200

        except:
            return jsonify("A problem ocurred when removing an event."),400
    
    def validateAttributes(self,attributes):
        """
        Validates the attributes dictionary given for the addEvent() and editEvent()
        functions.

        Args:
            attributes: A dictionary containing the attributes of an event to be added or 
                        edited.
        Returns:
            A string with an error message if the validation fails an integer otherwise.        
        """
       
        try:
            eventDate = attributes['event_date']
            isLocal = attributes['is_local']
            venue = attributes['venue']            
            opponentName = attributes['opponent_name']
            eventSummary = attributes['event_summary'] 

            #Regular Expressions for input validation            
            phraseRegex = "^[a-zA-Z0-9- ',.;:!]*$"
            alphaSpaceRegex = "^[a-zA-Z ]*$"
            
            #Compiled Regular Expressions            
            cPhraseReg = re.compile(phraseRegex)
            cAlphaSpaceReg = re.compile(alphaSpaceRegex)

            if not eventDate or not isinstance(eventDate,str):
                return "Invalid date given."
            
            try:#Date format validation                    
                parse(eventDate)
            except:
                return "The event date given is not valid."

            if not isLocal or not isinstance(bool(isLocal),bool):
                return "Invalid locality given."

            if venue:
                if not isinstance(venue,str) or not re.search(cAlphaSpaceReg,venue):
                    return "Invalid venue given."

            if opponentName:
                if not isinstance(opponentName,str) or not re.search(cPhraseReg,opponentName):
                    return "Invalid opponent name given."               

            if eventSummary:
                if not isinstance(eventSummary,str) or len(eventSummary)>250:
                    return "Invalid event summary given."
            
            return 1

        except:
            return "Bad arguments were given." 

    def _pbp_exists(self,eID):
        """
        Mock function of the on found in PBP DAO
        using it to return true if a volleyball event
        identified by their id has a pbp sequence.

        Args:
            eID: The id of the volleyball event.
        Returns:
            True if the id matches a predefined one, False otherwise
        """  

        if eID == 7:
            return True
        else:
            return False

    
    
    

        
        
    




    