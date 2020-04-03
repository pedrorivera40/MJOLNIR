from .config.sqlconfig import db_config
from flask import jsonify
import psycopg2

class VolleyballEventDAO:


# athletes 70 and 71 play F Volleybal (12) on Teams 4 and 5. 


# getAllStatisticsByEventID(eID)//Return all statistics of a Volleyball Event event.
# getAllAthleteStatisticsByEventId(eID,aID)//Returns all of an Athlete statistics of a Volleyball Event for a given id.
# addStatistics(eID,aID,points,rebounds,assists,steals,blocks,turnovers,fieldGoalPe rcentage,threePointPercentage,freeThrowPercentage)//Adds a Volleyball Event record in the database and returns the id of the inserted record.
# editStatistics(eID,aID,points,rebounds,assists,steals,blocks,turnovers,fieldGoalPe rcentage,threePointPercentage,freeThrowPercentage)//Edits a Volleyball record in the database for a specific Athlete during an Event by the ids given and returns the updated record.
# removesStatistics(eID, aID)//Invalidates a Volleyball Event record on a database and it returns the invalidated record.
# commitChanges()//Commits changes on the database after an insertion or update query.
    def __init__(self):
        connection_url = "dbname={} user={} password={} host ={} ".format(
        db_config['database'],
        db_config['username'],
        db_config['password'],
        db_config['host']
        )
        self.conn = psycopg2.connect(connection_url)

#=============================//HELPERS//====================
    def getVolleyballEventID(self,eID,aID):
        """
        Checks if volleyball event exists.

        This function uses IDs to perform a query to the database
        that verifies if the Volleyball Event exists.

        Args:
            eID: The ID of the event 
            aID: The ID of the athlete
            
        Returns:
            The id of the volleyball event entry if it exists.
        """
        cursor = self.conn.cursor()
        query = """
                SELECT id
                FROM volleyball_event
                WHERE event_id = %s and athlete_id = %s and (is_invalid = false or is_invalid is Null);
                """
        cursor.execute(query,(int(eID),int(aID),))
        result = cursor.fetchone()
        return result
    
    def getVolleyballEventIDInvalid(self,eID,aID):
        """
        Checks if invalid volleyball event exists.

        This function uses IDs to perform a query to the database
        that verifies if the invalid Volleyball Event exists.

        Args:
            eID: The ID of the event 
            aID: The ID of the athlete
            
        Returns:
            The id of the invalid volleyball event entry if it exists.
        """
        cursor = self.conn.cursor()
        query = """
                SELECT id
                FROM volleyball_event
                WHERE event_id = %s and athlete_id = %s and (is_invalid = true);
                """
        cursor.execute(query,(int(eID),int(aID),))
        result = cursor.fetchone()
        return result
    
    def getVolleyballEventTeamStatsID(self,eID):
        """
        Checks if volleyball event team stats exist.

        This function uses IDs to perform a query to the database
        that verifies if the Volleyball Event exists.

        Args:
            eID: The ID of the event 
            
        Returns:
            The id of the volleyball event team stats entry if it exists.
        """
        cursor = self.conn.cursor()
        query = """
                SELECT id
                FROM volleyball_event_team_stats
                WHERE event_id = %s and (is_invalid = false or is_invalid is Null);
                """
        cursor.execute(query,(int(eID),))
        result = cursor.fetchone()
        #print(result)
        return result

    def getVolleyballEventTeamStatsIDInvalid(self,eID):
        """
        Checks if invalid volleyball event team stats exist.

        This function uses IDs to perform a query to the database
        that verifies if the invalid Volleyball Event exists.

        Args:
            eID: The ID of the event 
            
        Returns:
            The id of the invalid volleyball event team stats entry if it exists.
        """
        cursor = self.conn.cursor()
        query = """
                SELECT id
                FROM volleyball_event_team_stats
                WHERE event_id = %s and (is_invalid = true);
                """
        cursor.execute(query,(int(eID),))
        result = cursor.fetchone()
        #print(result)
        return result

    def getFinalScoreInvalid(self,eID):
        """
        Gets the invalid final score for a given event. 

        This function uses an ID to perform a query to the database
        that gets the invalid final score in the system that match the given ID.

        Args:
            eID: The ID of the event of final score need to be fetched.
            
        Returns:
           The id of the invalid event, if it exists. 
        """
        cursor = self.conn.cursor()
        query = """
                SELECT local_score, opponent_score, opponent_name, opponent_color, 
                event_id, id as final_score_id
                FROM final_score
                WHERE event_id = %s and 
                (is_invalid = true)
                """
        cursor.execute(query,(int(eID),))
        result = cursor.fetchone()
        return result

    
