from flask import jsonify
from .dao.final_score_dao import FinalScoreDAO
from .dao.event_dao import EventDAO
from .dao.athlete_dao import AthleteDAO
from .dao.team_dao import TeamDAO
from .dao.medal_based_event_dao import MedalBasedEventDAO



#Sport Constants

TENNIS_IDM = 9
TENNIS_IDF = 18
TABLE_TENNIS_IDM = 7
TABLE_TENNIS_IDF = 15
DANCE = 17
ATHLETSISM = 8
#Category Constants
M100 = 9
M400 = 12

CATEGORIES = dict(ATHLETSISM =[M100,M400])


class MedalBasedEventHandler():

   

    #===========================//DICTIONARY MAPPERS//==================================   
    def mapEventToDict(self,record):
        athlete_info = {}
        stat_info = {}
        event_info = {}

        athlete_info['athlete_id'] = record[0]
        athlete_info['first_name'] = record[1]
        athlete_info['middle_name'] = record[2]
        athlete_info['last_names'] = record[3]      
        athlete_info['number'] = record[4]
        athlete_info['profile_image_link'] = record[5]

        stat_info['matches_played'] = record[6]
        stat_info['matches_won'] = record[7]
        
        event_info['category_name'] = record[8]
        event_info['event_id'] = record[9]
        event_info['athlete_id'] = record[10]
        event_info['match_based_event_id'] = record[11]


        result = dict(athlete = athlete_info, event_info = event_info, event_statistics = stat_info)
        return result

        
    #For Specific Athlete Event Info
    def mapEventAthleteStatsToDict(self,record):
        stat_info = {}
        event_info = {}

        stat_info['medal_obtained'] = record[0]
        event_info['category_name'] = record[1]        
        event_info['event_id'] = record[2]
        event_info['athlete_id'] = record[3]
        event_info['medal_based_event_id'] = record[4]
        
        return dict(event_info= event_info, event_statistics = stat_info)

    # for team statistics
    def mapEventTeamStatsToDict(self,record):
        medal_based_statistics = {}
        #print(record)
        medal_based_statistics[record[0][2]] = []
        medal_based_statistics['event_id'] = record[0][4]
        for teamResults in record:
            medal_based_statistics[teamResults[2]].append({'medals_earned':teamResults[0],'type_of_medal':teamResults[1],'team_stats_id':teamResults[3]})
        
        print(medal_based_statistics)
        
        return dict(team_medal_based_statistics = medal_based_statistics)
        # UPRM_Score = final_record[0], Opponent_Score = final_record[1]
    
    def mapEventSeasonCollectionToDict(self,record):
        event_info = {}
        stat_info = {}   
        

       
        event_info['event_id'] = record[0]
        event_info['event_date'] = record[1]
        event_info['category_name'] = record[3]
        event_info['athlete_id'] = record[5]
        event_info['medal_based_event_id'] = record[4]
        
        stat_info['type of medal'] = record[2]
        

        result = dict(Event = event_info, Event_Statistics = stat_info)
        return result

    def mapAthleteSeasonAggregate(self, record):
        athlete_info = {}
        stat_info = {}
        #print(record)
        athlete_info['athlete_id'] = record[3]
        athlete_info['first_name'] = record[4]
        athlete_info['middle_name'] = record[5]
        athlete_info['last_names'] = record[6]
        athlete_info['number'] = record[7]
        athlete_info['profile_image_link'] = record[8]

        stat_info['medals_earned'] = record[0]
        stat_info['type_of_medal'] = record[1]
        stat_info['category_name'] = record[2]
        

        result = dict(Athlete = athlete_info, Event_Statistics = stat_info)
        return result

    def mapTeamSeasonAggregate(self, record):
        stat_info = {}
        
        stat_info['medals_earned'] = record[0]
        stat_info['type_of_medal'] = record[1]
        stat_info['category_name'] = record[2]
        

        result = dict(team_id = record[3], Event_Statistics = stat_info)
        return result


    def mapEventAllStatsToDict(self,team_records,athlete_records,final_record):
        
        try:
            opponent_name = athlete_records[0][10]
            event_info = dict(
                event_id = athlete_records[0][8],
            )
        except:
            opponent_name = athlete_records[10]
            event_info = dict(
                event_id = athlete_records[8],
            )
        medal_based_statistics = {}
                               
        
        
        for teamResults in team_records:
            try:
                #print(teamResults)
                if isinstance(teamResults[1],tuple):
                    #print(teamResults)
                    medal_based_statistics[teamResults[0][2]] = []
                    for results in teamResults:
                        print(results)
                        medal_based_statistics[teamResults[0][2]].append({'medals_earned':results[0],'type_of_medal':results[1],'team_stats_id':results[3]})
               
            except:                 
                medal_based_statistics[teamResults[0][2]] = {'medals_earned':teamResults[0][0],'type_of_medal':teamResults[0][1],'team_stats_id':teamResults[0][3]}
        
        

        team_statistics = dict(medal_based_statistics = medal_based_statistics)
       
        athlete_statistics = []

        for athlete_record in athlete_records:            
            athlete_info = dict(
                athlete_id = athlete_record[0],
                first_name = athlete_record[1],
                middle_name = athlete_record[2],
                last_names = athlete_record[3],    
                number = athlete_record[4],
                profile_image_link = athlete_record[5],
                match_based_event_id = athlete_record[9]
            )
            statistics = dict(
                medal_earned = athlete_record[6],
                category_name = athlete_record[7]                
            )
            athlete_statistics.append(dict(athlete_info = athlete_info, statistics = statistics))
       
        result = dict(event_info = event_info, team_statistics = team_statistics, 
        athlete_statistic = athlete_statistics, uprm_score = final_record[0], 
        opponent_score = final_record[1],opponent_name = opponent_name)
        return result

