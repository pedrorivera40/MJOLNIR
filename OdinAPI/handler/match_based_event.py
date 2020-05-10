from flask import jsonify
from .event_result import EventResultHandler
from .dao.final_score_dao import FinalScoreDAO
from .dao.event_dao import EventDAO
from .dao.athlete_dao import AthleteDAO
from .dao.match_based_event_dao import MatchBasedEventDAO
from .dao.team_dao import TeamDAO

#Constants
TENNIS_IDM = 9
TENNIS_IDF = 18
TABLE_TENNIS_IDM = 7
TABLE_TENNIS_IDF = 15
CATEGORIES = dict(TENNIS_IDM=[5,7],TENNIS_IDF=[11,6],TABLE_TENNIS_IDM=[3,8],TABLE_TENNIS_IDF=[4,10])


class MatchBasedEventHandler():

   

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

        stat_info['matches_played'] = record[0]
        stat_info['matches_won'] = record[1] 
        stat_info['category_id'] = record[6]

        event_info['category_name'] = record[2]        
        event_info['event_id'] = record[3]
        event_info['athlete_id'] = record[4]
        event_info['match_based_event_id'] = record[5]       
        
        return dict(event_info= event_info, event_statistics = stat_info)

    # for team statistics
    def mapEventTeamStatsToDict(self,record):
        stat_info = {}
        event_info = {}

        stat_info['matches_played'] = record[0]
        stat_info['matches_won'] = record[1]

        event_info['category_name'] = record[2]       
        event_info['event_id'] = record[3]        
        event_info['match_based_event_team_stats_id'] = record[4]

        
        return dict(event_info= event_info, event_statistics = stat_info)
        # UPRM_Score = final_record[0], Opponent_Score = final_record[1]
    
    def mapEventSeasonCollectionToDict(self,record):
        event_info = {}
        stat_info = {}   
        

       
        event_info['event_id'] = record[0]
        event_info['event_date'] = record[1]
        event_info['category_name'] = record[4]
        event_info['athlete_id'] = record[6]
        event_info['match_based_event_id'] = record[5]

        stat_info['matches_played'] = record[2]
        stat_info['matches_won'] = record[3]

        result = dict(Event = event_info, Event_Statistics = stat_info)
        return result

    def mapAthleteSeasonAggregate(self, record):
        athlete_info = {}
        stat_info = {}        
        athlete_info['athlete_id'] = record[3]
        athlete_info['first_name'] = record[4]
        athlete_info['middle_name'] = record[5]
        athlete_info['last_names'] = record[6]
        athlete_info['number'] = record[7]
        athlete_info['profile_image_link'] = record[8]

        stat_info['matches_played'] = record[0]
        stat_info['matches_won'] = record[1]
        stat_info['category_name'] = record[2]
        

        result = dict(Athlete = athlete_info, Event_Statistics = stat_info)
        return result

    def mapTeamSeasonAggregate(self, record):
        stat_info = {}
        
        stat_info['matches_played'] = record[0]
        stat_info['matches_won'] = record[1]
        stat_info['category_name'] = record[2]
        

        result = dict(team_id = record[3], Event_Statistics = stat_info)
        return result


    def mapEventAllStatsToDict(self,team_records,athlete_records,final_record):

        try:
            event_info = dict(
                event_id = team_records[0][3]                           
            )
            opponent_name = team_records[0][5]
        except:
            event_info = dict(
                event_id = team_records[3]                
            )
            opponent_name = team_records[5]
        
        match_based_statistics = {}
                               
        
        for teamResults in team_records:
            match_based_statistics[teamResults[2]] = {'match_based_team_stats_id':teamResults[4],'matches_played':teamResults[0],'matches_won':teamResults[1]}
           


        team_statistics = dict(match_based_statistics = match_based_statistics)
       
        athlete_statistics = []

        for athlete_record in athlete_records:
            athlete_info = dict(
                athlete_id = athlete_record[0],
                first_name = athlete_record[1],
                middle_name = athlete_record[2],
                last_names = athlete_record[3],    
                number = athlete_record[4],
                profile_image_link = athlete_record[5],
                match_based_event_id = athlete_record[10]
            )
            statistics = dict(
                matches_played = athlete_record[6],
                matches_won = athlete_record[7],
                category_name = athlete_record[8],
                category_id = athlete_record[11]                
            )

            athlete_statistics.append(dict(athlete_info = athlete_info, statistics = statistics))
        
        result = dict(event_info = event_info, team_statistics = team_statistics, 
        athlete_statistic = athlete_statistics, uprm_score = final_record[0], 
        opponent_score = final_record[1],opponent_name = opponent_name)#NOTE:This opponent name is not in final score dao.
        return result

