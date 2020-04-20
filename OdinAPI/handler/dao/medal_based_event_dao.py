from .config.sqlconfig import db_config
import psycopg2

#Constants
TENNIS_CIDM_SOLO=5
TENNIS_CIDM_DOUBLE=7
TENNIS_CIDF_SOLO=11
TENNIS_CIDF_DOUBLE=6
TABLE_TENNIS_CIDM_SOLO=3
TABLE_TENNIS_CIDM_DOUBLE=8
TABLE_TENNIS_CIDF_SOLO=10
TABLE_TENNIS_CIDF_DOUBLE=4

class MedalBasedEventDAO:

    def __init__(self):
        connection_url = "dbname={} user={} password={} host ={} ".format(
        db_config['database'],
        db_config['username'],
        db_config['password'],
        db_config['host']
        )
        self.conn = psycopg2.connect(connection_url)
    

    #=============================//HELPERS//====================
    def getMedalBasedEventID(self,eID,aID,cID):
        """
        Checks if medal_based event exists.

        This function uses IDs to perform a query to the database
        that verifies if the Medal Based Event exists.

        Args:
            eID: The ID of the event 
            aID: The ID of the athlete
            cID: The ID of the category
            
        Returns:
            The id of the medal_based event entry if it exists.
        """
        cursor = self.conn.cursor()
        query = """
                SELECT id
                FROM match_based_event
                WHERE event_id = %s and athlete_id = %s and category_id = %s and (is_invalid = false or is_invalid is Null);
                """
        cursor.execute(query,(int(eID),int(aID),cID,))
        result = cursor.fetchone()
        return result
    
    def getMedalBasedEventIDInvalid(self,eID,aID,cID):
        """
        Checks if invalid medal_based event exists.

        This function uses IDs to perform a query to the database
        that verifies if the invalid MedalBased Event exists.

        Args:
            eID: The ID of the event 
            aID: The ID of the athlete
            cID: The ID of the category
        Returns:
            The id of the invalid medal_based event entry if it exists.
        """
        cursor = self.conn.cursor()
        query = """
                SELECT id
                FROM medal_based_event
                WHERE event_id = %s and athlete_id = %s and category_id =%s and (is_invalid = true);
                """
        cursor.execute(query,(int(eID),int(aID),cID,))
        result = cursor.fetchone()
        return result
    
    def getMedalBasedEventTeamStatsID(self,eID,cID):
        """
        Checks if medal_based event team stats exist.

        This function uses IDs to perform a query to the database
        that verifies if the MedalBased Event exists.

        Args:
            eID: The ID of the event
            cID: The ID of the category of the event. 
            
        Returns:
            The id of the medal_based event team stats entry if it exists.
        """
        cursor = self.conn.cursor()
        query = """
                SELECT id
                FROM match_based_event_team_stats
                WHERE event_id = %s and category_id =%s and (is_invalid = false or is_invalid is Null);
                """
        cursor.execute(query,(eID,cID,))
        result = cursor.fetchone()
        #print(result)
        return result

    def getMedalBasedEventTeamStatsIDInvalid(self,eID,cID):
        """
        Checks if invalid medal_based event team stats exist.

        This function uses IDs to perform a query to the database
        that verifies if the invalid MedalBased Event exists.

        Args:
            eID: The ID of the event
            cID: The ID of the category of the event
            
        Returns:
            The id of the invalid medal_based event team stats entry if it exists.
        """
        cursor = self.conn.cursor()
        query = """
                SELECT id
                FROM match_based_event_team_stats
                WHERE event_id = %s and category_id=%s and (is_invalid = true);
                """
        cursor.execute(query,(eID,cID,))
        result = cursor.fetchone()
        #print(result)
        return result

    