#===========================//HANDLERS//==================================
#===========================//I.GETS//====================================

    def getAllAthleteStatisticsByEventIdAndCategoryId(self,eID,aID,cID):
        """
        Gets all the statistics for a given event and athlete. 

        Calls the MedalBasedEventDAO to get event statistics and maps the result to
        to a JSON that contains all the statistics for that athlete and event in the system. That
        JSON object is then returned.

        Args:
            eID: The ID of the event of which statistics need to be fetched.
            aID: The ID of the athlete of which statistics need to be fetched.
            cID: The ID of the category of which statistics need to be fetched.
            
        Returns:
            A JSON containing all the statistics in the system for the specified event and athlete.
        """

        #validate parameters given        
        if not isinstance(eID,int) or not isinstance(aID,int) or not self._validateMedalCategory(cID):
            return jsonify(Error = "Bad arguments"),400

        #validate existing event
        try:
            event = EventDAO().getEventByID(eID)
            if not event:
                return jsonify(Error = "Event with id:{} was not found.".format(eID)),404                 
    
        except:
           return jsonify("Problem ocurred while fetching a medal based event."),400
        
        #validate existing athlete 
        try:
           athlete = AthleteDAO().getAthleteByID(aID)
           if not athlete:
               return jsonify(Error = "Athlete with id:{} not found.".format(aID)),404                
        
        except:
           return jsonify("Problem ocurred while fetching a medal based event."),400

        
        try:
            result = MedalBasedEventDAO().getAllAthleteStatisticsByEventIdAndCategoryId(eID,aID,cID)
            if not result:
                return jsonify(Error = "No athlete statistics were found."),404
            
            #print(result)
            mappedResult = self.mapEventAthleteStatsToDict(result)

            return jsonify(Medal_Based_Event_Athlete_Statistics = mappedResult),200
        except:            
            return jsonify(Error = "A problem ocurred while fetching the athlete statistics of a medal based event."),400
        
        
       
       
    def getAllTeamStatisticsByEventIdAndCategoryId(self,eID,cID):
        """
        Gets all the statistics for a given event. 

        Calls the MedalBasedEventDAO to get event team statistics and maps the result to
        to a JSON that contains all the team statistics for that event in the system. That
        JSON object is then returned.

        Args:
            eID: The ID of the event of which team statistics need to be fetched.
            cID: The ID of the event of which team statistics need to be fetched.
            
            
        Returns:
            A JSON containing all the team statistics in the system for the specified event.
        """

        #validate parameters given
        try:
            if not isinstance(eID,int) or not self._validateMedalCategory(cID):
                return jsonify(Error = "Bad arguments"),400
        except:
            return jsonify(Error = "Bad arguments"),400

        #validate existing event
        try:
            event = EventDAO().getEventByID(eID)
            if not event:
                return jsonify(Error = "Event with id:{} was not found.".format(eID)),404                 
    
        except:
           return jsonify("Problem ocurred while fetching a medal based event."),400
       
        try:
            dao = MedalBasedEventDAO()
            team_results = dao.getAllTeamStatisticsByEventIdAndCategoryId(eID,cID)
            result = []
            for row in team_results:
                result.append(row)
            if not result:
                return jsonify(Error = "Medal Based Event Team Statistics not found for the event: {}".format(eID)),404
            mappedResult = self.mapEventTeamStatsToDict(result)
        except Exception as e:
            return jsonify(ERROR="Unable to verify medal_based_event_team_stats from DAO." + str(e)), 500
         
        return jsonify(Medal_Based_Event_Team_Stats = mappedResult),200

    def getAllAthleteStatisticsPerSeason(self,aID,seasonYear):
        """
        Gets all the statistics for a given athlete during a given season. 

        Calls the MedalBasedEventDAO to get event statistics and maps the result to
        to a JSON that contains all the statistics for that athlete during the given season
        in the system. That JSON object is then returned.

        Args:
            seasonYear: the season year of which statistics need to be fetched
            aID: The ID of the athlete of which statistics need to be fetched
            
        Returns:
            A JSON containing all the statistics in the system for the specified athlete and season year.
        """

        if not isinstance(aID,int) or not isinstance(seasonYear,int):
            return jsonify(Error = "Bad arguments"),400
        
        #validate existing athlete 
        try:
           athlete = AthleteDAO().getAthleteByID(aID)
           if not athlete:
               return jsonify(Error = "Athlete with id:{} not found.".format(aID)),404                
        
        except:
           return jsonify("Problem ocurred while fetching a medal based event."),500        
        
        
        try:
            dao = MedalBasedEventDAO()
            result = dao.getAllAthleteStatisticsPerSeason(aID,seasonYear)
            if not result:
                return jsonify(Error = "Medal Based Event Statistics not found for the athlete id:{} in season year:{}.".format(aID,seasonYear)),404
            mappedResult = []
            for athlete_statistics in result:                     
                mappedResult.append(self.mapEventSeasonCollectionToDict(athlete_statistics))
            
        except:
            return jsonify(ERROR="Unable to verify medal based event from DAO."), 500
         
        return jsonify(Medal_Based_Event_Season_Athlete_Statistics = mappedResult), 200


    def getAggregatedAthleteStatisticsPerSeason(self,aID,seasonYear):
        """
        Gets aggregated statistics for a given athlete during a given season. 

        Calls the MedalBasedEventDAO to get aggregated event statistics and maps the result to
        to a JSON that contains all the statistics for that athlete during the given season
        in the system. That JSON object is then returned.

        Args:
            seasonYear: the season year of which statistics need to be fetched
            aID: The ID of the athlete of which statistics need to be fetched
            
        Returns:
            A JSON containing aggregated  statistics in the system for the specified athlete and season year.
        """

        if not isinstance(aID,int) or not isinstance(seasonYear,int):
            return jsonify(Error = "Bad arguments"),400

        #validate existing athlete 
        
        try:
            a_dao = AthleteDAO() 
            athlete = a_dao.getAthleteByID(aID)
            if not athlete:
                return jsonify(Error = "Athlete for ID:{} not found.".format(aID)),400
        except:
            return jsonify(ERROR="Unable to verify athlete from DAO."), 500
         
        # validate existing medal_based_event entries and format returnable
        
        try:
            dao = MedalBasedEventDAO()
            result = dao.getAggregatedAthleteStatisticsPerSeason(aID,seasonYear)
            if not result:
                return jsonify(Error = "Medal Based Event Statistics not found for the athlete id:{} in season year:{}.".format(aID,seasonYear)),404
            mappedResult = []
            for row in result:
                mappedResult.append(self.mapAthleteSeasonAggregate(row))
            #print(mappedResult)
        except:
            return jsonify(ERROR="Unable to verify medal_based event from DAO."), 500
         
        return jsonify(Medal_Based_Event_Season_Athlete_Statistics = mappedResult), 200

    
    def getAllAggregatedAthleteStatisticsPerSeason(self,sID,seasonYear):
        """
        Gets all aggregated statistics for athletes during a given season. 

        Calls the MedalBasedEventDAO to get  all aggregated event statistics and maps the result to
        to a JSON that contains all the aggregated statistics  during the given season
        in the system. That JSON object is then returned.

        Args:
            seasonYear: the season year of which statistics need to be fetched
            sID: The ID of the sport of which statistics need to be fetched
            
        Returns:
            A JSON containing all the aggregated statistics in the system for the specified sport and season year.
        """

        if not isinstance(sID,int) or not isinstance(seasonYear,int):
            return jsonify(Error = "Bad arguments"),400
   
        # validate existing medal_based_event entries and format returnable
        
        try:
            dao = MedalBasedEventDAO()
            result = dao.getAllAggregatedAthleteStatisticsPerSeason(sID,seasonYear)
            if not result:
                return jsonify(Error = "Medal Based Event Statistics not found for the sport id:{} in season year:{}.".format(sID,seasonYear)),404
            mappedResult = []
            for athlete_statistics in result:                     
                mappedResult.append(self.mapAthleteSeasonAggregate(athlete_statistics))
            #print(mappedResult)
        except Exception as e:
            return jsonify(ERROR="Unable to verify medal_based event from DAO." + str(e)), 500
         
        return jsonify(Medal_Based_Event_Season_Athlete_Statistics = mappedResult), 200


    
    def getAggregatedTeamStatisticsPerSeason(self,sID,seasonYear):
        """
        Gets all aggregated statistics for a given team during a season.  

        Calls the MedalBasedEventDAO to get  all aggregated event statistics and maps the result to
        to a JSON that contains all the statistics for that athlete during the given season
        in the system. That JSON object is then returned.

        Args:
            seasonYear: the season year of which statistics need to be fetched
            sID: The ID of the sport of which team statistics need to be fetched
            
        Returns:
            A JSON containing the aggregated team statistics in the system for the specified team and season year.
        """
        if not isinstance(sID,int) or not isinstance(seasonYear,int):
            return jsonify(Error = "Bad arguments"),400
         
        # validate existing medal_based_event entries and format returnable
        
        try:
            dao = MedalBasedEventDAO()
            result = dao.getAggregatedTeamStatisticsPerSeason(sID,seasonYear)
            if not result:
                return jsonify(Error = "Medal Based Event Team Statistics not found for sport id:{} in season year:{}.".format(sID,seasonYear)),404
            mappedResult = []            
            for row in result:
                mappedResult.append(self.mapTeamSeasonAggregate(row))
            
            
        except Exception as e:
            return jsonify(ERROR="Unable to verify medal_based event team stats from DAO." + str(e)), 500
         
        return jsonify(Medal_Based_Event_Season_Team_Statistics = mappedResult), 200

    
    def getAllStatisticsByEventID(self,eID):
        """
        Gets all the team and individual statistics for a given event. 

        Calls the MedalBasedEventDAO to get event statistics and maps the result to
        to a JSON that contains all the statistics for that event in the system. 
        That JSON object is then returned.

        Args:
            eID: The ID of the event of which statistics need to be fetched
            
        Returns:
            A JSON containing all the statistics in the system for the specified event.
        """

        #validate parameters given
        
        
        if not isinstance(eID,int):
            return jsonify(Error = "Bad arguments"),400
       

        #validate existing event
        try:
            event = EventDAO().getEventByID(eID)
            if not event:
                return jsonify(Error = "Event with id:{} was not found.".format(eID)),404                 
    
        except:
           return jsonify("Problem ocurred while fetching a medal based event."),400

        dao = MedalBasedEventDAO()

        try:  
            categoriesPlayed = dao.getCategoriesOfTheEvent(eID)
            if not categoriesPlayed:
                return jsonify(Error = "Medal Based Event Team Statistics not found for the event: {}".format(eID)),404  

            team_results = []
            for category in categoriesPlayed:
                team_results.append(dao.getAllTeamStatisticsByEventIdAndCategoryId(eID,category))
            if not team_results:
                return jsonify(Error = "Medal Based Event Team Statistics not found for the event: {}".format(eID)),404
        except Exception as e:
            return jsonify(ERROR="Unable to verify medal based event team stats from DAO." + str(e)), 500
        
        try:
            all_stats_result = dao.getAllStatisticsByEventID(eID)
            if not all_stats_result:            
                return jsonify(Error = "Medal Based Event Statistics not found for the event: {}.".format(eID)),404
        except Exception as e:
            return jsonify(ERROR="Unable to verify medal based event from DAO." + str(e)), 500
         
        try:
            fs_dao = FinalScoreDAO()
            final_score_result = fs_dao.getFinalScore(eID)
            if not final_score_result:                
                return jsonify(Error = "Medal Based Event Statistics not found for the event: {}.".format(eID)),404
            #print(team_results)
            mappedResult = self.mapEventAllStatsToDict(team_results,all_stats_result, final_score_result)
            return jsonify(Medal_Based_Event_Statistics = mappedResult),200

        except Exception as e:
            return jsonify(ERROR="Unable to verify final score from DAO." + str(e)), 500
         
      