#=============================//GETS//=======================
    #NEW get the final score table detal
    def getFinalScore(self,eID):
        """
        Gets the final score for a given event. 

        This function uses an ID to perform a query to the database
        that gets the final score in the system that match the given ID.

        Args:
            eID: The ID of the event of final score need to be fetched.
            
        Returns:
            A list containing the response to the database query
            containing athe final score in the system containing 
            the matching record for the given ID.
        """
        cursor = self.conn.cursor()
        query = """
                SELECT local_score, opponent_score, opponent_name, opponent_color, 
                event_id, id as final_score_id
                FROM final_score
                WHERE event_id = %s and 
                (is_invalid = false or is_invalid is Null)
                """
        cursor.execute(query,(int(eID),))
        result = cursor.fetchone()
        return result
       
    def getAllStatisticsByEventID(self,eID):
        """
        Gets all the statistics per athlete for a given event. 

        This function uses an ID to perform a query to the database
        that gets all the statistics in the system that match the given ID.

        Args:
            eID: The ID of the event of which statistics need to be fetched.
            
        Returns:
            A list containing the response to the database query
            containing all the statistics in the system containing 
            the matching record for the given ID.
        """
        cursor = self.conn.cursor()
        #TODO: Confirm that's the info we want from athlete...
        #TODO: verify if need to check the joined column's is_invalid (And all the foreign keys)
        query = """
                SELECT
                athlete.id as athlete_id, athlete.first_name, athlete.middle_name, athlete.last_names, 
                athlete.number, athlete.profile_image_link,
                kill_points, attack_errors, assists, aces, service_errors, digs, blocks, blocking_errors,
                reception_errors,
                volleyball_event.event_id, volleyball_event.id as volleyball_event_id
                FROM volleyball_event
                INNER JOIN athlete ON athlete.id = volleyball_event.athlete_id
                WHERE event_id = %s and 
                (volleyball_event.is_invalid = false or volleyball_event.is_invalid is null);
                """
        #TODO: need to avoid sql injections. the use of  %s and just a non-validated string is dangerous. 
        cursor.execute(query,(int(eID),))        
        result = []
        for row in cursor:
            #print(row)
            result.append(row)
        return result 

    
    def getAllAthleteStatisticsByEventID(self,eID,aID):
        """
        Gets all the statistics for a given athlete and event. 

        This function uses two IDs to perform a query to the database
        that gets all the statistics in the system that match the given IDs.

        Args:
            eID: The ID of the event of which statistics need to be fetched.
            aID: The ID of the athlete of which statistics need to be fetched. 
            
            
        Returns:
            A list containing the response to the database query
            containing all the statistics in the system containing 
            the matching record for the given IDs.
        """
        cursor = self.conn.cursor()
        query = """
                SELECT
                kill_points, attack_errors, assists, aces, service_errors, digs, blocks, blocking_errors,
                reception_errors,
                volleyball_event.event_id, volleyball_event.id as volleyball_event_id, volleyball_event.athlete_id
                FROM volleyball_event
                WHERE event_id = %s and athlete_id = %s and 
                (volleyball_event.is_invalid = false or volleyball_event.is_invalid is null);
                """
        cursor.execute(query,(int(eID),int(aID),))
        result = cursor.fetchone()
        return result



    #NEW: given an event, get aggregate of team statistics
    def getAllTeamStatisticsByEventID(self,eID):
        """
        Gets the team statistics for a given event. 

        This function uses an ID to perform a query to the database
        that gets all the statistics in the system that match the given ID.

        Args:
            eID: The ID of the event of which team statistics need to be fetched.
            
            
        Returns:
            A list containing the response to the database query
            containing all the statistics in the system containing 
            the matching record for the given ID.
        """
        cursor = self.conn.cursor()
        query = """
                SELECT
                kill_points, attack_errors, assists, aces, service_errors, digs, blocks, blocking_errors,
                reception_errors,
                volleyball_event_team_stats.event_id, volleyball_event_team_stats.id as volleyball_event_team_stats_id
                FROM volleyball_event_team_stats
                WHERE event_id = %s  and 
                (volleyball_event_team_stats.is_invalid = false or volleyball_event_team_stats.is_invalid is null);
                """
        cursor.execute(query,(int(eID),))
        result = cursor.fetchone()
        return result


    
    #NEW : given team and athlete, return all statistics
    def getAllAthleteStatisticsPerSeason(self,aID,seasonYear):
        """
        Gets all the statistics for a given athlete and season. 

        This function uses and ID and a year number to perform a query to the database
        that gets all the statistics in the system that match the given ID and season year.

        Args:
            aID: The ID of the athlete of which statistics need to be fetched.
            seasonYear: the season year of which statistics need to be fetched.
            
            
        Returns:
            A list containing the response to the database query
            containing all the statistics in the system containing 
            the matching record for the given ID and season year.
        """
        cursor = self.conn.cursor()
        query = """
                SELECT
                event.id as event_id, event.event_date,
                kill_points, attack_errors, assists, aces, service_errors, digs, blocks, blocking_errors,
                reception_errors,
                volleyball_event.id as volleyball_event_id,
                volleyball_event.athlete_id
                FROM volleyball_event
                INNER JOIN event ON event.id = volleyball_event.event_id
                INNER JOIN team on team.id = event.team_id
                WHERE athlete_id = %s and team.season_year = %s and
                (volleyball_event.is_invalid = false or volleyball_event.is_invalid is null);
                """
        cursor.execute(query,(int(aID),int(seasonYear),))        
        result = []
        for row in cursor:
            #print(row)
            result.append(row)
        return result  
    