#=============================//GETS//=======================
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
        query = """
                SELECT
                A.id as A_id, A.first_name, A.middle_name, A.last_names, 
                A.number, A.profile_image_link,M.matches_played,M.matches_won,C.name,               
                M.event_id, M.id as match_based_event_id
                FROM match_based_event as M INNER JOIN category as C ON M.category_id=C.id
                INNER JOIN athlete as A ON A.id = M.athlete_id
                WHERE event_id = %s and 
                (M.is_invalid = false or M.is_invalid is null);
                """
        
        cursor.execute(query,(eID,))        
        result = []
        for row in cursor:
            #print(row)
            result.append(row)
        return result 

    
    def getAllAthleteStatisticsByEventIdAndCategoryId(self,eID,aID,cID):
        """
        Gets all the statistics for a given athlete and event. 

        This function uses two IDs to perform a query to the database
        that gets all the statistics in the system that match the given IDs.

        Args:
            eID: The ID of the event of which statistics need to be fetched.
            aID: The ID of the athlete of which statistics need to be fetched.            
            cID: The ID of the category of which statistics need to be fetched. 
            
            
        Returns:
            A list containing the response to the database query
            containing all the statistics in the system containing 
            the matching record for the given IDs.
        """
        cursor = self.conn.cursor()
        query = """
                SELECT
                matches_played,matches_won,C.name,event_id,athlete_id,
                match_based_event.id as match_based_event_id
                FROM match_based_event INNER JOIN category as C ON match_based_event.category_id=C.id
                WHERE event_id = %s and athlete_id = %s and category_id=%s and 
                (match_based_event.is_invalid = false or match_based_event.is_invalid is null);
                """
        cursor.execute(query,(eID,aID,cID))
        result = cursor.fetchone()
        return result



    #NEW: given an event, get aggregate of team statistics
    def getAllTeamStatisticsByEventIdAndCategoryId(self,eID,cID):
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
                matches_played,matches_won,C.name,event_id,
                match_based_event_team_stats.id as match_based_event_team_stats_id,event.opponent_name
                FROM match_based_event_team_stats INNER JOIN category as C on match_based_event_team_stats.category_id=C.id INNER JOIN event on match_based_event_team_stats.event_id = event.id
                WHERE event_id = %s  and category_id = %s and
                (match_based_event_team_stats.is_invalid = false or match_based_event_team_stats.is_invalid is null);
                """
        cursor.execute(query,(eID,cID,))
        result = cursor.fetchone() 
                  
        if result:            
            if cID == TENNIS_CIDF_DOUBLE or cID == TENNIS_CIDM_DOUBLE or cID == TABLE_TENNIS_CIDF_DOUBLE or cID == TABLE_TENNIS_CIDM_DOUBLE:               
                result = list(result)
                result[0] = int(result[0]/2)
                result[1] = int(result[1]/2)
                result = tuple(result)
        return result


    
    
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
                matches_played,matches_won,C.name,
                match_based_event.id as match_based_event_id,
                match_based_event.athlete_id
                FROM match_based_event INNER JOIN category as C on match_based_event.category_id=C.id
                INNER JOIN event ON event.id = match_based_event.event_id
                INNER JOIN team on team.id = event.team_id
                WHERE athlete_id = %s and team.season_year = %s and
                (match_based_event.is_invalid = false or match_based_event.is_invalid is null);
                """
        cursor.execute(query,(aID,seasonYear,))        
        result = []
        for row in cursor:
            #print(row)
            result.append(row)
        return result  

    
    def getAggregatedAthleteStatisticsPerSeason(self,aID,seasonYear):
        """
        Gets the aggregated statistics for a given athlete and season. 

        This function uses and ID and a year number to perform a query to the database
        that gets the aggregated statistics in the system that match the given ID and season year.

        Args:
            aID: The ID of the athlete of which statistics need to be fetched.
            seasonYear: the season year of which statistics need to be fetched.
            
            
        Returns:
            A list containing the response to the database query
            containing the aggregated statistics in the system containing 
            the matching record for the given ID and season year.
        """
        cursor = self.conn.cursor()

        
        query = """
                with aggregate_query as(
                SELECT
                sum(matches_played) as matches_played,sum(matches_won) as matches_won,
                match_based_event.athlete_id,match_based_event.category_id

                FROM match_based_event
                INNER JOIN event ON event.id = match_based_event.event_id
                INNER JOIN team on team.id = event.team_id
                WHERE athlete_id = %s and team.season_year = %s and
                (match_based_event.is_invalid = false or match_based_event.is_invalid is null)                
                GROUP BY match_based_event.athlete_id,match_based_event.category_id)
                select 
                matches_played, matches_won,C.name,
                athlete_id, first_name, middle_name, last_names, number, profile_image_link
                from aggregate_query
                INNER JOIN athlete on athlete.id = aggregate_query.athlete_id
                INNER JOIN category as C on aggregate_query.category_id = C.id
                ;
                """
        cursor.execute(query,(aID,seasonYear,))        
        result = cursor.fetchone()
        return result

    
    def getAllAggregatedAthleteStatisticsPerSeason(self,sID,seasonYear):
        """
        Gets all the aggregated statistics for a given athlete and season. 

        This function uses and ID and a year number to perform a query to the database
        that gets the aggregated statistics in the system that match the given ID and season year.

        Args:
            sID: the sport id for the medal_based branch of which statistics need to be fetched
            seasonYear: the season year of which statistics need to be fetched.
            
            
        Returns:
            A list containing the response to the database query
            containing all the aggregated statistics in the system containing 
            the matching record for the season year.
        """
        cursor = self.conn.cursor()
        query = """
                with aggregate_query as(
                SELECT
                sum(matches_played) as matches_played,sum(matches_won) as matches_won,
                match_based_event.athlete_id,match_based_event.category_id

                FROM match_based_event
                INNER JOIN event ON event.id = match_based_event.event_id
                INNER JOIN team on team.id = event.team_id
                WHERE team.sport_id = %s and team.season_year = %s and
                (match_based_event.is_invalid = false or match_based_event.is_invalid is null)
                GROUP BY match_based_event.athlete_id, match_based_event.category_id)
                select 
                matches_played, matches_won, C.name,
                athlete_id, first_name, middle_name, last_names, number, profile_image_link
                from aggregate_query
                INNER JOIN athlete on athlete.id = aggregate_query.athlete_id
                INNER JOIN category as C on aggregate_query.category_id = C.id                
                ;
                """
        cursor.execute(query,(int(sID),int(seasonYear),))        
        result = []
        for row in cursor:
            #print(row)
            result.append(row)
        return result  

   
    def getAggregatedTeamStatisticsPerSeason(self,sID,seasonYear):
        """
        Gets the aggregated team statistics for a given athlete and season. 

        This function uses and ID and a year number to perform a query to the database
        that gets the aggregated statistics in the system that match the given ID and season year.

        Args:
            sID: The ID of the sport of which statistics need to be fetched.
            seasonYear: the season year of which statistics need to be fetched.
            
            
        Returns:
            A list containing the response to the database query
            containing the aggregated team statistics in the system containing 
            the matching record for the given ID and season year.
        """
        cursor = self.conn.cursor()
        #first query is for solo matches
        solo_query = """
                with aggregate_query as(
                SELECT
                sum(matches_played) as matches_played,sum(matches_won) as matches_won,
                match_based_event_team_stats.category_id,event.team_id
                FROM match_based_event_team_stats 
                INNER JOIN event ON event.id = match_based_event_team_stats.event_id
                INNER JOIN team ON team.id = event.team_id
                WHERE team.sport_id = %s and team.season_year = %s and
                (match_based_event_team_stats.is_invalid = false or match_based_event_team_stats.is_invalid is null) and
                (match_based_event_team_stats.category_id = %s or match_based_event_team_stats.category_id = %s or match_based_event_team_stats.category_id = %s or match_based_event_team_stats.category_id = %s)
                GROUP BY event.team_id,match_based_event_team_stats.category_id)
                SELECT 
                matches_played,matches_won,C.name,
                team_id
                FROM aggregate_query INNER JOIN category as C ON aggregate_query.category_id=C.id
                ;
                """
        cursor.execute(solo_query,(sID,seasonYear,TENNIS_CIDM_SOLO,TENNIS_CIDF_SOLO,TABLE_TENNIS_CIDM_SOLO,TABLE_TENNIS_CIDF_SOLO,))        
        solo_result = cursor.fetchone()
        
        #secord query is for double matches
        double_query = """
                with aggregate_query as(
                SELECT
                sum(matches_played) as matches_played,sum(matches_won) as matches_won,
                match_based_event_team_stats.category_id,event.team_id
                FROM match_based_event_team_stats
                INNER JOIN event ON event.id = match_based_event_team_stats.event_id
                INNER JOIN team on team.id = event.team_id
                WHERE team.sport_id = %s and team.season_year = %s and
                (match_based_event_team_stats.is_invalid = false or match_based_event_team_stats.is_invalid is null) and
                (match_based_event_team_stats.category_id = %s or match_based_event_team_stats.category_id = %s or match_based_event_team_stats.category_id = %s or match_based_event_team_stats.category_id = %s)
                GROUP BY event.team_id,match_based_event_team_stats.category_id)
                select 
                matches_played,matches_won,C.name,
                team_id
                from aggregate_query INNER JOIN category as C ON aggregate_query.category_id=C.id
                ;
                """
        cursor.execute(double_query,(sID,seasonYear,TENNIS_CIDM_DOUBLE,TENNIS_CIDF_DOUBLE,TABLE_TENNIS_CIDM_DOUBLE,TABLE_TENNIS_CIDF_DOUBLE,))        
        double_result = cursor.fetchone()
        
        if double_result:
            double_result = list(double_result)
            double_result[0] = int(double_result[0]*0.5)
            double_result[1] = int(double_result[1]*0.5)
            double_result = tuple(double_result)

        if solo_result and not double_result:
            return solo_result
        elif not solo_result and double_result:
            return double_result
        elif solo_result and double_result:
            return [solo_result,double_result]
        

