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

ATLETISMO_CIDM_100M = 9
ATLETISMO_CIDM_400M = 12

NOMEDAL_ID = 4

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
                FROM individual_medal_event
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
                FROM individual_medal_event
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
                FROM individual_medal_event_team_stats
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
                FROM individual_medal_event_team_stats
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
                A.number, A.profile_image_link,M.type_of_medal,C.name,              
                individual_medal_event.event_id, individual_medal_event.id as individual_medal_event_id,E.opponent_name
                FROM individual_medal_event INNER JOIN category as C ON individual_medal_event.category_id=C.id
                INNER JOIN event as E on individual_medal_event.event_id = E.id
                INNER JOIN medal as M  on individual_medal_event.medal_id = M.id
                INNER JOIN athlete as A ON A.id = individual_medal_event.athlete_id
                WHERE event_id = %s and individual_medal_event.medal_id is not null and
                (individual_medal_event.is_invalid = false);
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
                M.type_of_medal,C.name,event_id,athlete_id,
                individual_medal_event.id as individual_medal_event_id
                FROM individual_medal_event INNER JOIN category as C ON individual_medal_event.category_id=C.id
                INNER JOIN medal as M on M.id = individual_medal_event.medal_id
                WHERE event_id = %s and athlete_id = %s and category_id=%s and individual_medal_event.medal_id is not null and
                (individual_medal_event.is_invalid = false);
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
                with aggregate_query as(
                SELECT
                count(medal_id) as medals_earned, individual_medal_event_team_stats.medal_id as medal_id,
                individual_medal_event_team_stats.category_id, individual_medal_event_team_stats.id as team_stats_id, event.id as eid
                FROM individual_medal_event_team_stats
                INNER JOIN event ON event.id = individual_medal_event_team_stats.event_id                
                WHERE event_id = %s and category_id=%s and individual_medal_event_team_stats.medal_id is not null and
                individual_medal_event_team_stats.is_invalid = false
                GROUP BY individual_medal_event_team_stats.medal_id, individual_medal_event_team_stats.category_id,individual_medal_event_team_stats.id,event.id)
                select 
                medals_earned, type_of_medal,C.name, team_stats_id,eid
                From aggregate_query                
                INNER JOIN category as C on aggregate_query.category_id = C.id  
                INNER JOIN medal as M on aggregate_query.medal_id = M.id
                """
        cursor.execute(query,(eID,cID,))
        
        result = []
        for row in cursor:
            result.append(row)                 
       
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
                M.type_of_medal,C.name,
                individual_medal_event.id as individual_medal_event_id,
                individual_medal_event.athlete_id
                FROM individual_medal_event INNER JOIN category as C on individual_medal_event.category_id=C.id
                INNER JOIN medal as M ON M.id = individual_medal_event.medal_id
                INNER JOIN event ON event.id = individual_medal_event.event_id
                INNER JOIN team on team.id = event.team_id
                WHERE athlete_id = 131 and team.season_year = 2020 and individual_medal_event.medal_id is not null and
                individual_medal_event.is_invalid = false;
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
                count(medal_id) as medals_earned, individual_medal_event.medal_id as medal_id,
                individual_medal_event.athlete_id,individual_medal_event.category_id

                FROM individual_medal_event
                INNER JOIN event ON event.id = individual_medal_event.event_id
                INNER JOIN team on team.id = event.team_id
                WHERE athlete_id = %s and team.season_year = %s and individual_medal_event.medal_id is not null and
                individual_medal_event.is_invalid = false
                GROUP BY individual_medal_event.athlete_id,individual_medal_event.medal_id, individual_medal_event.category_id)
                select 
                medals_earned, type_of_medal,C.name,
                athlete_id, first_name, middle_name, last_names, number, profile_image_link
                from aggregate_query
                INNER JOIN athlete on athlete.id = aggregate_query.athlete_id
                INNER JOIN category as C on aggregate_query.category_id = C.id  
                INNER JOIN medal as M on aggregate_query.medal_id = M.id
                ;
                """
        cursor.execute(query,(aID,seasonYear,))        
        result = []
        for row in cursor:
            result.append(row)
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
                count(medal_id) as medals_earned, individual_medal_event.medal_id as medal_id,
                individual_medal_event.athlete_id,individual_medal_event.category_id

                FROM individual_medal_event
                INNER JOIN event ON event.id = individual_medal_event.event_id
                INNER JOIN team on team.id = event.team_id
                WHERE team.sport_id = %s and team.season_year = %s and individual_medal_event.medal_id is not null and
                individual_medal_event.is_invalid = false
                GROUP BY individual_medal_event.athlete_id,individual_medal_event.medal_id, individual_medal_event.category_id)
                select 
                medals_earned, type_of_medal,C.name,
                athlete_id, first_name, middle_name, last_names, number, profile_image_link
                from aggregate_query
                INNER JOIN athlete on athlete.id = aggregate_query.athlete_id
                INNER JOIN category as C on aggregate_query.category_id = C.id  
                INNER JOIN medal as M on aggregate_query.medal_id = M.id               
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
        
        query = """
                with aggregate_query as(
                SELECT
                count(medal_id) as medals_earned,individual_medal_event_team_stats.medal_id,
                individual_medal_event_team_stats.category_id,event.team_id
                FROM individual_medal_event_team_stats 
                INNER JOIN event ON event.id = individual_medal_event_team_stats.event_id
                INNER JOIN team ON team.id = event.team_id
                WHERE team.sport_id = %s and team.season_year = %s and
                (individual_medal_event_team_stats.is_invalid = false or individual_medal_event_team_stats.is_invalid is null)                
                GROUP BY event.team_id,individual_medal_event_team_stats.category_id,individual_medal_event_team_stats.medal_id)
                SELECT 
                medals_earned,M.type_of_medal,C.name,
                team_id
                FROM aggregate_query INNER JOIN category as C ON aggregate_query.category_id=C.id
                INNER JOIN medal as M on aggregate_query.medal_id = M.id
                ;
                """
        cursor.execute(query,(sID,seasonYear,))        
        result = []
        for row in cursor:
            result.append(row)
        
        return result
              
        
        

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
                INSERT INTO individual_medal_event(event_id,athlete_id,category_id,medal_id,is_invalid)
                VALUES(%s,%s,%s,%s,false) returning id;
                """
        cursor.execute(query,(eID,aID,category_id,medal_id,))
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
                INSERT INTO individual_medal_event_team_stats(event_id,category_id,medal_id,is_invalid)
                VALUES(%s,%s,%s,false) returning id;
                """
        try:
            cursor.execute(query,(eID,category_id,medal_id,))
            tsID = cursor.fetchone()[0]
            if not tsID:
                return tsID
            #self.commitChanges()
            return tsID
        except Exception as e:
            return str(e)
    
   

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
                UPDATE individual_medal_event
                SET medal_id = %s,                                        
                    is_invalid = false
                WHERE event_id = %s and athlete_id = %s and category_id = %s
                RETURNING
                    medal_id,category_id,
                    event_id, individual_medal_event.id as medal_based_event_id,athlete_id;

                """
        cursor.execute(query,(medal_id,eID,aID,category_id,))
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
        #the first query collects the medals earned by the individuals
        query = """
                select distinct medal_id
                from individual_medal_event
                where event_id = %s
                and category_id = %s
                and is_invalid = false
                """
        cursor.execute(query,(eID,cID))
        indv_medal_ids = []#Individual medal ids
        for row in cursor:
            indv_medal_ids.append(row)

        #the second query collects the medals earned by the team 
        query = """
                select id,medal_id
                from individual_medal_event_team_stats
                where event_id = %s
                and category_id = %s
                and is_invalid = false
                """
        cursor.execute(query,(eID,cID))
        team_medal_ids = []#Team medal ids
        for row in cursor:
            team_medal_ids.append(row)
        
        numIndvMedals = len(indv_medal_ids)#Number of individual medals
        numTeamMedals = len(team_medal_ids)#Number of team medals
        if not numIndvMedals == numTeamMedals:
            if numIndvMedals < numTeamMedals:
                return "There are missing individual medals in a category"
            elif numIndvMedals > numTeamMedals:
                return "There are missing team medals in a category"
    
        
        teamIndex = 0        

        query = """
                UPDATE individual_medal_event_team_stats
                SET medal_id = %s,                                        
                    is_invalid = false
                WHERE event_id = %s
                and category_id=%s 
                and id = %s
                RETURNING
                    medal_id,                    
                    category_id,
                    individual_medal_event_team_stats.event_id, individual_medal_event_team_stats.id as medal_based_event_team_stats_id;
                """
        result = []
        
        for indmedal in indv_medal_ids:
            cursor.execute(query,(indmedal,eID,cID,team_medal_ids[0][teamIndex],))
            result.append(cursor.fetchone()[3])
            teamIndex += 1
        
        
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
                UPDATE individual_medal_event
                SET medal_id = %s
                WHERE event_id = %s  and athlete_id = %s and category_id=%s
                RETURNING id;
                """
        try:
            cursor.execute(query,(NOMEDAL_ID,eID,aID,cID))
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
                UPDATE individual_medal_event_team_stats
                SET medal_id = %s
                WHERE event_id = %s
                and category_id = %s
                RETURNING id;
                """
        cursor.execute(query,(NOMEDAL_ID,eID,cID,))
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
                from individual_medal_event_team_stats 
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


        
            
            

         