#=============================//POST//=======================
    
    # Need to validate: event exists. athlete belongs to team  that is tied to the event. 
    # needless to say, a bunch changes since these are more complex statistics...
    # TODO: need to update documentation, substitute percentages for success/attempt.
    def addStatistics(self,eID,aID,kill_points, attack_errors, assists, aces, service_errors, 
    digs, blocks, blocking_errors,reception_errors):
        """
        Adds a new volleyball event statistics record with the provided information.

        This function accepts two IDs and sports-specific statistics 
        to perform a query to the database that adds a new statistics record 
        to the system with the provided information.

        Args:
            eID: the ID of the event for which the statistics record will be added.
            aID: the ID of the athlete for which the statistics record will be added.
            kill_points:
            attack_errors:
            assists:
            aces:
            service_errors:
            digs:
            blocks:
            blocking_errors:
            reception_errors:
            
        Returns:
            A list containing the response to the database query
            containing the matching record for the new statistics entry. 
        """
        cursor = self.conn.cursor()
        query = """
                INSERT INTO volleyball_event(kill_points, attack_errors,
                assists, aces, service_errors, digs, blocks, blocking_errors,
                reception_errors,event_id,athlete_id,is_invalid)
                VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,false) returning id;
                """
        cursor.execute(query,(int(kill_points),int(attack_errors),int(assists),int(aces),int(service_errors),int(digs),int(blocks),
        int(blocking_errors),int(reception_errors),int(eID),int(aID),))
        sID = cursor.fetchone()[0]
        if not sID:
            return sID
        #self.commitChanges()
        return sID

    
    #NEW: add team statistics aggregate passed by parameter
    def addTeamStatistics(self,eID,kill_points, attack_errors, assists, aces, service_errors, 
    digs, blocks, blocking_errors,reception_errors):
        """
        Adds a new volleyball event team statistics record with the provided information.

        This function accepts an ID and sports-specific statistics 
        to perform a query to the database that adds a new team statistics record 
        to the system with the provided information.

        Args:
            eID: the ID of the event for which the team statistics record will be added.
            kill_points:
            attack_errors:
            assists:
            aces:
            service_errors:
            digs:
            blocks:
            blocking_errors:
            reception_errors:
            
        Returns:
            A list containing the response to the database query
            containing the matching record for the new team statistics entry. 
        """
        cursor = self.conn.cursor()
        query = """
                INSERT INTO volleyball_event_team_stats(kill_points, attack_errors,
                assists, aces, service_errors, digs, blocks, blocking_errors,
                reception_errors,event_id,is_invalid)
                VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,false) returning id;
                """
        cursor.execute(query,(int(kill_points),int(attack_errors),int(assists),int(aces),int(service_errors),int(digs),int(blocks),
        int(blocking_errors),int(reception_errors),int(eID),))
        tsID = cursor.fetchone()[0]
        if not tsID:
            return tsID
        #self.commitChanges()
        return tsID

    #NEW: add final score
    def addFinalScore(self,eID, local_score, opponent_score, opponent_name, opponent_color):
        """
        Adds a new volleyball event final score with the provided information.

        This function accepts an ID and score information 
        to perform a query to the database that adds a final score record 
        to the system with the provided information.

        Args:
            eID: the ID of the event for which the final score record will be added.
            local_score: the final score of the local team for the event
            opponent_score: the final score of the opponent team for the event
            opponent_name: name of the opponent team
            opponent_color: color to be used for opponent team
            
        Returns:
            A list containing the response to the database query
            containing the matching record for the new final record entry. 
        """
        cursor = self.conn.cursor()
        query = """
                INSERT INTO final_score(local_score,opponent_score,event_id,is_invalid,
                opponent_name, opponent_color)
                VALUES(%s,%s,%s,false,%s,%s) returning id;
                """
        cursor.execute(query,(int(local_score),int(opponent_score),int(eID),str(opponent_name),str(opponent_color),))
        fsID = cursor.fetchone()[0]
        if not fsID:
            return fsID
        #self.commitChanges()
        return fsID

    
    #NEW : aggregate statistics automatically and insert new team stats
    #TODO: name better. this method will take the aggregate and add the necessary team statistics
    def addTeamStatisticsAuto(self,eID):
        """
        Adds a new volleyball event team statistics record with provided and existing information.

        This function accepts an ID to perform a query to the database that adds a 
        new team statistics record to the system with the provided information and 
        an aggregate of existing information. 

        Args:
            eID: the ID of the event for which the statistics record will be added
            
        Returns:
            A list containing the response to the database query
            containing the matching record for the new statistics entry. 
        """
        cursor = self.conn.cursor()
        #the first query collects the aggregate
        #DONE: needed to add subquery so we only aggregate from the valid events :)
        query = """
                with valid_volleyball_events as
                (SELECT *
                FROM volleyball_event
                WHERE (is_invalid=false or is_invalid is null))
                select 
                sum(kill_points) as kill_points,sum(attack_errors) as attack_errors, sum(assists) as assists,sum(aces) as aces,
                sum(service_errors) as service_errors,sum(digs) as digs,sum(blocks) as blocks,
                sum(blocking_errors) as blocking_errors,sum(reception_errors) as reception_errors
                from valid_volleyball_events
                WHERE event_id = %s;
                """
        cursor.execute(query,(int(eID),))
        resultTeam = cursor.fetchone()
        #TODO: Add case of query failure?
        if not resultTeam:
            return resultTeam
        query = """
                INSERT INTO volleyball_event_team_stats(kill_points, attack_errors, assists, aces, service_errors, 
                digs, blocks, blocking_errors,reception_errors,event_id,is_invalid)
                VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,false) returning id;
                """
        cursor.execute(query,(int(resultTeam[0]),int(resultTeam[1]),int(resultTeam[2]),int(resultTeam[3]),
        int(resultTeam[4]),int(resultTeam[5]),int(resultTeam[6]),int(resultTeam[7]),int(resultTeam[8]),int(eID),))
        tsID = cursor.fetchone()[0]
        if not tsID:
            return tsID
        #self.commitChanges()
        return tsID