#=============================//POST//=======================
    
    
    
    def addStatistics(self,eID,aID,category_id,medal_id):
        """
        Adds a new medal_based event statistics record with the provided information.

        This function accepts two IDs and sports-specific statistics 
        to perform a query to the database that adds a new statistics record 
        to the system with the provided information.

        Args:
            eID: the ID of the event for which the statistics record will be added.
            aID: the ID of the athlete for which the statistics record will be added.            
            category_id: The id of the category played by the athlete in the event.
            medal_id: The id of the medal awarded.
        Returns:
            A list containing the response to the database query
            containing the matching record for the new statistics entry. 
        """
        cursor = self.conn.cursor()
        query = """
                INSERT INTO match_based_event(matches_played,matches_won,category_id,event_id,athlete_id,is_invalid)
                VALUES(%s,%s,%s,%s,%s,false) returning id;
                """
        cursor.execute(query,(matches_played,matches_won,category_id,eID,aID,))
        mbID = cursor.fetchone()[0]
        if not mbID:
            return mbID
        
        return mbID

    
   
    def addTeamStatistics(self,eID,category_id,medal_id):
        """
        Adds a new medal_based event team statistics record with the provided information.

        This function accepts an ID and sports-specific statistics 
        to perform a query to the database that adds a new team statistics record 
        to the system with the provided information.

        Args:
            eID: the ID of the event for which the team statistics record will be added.           
            category_id: The id of the category played by the athlete in the event.
            medal_id: The id of the medal awarded.
            
        Returns:
            A list containing the response to the database query
            containing the matching record for the new team statistics entry. 
        """
        
        cursor = self.conn.cursor()
        query = """
                INSERT INTO match_based_event_team_stats(matches_played,matches_won,category_id,event_id,is_invalid)
                VALUES(%s,%s,%s,%s,false) returning id;
                """
        try:
            cursor.execute(query,(matches_played,matches_won,category_id,eID,))
            tsID = cursor.fetchone()[0]
            if not tsID:
                return tsID
            #self.commitChanges()
            return tsID
        except:
            return None
    
   

