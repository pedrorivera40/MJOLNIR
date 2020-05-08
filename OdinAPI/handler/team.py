from flask import jsonify

from .dao.team_dao import TeamDAO
from .dao.athlete_dao import AthleteDAO
from .dao.sport_dao import SportDAO


class TeamHandler():

    # getAllTeams()//Instantiates a Team DAO in order to complete the desired get request and it returns a JSON with the desired information or with an error message.

    # getTeam(sID,tBranch) //Instantiates a Team DAO in order to complete the desired get request and it returns a JSON with the desired information or with an error message.

    # getTeamById(tID) //Instantiates a Team DAO in order to complete the desired get request and it returns a JSON with the desired information or with an error message.

    # getTeamByYear(sID,tBranch,tYear) //Instantiates a Team DAO in order to complete the desired get information or with an error message.

    # addTeam(sID,tBranch, tRoster, tYear) //Instantiates a Team DAO in order to complete the desired post request and it returns a JSON with either a confirmation or error message.

    # editTeam(tID,sID,tRoster,tYear)//Instantiates a Team DAO in order to complete the desired put request and it returns a JSON with either a confirmation or error message.

    # removeTeam(tID,sID)//Instantiates a Team DAO in order to complete the desired put request and it returns a JSON with either a confirmation or error message.

    # mapTeamToDict(record)//Maps a Team record to a dictionary and returns it.

    # NEW:
    # def getTeamSportByID(self, tID): #helper for event result handlers (NOT NEEDED)
    # def getTeamMemberByIDs(self, aID,tID): # validates if an athlete belongs to a team. returns info.
    # def addTeamMember(self, aID,tID): # adds someone to ateam
    # def editTeamMember(self, aID,tID): (NOT NEEDED)
    # def removeTeamMember(self, aID,tID):
    # def getTeamMembersByID(self, tID):
    # def addTeamMembers()
    # ===========================//DICTIONARY MAPPERS//==================================
    # NEW (name): basic team info
    def mapTeamToDict(self, record):
        team_info = {}

        team_info['team_id'] = record[0]
        team_info['sport_id'] = record[1]
        team_info['season_year'] = record[2]
        team_info['team_image_url'] = record[3]
        team_info['sport_name'] = record[4]
        team_info['branch_id'] = record[5]
        team_info['branch_name'] = record[6]
        team_info['about_team'] = record[7]

        result = dict(team_info=team_info)
        return result

    # NEW
    """
    team_members_id, team_id, athlete_id, 
    first_name,middle_name,last_names, number, profile_image_link,
    height_inches, study_program, school_of_precedence, years_of_participation,
    positions[], categories[]
    """

    def mapTeamMembersToDict(self, record):

        # {
        # "team_id":1,
        # "team_members":[
        #     {
        #         "team_member_id":1,
        #         "athlete_id":1,
        #         "first_name":"Bruce",
        #         "middle_name":"Batman",
        #         "last_names":"Wayne",
        #         "number":27,
        #         "profile_image_link":"www.google.com",
        #         "height_inches":70,
        #         "study_program": "detective",
        #         "school_of_precedence":"gotham high",
        #         "years_of_participation":3,
        #         "positions":["position1","position2"],
        #         "categories":["category1","category2"]
        #     },
        #     {
        #         "team_member_id":2,
        #         "athlete_id":2,
        #         "first_name":"Clark",
        #         "middle_name":"Superman",
        #         "last_names":"Kent",
        #         "number":3,
        #         "profile_image_link":"www.google.com",
        #         "height_inches":70,
        #         "study_program": "reporter",
        #         "school_of_precedence":"smallville high",
        #         "years_of_participation":3,
        #         "positions":["position1","position2"],
        #         "categories":["category1","category2"]
        #     }
        #     ]
        # }

        team_members = []
        for team_member in record:
            positions_list = []
            categories_list = []
            for position in team_member[12]:
                if position is not None:
                    positions_list.append(position)
            if len(positions_list) == 0:
                positions_list = None
            for category in team_member[13]:
                if category is not None:
                    categories_list.append(category)
            if len(categories_list) == 0:
                categories_list = None
            team_id = team_member[1]
            team_members.append(dict(
                team_members_id=team_member[0],
                athlete_id=team_member[2],
                first_name=team_member[3],
                middle_name=team_member[4],
                last_names=team_member[5],
                number=team_member[6],
                profile_image_link=team_member[7],
                height_inches=team_member[8],
                study_program=team_member[9],
                school_of_precedence=team_member[10],
                years_of_participation=team_member[11],
                positions=positions_list,
                categories=categories_list
            ))

        result = dict(team_id=team_id, team_members=team_members)
        return result

    def mapTeamMemberToDict(self, record):

        # {
        # "team_member":
        #     {
        #         "team_member_id":1,
        #         "team_id":1,
        #         "athlete_id":1,
        #         "first_name":"Bruce",
        #         "middle_name":"Batman",
        #         "last_names":"Wayne",
        #         "number":27,
        #         "profile_image_link":"www.google.com",
        #     }
        # }

        team_member = dict(
            team_members_id=record[0],
            team_id=record[1],
            athlete_id=record[2],
            first_name=record[3],
            middle_name=record[4],
            last_names=record[5],
            number=record[6],
            profile_image_link=record[7]
        )

        result = dict(team_member=team_member)
        return result

    # DEPRECATED, DONT NEED ALL TOGETHER DUE TO DIFFERENT VIEWS
    # # Updated: this will be so that it has the team AND the members
    # def mapTeamToDict(self,record):

    #     # This one will have the TEAM info first and then the info of each member

    #     ## WHAT IT RETURNS:
    #     # {
    #     # "team":{
    #     #     "team_id":1,
    #     #     "sport_id":1,
    #     #     "sport_name":"SampleSport",
    #     #     "season_year":"2020",
    #     #     "team_image_url":"www.google.com"
    #     #     "branch_id":2,
    #     #     "branch_name":"Femenina"
    #     # }
    #     # "team_members":[
    #     #     {
    #     #         "team_member_id":1,
    #     #         "first_name"="Bruce",
    #     #         "middle_name"="Batman",
    #     #         "last_names"="Wayne",
    #     #         "number"=27,
    #     #         "profile_image_link"="www.google.com",
    #     #     },
    #     #     {
    #     #         "team_member_id":2,
    #     #         "first_name"="Clark",
    #     #         "middle_name"="Superman",
    #     #         "last_names"="Kent",
    #     #         "number"=3,
    #     #         "profile_image_link"="www.google.com",
    #     #     },
    #     #     }
    #     #     ]
    #     # }

    #     #  SELECT team.id as team_id, team.sport_id, team.season_year, team.team_image_url, sport.name as sport_name,
    #     #         branch.id as branch_id, branch.name as branch_name
    #     # SELECT team_members.id as team_members_id, team_members.team_id, team_members.athlete_id,
    #     #         athlete.id,athlete.first_name,athlete.middle_name,athlete.last_names, athlete.number, athlete.profile_image_link

    #     team_info = {}
    #     team_info['team_id']=record[0]
    #     team_info['sport_id']=record[1]
    #     team_info['season_year']=record[2]
    #     team_info['team_image_url']=record[3]
    #     team_info['sport_name']=record[4]
    #     team_info['branch_id']=record[5]
    #     team_info['branch_name']=record[6]

    #     team_members = []

    #     for team_member in record:
    #         team_members.append(dict(
    #             team_members_id = record[0],
    #             team_id = record[1],
    #             athlete_id = record[2],
    #             first_name = record[3],
    #             middle_name = record[4],
    #             last_names = record[5],
    #             number = record[6],
    #             profile_image_link = record[7]
    #             ))

    #     result = dict()
    #     return result

    # ===========================//HANDLERS//==================================
    # ===========================//I.GETS//====================================

    # TODO: Likely remove, not necessary as of now. check front end
    # gets all the information...
    def getAllTeams(self):
        """
        Gets all the teams in the system. 

        Calls the TeamDAO to get team entries and maps the result
        to a JSON that contains all the teams in the system. That
        JSON object is then returned.

        Returns:
            A JSON containing all the teams in the system.
        """
        try:
            dao = TeamDAO()
            result = dao.getAllTeams()
            if not result:
                return jsonify(Error="No se encontraron Equipos."), 404
            mappedResult = []
            for team in result:
                mappedResult.append(self.mapTeamToDict(team))
        except (TypeError, ValueError):
            return jsonify(ERROR="Solicitud Incorrecta, Error de Tipo."), 400
        except:
            return jsonify(ERROR="No se pudo verificar Equipo desde DAO."), 500

        return jsonify(Teams=mappedResult), 200

    def getTeams(self, sID):
        """
        Gets all the teams in the system that match the given sport id. 

        Calls the TeamDAO to get team entries and maps the result
        to a JSON that contains all the teams in the system that match the sport ID. That
        JSON object is then returned.

        Args:
            sID: the ID of the sport of which the teams will be returned

        Returns:
            A JSON containing all the teams in the system for that sport.
        """
        try:
            # TODO: validate sport
            pass
        except (TypeError, ValueError):
            return jsonify(ERROR="Solicitud Incorrecta, Error de Tipo."), 400
        except:
            return jsonify(ERROR="No se pudo verificar deporte desde DAO."), 500

        try:
            dao = TeamDAO()
            result = dao.getTeams(sID)
            if not result:
                return jsonify(Error="No se encontraron equipos para deporte con ID:{}.".format(sID)), 404
            mappedResult = []
            for team in result:
                mappedResult.append(self.mapTeamBasicToDict(team))
        except (TypeError, ValueError):
            return jsonify(ERROR="Solicitud Incorrecta, Error de Tipo."), 400
        except:
            return jsonify(ERROR="No se pudo verificar Equipo desde DAO."), 500

        return jsonify(Teams=mappedResult), 200

    # same info as getTeam, but different query
    def getTeamByID(self, tID):
        """
        Gets the team in the system that matches the given team id.  

        Calls the TeamDAO to get the team entry and maps the result
        to a JSON that contains the team in the system that matches the team ID. 
        That JSON object is then returned.

        Args:
            tID: the ID of the team which will be returned

        Returns:
            A JSON containing the team.
        """
        # it's a get, so tID validation is just if it exists as a valid entry

        # GET TEAM
        try:
            dao = TeamDAO()
            result = dao.getTeamByID(tID)
            if not result:
                return jsonify(Error="Equipo no encontro con ID:{}.".format(tID)), 404
            mappedResult = self.mapTeamToDict(result)
        except (TypeError, ValueError):
            return jsonify(ERROR="Solicitud Incorrecta, Error de Tipo."), 400
        except:
            return jsonify(ERROR="No se pudo verificar Equipo desde DAO."), 500

        return jsonify(Team=mappedResult), 200

    # this one would be general team information, similar to get all teams but filtered by season
    # updated: dont need branch
    def getTeamByYear(self, sID, tYear):
        """
        Gets the team in the system that matches the given sport and season year.  

        Calls the TeamDAO to get the team entry and maps the result
        to a JSON that contains the team in the system that matches the sport and season. 
        That JSON object is then returned.

        Args:
            sID: the ID of the sport of which the team will be returned
            tYear: the season year from which the team will be returned

        Returns:
            A JSON containing the team.
        """
        # it's a get, so tID validation is just if it exists as a valid entry
        try:
            # TODO: validate sport
            # TODO: do we validate year? prob not, just an int.
            pass
        except (TypeError, ValueError):
            return jsonify(ERROR="Solicitud Incorrecta, Error de Tipo."), 400
        except:
            return jsonify(ERROR="No se pudo verificar deporte desde DAO."), 500

        # get team
        try:
            dao = TeamDAO()
            result = dao.getTeamByYear(sID, tYear)
            if not result:
                return jsonify(Error="Equipo no se encontro para Deporte con ID:{} y Año de Temporada:{}.".format(sID, tYear)), 404
            mappedResult = self.mapTeamToDict(result)
        except (TypeError, ValueError):
            return jsonify(ERROR="Solicitud Incorrecta, Error de Tipo."), 400
        except:
            return jsonify(ERROR="No se pudo verificar Equipo desde DAO."), 500

        return jsonify(Team=mappedResult), 200

    """
    team_members_id, team_id, athlete_id, 
    first_name,middle_name,last_names, number, profile_image_link,
    height_inches, study_program, school_of_precedence, years_of_participation,
    positions[], categories[]
    """

    def getTeamMembersByID(self, tID):
        """
        Gets the team members in the system that match the given team.  

        Calls the TeamDAO to get the team member entries and maps the result
        to a JSON that contains the team members in the system that match the team id.
        That JSON object is then returned.

        Args:
            tID: the ID of the team of which members will be fetched

        Returns:
            A JSON containing the team members
        """
        # Validate Existing Team
        try:
            dao = TeamDAO()
            if not dao.getTeamByID(tID):
                return jsonify(Error="Equipo no existe para ID:{}.".format(tID)), 400
        except (TypeError, ValueError):
            return jsonify(ERROR="Solicitud Incorrecta, Error de Tipo."), 400
        except:
            return jsonify(ERROR="No se pudo verificar Equipo desde DAO."), 500

        # get members
        try:
            result = dao.getTeamMembersByID(tID)
            if not result:
                return jsonify(Error="Equipo con ID:{} no tiene miembros.".format(tID)), 400
            mappedResult = self.mapTeamMembersToDict(result)
        except (TypeError, ValueError):
            return jsonify(ERROR="Solicitud Incorrecta, Error de Tipo."), 400
        except:
            return jsonify(ERROR="No se pudo verificar Miembros de Equipo desde DAO."), 500
        return jsonify(Team=mappedResult), 200

    def getTeamMemberByIDs(self, aID, tID):
        """
        Gets the team member entry in the system that matches the given athlete and team.  

        Calls the TeamDAO to get the team member entry and maps the result
        to a JSON that contains the team member in the system that matches the athlete and team. 
        That JSON object is then returned.

        Args:
            aID: the ID of the athlete from which the team member will be returned
            tID: the ID of the team from which the team member will be returned

        Returns:
            A JSON containing the team member.
        """
        # Validate Existing Team
        try:
            dao = TeamDAO()
            if not dao.getTeamByID(tID):
                return jsonify(Error="Equipo no existe para ID:{}.".format(tID)), 400
        except (TypeError, ValueError):
            return jsonify(ERROR="Solicitud Incorrecta, Error de Tipo."), 400
        except:
            return jsonify(ERROR="No se pudo verificar Equipo desde DAO."), 500

        # verify existing athlete & correct sport
        try:
            a_dao = AthleteDAO()
            athlete = a_dao.getAthleteByID(aID)
            if not athlete:
                return jsonify(Error="No se encontro Atleta para ID:{}.".format(aID)), 400
            # MOCKED METHOD TO GET ATHLETE SPORT
            athlete_sport = a_dao.getAthleteSportByID(aID)
            sID = dao.getTeamSportByID(tID)[0]
            if athlete_sport != sID:
                return jsonify(Error="Atleta con ID:{} no coincide con el ID de deporte:{} del Equipo, ya que tiene ID de deporte:{}".format(aID, sID,athlete_sport)), 400
        except (TypeError, ValueError):
            return jsonify(ERROR="Solicitud Incorrecta, Error de Tipo."), 400
        except:
            return jsonify(ERROR="No se pudo verificar Atleta desde DAO."), 500

        # get members
        try:
            result = dao.getTeamMemberByIDs(aID, tID)
            if not result:
                return jsonify(Error="Atleta con ID:{} no pertenece a equipo con ID:{}.".format(aID, tID)), 400
            mappedResult = self.mapTeamMemberToDict(result)
        except (TypeError, ValueError):
            return jsonify(ERROR="Solicitud Incorrecta, Error de Tipo."), 400
        except:
            return jsonify(ERROR="No se pudo verificar Miembros de Equipo desde DAO."), 500
        return jsonify(Team=mappedResult), 200
    # ===========================//II.POSTS//====================================
    # update: image link was missing? tRoster removed, separate

    def addTeam(self, sID, tYear, tImageLink, aboutTeam):
        """
        Adds a new team with the provided information.

        Calls the TeamDAO to add a new team record and maps the result to
        to a JSON. That JSON object is then returned.

        Args:
            sID: the sport id of the team to be added
            tYear: the season year of the team to be added
            tImageLink: the image link for the team
            aboutTeam: short description about team

        Returns:
            A JSON containing the id for the new Team record.
        """

        try:
            s_dao = SportDAO()
            if not s_dao.getSportById(sID):
                return jsonify(Error="Deporte con ID:{} no existe.".format(sID)), 400
        except (TypeError, ValueError):
            return jsonify(ERROR="Solicitud Incorrecta, Error de Tipo."), 400
        except:
            return jsonify(ERROR="No se pudo verificar deporte desde DAO."), 500

        # Validate Avoid Duplication Team
        try:
            dao = TeamDAO()
            if dao.getTeamByYear(sID, tYear):
                return jsonify(Error="Equipo ya existe para Deporte con ID:{} y Año de Temporada:{}.".format(sID, tYear)), 400
        except (TypeError, ValueError):
            return jsonify(ERROR="Solicitud Incorrecta, Error de Tipo."), 400
        except:
            return jsonify(ERROR="No se pudo verificar Equipo desde DAO."), 500

        # TODO: Validate Existing Duplicate, convert to update (need to create new DAO function)
        # TODO: Validate Sport (already done by validatig the athlete?)

        # add team (Check if previous existed)
        try:
            invalid_duplicate = dao.getTeamByYearInvalid(sID, tYear)
        except (TypeError, ValueError):
            return jsonify(ERROR="Solicitud Incorrecta, Error de Tipo."), 400
        except:
            return jsonify(ERROR="No se pudo verificar Equipo desde DAO."), 500
        # the case of there already existing an entry, but marked as invalid
        if invalid_duplicate:
            # edit team (since previously existed)
            team_id = invalid_duplicate[0]
            try:
                result = dao.editTeamByYear(sID, tYear, tImageLink, aboutTeam)
                if not result:
                    return jsonify(Error="Problema actualizando record de equipo."), 500
            except (TypeError, ValueError):
                return jsonify(ERROR="Solicitud Incorrecta, Error de Tipo."), 400
            except:
                return jsonify(ERROR="No se pudo verificar Equipo desde DAO."), 500

        # normal add
        else:
            # add the team
            try:
                team_id = dao.addTeam(sID, tYear, tImageLink, aboutTeam)
                if not team_id:
                    return jsonify(Error="Problema insertando nuevo record de equipo."), 500
            except (TypeError, ValueError):
                return jsonify(ERROR="Solicitud Incorrecta, Error de Tipo."), 400
            except:
                return jsonify(ERROR="No se pudo verificar Equipo desde DAO."), 500

        dao.commitChanges()
        # FIX BECAUSE IN CASE OF INVALID DID UPDATE AND DONT KNOW TEAM ID.
        return jsonify(Team="Se añadio un nuevo record de equipo con ID:{} para Deporte con ID:{} y Año de Temporada:{}.".format(team_id, sID, tYear))

    # NEW
    def addTeamMembers(self, tID, tRoster):
        """
        Adds a new team member record with the provided information.

        Calls the TeamDAO to add new team member records and maps the result to
        to a JSON. That JSON object 
        is then returned.

        Args:
            tID: the team to which members will be added
            tRoster:
                athlete_id: the id of an athlete that will be added to the team
        Returns:
            A JSON containing containing the id for the updated team.
        """
        # Validate Existing Team
        try:
            dao = TeamDAO()
            if not dao.getTeamByID(tID):
                return jsonify(Error="Equipo no existe para ID:{}.".format(tID)), 400
        except (TypeError, ValueError):
            return jsonify(ERROR="Solicitud Incorrecta, Error de Tipo."), 400
        except:
            return jsonify(ERROR="No se pudo verificar Equipo desde DAO."), 500

        # go through list and add members
        for team_member in tRoster:
            aID = team_member['athlete_id']

            # verify existing athlete & correct spot
            try:
                a_dao = AthleteDAO()
                athlete = a_dao.getAthleteByID(aID)
                if not athlete:
                    return jsonify(Error="No se encontro Atleta para ID:{}.".format(aID)), 400
                # MOCKED METHOD TO GET ATHLETE SPORT
                athlete_sport = a_dao.getAthleteSportByID(aID)
                sID = dao.getTeamSportByID(tID)[0]
                if athlete_sport != sID:
                    return jsonify(Error="Atleta con ID:{} no coincide con el ID de deporte:{} del Equipo.".format(aID, sID)), 400
            except (TypeError, ValueError):
                return jsonify(ERROR="Solicitud Incorrecta, Error de Tipo."), 400
            except:
                return jsonify(ERROR="No se pudo verificar Atleta desde DAO."), 500

            # Validate Avoid Duplication Team member
            try:
                if dao.getTeamMemberByIDs(aID, tID):
                    return jsonify(Error="Miembro de Equipo con ID de Atleta:{} ya existe para Equipo con ID:{}.".format(aID, tID)), 400
            except (TypeError, ValueError):
                return jsonify(ERROR="Solicitud Incorrecta, Error de Tipo."), 400
            except:
                return jsonify(ERROR="No se pudo verificar Equipo desde DAO."), 500

            # add team member
            try:
                invalid_duplicate = dao.getTeamMemberByIDsInvalid(aID, tID)
            except (TypeError, ValueError):
                return jsonify(ERROR="Solicitud Incorrecta, Error de Tipo."), 400
            except:
                return jsonify(ERROR="No se pudo verificar Miembro de Equipo desde DAO."), 500
            # the case of there already existing an entry, but marked as invalid
            if invalid_duplicate:
                # edit team member
                try:
                    result = dao.editTeamMember(aID, tID)
                    if not result:
                        return jsonify(Error="Problema actualizando el record de Miembro de Equipo."), 500
                except (TypeError, ValueError):
                    return jsonify(ERROR="Solicitud Incorrecta, Error de Tipo."), 400
                except:
                    return jsonify(ERROR="No se pudo verificar Miembro de Equipo desde DAO."), 500
            # normal add
            else:
                try:
                    athlete_id = dao.addTeamMember(aID, tID)
                    if not athlete_id:
                        return jsonify(Error="Problema insertando record de miembro de Equipo."), 500
                except (TypeError, ValueError):
                    return jsonify(ERROR="Solicitud Incorrecta, Error de Tipo."), 400
                except:
                    return jsonify(ERROR="No se pudo verificar Miembro de Equipo desde DAO."), 500

        dao.commitChanges()
        return jsonify(Team="Added new team members to team with id:{}".format(tID,)), 201

    # NEW
    def addTeamMember(self, aID, tID):
        """
        Adds a new team member record with the provided information.

        Calls the TeamDAO to add new team member records and maps the result to
        to a JSON. That JSON object 
        is then returned.

        Args:
            tID: the team to which member will be added
            athlete_id: the id of an athlete that will be added to the team
        Returns:
            A JSON containing containing the id for the updated team.
        """
        # Validate Existing Team
        try:
            dao = TeamDAO()
            if not dao.getTeamByID(tID):
                return jsonify(Error="Equipo no existe para ID:{}.".format(tID)), 400
        except (TypeError, ValueError):
            return jsonify(ERROR="Solicitud Incorrecta, Error de Tipo."), 400
        except:
            return jsonify(ERROR="No se pudo verificar Equipo desde DAO."), 500

        # verify existing athlete & correct sport
        try:
            a_dao = AthleteDAO()
            athlete = a_dao.getAthleteByID(aID)
            if not athlete:
                return jsonify(Error="No se encontro Atleta para ID:{}.".format(aID)), 400
            # MOCKED METHOD TO GET ATHLETE SPORT
            athlete_sport = a_dao.getAthleteSportByID(aID)
            sID = dao.getTeamSportByID(tID)[0]
            if athlete_sport != sID:
                return jsonify(Error="Atleta con ID:{} no coincide con el ID de deporte:{} del Equipo.".format(aID, sID)), 400
        except (TypeError, ValueError):
            return jsonify(ERROR="Solicitud Incorrecta, Error de Tipo."), 400
        except:
            return jsonify(ERROR="No se pudo verificar Atleta desde DAO."), 500

        # Validate Avoid Duplication Team member
        try:
            if dao.getTeamMemberByIDs(aID, tID):
                return jsonify(Error="Miembro de Equipo con ID de Atleta:{} ya existe para Equipo con ID:{}.".format(aID, tID)), 400
        except (TypeError, ValueError):
            return jsonify(ERROR="Solicitud Incorrecta, Error de Tipo."), 400
        except:
            return jsonify(ERROR="No se pudo verificar Equipo desde DAO."), 500

        # add team member
        try:
            invalid_duplicate = dao.getTeamMemberByIDsInvalid(aID, tID)
        except (TypeError, ValueError):
            return jsonify(ERROR="Solicitud Incorrecta, Error de Tipo."), 400
        except:
            return jsonify(ERROR="No se pudo verificar Miembro de Equipo desde DAO."), 500
        # the case of there already existing an entry, but marked as invalid
        if invalid_duplicate:
            # edit team member
            try:
                result = dao.editTeamMember(aID, tID)
                if not result:
                    return jsonify(Error="Problema actualizando el record de Miembro de Equipo."), 500
            except (TypeError, ValueError):
                return jsonify(ERROR="Solicitud Incorrecta, Error de Tipo."), 400
            except:
                return jsonify(ERROR="No se pudo verificar Miembro de Equipo desde DAO."), 500
        # normal add
        else:
            # add team member
            try:
                result = dao.addTeamMember(aID, tID)
                if not result:
                    return jsonify(Error="Problema insertando record de miembro de Equipo."), 500
            except (TypeError, ValueError):
                return jsonify(ERROR="Solicitud Incorrecta, Error de Tipo."), 400
            except:
                return jsonify(ERROR="No se pudo verificar Miembro de Equipo desde DAO."), 500

        dao.commitChanges()
        return jsonify(Team="Added athlete id:{} as a team member of team with id:{}".format(aID, tID,)), 201
    # ===========================//III.PUTS//====================================

    def editTeam(self, tID, tImageLink, aboutTeam):
        """"
        Updates the team with the given ID.

        Calls the TeamDAO to update the team record. It then
        maps the result to a JSON that contains the desired record. That JSON 
        object is then returned.

        Args:
            tID: the id of the team to be updated
            tImagelINK: the updated image link
            aboutTeam: short description about team

        Returns:
            A JSON containing the the updated entry.
        """

        # Validate Team Exists
        try:
            dao = TeamDAO()
            if not dao.getTeamByYear(tID):
                return jsonify(Error="Equipo no existe para ID:{}.".format(tID)), 400
        except (TypeError, ValueError):
            return jsonify(ERROR="Solicitud Incorrecta, Error de Tipo."), 400
        except:
            return jsonify(ERROR="No se pudo verificar Equipo desde DAO."), 500

        # TODO: Validate Existing Duplicate, convert to update (need to create new DAO function)
        # TODO: Validate Sport (already done by validatig the athlete?)

        # edit the team
        try:
            team_id = dao.editTeam(tID, tImageLink)
            if not team_id:
                return jsonify(Error="Problema actualizando record de equipo."), 500

            #mappedResult = self.mapTeamBasic(result)
        except (TypeError, ValueError):
            return jsonify(ERROR="Solicitud Incorrecta, Error de Tipo."), 400
        except:
            return jsonify(ERROR="No se pudo verificar Equipo desde DAO."), 500

        # return the updated team
        try:
            # verify this works
            returnable = dao.getTeamByID(tID)
            mappedResult = self.mapTeamToDict(returnable)
        except (TypeError, ValueError):
            return jsonify(ERROR="Solicitud Incorrecta, Error de Tipo."), 400
        except:
            return jsonify(ERROR="No se pudo verificar Equipo desde DAO."), 500
        dao.commitChanges()
        return jsonify(Team=mappedResult), 200

    def editTeamByYear(self, sID, tYear, tImageLink, aboutTeam):
        """"
        Updates the team with the given ID.

        Calls the TeamDAO to update the team record. It then
        maps the result to a JSON that contains the desired record. That JSON 
        object is then returned.

        Args:
            sID: the sport id of the team to be updated
            tYear: the season year of the team to be updated
            tImagelINK: the updated image link

        Returns:
            A JSON containing the the updated entry.
        """

        # Validate Team Exists
        try:
            dao = TeamDAO()
            if not dao.getTeamByYear(sID, tYear):
                return jsonify(Error="Equipo no existe para Deporte con ID:{} y Año de Temporada:{}.".format(sID, tYear)), 400
        except (TypeError, ValueError):
            return jsonify(ERROR="Solicitud Incorrecta, Error de Tipo."), 400
        except:
            return jsonify(ERROR="No se pudo verificar Equipo desde DAO."), 500

        # TODO: Validate Existing Duplicate, convert to update (need to create new DAO function)
        # TODO: Validate Sport (already done by validatig the athlete?)

        # edit the team
        try:
            team_id = dao.editTeamByYear(sID, tYear, tImageLink, aboutTeam)
            if not team_id:
                return jsonify(Error="Problema actualizando record de equipo."), 500

            #mappedResult = self.mapTeamBasic(result)
        except (TypeError, ValueError):
            return jsonify(ERROR="Solicitud Incorrecta, Error de Tipo."), 400
        except:
            return jsonify(ERROR="No se pudo verificar Equipo desde DAO."), 500

        # return the updated team
        try:
            # verify this works
            returnable = dao.getTeamByYear(sID, tYear)
            mappedResult = self.mapTeamToDict(returnable)
        except (TypeError, ValueError):
            return jsonify(ERROR="Solicitud Incorrecta, Error de Tipo."), 400
        except:
            return jsonify(ERROR="No se pudo verificar Equipo desde DAO."), 500
        dao.commitChanges()
        return jsonify(Team=mappedResult), 200

    # ===========================//IV.REMOVE//====================================

    # updated, dont need sport id
    def removeTeam(self, tID):
        """
        Invalidates a team record in the database based on the given ID.

        Calls the TeamDAO to invalidate a team record. It then
        maps the result to a JSON that contains the desired record. That JSON 
        object is then returned.

        Args:
            tID: the ID of the team for which the  record will be invalidated.

        Returns:
            A JSON containing the id of the invalidated record.
        """
        # Validate Team Exists
        try:
            dao = TeamDAO()
            if not dao.getTeamByID(tID):
                return jsonify(Error="Equipo no existe para ID:{}.".format(tID)), 400
        except (TypeError, ValueError):
            return jsonify(ERROR="Solicitud Incorrecta, Error de Tipo."), 400
        except:
            return jsonify(ERROR="No se pudo verificar Equipo desde DAO."), 500

        # TODO: Validate Existing Duplicate, convert to update (need to create new DAO function)
        # TODO: Validate Sport (already done by validatig the athlete?)

        # remove the team
        try:
            team_id = dao.removeTeam(tID)
            if not team_id:
                return jsonify(Error="Problema removiendo record de equipo."), 500
        except (TypeError, ValueError):
            return jsonify(ERROR="Solicitud Incorrecta, Error de Tipo."), 400
        except:
            return jsonify(ERROR="No se pudo verificar Equipo desde DAO."), 500

        dao.commitChanges()
        return jsonify(team="Removed team record with id:{}.".format(tID)), 200

    # new
    def removeTeamByYear(self, sID, tYear):
        """
        Invalidates a team record in the database based on the given ID.

        Calls the TeamDAO to invalidate a team record. It then
        maps the result to a JSON that contains the desired record. That JSON 
        object is then returned.

        Args:
            sID: the sport ID of the team for which the  record will be invalidated.
            tYear: the season year of the team for which the  record will be invalidated.

        Returns:
            A JSON containing the id of the invalidated record.
        """
        # Validate Team Exists
        try:
            dao = TeamDAO()
            if not dao.getTeamByYear(sID, tYear):
                return jsonify(Error="Equipo no existe para Deporte con ID:{} y Año de Temporada:{}.".format(sID, tYear)), 400
        except (TypeError, ValueError):
            return jsonify(ERROR="Solicitud Incorrecta, Error de Tipo."), 400
        except:
            return jsonify(ERROR="No se pudo verificar Equipo desde DAO."), 500

        # TODO: Validate Existing Duplicate, convert to update (need to create new DAO function)
        # TODO: Validate Sport (already done by validatig the athlete?)

        # remove the team
        try:
            team_id = dao.removeTeamByYear(sID, tYear)
            if not team_id:
                return jsonify(Error="Problema removiendo record de equipo."), 500
        except (TypeError, ValueError):
            return jsonify(ERROR="Solicitud Incorrecta, Error de Tipo."), 400
        except:
            return jsonify(ERROR="No se pudo verificar Equipo desde DAO."), 500

        dao.commitChanges()
        return jsonify(team="Removed team record for sport ID:{} team for season year:{}.".format(sID, tYear)), 200

    # NEW
    def removeTeamMember(self, aID, tID):
        """
        Invalidates a team member record in the database based on the given ID.

        Calls the TeamDAO to invalidate a team member record. It then
        maps the result to a JSON that contains the desired record. That JSON 
        object is then returned.

        Args:
            aID: the athlete ID of the team member for which the  record will be invalidated.
            tID: the team ID of the team for which the  record will be invalidated.

        Returns:
            A JSON containing the id of the invalidated record.
        """
        # Validate Existing Team
        try:
            dao = TeamDAO()
            if not dao.getTeamByID(tID):
                return jsonify(Error="Equipo no existe para ID:{}.".format(tID)), 400
        except (TypeError, ValueError):
            return jsonify(ERROR="Solicitud Incorrecta, Error de Tipo."), 400
        except:
            return jsonify(ERROR="No se pudo verificar Equipo desde DAO."), 500

        # go through list and add members

        # verify existing athlete & correct sport
        try:
            a_dao = AthleteDAO()
            athlete = a_dao.getAthleteByID(aID)
            if not athlete:
                return jsonify(Error="No se encontro Atleta para ID:{}.".format(aID)), 400
            # MOCKED METHOD TO GET ATHLETE SPORT
            athlete_sport = a_dao.getAthleteSportByID(aID)
            sID = dao.getTeamSportByID(tID)[0]
            if athlete_sport != sID:
                return jsonify(Error="Atleta con ID:{} no coincide con el ID de deporte:{} del Equipo.".format(aID, sID)), 400
        except (TypeError, ValueError):
            return jsonify(ERROR="Solicitud Incorrecta, Error de Tipo."), 400
        except:
            return jsonify(ERROR="No se pudo verificar Atleta desde DAO."), 500

        # check it exists already
        try:
            if not dao.getTeamMemberByIDs(aID, tID):
                return jsonify(Error="Miembro de Equipo con ID de Atleta:{} para Equipo con ID:{} no existe.".format(aID, tID)), 400
        except (TypeError, ValueError):
            return jsonify(ERROR="Solicitud Incorrecta, Error de Tipo."), 400
        except:
            return jsonify(ERROR="No se pudo verificar Equipo desde DAO."), 500

        # remove team member
        try:
            result = dao.removeTeamMember(aID, tID)
            if not result:
                return jsonify(Error="Problema removiendo record de miembro de Equipo.."), 500
        except (TypeError, ValueError):
            return jsonify(ERROR="Solicitud Incorrecta, Error de Tipo."), 400
        except:
            return jsonify(ERROR="No se pudo verificar Miembro de Equipo desde DAO."), 500

        dao.commitChanges()
        return jsonify(team="Se removio miembro de equipo con ID de Atleta:{} de Equipo con ID:{}.".format(aID, tID)), 200