#=============================//PUTS//=======================

    #TODO: recal athlete will be validaded by handler
    def editStatistics(self,eID,aID,kill_points, attack_errors, assists, aces, service_errors, 
    digs, blocks, blocking_errors,reception_errors):
        """
        Updates the statistics for the volleyball event with the given IDs.

        This function accepts two IDs and sports specific statistics and uses them 
        to update the statistics in the record of the volleyball event with the 
        matching IDs.

        Args:
            eID: the ID of the event for which the statistics record will be updated.
            aID: the ID of the athlete for which the statistics record will be updated.
            kill_points:
            attack_errors:
            assists:
            aces:
            service_errors:
            digs:
            blocks:
            blocking_errors:
            reception_errors:
            
        Returns:
            A list containing the response to the database query
            containing the matching record for the modified volleyball
            event statistics.
        """
        #NEW: will also have to update the team statistics
        #TODO: update team statistic. simply call the outside dao?
        cursor = self.conn.cursor()
        query = """
                UPDATE volleyball_event
                SET kill_points = %s,
                    attack_errors = %s,
                    assists = %s,
                    aces = %s,
                    service_errors = %s,
                    digs = %s,
                    blocks = %s,
                    blocking_errors = %s,
                    reception_errors = %s,
                    is_invalid = false
                WHERE event_id = %s and athlete_id = %s 
                RETURNING
                    kill_points,
                    attack_errors,
                    assists,
                    aces,
                    service_errors,
                    digs,
                    blocks,
                    blocking_errors,
                    reception_errors,
                    volleyball_event.event_id, volleyball_event.id as volleyball_event_id, volleyball_event.athlete_id;

                """
        cursor.execute(query,(int(kill_points),int(attack_errors),int(assists),int(aces),int(service_errors),int(digs),int(blocks),
        int(blocking_errors),int(reception_errors),int(eID),int(aID),))
        result = cursor.fetchone()
        if not result:
            return result
        #self.commitChanges()
        return result

    #NEW: edit team statistics. automatically update based on aggregate. 
    def editTeamStatistics(self,eID):
        """
        Updates the statistics for the volleyball event with the given IDs.

        This function accepts an ID and uses it to automatically update the 
        team statistics in the record of the volleyball event team stats with 
        the matching ID based on an aggregate of existing statistics.

        Args:
            eID: the ID of the event for which the team statistics record will be updated
            
        Returns:
            A list containing the response to the database query
            containing the matching record for the modified volleyball
            event team statistics.
        """
        cursor = self.conn.cursor()
        #the first query collects the aggregate
        query = """
                with valid_volleyball_events as
                (SELECT *
                FROM volleyball_event
                WHERE (is_invalid=false or is_invalid is null))
                select 
                sum(kill_points) as kill_points,sum(attack_errors) as attack_errors, sum(assists) as assists,sum(aces) as aces,
                sum(service_errors) as service_errors,sum(digs) as digs,sum(blocks) as blocks,
                sum(blocking_errors) as blocking_errors,sum(reception_errors) as reception_errors
                from valid_volleyball_events
                WHERE event_id = %s;
                """
        cursor.execute(query,(int(eID),))
        resultTeam = cursor.fetchone()
        #TODO: Add case of query failure?
        if not resultTeam:
            return resultTeam
        #the second query updates the volleyball_event_team_stats based on aggregate results
        query = """
                UPDATE volleyball_event_team_stats
                SET kill_points = %s,
                    attack_errors = %s,
                    assists = %s,
                    aces = %s,
                    service_errors = %s,
                    digs = %s,
                    blocks = %s,
                    blocking_errors = %s,
                    reception_errors = %s,
                    is_invalid = false
                WHERE event_id = %s
                RETURNING
                    kill_points,
                    attack_errors,
                    assists,
                    aces,
                    service_errors,
                    digs,
                    blocks,
                    blocking_errors,
                    reception_errors,
                    volleyball_event_team_stats.event_id, volleyball_event_team_stats.id as volleyball_event_team_stats_id;

                """
        cursor.execute(query,(int(resultTeam[0]),int(resultTeam[1]),int(resultTeam[2]),int(resultTeam[3]),
        int(resultTeam[4]),int(resultTeam[5]),int(resultTeam[6]),int(resultTeam[7]),int(resultTeam[8]),
        int(eID),))
        result = cursor.fetchone()
        if not result:
            return result
        #self.commitChanges()
        return result

    #NEW: edit final score for an event 
    def editFinalScore(self,eID, local_score, opponent_score,opponent_name, opponent_color):
        """
        Updates the final score for the volleyball event with the given IDs.

        This function accepts an ID and the updated scores and uses them to update
        the final score entry of an event in the system

        Args:
            eID: the ID of the event for which the final score record will be updated
            local_score: the local score to be updated
            opponent_score: the opponent score to be updated
            opponent_name: name of the opponent team
            opponent_color: color to be used for opponent team
            
        Returns:
            A list containing the response to the database query
            containing the matching record for the modified volleyball
            event final score.
        """
        cursor = self.conn.cursor()
        query = """
                UPDATE final_score
                SET local_score = %s,
                    opponent_score = %s,
                    opponent_name = %s,
                    opponent_color = %s,
                    is_invalid = false
                WHERE event_id = %s 
                RETURNING
                    local_score,
                    opponent_score,
                    opponent_name,
                    opponent_color, 
                    event_id, 
                    id as final_score_id;
                """
        cursor.execute(query,(int(local_score),int(opponent_score),str(opponent_name),str(opponent_color),int(eID),))
        result = cursor.fetchone()
        if not result:
            return result
        #self.commitChanges()
        return result