#===========================//HANDLERS//==================================
#===========================//I.GETS//====================================

    def getAllAthleteStatisticsByEventIdAndCategoryId(self,eID,aID,cID):
        """
        Gets all the statistics for a given event and athlete. 

        Calls the MatchBasedEventDAO to get event statistics and maps the result to
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
        if not isinstance(eID,int) or not isinstance(aID,int) or not self._validateMatchCategory(cID):
            return jsonify(Error = "Argumentos incorrectos fueron dados."),400

        #validate existing event
        try:
            event = EventDAO().eventExists(eID)
            if not event:
                return jsonify(Error = "Evento con id:{} no fue encontrado.".format(eID)),404                 
    
        except Exception as e:
            print(e)
            return jsonify(Error = "Ocurrió un problema interno tratando de buscar un evento de partido."),500
        
        #validate existing athlete 
        try:
            athlete = AthleteDAO().athleteExists(aID)
            if not athlete:
                return jsonify(Error = "Atleta con id:{} no fue encotrado.".format(aID)),404                
        
        except Exception as e:
            print(e)
            return jsonify(Error = "Ocurrió un problema interno tratando de buscar un evento de partido."),500

        
        try:
            result = MatchBasedEventDAO().getAllAthleteStatisticsByEventIdAndCategoryId(eID,aID,cID)
            if not result:
                return jsonify(Error = "No se encontraron estadísticas para atletas."),404
            
            #print(result)
            mappedResult = self.mapEventAthleteStatsToDict(result)

            return jsonify(Match_Based_Event_Athlete_Statistics = mappedResult),200
        except Exception as e:          
            print(e)
            return jsonify(Error = "Ocurrió un problema interno tratando de buscar las estadísticas de atletas para un evento de partido."),500
        
        
       
       
    def getAllTeamStatisticsByEventIdAndCategoryId(self,eID,cID):
        """
        Gets all the statistics for a given event. 

        Calls the MatchBasedEventDAO to get event team statistics and maps the result to
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
            if not isinstance(eID,int) or not self._validateMatchCategory(cID):
                return jsonify(Error = "Argumentos incorrectos fueron dados."),400
        except:
            return jsonify(Error = "Argumentos incorrectos fueron dados."),400

        #validate existing event
        try:
            event = EventDAO().eventExists(eID)
            if not event:
                return jsonify(Error = "Evento con id:{} no fue encontrado.".format(eID)),404                 
    
        except Exception as e:
            print(e)
            return jsonify(Error = "Ocurrió un problema interno tratando de buscar un evento de partido."),500
       
        try:
            dao = MatchBasedEventDAO()
            result = dao.getAllTeamStatisticsByEventIdAndCategoryId(eID,cID)
            if not result:
                return jsonify(Error = "Estadisísticas de equipo pare un evento de partido no fueron encontradas para el evento con id: {}".format(eID)),404
            mappedResult = self.mapEventTeamStatsToDict(result)
        except Exception as e:
            print(e)
            return jsonify(Error="No se pudo verificar las estadísticas de equipo para un evento de partido."), 500
         
        return jsonify(Match_Based_Event_Team_Stats = mappedResult),200

    def getAllAthleteStatisticsPerSeason(self,aID,seasonYear):
        """
        Gets all the statistics for a given athlete during a given season. 

        Calls the MatchBasedEventDAO to get event statistics and maps the result to
        to a JSON that contains all the statistics for that athlete during the given season
        in the system. That JSON object is then returned.

        Args:
            seasonYear: the season year of which statistics need to be fetched
            aID: The ID of the athlete of which statistics need to be fetched
            
        Returns:
            A JSON containing all the statistics in the system for the specified athlete and season year.
        """

        if not isinstance(aID,int) or not isinstance(seasonYear,int):
            return jsonify(Error = "Argumentos incorrectos fueron dados."),400
        
        #validate existing athlete 
        try:
            athlete = AthleteDAO().athleteExists(aID)
            if not athlete:
                return jsonify(Error = "Atleta con id:{} no fue encotrado.".format(aID)),404                
        
        except:            
            return jsonify(Error = "Ocurrió un problema interno tratando de buscar un evento de partido."),500        
        
        
        try:
            dao = MatchBasedEventDAO()
            result = dao.getAllAthleteStatisticsPerSeason(aID,seasonYear)
            if not result:
                return jsonify(Error = "Estadísticas de un evento de partido no fueron encontradas para el atleta con id: {} en la temporada: {}.".format(aID,seasonYear)),404
            mappedResult = []
            for athlete_statistics in result:                     
                mappedResult.append(self.mapEventSeasonCollectionToDict(athlete_statistics))
            
        except:
            return jsonify(Error="No se pudo verificar el evento de partido."), 500
         
        return jsonify(Match_Based_Event_Season_Athlete_Statistics = mappedResult), 200


    def getAggregatedAthleteStatisticsPerSeason(self,aID,seasonYear):
        """
        Gets aggregated statistics for a given athlete during a given season. 

        Calls the MatchBasedEventDAO to get aggregated event statistics and maps the result to
        to a JSON that contains all the statistics for that athlete during the given season
        in the system. That JSON object is then returned.

        Args:
            seasonYear: the season year of which statistics need to be fetched
            aID: The ID of the athlete of which statistics need to be fetched
            
        Returns:
            A JSON containing aggregated  statistics in the system for the specified athlete and season year.
        """

        if not isinstance(aID,int) or not isinstance(seasonYear,int):
            return jsonify(Error = "Argumentos incorrectos fueron dados."),400

        #validate existing athlete 
        
        try:
            a_dao = AthleteDAO() 
            athlete = a_dao.athleteExists(aID)
            if not athlete:
                return jsonify(Error = "El atleta con id:{} no fue encontrado.".format(aID)),404
        except:
            return jsonify(Error="No se pudo verificar el atleta."), 500
         
        # validate existing match_based_event entries and format returnable
        
        try:
            dao = MatchBasedEventDAO()
            result = dao.getAggregatedAthleteStatisticsPerSeason(aID,seasonYear)
            if not result:
                return jsonify(Error = "Estadísticas de un evento de partido no fueron encontradas para el atleta con id: {} en la temporada: {}.".format(aID,seasonYear)),404
            mappedResult = self.mapAthleteSeasonAggregate(result)
            #print(mappedResult)
        except:
            return jsonify(Error="No se pudo verificar un evento de partido."), 500
         
        return jsonify(Match_Based_Event_Season_Athlete_Statistics = mappedResult), 200

    
    def getAllAggregatedAthleteStatisticsPerSeason(self,sID,seasonYear):
        """
        Gets all aggregated statistics for athletes during a given season. 

        Calls the MatchBasedEventDAO to get  all aggregated event statistics and maps the result to
        to a JSON that contains all the aggregated statistics  during the given season
        in the system. That JSON object is then returned.

        Args:
            seasonYear: the season year of which statistics need to be fetched
            sID: The ID of the sport of which statistics need to be fetched
            
        Returns:
            A JSON containing all the aggregated statistics in the system for the specified sport and season year.
        """

        if not isinstance(sID,int) or not isinstance(seasonYear,int):
            return jsonify(Error = "Argumentos incorrectos fueron dados."),400
   
        # validate existing match_based_event entries and format returnable
        
        try:
            dao = MatchBasedEventDAO()
            result = dao.getAllAggregatedAthleteStatisticsPerSeason(sID,seasonYear)
            if not result:
                return jsonify(Error = "Estadísticas para un evento de partido no fueron encontradas para el deporte con id:{} en la temporada:{}.".format(sID,seasonYear)),404
            mappedResult = []
            for athlete_statistics in result:                     
                mappedResult.append(self.mapAthleteSeasonAggregate(athlete_statistics))
            #print(mappedResult)
        except Exception as e:
            print(e)
            return jsonify(Error="No se pudo verificar un evento de partido."), 500
         
        return jsonify(Match_Based_Event_Season_Athlete_Statistics = mappedResult), 200


    
    def getAggregatedTeamStatisticsPerSeason(self,sID,seasonYear):
        """
        Gets all aggregated statistics for a given team during a season.  

        Calls the MatchBasedEventDAO to get  all aggregated event statistics and maps the result to
        to a JSON that contains all the statistics for that athlete during the given season
        in the system. That JSON object is then returned.

        Args:
            seasonYear: the season year of which statistics need to be fetched
            sID: The ID of the sport of which team statistics need to be fetched
            
        Returns:
            A JSON containing the aggregated team statistics in the system for the specified team and season year.
        """
        if not isinstance(sID,int) or not isinstance(seasonYear,int):
            return jsonify(Error = "Argumentos incorrectos fueron dados."),400
         
        # validate existing match_based_event entries and format returnable
        
        try:
            dao = MatchBasedEventDAO()
            result = dao.getAggregatedTeamStatisticsPerSeason(sID,seasonYear)
            if not result:
                return jsonify(Error = "Estadísticas de equipo para un evento de partido no fueron encontradas para el deporte con id:{} en la temporada:{}.".format(sID,seasonYear)),404
            mappedResult = []
            if len(result) == 2:#This has two lists
                for row in result:
                    mappedResult.append(self.mapTeamSeasonAggregate(row))
            else:
                mappedResult = self.mapTeamSeasonAggregate(result)
            
        except Exception as e:
            print(e)
            return jsonify(Error="Estadísticas de equipo para un evento de partido no pudieron ser verificadas."), 500
         
        return jsonify(Match_Based_Event_Season_Team_Statistics = mappedResult), 200

    
    def getAllStatisticsByEventID(self,eID):
        """
        Gets all the team and individual statistics for a given event. 

        Calls the MatchBasedEventDAO to get event statistics and maps the result to
        to a JSON that contains all the statistics for that event in the system. 
        That JSON object is then returned.

        Args:
            eID: The ID of the event of which statistics need to be fetched
            
        Returns:
            A JSON containing all the statistics in the system for the specified event.
        """

        #validate parameters given
        
        
        if not isinstance(eID,int):
            return jsonify(Error = "Argumentos incorrectos fueron dados."),400
       

        #validate existing event
        try:
            event = EventDAO().eventExists(eID)
            if not event:
                return jsonify(Error = "Evento con id:{} no fue encontrado.".format(eID)),404                 
    
        except:
           return jsonify(Error = "Ocurrió un problema interno tratando de buscar un evento de partido."),500

        dao = MatchBasedEventDAO()

        try:  
            categoriesPlayed = dao.getCategoriesOfTheEvent(eID)
            if not categoriesPlayed:
                return jsonify(Error = "Estadisísticas de equipo pare un evento de partido no fueron encontradas para el evento con id: {}".format(eID)),404  

            team_results = []
            print(categoriesPlayed)
            for category in categoriesPlayed:
                team_results.append(dao.getAllTeamStatisticsByEventIdAndCategoryId(eID,category))
            if not team_results:
                return jsonify(Error = "Estadisísticas de equipo pare un evento de partido no fueron encontradas para el evento con id: {}".format(eID)),404
        except Exception as e:
            print(e)
            return jsonify(Error="Estadísticas de equipo para un evento de partido no pudieron ser verificadas."), 500
        
        try:
            all_stats_result = dao.getAllStatisticsByEventID(eID)
            if not all_stats_result:            
                return jsonify(Error = "No se encontraron estadísticas para un evento de partido  pare el evento con id:{}.".format(eID)),404
        except Exception as e:
            print(e)
            return jsonify(Error="No se pudo verificar el evento de partido."), 500
         
        try:
            fs_dao = FinalScoreDAO()
            final_score_result = fs_dao.getFinalScore(eID)
            if not final_score_result:                
                return jsonify(Error = "No se encontraron estadísticas para un evento de partido  pare el evento con id:{}.".format(eID)),404            
            mappedResult = self.mapEventAllStatsToDict(team_results,all_stats_result, final_score_result)
            return jsonify(Match_Based_Event_Statistics = mappedResult),200

        except Exception as e:
            print(e)
            return jsonify(Error="No se pudo verificar la puntuación final."), 500
         
      