#=============================//PUTS//=======================

    
    def editStatistics(self,eID,aID,category_id,medal_id):
        """
        Updates the statistics for the medal_based event with the given IDs.

        This function accepts two IDs and sports specific statistics and uses them 
        to update the statistics in the record of the medal_based event with the 
        matching IDs.

        Args:
            eID: the ID of the event for which the statistics record will be updated.
            aID: the ID of the athlete for which the statistics record will be updated.          
            category_id: The id of the category played by the athlete in the event.
            medal_id: The id of the medal awarded.
            
        Returns:
            A list containing the response to the database query
            containing the matching record for the modified medal_based
            event statistics.
        """
        
        cursor = self.conn.cursor()
        query = """
                UPDATE match_based_event
                SET matches_played = %s,
                    matches_won = %s,                    
                    is_invalid = false
                WHERE event_id = %s and athlete_id = %s and category_id = %s
                RETURNING
                    matches_won,matches_played,category_id,
                    match_based_event.event_id, match_based_event.id as match_based_event_id, match_based_event.athlete_id;

                """
        cursor.execute(query,(matches_played,matches_won,eID,aID,category_id,))
        result = cursor.fetchone()
        if not result:
            return result
        
        return result

    #NEW: edit team statistics. automatically update based on aggregate. 
    def editTeamStatistics(self,eID,cID):
        """
        Updates the statistics for the medal_based event with the given IDs.

        This function accepts an ID and uses it to automatically update the 
        team statistics in the record of the medal_based event team stats with 
        the matching ID based on an aggregate of existing statistics.

        Args:
            eID: the ID of the event for which the team statistics record will be updated
            cID: The id of the category for the event.
            
        Returns:
            A list containing the response to the database query
            containing the matching record for the modified medal_based
            event team statistics.
        """
        cursor = self.conn.cursor()
        #the first query collects the aggregate
        query = """
                with aggregate_query as(
                with valid_match_based_events as
                (SELECT *
                FROM match_based_event
                WHERE (is_invalid=false or is_invalid is null))
                select 
                sum(matches_played) as matches_played,sum(matches_won) as matches_won
                from valid_match_based_events
                WHERE event_id = %s and category_id=%s)
                select * 
                from aggregate_query
                where aggregate_query.matches_played is not null;
                """
        cursor.execute(query,(eID,cID))
        resultTeam = cursor.fetchone()
  
        #the second query updates the medal_based_event_team_stats based on aggregate results
        query = """
                UPDATE match_based_event_team_stats
                SET matches_played = %s,
                    matches_won = %s,                    
                    is_invalid = false
                WHERE event_id = %s
                and category_id=%s 
                RETURNING
                    matches_played,
                    matches_won,
                    category_id,
                    match_based_event_team_stats.event_id, match_based_event_team_stats.id as match_based_event_team_stats_id;
                """
        if resultTeam:
            cursor.execute(query,(resultTeam[0],resultTeam[1],eID,cID,))
        else:
            cursor.execute(query,(0,0,eID,cID,))
        result = cursor.fetchone()
        if not result:
            return result
        #self.commitChanges()
        return result