#=============================//DELETE//=======================
     
    #TODO: in handler must call update team statistics (auto) after this. 
    def removeStatistics(self,eID,aID):
        """
        Invalidates a volleyball event statistics entry in the database.

        This function accepts two IDs and uses them to set the valid field
        within the database as invalid, this acts as a deletion of the 
        statistics entry from the system.

        Args:
            eID: The ID of the event for which the statistics will be invalidated.
            aID: The ID of the athlete for which the statistics will be invalidated.
            
        Returns:
            A list containing the response to the database query
            containing the matching record for the modified statistics entry.
        """
        cursor = self.conn.cursor()
        query = """
                UPDATE volleyball_event
                SET is_invalid = true
                WHERE event_id = %s  and athlete_id = %s
                RETURNING id;
                """
        cursor.execute(query,(int(eID),int(aID),))
        result = cursor.fetchone()
        if not result:
            return result
        #self.commitChanges()
        return result

    #NEW : remove team statistics
    def removeTeamStatistics(self,eID):
        """
        Invalidates a volleyball event team statistics entry in the database.

        This function accepts an ID and uses it to set the valid field
        within the database as invalid, this acts as a deletion of the 
        team statistics entry from the system.

        Args:
            eID: The ID of the event for which the team statistics will be invalidated.
            
        Returns:
            A list containing the response to the database query
            containing the matching record for the modified team 
            statistics entry.
        """
        cursor = self.conn.cursor()
        query = """
                UPDATE volleyball_event_team_stats
                SET is_invalid = true
                WHERE event_id = %s
                RETURNING id;
                """
        cursor.execute(query,(int(eID),))
        result = cursor.fetchone()
        if not result:
            return result
        #self.commitChanges()
        return result

    #NEW : remove final score
    def removeFinalScore(self,eID):
        """
        Invalidates a volleyball event final score entry in the database.

        This function accepts an ID and uses it to set the valid field
        within the database as invalid, this acts as a deletion of the 
        final score entry from the system.

        Args:
            eID: The ID of the event for which the final score will be invalidated.
            
        Returns:
            A list containing the response to the database query
            containing the matching record for the modified 
            final score entry.
        """
        cursor = self.conn.cursor()
        query = """
                UPDATE final_score
                SET is_invalid = true
                WHERE event_id = %s
                RETURNING id;
                """
        cursor.execute(query,(int(eID),))
        result = cursor.fetchone()
        if not result:
            return result
        #self.commitChanges()
        return result

    def commitChanges(self):
        self.conn.commit()

# #Launch app.
# if __name__ == '__main__':
#     dao = VolleyballEventDAO()
#     print(dao.getAllStatisticsByEventID(3))