#===========================//II.POSTS//====================================
    def addStatistics(self,eID,aID,attributes): 
        """
        Adds a new statistics record with the provided information.

        Calls the MedalBasedEventDAO to add a new statistics record and maps the result to
        to a JSON that contains the desired record. That JSON object 
        is then returned.

        Args:
            eID: the ID of the event for which the statistics record will be added.
            aID: the ID of the athlete for which the statistics record will be added.
            attributes:                
                category_id: The id of the category played by the athlete in the event.
                medal_id: The id of the medal awarded.
        Returns:
            A JSON containing the id for the new Medal Based Event record.
        """

        if not isinstance(eID,int) or not isinstance(aID,int) or not self.validateAttributes(attributes):
            return jsonify(Error = "Bad arguments"),400

        # Validate Avoid Duplication
        
        dao = MedalBasedEventDAO()

        try:           
            if dao.getMedalBasedEventID(eID,aID,attributes['category_id']):
                return jsonify(Error = "Medal Based Event Entry already exists for Event ID:{} and Athlete ID:{}".format(eID,aID)),403 #TODO: Use 403 for duplicates
        except:
            return jsonify(ERROR="Unable to verify medal_based_event from DAO."), 500

        # Validate existing event  
        e_dao = EventDAO()      
        try:            
            event = e_dao.getEventByID(eID)
            if not event:
                return jsonify(Error = "Event for ID:{} not found.".format(eID)),400
        except:
            return jsonify(ERROR="Unable to verify event from DAO."), 500
       
        
        # Get Event Team For Validation        
        t_dao = TeamDAO()
        try:
            t_dao = TeamDAO()
            tID = e_dao.getEventTeamByID(eID)
        except:
            return jsonify(ERROR="Unable to verify event from DAO."), 500

        # Validate that the event belongs to the correct sport and the category is correct.     
        try:
            sID = t_dao.getTeamSportByID(tID)[0] 
            
            if sID != ATHLETSISM:
                return jsonify(Error = "Malformed Query, Event ID:{} does not belong to Medal Based.".format(eID)),400

            if not self._validateCategory(sID,attributes['category_id']):
                return jsonify(Error = "Bad request, category {} does not match the sport of the team.".format(attributes['category_id'])),400        
            
        except:
            return jsonify(ERROR="Unable to verify team from DAO."), 500

        # Validate existing athlete 
        
        try:
            a_dao = AthleteDAO()
            athlete = a_dao.getAthleteByID(aID)
            if not athlete:
                return jsonify(Error = "Athlete for ID:{} not found.".format(aID)),400
        except:
            return jsonify(ERROR="Unable to verify athlete from DAO."), 500

        # Validate athlete belongs to team playing event        
        try:
            if not t_dao.getTeamMemberByIDs(aID,tID):
                return jsonify(Error = "Malformed Query, Athlete ID:{} does not belong to Team ID:{} from Event ID:{}.".format(aID,tID,eID)),400
        except:
            return jsonify(ERROR="Unable to verify team from DAO."), 500

        #check if existing invalid, in this case we PUT/update instead of POST/add. sorta. 
        invalid_duplicate = False
        try:
            if dao.getMedalBasedEventIDInvalid(eID,aID,attributes['category_id']):
                invalid_duplicate = True
        except:
            return jsonify(ERROR="Unable to verify medal_based_event from DAO."), 500
        
        #the case of there already existing an entry, but marked as invalid
        if invalid_duplicate:
            try:
                result = dao.editStatistics(eID,aID,attributes['category_id'],attributes['medal_id'])
                    
                if not result:
                    return jsonify(Error = "Statistics Record not found for athlete id:{} in event id:{}.".format(aID,eID)),404
                
            except Exception as e:
                return jsonify(ERROR="HERE! Unable to verify medal based event from DAO." + str(e)), 500
        else:
            # Create and Validate new Medal_Based_Event
            try:
                result = dao.addStatistics(eID,aID,attributes['category_id'],attributes['medal_id'])                    
                if not result:
                    return jsonify(Error = "Problem inserting new statistics record."),500
            except Exception as e:
                return jsonify(ERROR="Unable to verify medal based event from DAO." + str(e)), 500
        
        #update and validate Medal Based Event Team Statistic
        # If existing Team Statistics update, else create
        try:
            if dao.getMedalBasedEventTeamStatsID(eID,attributes['category_id']) or dao.getMedalBasedEventTeamStatsIDInvalid(eID,attributes['category_id']):
                team_result = dao.editTeamStatistics(eID,attributes['category_id'])
                print(team_result)
                if not team_result:
                    return jsonify(Error = "Team Statistics Record not found for event id:{}.".format(eID)),404
            else:                           
                team_result = dao.addTeamStatistics(eID,attributes['category_id'],attributes['medal_id'])
                print(team_result)
        except Exception as e:
            return jsonify(ERROR="HERE Unable to verify medal based event team statistics from DAO." + str(e)), 500       

        
        if invalid_duplicate:
            mappedResult = self.mapEventAthleteStatsToDict(result)
            dao.commitChanges()
            return jsonify(Medal_Based_Event_Athlete_Statistics = mappedResult),200
        else:
           
            dao.commitChanges()
            return jsonify(Medal_Based_Event_Athlete_Statistics = "Added new statistics record with id:{} for athlete id:{} in event id:{}.".format(result,aID,eID)),201

    
    def addTeamStatistics(self,eID,attributes): 
        """
        Adds a new team statistics record with the provided information.

        Calls the MedalBasedEventDAO to add a new team statistics record and maps the result to
        to a JSON that contains the desired record. That JSON object 
        is then returned.

        Args:
            eID: the ID of the event for which the statistics record will be added.
            attributes:                
                category_id: The id of the category played by the athlete in the event.
                medal_id: The id of the medal awarded.
            
        Returns:
            A JSON containing the id for the new Medal Based Event team statistics record.
        """

        if not isinstance(eID,int) or not self.validateAttributes(attributes):
            return jsonify(Error = "Bad arguments"),400

        # Validate Avoid Duplication
        dao = MedalBasedEventDAO()
        try:            
            if dao.getMedalBasedEventTeamStatsID(eID,attributes['category_id']):
                return jsonify(Error = "Medal Based Event Team Stats Entry already exists for Event ID:{}".format(eID)),400
        except:
            return jsonify(ERROR="Unable to verify medal_based_event_team_stats from DAO."), 500

        # Validate existing event
        e_dao =EventDAO()        
        try:            
            event = e_dao.getEventByID(eID)
            if not event:
                return jsonify(Error = "Event for ID:{} not found.".format(eID)),400
        except:
            return jsonify(ERROR="Unable to verify event from DAO."), 500

        # Get Event Team For Validation 
        t_dao = TeamDAO()      
        try:           
            tID = e_dao.getEventTeamByID(eID)
        except:
            return jsonify(ERROR="Unable to verify team from DAO."), 500

        # Validate that the event belongs to the correct sport.        
        try:
            sID = t_dao.getTeamSportByID(tID)[0]
            
            if sID != ATHLETSISM:
                return jsonify(Error = "Malformed Query, Event ID:{} does not belong to Medal Based.".format(eID)),400
             
            if not self._validateCategory(sID,attributes['category_id']):
                return jsonify(Error = "Bad request, category {} does not match the sport of the team.".format(attributes['category_id'])),400
            
        except:
            return jsonify(ERROR="Unable to verify team from DAO."), 500

        #check if existing invalid, in this case we PUT/update instead of POST/add 
        invalid_duplicate = False
        try:
            if dao.getMedalBasedEventTeamStatsIDInvalid(eID,attributes['category_id']):
                invalid_duplicate = True
        except:
            return jsonify(ERROR="Unable to verify medal_based_event_team_Stats from DAO."), 500
        #the case of there already existing an entry, but marked as invalid
        if invalid_duplicate:
            try:
                result = dao.editTeamStatistics(eID,attributes['category_id'])
                if not result:
                    return jsonify(Error = "Team statistics Record not found for athlete id:{} in event id:{}.".format(aID,eID)),404  
            except:
                return jsonify(ERROR="Unable to verify medal based team event from DAO."), 500
            
            mappedResult = self.mapEventTeamStatsToDict(result)
            dao.commitChanges()
            return jsonify(Medal_Based_Event_Team_Stats = mappedResult),200
        else:
            # Create and Validate new Medal_Based_Event team stats
            try:
                result = dao.addTeamStatistics(eID,attributes['category_id'],attributes['medal_id'])

                if not result:
                    return jsonify(Error = "Problem inserting new team statistics record."),500
            except:
                return jsonify(ERROR="Unable to verify medal_based_event_team_stats from DAO."), 500
           
            dao.commitChanges()
            return jsonify(Medal_Based_Event_Team_Stats = "Added new team statistics record with id:{} for event id:{}.".format(result,eID)),201
           

    
    def addAllEventStatistics(self,eID,attributes):
        """
        Adds new statistics records with the provided information.

        Calls the MedalBasedEventDAO to add new statistics records and maps the result to
        to a JSON that contains the desired records. That JSON object 
        is then returned.

        Args:
            eID: the ID of the event for which the statistics record will be added.
            team_statistics: the IDs of the athletes for which the statistics record will be added.
            Attributes:
                Athlete Statistics:                    
                    category_id: The id of the category played by the athlete in the event.
                team_statistics: List containing various dictionary that follow the format below.                    
                    category_id: The id of the category played by the athlete in the event.
                    medal_id: The id of the medal awarded.                  
                uprm_score: the final score for the local uprm team.
                opponent_score: the final score for the opponent team.               
            
        Returns:
            A JSON the id for the new Medal Based Event record.
        """
        
        

        if not isinstance(eID,int): #or not self._validateStatisticsAttributes(attributes):
            return jsonify(Error = "Bad arguments"),400 

        local_score = attributes['uprm_score']     
        opponent_score = attributes['opponent_score']        
        team_statistics = attributes['team_statistics']
        athlete_statistics = attributes['athlete_statistics']
        
        
        # Validate Avoid Duplication Team Stats
        dao = MedalBasedEventDAO()
        try:
            for categories in team_statistics:     
                if dao.getMedalBasedEventTeamStatsID(eID,categories['category_id']):
                    return jsonify(Error = "Medal Based Event Team Stats Entry already exists for Event ID:{}".format(eID)),400
        except:
            return jsonify(ERROR="Unable to verify medal based event team stats from DAO."), 500
         
        # Validate existing event
        e_dao = EventDAO()
        try:           
            event = e_dao.getEventByID(eID)
            if not event:
                return jsonify(Error = "Event for ID:{} not found.".format(eID)),400
        except:
            return jsonify(ERROR="Unable to verify event from DAO."), 500
         
        # Get Event Team For Validation
        
        t_dao = TeamDAO()
        try:            
            tID = e_dao.getEventTeamByID(eID)
        except:
            return jsonify(ERROR="Unable to verify team from DAO."), 500
         

        # Validate that the event belongs to the correct sport.        
        try:
            sID = t_dao.getTeamSportByID(tID)[0]
            if sID != ATHLETSISM:
                return jsonify(Error = "Malformed Query, Event ID:{} does not belong to Medal Based.".format(eID)),400
            
            for categories in team_statistics:   
                if not self._validateCategory(sID,categories['category_id']):
                    return jsonify(Error = "Bad request, category {} does not match the sport of the team.".format(attributes['category_id'])),400
        except:
            return jsonify(ERROR="Unable to verify team from DAO."), 500
         
        # Go through every set of athlete to add attributes for. 
        for athlete_attributes in athlete_statistics:

            aID = athlete_attributes['athlete_id']            
            try:
                # Validate Avoid Duplication Medal Based Event Entry
               
                for stat in athlete_attributes['statistics']['medal_based_statistics']:
                    if dao.getMedalBasedEventID(eID,aID,stat['category_id']):
                        return jsonify(Error = "Medal Based Event Entry already exists for Event ID:{} and Athlete ID:{}".format(eID,aID)),400
                    
            except:
                return jsonify(ERROR="Unable to verify medal based event from DAO."), 500
         
            # Validate existing athlete 
            statistics = athlete_attributes['statistics']['medal_based_statistics']
            
            try:
                a_dao = AthleteDAO()                
                athlete = a_dao.getAthleteByID(aID)
                if not athlete:
                    return jsonify(Error = "Athlete for ID:{} not found.".format(aID)),400
            except Exception as e:
                return jsonify(ERROR="Unable to verify athlete from DAO." + str(e)), 500
         
            # Validate athlete belongs to team playing event           
            try:
                if not t_dao.getTeamMemberByIDs(aID,tID): 
                    return jsonify(Error = "Malformed Query, Athlete ID:{} does not belong to Team ID:{} from Event ID:{}.".format(aID,tID,eID)),400
            except:
                return jsonify(ERROR="Unable to verify team from DAO."), 500
         
            # Create and Validate new Medal_Based_Event
            try:
                for medalStats in statistics:
                    result = dao.addStatistics(eID,aID,medalStats['category_id'],medalStats['medal_id'])               
                    if not result:
                        return jsonify(Error = "Problem inserting new statistics record."),500
            except Exception as e:
                return jsonify(ERROR="Unable to verify medal based event from DAO." + str(e)), 500         
      
            
        # Create and Validate Final Score entry
        try:
            fs_dao = FinalScoreDAO()
            result = fs_dao.addFinalScore(eID,local_score, opponent_score)
            if not result:
                return jsonify(Error = "Problem inserting new final score record."),500
        except:
            return jsonify(ERROR="Unable to verify final score from DAO."), 500
         

        # Create and Validate new Medal_Based_Event team stats
        try:
            for teamStats in team_statistics:
                result = dao.addTeamStatistics(eID,teamStats['category_id'],teamStats['medal_id'])
                    
                if not result:
                    return jsonify(Error = "Problem inserting new team statistics record."),500
        except Exception as e:
            return jsonify(ERROR="Unable to verify medal based event team statistics from DAO." + str(e)), 500
        fs_dao.commitChanges() 
        dao.commitChanges()
        return jsonify(Medal_Based_Event_Team_Stats = "Added new team statistics record with id:{} and individual statistics for event id:{}.".format(result,eID)),201