#===========================//II.POSTS//====================================
    def addStatistics(self,eID,aID,attributes): 
        """
        Adds a new statistics record with the provided information.

        Calls the MatchBasedEventDAO to add a new statistics record and maps the result to
        to a JSON that contains the desired record. That JSON object 
        is then returned.

        Args:
            eID: the ID of the event for which the statistics record will be added.
            aID: the ID of the athlete for which the statistics record will be added.
            attributes:
                matchesPlayed: Number of matches played by the athlete in the event.
                matchesWon: Number of matches won by the athlete in the event.
                category_id: The id of the category played by the athlete in the event.
            
        Returns:
            A JSON containing the id for the new Match Based Event record.
        """

        if not isinstance(eID,int) or not isinstance(aID,int) or not self.validateAttributes(attributes):
            return jsonify(Error = "Argumentos incorrectos fueron dados."),400

        # Validate Avoid Duplication
        
        dao = MatchBasedEventDAO()

        try:           
            if dao.getMatchBasedEventID(eID,aID,attributes['category_id']):
                return jsonify(Error = "Ya existen una entrada de un evento de partido para el evento con id:{} y el atleta con id:{}.".format(eID,aID)),403 
        except:
            return jsonify(Error="No se puede verificar el evento de partido."), 500

        # Validate existing event  
        e_dao = EventDAO()      
        try:            
            event = e_dao.eventExists(eID)
            if not event:
                return jsonify(Error = "Evento con id:{} no fue encontrado.".format(eID)),404
        except:
            return jsonify(Error="No se pudo verificar el evento."), 500
       
        
        # Get Event Team For Validation        
        t_dao = TeamDAO()
        try:
            t_dao = TeamDAO()
            tID = e_dao.getEventTeamByID(eID)
        except:
            return jsonify(Error="No se pudo verificar el evento."), 500

        # Validate that the event belongs to the correct sport and the category is correct.     
        try:
            sID = t_dao.getTeamSportByID(tID)[0] 
            print(sID)
            if sID != TENNIS_IDM and sID != TENNIS_IDF and sID != TABLE_TENNIS_IDM and sID != TABLE_TENNIS_IDF:
                return jsonify(Error = "El evento con id:{} no es un evento de partido.".format(eID)),400

            if not self._validateCategory(sID,attributes['category_id']):
                return jsonify(Error = "La categoría con id:{} no le pertenece al deporte del equipo.".format(attributes['category_id'])),400        
            
        except:
            return jsonify(Error="No se pudo verificar el equipo."), 500

        # Validate existing athlete 
        
        try:
            a_dao = AthleteDAO()
            athlete = a_dao.athleteExists(aID)
            if not athlete:
                return jsonify(Error = "El atleta con id:{} no fue encontrado.".format(aID)),404
        except:
            return jsonify(Error="No se pudo verificar el atleta."), 500

        # Validate athlete belongs to team playing event        
        try:
            if not t_dao.getTeamMemberByIDs(aID,tID):
                return jsonify(Error = "El atleta con id:{} no pertenece al equipo con id:{} del evento con id:{}.".format(aID,tID,eID)),400
        except:
            return jsonify(Error="No se pudo verificar el equipo."), 500

        #check if existing invalid, in this case we PUT/update instead of POST/add. sorta. 
        invalid_duplicate = False
        try:
            if dao.getMatchBasedEventIDInvalid(eID,aID,attributes['category_id']):
                invalid_duplicate = True
        except:
            return jsonify(Error="No se puede verificar el evento de partido."), 500
        
        #the case of there already existing an entry, but marked as invalid
        if invalid_duplicate:
            try:
                result = dao.editStatistics(eID,aID,attributes['matches_played'],attributes['matches_won'],attributes['category_id'])
                    
                if not result:
                    return jsonify(Error = "No se encontraron estadísticas para el atleta con id:{} en el evento con id:{}.".format(aID,eID)),404
                
            except Exception as e:
                print(e)
                return jsonify(Error="No se pudo verificar el evento de partido."), 500
        else:
            # Create and Validate new Match_Based_Event
            try:
                result = dao.addStatistics(eID,aID,attributes['matches_played'],attributes['matches_won'],attributes['category_id'])                    
                if not result:
                    return jsonify(Error = "Ocurrió un problema interno intentando añadir nuevas estadísticas."),500
            except:
                return jsonify(Error="No se pudo verificar el evento de partido."), 500
        
        #update and validate Match Based Event Team Statistic
        # If existing Team Statistics update, else create
        try:
            if dao.getMatchBasedEventTeamStatsID(eID,attributes['category_id']) or dao.getMatchBasedEventTeamStatsIDInvalid(eID,attributes['category_id']):
                team_result = dao.editTeamStatistics(eID,attributes['category_id'])
                if not team_result:
                    return jsonify(Error = "Estadísticas de equipo ne fueron encontradas para el evento con id:{}.".format(eID)),404
            else:                           
                dao.addTeamStatistics(eID,attributes['matches_played'],attributes['matches_won'],attributes['category_id'])
        except Exception as e:
            print(e)
            return jsonify(Error="No se pudo verificar las estadísticas de un equipo para un evento de partido."), 500       

        
        if invalid_duplicate:
            
            dao.commitChanges()
            return jsonify(Match_Based_Event_Athlete_Statistics = "Se editaron las estadísticas de un evento de partido para el atleta con id:{} en el evento con id:{}.".format(aID,eID)),200
        else:
            dao.commitChanges()
            return jsonify(Match_Based_Event_Athlete_Statistics = "Se añadió una nueva entrada de estadísticas con id:{}  para el atlteta con id:{} en el  evento con id:{}.".format(result,aID,eID)),201

    
    def addTeamStatistics(self,eID,attributes): 
        """
        Adds a new team statistics record with the provided information.

        Calls the MatchBasedEventDAO to add a new team statistics record and maps the result to
        to a JSON that contains the desired record. That JSON object 
        is then returned.

        Args:
            eID: the ID of the event for which the statistics record will be added.
            attributes:
                matchesPlayed: Number of matches played by the athlete in the event.
                matchesWon: Number of matches won by the athlete in the event.
                category_id: The id of the category played by the athlete in the event.
            
        Returns:
            A JSON containing the id for the new Match Based Event team statistics record.
        """

        if not isinstance(eID,int) or not self.validateAttributes(attributes):
            return jsonify(Error = "Argumentos incorrectos fueron dados."),400

        # Validate Avoid Duplication
        dao = MatchBasedEventDAO()
        try:            
            if dao.getMatchBasedEventTeamStatsID(eID,attributes['category_id']):
                return jsonify(Error = "Ya existe una entrada para estadísticas  de equipo  para el evento con id:{}.".format(eID)),500
        except:
            return jsonify(Error="No se pudo verificar las estadísticas de equipo para un evento de partido."), 500

        # Validate existing event
        e_dao =EventDAO()        
        try:            
            event = e_dao.eventExists(eID)
            if not event:
                return jsonify(Error = "Evento con id:{} no fue encontrado.".format(eID)),404
        except:
            return jsonify(Error="No se pudo verificar el evento."), 500

        # Get Event Team For Validation 
        t_dao = TeamDAO()      
        try:           
            tID = e_dao.getEventTeamByID(eID)
        except:
            return jsonify(Error="No se pudo verificar el equipo."), 500

        # Validate that the event belongs to the correct sport.        
        try:
            sID = t_dao.getTeamSportByID(tID)[0]
            
            if sID != TENNIS_IDM and sID != TENNIS_IDF and sID != TABLE_TENNIS_IDM and sID != TABLE_TENNIS_IDF:                
                return jsonify(Error = "El evento con id:{} no es un evento de partido.".format(eID)),400
             
            if not self._validateCategory(sID,attributes['category_id']):
                return jsonify(Error = "La categoría con id:{} no le pertenece al deporte del equipo.".format(attributes['category_id'])),400
            
        except:
            return jsonify(Error="No se pudo verificar el equipo."), 500

        #check if existing invalid, in this case we PUT/update instead of POST/add 
        invalid_duplicate = False
        try:
            if dao.getMatchBasedEventTeamStatsIDInvalid(eID,attributes['category_id']):
                invalid_duplicate = True
        except:
            return jsonify(Error="No se pudo verificar las estadísticas de equipo."), 500
        #the case of there already existing an entry, but marked as invalid
        if invalid_duplicate:
            try:
                result = dao.editTeamStatistics(eID,attributes['category_id'])
                if not result:
                    return jsonify(Error = "No se encontraron estadísticas de equipo para el atlta con id:{} en el evento con id:{}.".format(aID,eID)),404  
            except:
                return jsonify(Error="No se pudo verificar las estadísticas de equipo para un evento de partido."), 500
            
            mappedResult = self.mapEventTeamStatsToDict(result)
            dao.commitChanges()
            return jsonify(Match_Based_Event_Team_Stats = mappedResult),201
        else:
            # Create and Validate new Match_Based_Event team stats
            try:
                result = dao.addTeamStatistics(eID,attributes['matches_played'],attributes['matches_won'],attributes['category_id'])

                if not result:
                    return jsonify(Error = "Ocurrió un problema interno insertando una nueva entrada de estadísticas de equipo."),500
            except:
                return jsonify(Error="No se pudo verificar las estadísticas de equipo para un evento de partido."), 500
           
            dao.commitChanges()
            return jsonify(Match_Based_Event_Team_Stats = "Se insertaron nuevas estadísticas de equipo para el evento con id:{}".format(eID)),201
           

    
    def addAllEventStatistics(self,eID,attributes):
        """
        Adds new statistics records with the provided information.

        Calls the MatchBasedEventDAO to add new statistics records and maps the result to
        to a JSON that contains the desired records. That JSON object 
        is then returned.

        Args:
            eID: the ID of the event for which the statistics record will be added.
            team_statistics: the IDs of the athletes for which the statistics record will be added.
            Attributes:
                Athlete Statistics:
                    matchesPlayed: Number of matches played by the athlete in the event.
                    matchesWon: Number of matches won by the athlete in the event.
                    category_id: The id of the category played by the athlete in the event.
                team_statistics: List containing various dictionary that follow the format below.

                    matchesPlayed: Number of matches played by the athlete in the event.
                    matchesWon: Number of matches won by the athlete in the event.
                    category_id: The id of the category played by the athlete in the event.                    
                uprm_score: the final score for the local uprm team.
                opponent_score: the final score for the opponent team.               
            
        Returns:
            A JSON the id for the new Match Based Event record.
        """
        
        

        if not isinstance(eID,int) or not self._validateStatisticsAttributes(attributes):
            return jsonify(Error = "Argumentos incorrectos fueron dados."),400 

        local_score = attributes['uprm_score']     
        opponent_score = attributes['opponent_score']        
        team_statistics = attributes['team_statistics']
        athlete_statistics = attributes['athlete_statistics']
        
        
        # Validate Avoid Duplication Team Stats
        dao = MatchBasedEventDAO()
        try:
            for categories in team_statistics:     
                if dao.getMatchBasedEventTeamStatsID(eID,categories['category_id']):
                    return jsonify(Error = "Ya existe una entrada para estadísticas  de equipo  para el evento con id:{}.".format(eID)),400
        except:
            return jsonify(Error="Estadísticas de equipo para un evento de partido no pudieron ser verificadas."), 500
         
        # Validate existing event
        e_dao = EventDAO()
        try:           
            event = e_dao.eventExists(eID)
            if not event:
                return jsonify(Error = "Evento con id:{} no fue encontrado.".format(eID)),404
        except:
            return jsonify(Error="No se pudo verificar el evento."), 500
         
        # Get Event Team For Validation
        
        t_dao = TeamDAO()
        try:            
            tID = e_dao.getEventTeamByID(eID)
        except:
            return jsonify(Error="No se pudo verificar el equipo."), 500
         

        # Validate that the event belongs to the correct sport.        
        try:
            sID = t_dao.getTeamSportByID(tID)[0]
            if sID != TENNIS_IDM and sID != TENNIS_IDF and sID != TABLE_TENNIS_IDM and sID != TABLE_TENNIS_IDF :
                return jsonify(Error = "El evento con id:{} no es un evento de partido.".format(eID)),400
            
            for categories in team_statistics:   
                if not self._validateCategory(sID,categories['category_id']):
                    return jsonify(Error = "La categoría con id:{} no le pertenece al deporte del equipo.".format(attributes['category_id'])),400
        except:
            return jsonify(Error="No se pudo verificar el equipo."), 500
         
        # Go through every set of athlete to add attributes for. 
        for athlete_attributes in athlete_statistics:

            aID = athlete_attributes['athlete_id']            
            try:
                # Validate Avoid Duplication Match Based Event Entry
                if dao.getMatchBasedEventID(eID,aID,athlete_attributes['statistics']['match_based_statistics']['category_id']):
                    return jsonify(Error = "Ya existen una entrada de un evento de partido para el evento con id:{} y el atleta con id:{}.".format(eID,aID)),400
            except:
                return jsonify(Error="No se pudo verificar el evento de partido."), 500
         
            # Validate existing athlete 
            statistics = athlete_attributes['statistics']['match_based_statistics']
            
            try:
                a_dao = AthleteDAO()                
                athlete = a_dao.athleteExists(aID)
                if not athlete:
                    return jsonify(Error = "El atleta con id:{} no fue encontrado.".format(aID)),404
            except Exception as e:
                print(e)
                return jsonify(Error="No se pudo verificar el atleta."), 500
         
            # Validate athlete belongs to team playing event           
            try:
                if not t_dao.getTeamMemberByIDs(aID,tID): 
                    return jsonify(Error = "El atleta con id:{} no pertenece al equipo con id:{} del evento con id:{}.".format(aID,tID,eID)),400
            except:
                return jsonify(Error="No se pudo verificar el equipo."), 500
         
            # Create and Validate new Match_Based_Event
            try:
                result = dao.addStatistics(eID,aID,statistics['matches_played'],statistics['matches_won'],statistics['category_id'])               
                if not result:
                    return jsonify(Error = "Ocurrió un problema interno intentando añadir nuevas estadísticas."),500
            except:
                return jsonify(Error="No se pudo verificar el evento de partido."), 500         
      
            
        # Create and Validate Final Score entry
        try:
            fs_dao = FinalScoreDAO()
            result = fs_dao.addFinalScore(eID,local_score, opponent_score)
            if not result:
                return jsonify(Error = "Problem inserting new final score record."),500
        except:
            return jsonify(Error="No se pudo verificar la puntuación final."), 500
         

        # Create and Validate new Match_Based_Event team stats
        try:
            for teamStats in team_statistics:
                result = dao.addTeamStatistics(eID,teamStats['matches_played'],teamStats['matches_won'],teamStats['category_id'])
                    
                if not result:
                    return jsonify(Error = "Ocurrió un problema interno insertando una nueva entrada de estadísticas de equipo."),500
        except Exception as e:
            print(e)
            return jsonify(Error="No se pudo verificar las estadísticas de un equipo para un evento de partido."), 500
        fs_dao.commitChanges() 
        dao.commitChanges()
        return jsonify(Match_Based_Event_Team_Stats = "Se insertaron nuevas estadísticas de equipo e individuos para el evento con id:{}.".format(eID)),201



