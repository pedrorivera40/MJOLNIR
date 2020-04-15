from .config.sqlconfig import db_config
from flask import jsonify
import psycopg2


class EventDAO:

    def __init__(self):
        connection_url = "dbname={} user={} password={} host ={} ".format(
        db_config['database'],
        db_config['username'],
        db_config['password'],
        db_config['host']
        )

        self.conn = psycopg2.connect(connection_url)#Establish a connection with the relational database.

    ## @brief         Gets all events in the database.
    #
    #        Performs a query on the database in order to get all
    #        valid events in the database. It returns a list of the
    #        of the events with their information including their
    #        sport, branch. It will also include the scores of an
    #        event if they exist.
    # @return
    #            A list containing  all te valid events in the
    #            database  with their information.
    #

    def getAllEvents(self):
        cursor = self.conn.cursor()

        query = """select E.id,E.event_date,E.is_local,E.venue,E.team_id,E.opponent_name,E.event_summary,S.name,S.sport_image_url,B.name,F.local_score,F.opponent_score
                   from (event as E inner join ((sport as S inner join branch as B on S.branch_id=B.id) inner join team as T on S.id=T.sport_id) on E.team_id=T.id) full outer join final_score as F on F.event_id=E.id
                   where E.is_invalid=false
                   and T.is_invalid=false
                   and (F.is_invalid=false
                   or F.is_invalid is null)
                """
        try:
            cursor.execute(query)
            result = []#Will contain the event records
            for row in cursor:
                result.append(row)

            if not result:#No valid event exist
                return "There are no valid events."

            return result
        except:
            return "A problem ocurred when fetching all events."


    #        Gets all the events in the database of a
    #        team by their id.
    #
    #        Performs a query on the database in order to fetch
    #        all valid events of a team by their id. It returns
    #        a list containing all the valid events of the team.
    #
    #
    # @param		tID	The id of the team participating in the events.
    #
    # @return
    #            A list containing the all of the valid events in
    #            the database that have the team identified by their
    #            id as a participant.
    #

    def getEventsByTeam(self,tID):
        cursor = self.conn.cursor()
        query = """select E.id,E.event_date,E.is_local,E.venue,E.team_id,E.opponent_name,E.event_summary,S.name,S.sport_image_url,B.name,F.local_score,F.opponent_score
                   from (event as E inner join ((sport as S inner join branch as B on S.branch_id=B.id) inner join team as T on S.id=T.sport_id) on E.team_id=T.id) full outer join final_score as F on F.event_id=E.id
                   where E.is_invalid=false
                   and T.is_invalid=false
                   and E.team_id=%s
                   and (F.is_invalid=false
                   or F.is_invalid is null)
                """
        try:
            cursor.execute(query,(tID,))
            result = []#Will contain the event records
            for row in cursor:
                result.append(row)

            if not result:#No valid event exist
                return "There are no valid events for that team."

            return result
        except:
            return "A problem ocurred when fetching the events of a team."

    #        Gets a single event in the database by the
    #        id of the event given.
    #
    #        Performs a query on the database in order to fetch
    #        a valid event in the database by the id given.
    #
    #
    # @param		eID	The id of the event to be fetched.
    # @return
    #            A list containing the information of the event in
    #            the database that has the id given.
    #

    def getEventByID(self,eID):
        cursor = self.conn.cursor()
        query = """select E.id,E.event_date,E.is_local,E.venue,E.team_id,E.opponent_name,E.event_summary,S.name,S.sport_image_url,B.name,T.season_year
                   from (event as E inner join ((sport as S inner join branch as B on S.branch_id=B.id) inner join team as T on S.id=T.sport_id) on E.team_id=T.id)
                   where E.is_invalid=false
                   and T.is_invalid=false
                   and E.id=%s
                """
        try:
            cursor.execute(query,(eID,))
            result = cursor.fetchone()

            if not result:#No valid event exist
                return "The event does not exist."

            return result
        except:
            return "A problem ocurred when fetching the event."

    ## @brief         Returns the team id of an existing event.
    #
    #        Peforms a query in the database in order to
    #        get the id of the team participating in the
    #        event identified by the eID given. Then it
    #        returns the id of the team if the event is
    #        valid and it exists.
    #
    #
    # @param		eID	The id of the event.
    # @return
    #            The id of the team participating in the
    # @return		            event.
    #
    #

    def getEventTeamByID(self,eID):
        cursor =self.conn.cursor()
        query = """select T.id
                   from (event as E inner join ((sport as S inner join branch as B on S.branch_id=B.id) inner join team as T on S.id=T.sport_id) on E.team_id=T.id)
                   where E.is_invalid=false
                   and T.is_invalid=false
                   and E.id=%s
                """
        try:
            cursor.execute(query,(eID,))
            tID = cursor.fetchone()[0]

            return tID
        except:
            return "A problem ocurred when fetching the team id."

    ## @brief         Adds a new event into the database with the information given.
    #
    #        Uses the arguments given in order to perform an insert query on
    #        the database.Then it returns the id of the newly added event in
    #        the datase.
    #
    #
    # @param		tID	The id of the team participating in the event.
    # @param		eventDate	Date of the event.
    # @param		isLocal	Designates if the game is local.
    # @param		venue	The venue for the event.
    # @param		opponentName	The name of the opponent team.
    # @param		eventSummary	A summary of the event.
    # @return
    #            The id of the newly added event.
    #

    def addEvent(self,tID,eventDate,isLocal,venue,opponentName,eventSummary):
        cursor = self.conn.cursor()

        query = """insert into event(team_id,event_date,is_local,venue,opponent_name,event_summary,is_invalid)
                   values(%s,%s,%s,%s,%s,%s,false)
                   returning id;
                """

        try:
            cursor.execute(query,(tID,eventDate,isLocal,venue,opponentName,eventSummary,))
            eID = cursor.fetchone()[0]
            if not eID:
                return "Insert query failed."

            self.commitChanges()

            return eID
        except:
            return "A problem ocurred when inserting the event."



    ## @brief         Updates an existing event in the database.
    #
    #        Uses the arguments given in order to perform an update query on
    #        the database with the id of the edit given.Then it returns
    #        the id of the newly updated event in the datase.
    #
    #
    # @param		eID	The id of event to be updated.
    # @param		eventDate	Date of the event.
    # @param		isLocal	Designates if the game is local.
    # @param		venue	The venue for the event.
    # @param		opponentName	The name of the opponent team.
    # @param		eventSummary	A summary of the event.
    # @return
    #            The id of the newly updated event.
    #

    def editEvent(self,eID,eventDate,isLocal,venue,opponentName,eventSummary):
        cursor = self.conn.cursor()
        query = """update event
                   set event_date=%s,
                       is_local=%s,
                       venue=%s,
                       opponent_name=%s,
                       event_summary=%s
                   where id=%s
                   and is_invalid=false
                   returning id;
                """
        try:
            cursor.execute(query,(eventDate,isLocal,venue,opponentName,eventSummary,eID,))

            eid = cursor.fetchone()[0]

            if not eid:
                return "The update query failed."

            self.commitChanges()

            return eid
        except:
            return "A problem ocurred when updating the event."

    ## @brief         Invalidates an event on the database.
    #
    #        This method accepts the id of the event in order
    #        to set the is_invalid field to true in the database.
    #        This effectively acts as a removal of the event in
    #        from the system.
    #
    #
    # @param		eID	The id of the event to invalidate.
    # @param		        Returns
    #            The id of the updated event record.
    #

    def removeEvent(self,eID):

        cursor = self.conn.cursor()
        query = """update event
                   set is_invalid=true
                   where id=%s
                   returning id;
                """
        try:
            cursor.execute(query,(eID,))
            eid = cursor.fetchone()[0]

            if not eid:
                return "The update query failed."
            self.commitChanges()

            return eid
        except:
            return "A problem ocurred when updating the event."

    #        Commits the changes done on the database after
    #        insertion and update queries have been done on the
    #        database.
    #
    #        Uses the connection created when this EventDAO was
    #        instantiated to commit the changes performed on the datasase
    #        after insertion and update queries.
    #

    def commitChanges(self):

        self.conn.commit()