#===========================//III.PUTS//====================================

    def editStatistics(self,eID,aID,attributes): # Instantiates a Medal Based Event DAO in order to complete the desired put request and it returns a JSON with either a confirmation or error message.
        """
        Updates the statistics for the medal based event with the given IDs.

        Calls the MedalBasedEventDAO to update the statistics of a medal based event. It then
        maps the result to a JSON that contains the desired record. That JSON 
        object is then returned.

        Args:
            eID: the ID of the event for which the statistics record will be updated.
            aID: the ID of the athlete for which the statistics record will be updated.
            attributes:               
                category_id: The id of the category played by the athlete in the event.
                medal_id: The id of the medal awarded.
        Returns:
            A JSON containing all the user with the updated entry.
        """
        if not isinstance(eID,int) or not isinstance(aID,int) or not self.validateAttributes(attributes) or not self._validateMedalCategory(attributes['category_id']):
            return jsonify(Error = "Bad arguments"),400


        # Validate Exists in order to update
        
        dao = MedalBasedEventDAO()
        try:        
           
            if not dao.getMedalBasedEventID(eID,aID,attributes['category_id']):
                return jsonify(Error = "Medal Based Event Entry does not exists for Event ID:{} and Athlete ID:{}".format(eID,aID)),404 
        except:
            return jsonify(ERROR="Unable to verify medal_based_event from DAO."), 500

        # Validate existing event       
        try:
            e_dao = EventDAO()            
            event = e_dao.getEventByID(eID)
            if not event:
                return jsonify(Error = "Event for ID:{} not found.".format(eID)),400
        except:
            return jsonify(ERROR="Unable to verify event from DAO."), 500
         
        # Validate existing athlete       
        try:
            a_dao = AthleteDAO()
            athlete = a_dao.getAthleteByID(aID)
            if not athlete:
                return jsonify(Error = "Athlete for ID:{} not found.".format(aID)),400
        except:
            return jsonify(ERROR="Unable to verify athlete from DAO."), 500
         
        
       

        try:            
            result = dao.editStatistics(eID,aID,attributes['category_id'],attributes['medal_id'])               
            if not result:
                return jsonify(Error = "Statistics Record not found for athlete id:{} in event id:{}.".format(aID,eID)),404
        except:
            return jsonify(ERROR="Unable to verify medal based event from DAO."), 500
         
        #update and validate Medal Based Event Team Statistic
        try:
            team_result = dao.editTeamStatistics(eID,attributes['category_id'])
            if not team_result:
                return jsonify(Error = "Team Statistics Record not found for event id:{}.".format(eID)),404
            print('G')
            mappedResult = self.mapEventAthleteStatsToDict(result)
        except Exception as e:
            return jsonify(ERROR="Unable to verify medal based event team statistics from DAO." + str(e)), 500
         
        dao.commitChanges()
        return jsonify(Medal_Based_Event_Athlete_Statistics = mappedResult),200


    def editTeamStatistics(self,eID,cID): 
        """
        Updates the team statistics for the medal based event with the given ID and aggregates of existing data.

        Calls the MedalBasedEventDAO to update the statistics of a medal based event. It then
        maps the result to a JSON that contains the desired record. That JSON 
        object is then returned.

        Args:
            eID: the ID of the event for which the statistics record will be updated.
            cID: The ID of the category which the statistics record will be added.        
            
        Returns:
            A JSON containing all the user with the updated entry.
        """
        if not isinstance(eID,int) or not isinstance(cID,int) or not self._validateMedalCategory(cID):
            return jsonify(Error = "Bad arguments"),400

        # Validate exists so can update 
        dao = MedalBasedEventDAO()       
        try:            
            if not dao.getMedalBasedEventTeamStatsID(eID,cID):
                return jsonify(Error = "Medal Based Event Team Stats Entry does not exists for Event ID:{}".format(eID)),400
        except:
            return jsonify(ERROR="Unable to verify medal_based_event_team_stats from DAO."), 500

        # Validate existing event        
        try:
            e_dao = EventDAO()
            event = e_dao.getEventByID(eID)
            if not event:
                return jsonify(Error = "Event for ID:{} not found.".format(eID)),400
        except:
            return jsonify(ERROR="Unable to verify event from DAO."), 500
         
        # Update and Validate Medal Based event team stats, format returnable        
        try:            
            result = dao.editTeamStatistics(eID,cID)
            if not result:
                return jsonify(Error = "Team Statistics Record not found for event id:{}.".format(eID)),404
            
        except Exception as e:
            return jsonify(ERROR="Unable to verify medal based event team statistics from DAO." + str(e)), 500
         
        dao.commitChanges()
        return jsonify(Medal_Based_Event_Team_Stats = "Edited the medal based event team stats with the following ids:{} ".format(result)),200

