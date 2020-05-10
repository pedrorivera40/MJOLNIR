from flask import jsonify
from .dao.event_dao import EventDAO
from .dao.pbp_dao import PBPDao
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
        result['sport_id'] = record[8]
        result['sport_img_url'] = record[9]
        result['branch'] = record[10]
        result['team_season_year'] = record[11]
        

        if 'Voleibol' in record[7]:
            result['hasPBP'] = self._check_pbp(record[0])

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
        result['team_season_year'] = record[10]
        result['local_score'] = record[11]
        result['opponent_score'] = record[12]

        if 'Voleibol' in record[7]:
            result['hasPBP'] = self._check_pbp(record[0])

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
        dao = None
        try:
            dao = EventDAO()
            result = dao.getAllEvents()
            if not result:
                dao._closeConnection()
                return jsonify(Error = "No existen eventos en el systema."),404
            mappedResult = []
            for event in result:
                mappedResult.append(self.mapEventWithScoresToDict(event))
            return jsonify(Events = mappedResult),200
            
        except Exception as e:
            print(e)
            if dao:
                dao._closeConnection()
            return jsonify(Error = "Occurrió un error interno tratando de recolectar todos los eventos."),500  
        
    
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
                return jsonify(Error = "Argumentos dados son incorrectos."),400
        except:
            return jsonify(Error = "Argumentos dados son incorrectos."),400        
        dao = None
        try:            
            dao = EventDAO()
            if not dao.teamExists(tID):
                dao._closeConnection()
                return jsonify(Error = "Equipo no existe con el identificador:{}".format(tID)),404

            result = dao.getEventsByTeam(tID)

            if isinstance(result,str):
                return jsonify(Error = result),500
            mappedResult = []
            for event in result:
                mappedResult.append(self.mapEventWithScoresToDict(event))
            return jsonify(Events = mappedResult),200
        except Exception as e:
            print(e)
            if dao:
                dao._closeConnection()
            return jsonify(Error = "Occurrió un error interno tratando de recolectar los eventos de un equipo."),500

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
                return jsonify(Error = "Argumentos dados son incorrectos."),400
        except:
            return jsonify(Error = "Argumentos dados son incorrectos."),400
        dao = None
        try:
            dao = EventDAO()
            if not dao.eventExists(eID):
                dao._closeConnection()
                return jsonify(Error = "Evento no existe con el identificador:{}".format(eID)),404

            result = dao.getEventByID(eID)

            if isinstance(result,str):
                return jsonify(Error = result),500

            mappedResult = self.mapEventToDict(result)

            return jsonify(Event = mappedResult),200
        except Exception as e:
            print(e) 
            if dao:
                dao._closeConnection()
            return jsonify(Error = "Occurrió un error interno tratando de recolectar un evento por su identificador."),500
    

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
                return jsonify(Error = "Argumentos dados son incorrectos."),400
        except:
            return jsonify(Error = "Argumentos dados son incorrectos."),400            
        dao = None
        try:   
            dao = EventDAO()
            attributesValidation = self.validateAttributes(attributes)

            if isinstance(attributesValidation,str):
                dao._closeConnection()
                return jsonify(Error = attributesValidation),400            
            
            if not dao.teamExists(tID):
                dao._closeConnection()
                return jsonify(Error = "Equipo no existe con el identificador:{}".format(tID)),404

            result = dao.addEvent(tID,attributes['event_date'],attributes['is_local'],attributes['venue'],attributes['opponent_name'],attributes['event_summary'])

            if isinstance(result,str):
                dao._closeConnection()
                return jsonify(Error = result),500

            event = dao.getEventByID(result)
            mappedEvent = self.mapEventToDict(event)

            return jsonify(Event =  mappedEvent),201
            
        except Exception as e:
            print(e)
            if dao:
                dao._closeConnection()
            return jsonify(Error = "Occurrió un error interno tratando de añadir un evento."),500
        
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
                return jsonify(Error = "Argumentos dados son incorrectos."),400
        except:
            return jsonify(Error = "Argumentos dados son incorrectos."),400

        dao = None
        try:  
            dao = EventDAO()            
            attributesValidation = self.validateAttributes(attributes)

            if isinstance(attributesValidation,str):
                dao._closeConnection()
                return jsonify(Error = attributesValidation),400
            
            
            if not dao.eventExists(eID):
                dao._closeConnection()
                return jsonify(Error = "Evento no existe con el identificador:{}".format(eID)),404

            result = dao.editEvent(eID,attributes['event_date'],attributes['is_local'],attributes['venue'],attributes['opponent_name'],attributes['event_summary'])

            if isinstance(result,str):
                dao._closeConnection()
                return jsonify(Error = result),500
            
            event = dao.getEventByID(result)
            mappedEvent = self.mapEventToDict(event)
                
            return jsonify(Event = mappedEvent),200
            
        except Exception as e:
            print(e)
            if dao:
                dao._closeConnection()            
            return jsonify(Error = "Occurrió un error interno tratando de editar un evento."),500
        
    
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
                return jsonify(Error = "Argumentos dados son incorrectos."),400
        except:
            return jsonify(Error = "Argumentos dados son incorrectos."),400   
        dao = None     
        try: 
            dao = EventDAO()           
            if not dao.eventExists(eID):
                dao._closeConnection()
                return jsonify(Error = "Evento no existe con el identificador:{}".format(eID)),404

            result = dao.removeEvent(eID)

            if isinstance(result,str):
                dao._closeConnection()
                return jsonify(Error = result),500

            return jsonify(Event = "Se removió el evento con el identificador:{}".format(result)),200

        except Exception as e:
            print(e)
            if dao:
                dao._closeConnection()
            return jsonify(Error = "Occurrió un error interno tratando de remover un evento."),500
    
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
                return "Fecha del evento dada es invalida."
            
            try:#Date format validation                    
                parse(eventDate)
            except:
                return "Fecha del evento dada es invalida."

            if isLocal == None or not isinstance(bool(isLocal),bool):                
                return "Localidad dada es invalida."

            if venue:
                if not isinstance(venue,str) or not re.search(cAlphaSpaceReg,venue):
                    return "Lugar del evento dado es invalido."

            if opponentName:
                if not isinstance(opponentName,str) or not re.search(cPhraseReg,opponentName):
                    return "Nombre del oponente dado es invalido."               

            if eventSummary:
                if not isinstance(eventSummary,str) or len(eventSummary)>250:
                    return "Resumen del evento dado es invalido."
            
            return 1

        except Exception as e:
            print(e)
            return "Bad arguments were given." 

    def _check_pbp(self,eID):
        """
        Will check the existance of a pbp sequence 
        for an event.

        Uses a PBPDao to determine the existance of
        a PBP sequence.

        Args:
            eID: The id of the event.
        Returns:
            True if pbp sequence exists, False otherwise
        """  
        
        try:
            return PBPDao().pbp_exists(eID)

        except Exception as e:
            print(e)
            return False
       

    
    
    

        
        
    




    