#===========================//III.PUTS//====================================

    def editStatistics(self,eID,aID,attributes): # Instantiates a Match Based Event DAO in order to complete the desired put request and it returns a JSON with either a confirmation or error message.
        """
        Updates the statistics for the match based event with the given IDs.

        Calls the MatchBasedEventDAO to update the statistics of a match based event. It then
        maps the result to a JSON that contains the desired record. That JSON 
        object is then returned.

        Args:
            eID: the ID of the event for which the statistics record will be updated.
            aID: the ID of the athlete for which the statistics record will be updated.
            attributes:
                matchesPlayed: Number of matches played by the athlete in the event.
                matchesWon: Number of matches won by the athlete in the event.
                category_id: The id of the category played by the athlete in the event.
            
        Returns:
            A JSON containing all the user with the updated entry.
        """
        if not isinstance(eID,int) or not isinstance(aID,int) or not self.validateAttributes(attributes) or not self._validateMatchCategory(attributes['category_id']):
            return jsonify(Error = "Argumentos incorrectos fueron dados."),400


        # Validate Exists in order to update
        
        dao = MatchBasedEventDAO()
        try:        
           
            if not dao.getMatchBasedEventID(eID,aID,attributes['category_id']):
                return jsonify(Error = "No existe una entrada de un evento de partido  para el evento con id:{} y atleta con id:{}.".format(eID,aID)),404 
        except:
            return jsonify(Error="No se puede verificar el evento de partido."), 500

        # Validate existing event       
        try:
            e_dao = EventDAO()            
            event = e_dao.eventExists(eID)
            if not event:
                return jsonify(Error = "Evento con id:{} no fue encontrado.".format(eID)),404
        except:
            return jsonify(Error="No se pudo verificar el evento."), 500
         
        # Validate existing athlete       
        try:
            a_dao = AthleteDAO()
            athlete = a_dao.athleteExists(aID)
            if not athlete:
                return jsonify(Error = "El atleta con id:{} no fue encontrado.".format(aID)),404
        except:
            return jsonify(Error="No se pudo verificar el atleta."), 500
         
        
       

        try:            
            result = dao.editStatistics(eID,aID,attributes['matches_played'],attributes['matches_won'],attributes['category_id'])               
            if not result:
                return jsonify(Error = "No se encontraron estadísticas para el atleta con id:{} en el evento con id:{}.".format(aID,eID)),404
        except:
            return jsonify(Error="No se pudo verificar el evento de partido."), 500
         
        #update and validate Match Based Event Team Statistic
        try:
            team_result = dao.editTeamStatistics(eID,attributes['category_id'])
            if not team_result:
                return jsonify(Error = "Estadísticas de equipo ne fueron encontradas para el evento con id:{}.".format(eID)),404            
        except:
            return jsonify(Error="No se pudo verificar las estadísticas de un equipo para un evento de partido."), 500
         
        dao.commitChanges()
        return jsonify(Match_Based_Event_Athlete_Statistics = "Se edtaron las estadísticas de un evento de partido para el atleta con id:{} en el evento con id:{}.".format(aID,eID)),200


    def editTeamStatistics(self,eID,cID): 
        """
        Updates the team statistics for the match based event with the given ID and aggregates of existing data.

        Calls the MatchBasedEventDAO to update the statistics of a match based event. It then
        maps the result to a JSON that contains the desired record. That JSON 
        object is then returned.

        Args:
            eID: the ID of the event for which the statistics record will be updated.
            cID: The ID of the category which the statistics record will be added.        
            
        Returns:
            A JSON containing all the user with the updated entry.
        """
        if not isinstance(eID,int) or not isinstance(cID,int) or not self._validateMatchCategory(cID):
            return jsonify(Error = "Argumentos incorrectos fueron dados."),400

        # Validate exists so can update 
        dao = MatchBasedEventDAO()       
        try:            
            if not dao.getMatchBasedEventTeamStatsID(eID,cID):
                return jsonify(Error = "Match Based Event Team Stats Entry does not exists for Event ID:{}".format(eID)),404
        except:
            return jsonify(Error="No se pudo verificar las estadísticas de equipo para un evento de partido."), 500

        # Validate existing event        
        try:
            e_dao = EventDAO()
            event = e_dao.eventExists(eID)
            if not event:
                return jsonify(Error = "Evento con id:{} no fue encontrado.".format(eID)),404
        except:
            return jsonify(Error="No se pudo verificar el evento."), 500
         
        # Update and Validate Match Based event team stats, format returnable        
        try:            
            result = dao.editTeamStatistics(eID,cID)
            if not result:
                return jsonify(Error = "Estadísticas de equipo ne fueron encontradas para el evento con id:{}.".format(eID)),404
            mappedResult = self.mapEventTeamStatsToDict(result)
        except:
            return jsonify(Error="No se pudo verificar las estadísticas de un equipo para un evento de partido."), 500
         
        dao.commitChanges()
        return jsonify(Match_Based_Event_Team_Stats = mappedResult),200

