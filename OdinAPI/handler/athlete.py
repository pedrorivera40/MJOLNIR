from flask import jsonify
from .dao.athlete import AthleteDAO

class AthleteHandler:
    
    def mapAthleteToDict(self,record):
        """
        Converts an athlete record returned by the Athlete DAO into a dictionary 
        and returns it.

        Creates a result dictionary an then maps the values from the record 
        list into the dictionary before sending it to the caller.

        Args:
            record: An athlete record in the database with basic athlete information
        Returns:
            A dictionay with the basic athlete information in the record list given
            mapped in it.
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
        return result

    def mapAthleteWithPositionsAndCategoriesToDict(self,records):
        """
        Converts athlete records returned by the Athlete DAO into a dictionary 
        and returns it.This dictionary will contain the positions or categories
        of an athlete if they have them.

        Creates a result dictionary an then maps the values from the records 
        list into the dictionary before sending it to the caller. This dictonary 
        will contain positions or categories of an athlete if the records given have
        a sublist.
     

        Args:
            records: An athlete record list in the database with basic athlete information if
                     if contains a sublist then it has positions or categories of an athlete.
        Returns:
            A dictionay with the basic athlete information in the records list given as well
            as athlete positions and categories, if the records list has them, mapped in it.
        """
        try:
            records[0][0]##Verfies if records has a sublist.
        except:
            return self.mapAthleteToDict(records)#If records does'nt have a sublist then the normal mapAthleteToDict function is called.
        
        result = self.mapAthleteToDict(records[0])#Get the athlete dictonary with the basic athlete information.
        positions = {}
        categories = {}
        for record in records:
            if record[12]:#Holds the position of the athlete if not null.
                positions.update(dict(((record[12],record[13]),)))
            if record[14]:#Holds the category of the athlete if not null.
                categories.update(dict(((record[14],record[15]),)))
        
        result.update(dict((('athlete_positions',positions),)))
        result.update(dict((('athlete_categories',categories),)))
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
        if not isinstance(sID,int):#Validate that the sport id is an integer.
            return jsonify(Error = "The id of the sport must be an integer."),400

        dao = AthleteDAO()
        try:            
            result = dao.getAthletesBySport(sID)
            if not result:
                return jsonify(Error = "Athletes not found for the sport: {}.".format(sID)),404
            mappedResult = []
            for athlete in result:   
                mappedResult.append(self.mapAthleteWithPositionsAndCategoriesToDict(athlete))
            return jsonify(Atheletes = mappedResult), 200
        except:
            return jsonify(Error = "An error ocurred while trying to get the athletes of a sport."),400
    
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
        if not isinstance(aID,int):#Validate that the athlete id is an integer.
            return jsonify(Error = "The id of the athlete must be an integer."),400

        dao = AthleteDAO()
        try:  
            
            result = dao.getAthleteByID(aID)
            if not result:
                return jsonify(Error = "Athlete with aID:{} not found.".format(aID)),404
            
            mappedResult = self.mapAthleteWithPositionsAndCategoriesToDict(result)
            return jsonify(Athlete = mappedResult), 200
        except:
            return jsonify(Error = "An error ocurred while trying to get an athelte by id."),400
    
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
        if not isinstance(sID,int):#Validate that the sport id is an integer.
            return jsonify(Error =  "The sport id must be in integer."),400

        validationResult = self._validateAttributesList(attributes)
        if isinstance(validationResult,str):
            return jsonify(Error = validationResult),400
        
        dao = AthleteDAO()
        try:            
            result = None
            if aPositions and not aCategories:                   
                result = dao.addAthleteWithPosition(sID,attributes[0],attributes[1],attributes[2],attributes[3],attributes[4],attributes[5],attributes[6],attributes[7],attributes[8],attributes[9],attributes[10])
            elif not aPositions and aCategories:                 
                result = dao.addAthleteWithCategory(sID,attributes[0],attributes[1],attributes[2],attributes[3],attributes[4],attributes[5],attributes[6],attributes[7],attributes[8],attributes[9],attributes[11])
            else:
                result = dao.addAthlete(sID,attributes[0],attributes[1],attributes[2],attributes[3],attributes[4],attributes[5],attributes[6],attributes[7],attributes[8],attributes[9])
            
            if isinstance(result,str):#If true, result will contain the error message.
                return jsonify(Error = result),400

            return jsonify(Athlete = "Added new athlete with id:{}.".format(result)),201
        except:
            return jsonify(Error = "Problem ocurred when adding a new athlete."),400
            
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
        if not isinstance(aID,int):
            return jsonify(Error =  "The athlete id must be in integer."),400

        validationResult = self._validateAttributesList(attributes)
        if isinstance(validationResult,str):
            return jsonify(Error = validationResult),400               
        dao = AthleteDAO()
        try:            
            result = dao.editAthlete(aID,attributes[0],attributes[1],attributes[2],attributes[3],attributes[4],attributes[5],attributes[6],attributes[7],attributes[8],attributes[9],attributes[10],attributes[11])
            if isinstance(result,str):
                return jsonify(Error = result),400
            
            return jsonify(Athlete = "Edited athlete with id: {}".format(result)),200
        except:
            return jsonify(Error = "Problem ocurred when updating an athlete."),400
    
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
        if not isinstance(aID,int):
            return jsonify(Error =  "The athlete id must be in integer."),400
        try:
            dao = AthleteDAO()
            result = dao.removeAthlete(aID)
            if not result:
                return jsonify(Error = "Athlete not found with id:{}.".format(aID)),404
            return jsonify(Athlete = "Removed athlete with id:{}.".format(result)),200
        except:
            return jsonify(Error = "Problem ocurred when removing an athlete.")

    def _validateAttributesList(self,attributes):
        """
        Validates the attributes list given for the addAthlete() and editAthlete()
        functions.

        Args:
            attributes: A list containing the attributes of an athelete to be added or 
                        edited.
        Returns:
            A string with an error message if the validation fails an integer otherwise.        
        """

        if not isinstance(attributes,list):
            return "The attributes of the athlete must be in a list."
        if not len(attributes) == 12:
            return "The attributes list does not have the correct ammount of elements."
        
        
        #Going to extract the inputs from the attributes list.
        aFName = attributes[0]
        aMName = attributes[1]
        aLName = attributes[2]
        aBio = attributes[3]
        aHeight = attributes[4]
        aStudyProgram = attributes[5]
        aDateOfBirth = attributes[6]
        aSchoolOfPrecedence = attributes[7]
        aNumber = attributes[8]
        aProfilePictureLink = attributes[9]
        aPositions = attributes[10]
        aCategories = attributes[11]    
   
        #Validation of inputs 
        if not aFName or not isinstance(aFName,str) or len(aFName)<2 or len(aFName)>20 or not aFName.isalpha():
            return "First name given does not follow the constraints."

        if aMName:
            if not isinstance(aMName,str) or len(aMName)<2 or len(aMName)>20 or not aMName.isalpha():
                return "Middle name given does nto follow the constraints."

        if not aLName or not isinstance(aLName,str) or len(aLName)<2 or len(aLName)>40:#Still need to validates all the characters in the last name string.
            return "Last name given does nto follow the constraints."

        if aBio:
            if not aBio or not isinstance(aBio,str) or len(aBio)<2 or len(aBio)>1000:
                return "Athlete bio given does nto follow the constraints."

        if aHeight:
            if not isinstance(aBio,float):
                return "The height given is not a real number."

        if aStudyProgram:
            if not isinstance(aStudyProgram,str):
                return "The study program given is not a string."

        if aDateOfBirth:
            if not isinstance(aDateOfBirth,str):
                return "The date of birth given is not valid."

        if aSchoolOfPrecedence:
            if not isinstance(aSchoolOfPrecedence,str):
                return "The input given for school of precedence is incorrect."

        if aNumber:
            if not isinstance(aNumber,int):
                return "The number of the athlete must be an integer."

        if aProfilePictureLink:
            if not isinstance(aProfilePictureLink,str):
                return "The profile picture link must be a string."

        if aPositions:
            if not isinstance(aPositions,dict):
                return "Positions must be in dictionary."

        if aCategories:
            if not isinstance(aCategories,dict):
                return "Categories must be in dictionary."  

        return 1            



        

        
        
        