#===========================//IV.REMOVE//====================================
    def removeStatistics(self,eID,aID,cID): # Instantiates a Medal Based Event DAO in order to complete the desired put request and it returns a JSON with either a confirmation or error message.
        """
        Invalidates a statistics record in the database based on the given IDs.

        Calls the MedalBasedEventDAO to invalidate a statistics record. It then
        maps the result to a JSON that contains the desired record. That JSON 
        object is then returned.

        Args:
            eID: the ID of the event for which the statistics record will be invalidated.
            aID: the ID of the athlete for which the statistics record will be invalidated.
            cID: The ID of the category which the statistics record will be invalidated.
            
        Returns:
            A JSON containing the id of the invalidated record.
        """
        if not isinstance(eID,int) or not isinstance(aID,int) or not isinstance(cID,int) or not self._validateMedalCategory(cID):
            return jsonify(Error = "Bad arguments"),400

        # Validate existing event        
        try:
            e_dao = EventDAO()
            event = e_dao.getEventByID(eID)
            if not event:
                return jsonify(Error = "Event for ID:{} not found.".format(eID)),400
        except:
            return jsonify(ERROR="Unable to verify event from DAO."), 500
         
        
        # Validate existing athlete 
        
        try:
            a_dao = AthleteDAO()
            athlete = a_dao.getAthleteByID(aID)
            if not athlete:
                return jsonify(Error = "Athlete for ID:{} not found.".format(aID)),400
        except:
            return jsonify(ERROR="Unable to verify athlete from DAO."), 500
         
        # Remove Medal_Based_Event Statistics and format returnabe
        
        
        try:
            dao = MedalBasedEventDAO()            
            result = dao.removeStatistics(eID,aID,cID)
            if not result:
                return jsonify(Error = "Statistics Record not found with event id:{} for athlete id:{}.".format(eID,aID)),404
        except Exception as e:
            return jsonify(ERROR="Unable to verify medal based event from DAO." + str(e)), 500
         
        #update and validate Medal Based Event Team Statistic
        try:
            team_result = dao.editTeamStatistics(eID,cID)
            if not team_result:
                return jsonify(Error = "Team Statistics Record not found for event id:{}.".format(eID)),404
            
        except:
            return jsonify(ERROR="Unable to verify medal based event team statistics from DAO."), 500

        dao.commitChanges()
        return jsonify(Medal_Based_Event_Athlete_Statistics = "Removed statistics record with id:{} for athlete id:{} in event id:{}.".format(result,aID,eID)),200

    
    def removeTeamStatistics(self,eID,cID): 
        """
        Invalidates a team statistics record in the database based on the given ID.

        Calls the MedalBasedEventDAO to invalidate a team statistics record. It then
        maps the result to a JSON that contains the desired record. That JSON 
        object is then returned.

        Args:
            eID: the ID of the event for which the statistics record will be invalidated.
            cID: The ID of the category which the statistics record will be invalidated.
            
        Returns:
            A JSON the id of the invalidated Medal Based Event.
        """

       
        
        #validate parameters given
        if not isinstance(eID,int):
            return jsonify(Error = "Bad arguments"),400

        #validate existing event
        try:
            event = EventDAO().getEventByID(eID)
            if not event:
                return jsonify(Error = "Event with id:{} was not found.".format(eID)),404                 
    
        except:
           return jsonify("Problem ocurred while fetching a medal based event."),400
         
        # Remove Medal_Based_Event Team Statistics and format returnabe
        
        try:
            dao = MedalBasedEventDAO()
            result = dao.removeTeamStatistics(eID,cID)
            if not result:
                return jsonify(Error = "Team Statistics Record not found with event id:{}.".format(eID)),404
        except:
            return jsonify(ERROR="Unable to verify medal based event team stats from DAO."), 500
         
        dao.commitChanges()
        return jsonify(Medal_Based_Event_Team_Statistics = "Removed team statistics record with id:{} for event id:{}.".format(result,eID)),200




       
    

    def validateAttributes(self,attributes):
        """
        Validates the attibutes given for a 
        medal based event.

        Args:
            attributes: Dictionary of attributes containing 
                        the statisctics for a medal based event.
        
        Returns:
            True if a valid attributes were given, False otherwise.
        """

        if not isinstance(attributes,dict):
            return False        
        
        if 'medal_id' not in attributes:
            return False       
        if 'category_id' not in attributes:
            return False             
        
        if not isinstance(attributes['medal_id'],int) or attributes['medal_id'] < 0 or attributes['medal_id'] > 4:
            return False  
        
        if not isinstance(attributes['category_id'],int):
            return False                                        
            
        return True

    def _validateStatisticsAttributes(self,attributes):

        if not 'athlete_statistics' in attributes:
            return False

        if not isinstance(attributes['athlete_statistics'],list):
            return False

        for athlete_attributes in attributes['athlete_statistics']:
                      

            if not 'athlete_id' in athlete_attributes:
                return False
            if not 'statistics' in athlete_attributes:
                return False
            if not athlete_attributes['statistics']:
                return False
            if not isinstance(athlete_attributes['statistics'],dict):
                return False
            if not 'match_based_statistics' in athlete_attributes['statistics']:
                return False
            if not athlete_attributes['statistics']['match_based_statistics']:
                return False
            if not isinstance(athlete_attributes['statistics']['match_based_statistics'],dict):
                return False

            athlete_statistics = athlete_attributes['statistics']['match_based_statistics']

            if not 'matches_played' in athlete_statistics:
                return False
            if not 'matches_won' in athlete_statistics:
                return False
            if not 'category_id' in athlete_statistics:
                return False
           

            if not isinstance(athlete_statistics['matches_played'],int) or athlete_statistics['matches_played'] < 0:
                return False
        
            if not isinstance(athlete_statistics['matches_won'],int) or athlete_statistics['matches_won'] < 0:
                return False
            
            if not isinstance(athlete_statistics['category_id'],int) or athlete_statistics['category_id'] < 0:
                return False   

        if  not 'team_statistics' in attributes:
            return False

        team_statistics = attributes['team_statistics'] 
        if not isinstance(team_statistics,list):
            return False
           
        for t_statistics in team_statistics:
            match_based_statistics = t_statistics

            if not isinstance(match_based_statistics,dict):
                return False

            if not 'matches_played' in match_based_statistics:
                return False
            if not 'matches_won' in match_based_statistics:
                return False
            if not 'category_id' in match_based_statistics:
                return False  

            if not isinstance(match_based_statistics['matches_played'],int):
                return False
        
            if not isinstance(match_based_statistics['matches_won'],int):
                return False
            
            if not isinstance(match_based_statistics['category_id'],int):
                return False                                 
            
        return True

    def _validateCategory(self,sID,category_id):

        if sID == ATHLETSISM:
            return category_id in CATEGORIES['ATHLETSISM']                

        elif sID == TENNIS_IDF:
            return category_id in CATEGORIES['TENNIS_IDF']
              
        elif sID == TABLE_TENNIS_IDM:
            return category_id in CATEGORIES['TABLE_TENNIS_IDM']
                
        elif sID == TABLE_TENNIS_IDF:
            return category_id in CATEGORIES['TABLE_TENNIS_IDF']

    
    def _validateMedalCategory(self,category_id):
        for sport in CATEGORIES.keys():
            if category_id in CATEGORIES[sport]:
                return True
        return False
    

   
        




