from flask import jsonify
from .dao.athlete import AthleteDAO

class AthleteHandler:
    
    def mapAthleteToDict(self,record):
        """
        Converts an athlete record returned by the Athlete DAO into a dictionary.
        """
        result = {}
        result['id'] = record[0]
        result['fName'] = record[1]
        result['mName'] = record[2]
        result['lName'] = record[3]      
        result['bio'] = record[4]
        result['height'] = record[5]
        result['sProgram'] = record[6]
        result['dBirth'] = record[7]
        result['school'] = record[8]
        result['number'] = record[9]
        result['profilePicLink'] = record[10]
        result['sportName'] = record[11]
        record['aPosition'] = record[12]
        record['aCategory'] = record[13]
        return result
    
    def getAthletesBySport(self,sID):
        """
        Gets all athletes belonging to a specific sport.

        Calls the AthletDAO to get a list of all athlete records
        that participate in a specific sport and maps the result 
        to a JSON that contains all those valid athletes in the 
        system. The JSON objects is then returned to the caller.
        
        Args:
            sID: The id of the sport in which the athletes parcipate.
        
        Returns:
            A JSON containing all valid athletes that participate in a
            specified sport by the given sport id.
        """
        dao = AthleteDAO()
        result = dao.getAthletesBySport(sID)
        if not result:
            return jsonify(Error = "Athletes not found for the sport: {}.".format(sID)),404
        mappedResult = []
        for athlete in result:                        
            mappedResult.append(self.mapAthleteToDict(athlete))
        return jsonify(Atheletes = mappedResult), 200
    
    def getAthleteByID(self,aID):
        """
        Gets a specified athletes by their id.

        Calls the AthleteDAO to get an athlete by their id 
        and maps the result to a JSON that contains the desired 
        record. The JSON object is then returned to the caller.

        Args:
            aID: The id of the athlete that needs to be fetched.

        Returns:
            A JSON containing the athlete with the given id.

        """
        dao = AthleteDAO()
        result = dao.getAthleteByID(aID)
        if not result:
            return jsonify(Error = "Athlete with aID:{} not found.".format(aID)),404
        mappedResult = self.mapAthleteToDict(result)
        return jsonify(Athlete = mappedResult), 200
    
    #Don't think this function is needed anymore.
    def getAthleteByName(self,aFName,aMName,aLName):
        dao = AthleteDAO()
        result = dao.getAthleteByName(aFName,aMName,aLName)
        if not result:
            return jsonify(Error = "Athletes not found with the name: {} {} {}.".format(aFName,aMName,aLName)),404
        mappedResult = []
        for athlete in result:
            mappedResult.append(self.mapAthleteToDict(athlete))
        return jsonify(Athletes = mappedResult), 200

    def addAthlete(self,sID,attributes):
        """
        Adds a new athlete with the information given.

        Calls a AthleteDAO to add a new athlete and maps the 
        result to a JSON object that contains the id of the newly added 
        athlete.

        Args:
            sID: The id of the sport in which the athlete participates.
            attributes: A list containing the attributes of the athlete to
                        be added.
        Returns:
            A JSON object containing the id of the newly added user.

        """
        dao = AthleteDAO()
        result = dao.addAthlete(sID,attributes[0],attributes[1],attributes[2],attributes[3],attributes[4],attributes[5],attributes[6],attributes[7],attributes[8],attributes[9],attributes[10],attributes[11])
        if not result:
            return jsonify(Error = "Problem inserting new athlete."),500
        return jsonify(Athlete = "Added new athlete with id:{}.".format(result)),201

    def editAthlete(self,aID,attributes):
        """
        Edits the attributes of an existing and valid athlete record with
        the given id.

        Calls the AthleteDAO to edit the athlete record. It then maps the result
        to a JSON that contains the desirerd record. The JSON object created is
        then returned to the caller.

        Args:
            aID: The id of the athlete that is going to be edited.
            attributes: The new attributes of the athlete to be edited.
        
        Returns:
            A JSON object containing the information of the edited athlete.
        """
        
        dao = AthleteDAO()
        result = dao.editAthlete(aID,attributes[0],attributes[1],attributes[2],attributes[3],attributes[4],attributes[5],attributes[6],attributes[7],attributes[8],attributes[9],attributes[10],attributes[11],attributes[12])
        if not result:
            return jsonify(Error = "Athlete not found with id:{}.".format(aID)),404
        mappedResult = self.mapAthleteToDict(result)
        return jsonify(Athlete = mappedResult),200
    
    def removeAthlete(self,aID):
        """
        Invalidates an athlete in the database.

        Call the AthleteDAO to invalidate the athlete record. It then
        maps the result to a JSON object that contains the id of the 
        invalidated user. The JSON object is then returned to the caller.

        Args:
            aID: The id of the athlete to be invalidated.
        Returns:
            A JSON containing the id of the invalidated athlete.
        """

        dao = AthleteDAO()
        result = dao.removeAthlete(aID)
        if not result:
            return jsonify(Error = "Athlete not found with id:{}.".format(aID)),404
        return jsonify(Athlete = "Removed athlete with id:{}.".format(result)),200
    