#===========================//IV.REMOVE//====================================
    def removeStatistics(self,eID,aID,cID): # Instantiates a Match Based Event DAO in order to complete the desired put request and it returns a JSON with either a confirmation or error message.
        """
        Invalidates a statistics record in the database based on the given IDs.

        Calls the MatchBasedEventDAO to invalidate a statistics record. It then
        maps the result to a JSON that contains the desired record. That JSON 
        object is then returned.

        Args:
            eID: the ID of the event for which the statistics record will be invalidated.
            aID: the ID of the athlete for which the statistics record will be invalidated.
            cID: The ID of the category which the statistics record will be invalidated.
            
        Returns:
            A JSON containing the id of the invalidated record.
        """
        if not isinstance(eID,int) or not isinstance(aID,int) or not isinstance(cID,int) or not self._validateMatchCategory(cID):
            return jsonify(Error = "Argumentos incorrectos fueron dados."),400

        # Validate existing event        
        try:
            e_dao = EventDAO()
            event = e_dao.eventExists(eID)
            if not event:
                return jsonify(Error = "Evento con id:{} no fue encontrado.".format(eID)),404
        except:
            return jsonify(Error="No se pudo verificar el evento."), 500
         
        
        # Validate existing athlete 
        
        try:
            a_dao = AthleteDAO()
            athlete = a_dao.athleteExists(aID)
            if not athlete:
                return jsonify(Error = "El atleta con id:{} no fue encontrado.".format(aID)),404
        except:
            return jsonify(Error="No se pudo verificar el atleta."), 500
         
        # Remove Match_Based_Event Statistics and format returnabe
        
        
        try:
            dao = MatchBasedEventDAO()            
            result = dao.removeStatistics(eID,aID,cID)
            if not result:
                return jsonify(Error = "No se encontraron estadísticas de un evento de partido para el atleta con id:{} en el evento con id:{}.".format(aID,eID)),404
        except Exception as e:
            print(e)
            return jsonify(Error="No se pudo verificar el evento de partido."), 500
         
        #update and validate Match Based Event Team Statistic
        try:
            team_result = dao.editTeamStatistics(eID,cID)
            if not team_result:
                return jsonify(Error = "Estadísticas de equipo ne fueron encontradas para el evento con id:{}.".format(eID)),404
            
        except:
            return jsonify(Error="No se pudo verificar las estadísticas de un equipo para un evento de partido."), 500

        dao.commitChanges()
        return jsonify(Match_Based_Event_Athlete_Statistics = "Se removieron las estadísticas de un evento de partido para la entrada con id:{}  para el atleta con id:{} en el evento con id:{}.".format(result,aID,eID)),200

    
    def removeTeamStatistics(self,eID,cID): 
        """
        Invalidates a team statistics record in the database based on the given ID.

        Calls the MatchBasedEventDAO to invalidate a team statistics record. It then
        maps the result to a JSON that contains the desired record. That JSON 
        object is then returned.

        Args:
            eID: the ID of the event for which the statistics record will be invalidated.
            cID: The ID of the category which the statistics record will be invalidated.
            
        Returns:
            A JSON the id of the invalidated Match Based Event.
        """

       
        
        #validate parameters given
        if not isinstance(eID,int):
            return jsonify(Error = "Argumentos incorrectos fueron dados."),400

        #validate existing event
        try:
            event = EventDAO().eventExists(eID)
            if not event:
                return jsonify(Error = "Evento con id:{} no fue encontrado.".format(eID)),404                 
    
        except:
           return jsonify(Error = "Ocurrió un problema interno tratando de buscar un evento de partido."),500
         
        # Remove Match_Based_Event Team Statistics and format returnabe
        
        try:
            dao = MatchBasedEventDAO()
            result = dao.removeTeamStatistics(eID,cID)
            if not result:
                return jsonify(Error = "Una entrada para estadísticas de equipo no fueron encontradas para el evento con id:{}.".format(eID)),404
        except:
            return jsonify(Error="Estadísticas de equipo para un evento de partido no pudieron ser verificadas."), 500
         
        dao.commitChanges()
        return jsonify(Match_Based_Event_Team_Statistics = "Se removieron las estadísticas de equipo de un evento de partido para la entrada con id:{} en el evento con id:{}.".format(result,eID)),200




       
    

    def validateAttributes(self,attributes):
        """
        Validates the attibutes given for a 
        match based event.

        Args:
            attributes: Dictionary of attributes containing 
                        the statisctics for a match based event.
        
        Returns:
            True if a valid attributes were given, False otherwise.
        """

        if not isinstance(attributes,dict):
            return False        
        
        if 'matches_played' not in attributes:
            return False
        if 'matches_won' not in attributes:
            return False
        if 'category_id' not in attributes:
            return False             
        
        if not isinstance(attributes['matches_played'],int):
            return False
        
        if not isinstance(attributes['matches_won'],int):
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

        if sID == TENNIS_IDM:
            return category_id in CATEGORIES['TENNIS_IDM']                

        elif sID == TENNIS_IDF:
            return category_id in CATEGORIES['TENNIS_IDF']
              
        elif sID == TABLE_TENNIS_IDM:
            return category_id in CATEGORIES['TABLE_TENNIS_IDM']
                
        elif sID == TABLE_TENNIS_IDF:
            return category_id in CATEGORIES['TABLE_TENNIS_IDF']

    
    def _validateMatchCategory(self,category_id):
        for sport in CATEGORIES.keys():
            if category_id in CATEGORIES[sport]:
                return True
        return False
    

   
        