#=============================//DELETE//=======================
     
     
    def removeStatistics(self,eID,aID,cID):
        """
        Invalidates a medal_based event statistics entry in the database.

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
                UPDATE match_based_event
                SET is_invalid = true
                WHERE event_id = %s  and athlete_id = %s and category_id=%s
                RETURNING id;
                """
        try:
            cursor.execute(query,(eID,aID,cID))
            result = cursor.fetchone()[0]
            if not result:
                return result      
            
            return result
        except: 
            return None

    
    def removeTeamStatistics(self,eID,cID):
        """
        Invalidates a medal_based event team statistics entry in the database.

        This function accepts an ID and uses it to set the valid field
        within the database as invalid, this acts as a deletion of the 
        team statistics entry from the system.

        Args:
            eID: The ID of the event for which the team statistics will be invalidated. 
            cID: The ID of the category of the event.
            
        Returns:
            A list containing the response to the database query
            containing the matching record for the modified team 
            statistics entry.
        """
        cursor = self.conn.cursor()
        query = """
                UPDATE match_based_event_team_stats
                SET is_invalid = true
                WHERE event_id = %s
                and category_id = %s
                RETURNING id;
                """
        cursor.execute(query,(eID,cID,))
        result = cursor.fetchone()[0]
        if not result:
            return result
       
        return result


    def getCategoriesOfTheEvent(self, eID):
        """
        Returns a list of categories that the event has.

        Performs a fetch query on the database in order 
        to collect the categories played in an event.

        Args:
            eID: The id of the event.

        Returns:
            A list containing the categories played in an event.    
        """

        cursor = self.conn.cursor()

        query = """
                select distinct category_id
                from match_based_event 
                where event_id = %s
                and is_invalid = false
                """
        try:
            cursor.execute(query,(eID,))
            categories = []
            for row in cursor:
                categories.append(row[0])
            return categories
        except:
            return []


        
    def commitChanges(self):
        """
        Commits the changes done on the database after
        insertion and update queries have been done on the
        database.
        
        Uses the connection created when this MedalBasedEventDAO was
        instantiated to commit the changes performed on the datasase
        after insertion and update queries. 
        """
        
        self.conn.commit()


        
            
            

         
