

class EventDAO:
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
        
        return []
    
    def getEventsByTeam(self,tID):
        """
        """
        return []

    def getEventByID(self,eID):
        return []

    def getEventTeamByID(self,eID):
        """
        """
        tID = None

        return tID

    def addEvent(self,tID,eventDate,venue,isLocal,opponentName,opponentColor):
        """
        """
        return 1
       
    def editEvent(self,eID,eventDate,venue,isLocal,opponentName,opponentColor):
        """
        """
        return 1
    
    def removeEvent(self,eID):
        """
        """
        return 1