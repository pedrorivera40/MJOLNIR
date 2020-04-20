from flask import jsonify
from dateutil.parser import parse
from .dao.athlete_dao import AthleteDAO
import re

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
        result['yearOfStudy'] = record[10]
        result['yearsOfParticipation'] = record[11]
        result['profilePicLink'] = record[12]
        result['sportName'] = record[13]
        result['sportBranch'] = record[14]        

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
            if record[15]:#Holds the position of the athlete if not null.
                positions.update(dict(((record[15],record[16]),)))
            if record[17]:#Holds the category of the athlete if not null.
                categories.update(dict(((record[17],record[18]),)))
        
        result.update(dict((('athlete_positions',positions),)))
        result.update(dict((('athlete_categories',categories),)))
        return result

    def getAllAthletes(self):
        """
        Gets all athletes in the database.
        Calls the AthletDAO to get a list of all athlete records
        maps the result to a JSON that contains all those valid athletes 
        in the database. The JSON objects is then returned to the caller.       
        
        Returns:
            A JSON containing all valid athletes that are in the database.
        """
        try:
            result = AthleteDAO().getAllAthletes()
            if not result:
                return jsonify(Error = "No athletes were found."),404
            mappedResult = []
            for athlete in result:
                mappedResult.append(self.mapAthleteToDict(athlete))
            return jsonify(Athletes = mappedResult),200


        except:
            jsonify(Error = "An error ocurred while fetching the athletes."),400

                
    
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
        try:
            if not isinstance(int(sID),int):#Validate that the sport id is an integer.
                return jsonify(Error = "The id of the sport given is invalid."),400
        except:
            return jsonify(Error = "The id of the sport given is invalid."),400

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
        Gets a specified athlete by their id.

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
            print(result)
            mappedResult = self.mapAthleteWithPositionsAndCategoriesToDict(result)
            return jsonify(Athlete = mappedResult), 200
        except:
            return jsonify(Error = "An error ocurred while trying to get an athelte by id."),400
    
 

    def addAthlete(self,sID,attributes):
        """
        Adds a new athlete with the information given.

        Calls a AthleteDAO to add a new athlete and maps the 
        result to a JSON object that contains the id of the newly added 
        athlete.

        Args:
            sID: The id of the sport in which the athlete participates.
            attributes: A dictionary containing the attributes of the athlete to
                        be added.
        Returns:
            A JSON object containing the id of the newly added event.

        """
        if not isinstance(sID,int):#Validate that the sport id is an integer.
            return jsonify(Error =  "The sport id must be in integer."),400

        validationResult = self._validateAttributes(attributes)
        if isinstance(validationResult,str):
            return jsonify(Error = validationResult),400
        
        dao = AthleteDAO()

        aPositions = attributes['positions']
        aCategories = attributes['categories']
        
        try:            
            result = None
            if aPositions and not aCategories:                   
                result = dao.addAthleteWithPosition(sID,attributes['first_name'],attributes['middle_name'],attributes['last_names'],
                                                    attributes['bio'],attributes['height'],attributes['study_program'],attributes['date_of_birth'],
                                                    attributes['school_of_precedence'],attributes['number'],attributes['year_of_study'],
                                                    attributes['years_of_participation'],attributes['profile_picture_link'],aPositions)
            elif not aPositions and aCategories:                 
                result = dao.addAthleteWithCategory(sID,attributes['first_name'],attributes['middle_name'],attributes['last_names'],
                                                        attributes['bio'],attributes['height'],attributes['study_program'],attributes['date_of_birth'],
                                                        attributes['school_of_precedence'],attributes['number'],attributes['year_of_study'],
                                                        attributes['years_of_participation'],attributes['profile_picture_link'],aCategories)

            else:
                result = dao.addAthlete(sID,attributes['first_name'],attributes['middle_name'],attributes['last_names'],
                                            attributes['bio'],attributes['height'],attributes['study_program'],attributes['date_of_birth'],
                                            attributes['school_of_precedence'],attributes['number'],attributes['year_of_study'],
                                            attributes['years_of_participation'],attributes['profile_picture_link'])
            if isinstance(result,str):#If true, result will contain the error message.
                return jsonify(Error = result),400

            return jsonify(Athlete = "Added new athlete with id:{}.".format(result)),201
        except Exception as e:
            return jsonify(Error = "Problem ocurred when adding a new athlete." + str(e)),400
            
    def editAthlete(self,aID,attributes):
        """
        Edits the attributes of an existing and valid athlete record with
        the given id.

        Calls the AthleteDAO to edit the athlete record. It then maps the result
        to a JSON that contains the desired record. The JSON object created is
        then returned to the caller.

        Args:
            aID: The id of the athlete that is going to be edited.
            attributes: A dictionary with the new attributes of the athlete 
                        to be edited.                        
        
        Returns:
            A JSON object containing the information of the edited athlete.
        """ 
        if not isinstance(aID,int) or aID < 1:
            return jsonify(Error =  "The athlete id given is invalid."),400

        validationResult = self._validateAttributes(attributes)
        if isinstance(validationResult,str):
            return jsonify(Error = validationResult),400
        
        try: 
            dao = AthleteDAO()                   
            if not dao.athleteExists(aID):
                return jsonify(Error = "Athlete with id:{} does not exist.".format(aID)),404           
            result = dao.editAthlete(aID,attributes['first_name'],attributes['middle_name'],attributes['last_names'],
                                                attributes['bio'],attributes['height'],attributes['study_program'],attributes['date_of_birth'],
                                                attributes['school_of_precedence'],attributes['number'],attributes['year_of_study'],
                                                attributes['years_of_participation'],attributes['profile_picture_link'],attributes['positions'],
                                                attributes['categories'])
            if isinstance(result,str):
                    return jsonify(Error = result),400
            
            return jsonify(Athlete = "Edited athlete with id: {}".format(result)),200
        except Exception as e:
            return jsonify(Error = str(e)),400
    
    def removeAthlete(self,aID):
        """
        Invalidates an athlete in the database.

        Call the AthleteDAO to invalidate the athlete record. It then
        maps the result to a JSON object that contains the id of the 
        invalidated athlete. The JSON object is then returned to the caller.

        Args:
            aID: The id of the athlete to be invalidated.
        Returns:
            A JSON containing the id of the invalidated athlete.
        """
        if not isinstance(aID,int) or aID < 1:
            return jsonify(Error =  "The athlete id given is invalid"),400
        try:
            dao = AthleteDAO()                              
            if not dao.athleteExists(aID):
                return jsonify(Error = "Athlete with id:{} does not exist.".format(aID)),404
            result = dao.removeAthlete(aID)            
            return jsonify(Athlete = "Removed athlete with id:{}.".format(result)),200
        except:
            return jsonify(Error = "Problem ocurred when removing an athlete.")

    def _validateAttributes(self,attributes):
        """
        Validates the attributes dictionary given for the addAthlete() and editAthlete()
        functions.

        Args:
            attributes: A dictionary containing the attributes of an athelete to be added or 
                        edited.
        Returns:
            A string with an error message if the validation fails an integer otherwise.        
        """

        if not isinstance(attributes,dict):
            return "The attributes of the athlete must be in a list."
        
        
        
        #Going to extract the inputs from the attributes dictonary.

        try:
            
            aFName = attributes['first_name']
            aMName = attributes['middle_name']
            aLName = attributes['last_names']
            aBio = attributes['bio']
            aHeight = attributes['height']
            aStudyProgram = attributes['study_program']
            aDateOfBirth = attributes['date_of_birth']
            aSchoolOfPrecedence = attributes['school_of_precedence']
            aNumber = attributes['number']
            aYearOfStudy = attributes['year_of_study']
            aYearsOfParticipation = attributes['years_of_participation']
            aProfilePictureLink = attributes['profile_picture_link']
            aPositions = attributes['positions']
            aCategories = attributes['categories']  
            
            #Regular Expressions for input validation
            nameRegex = "^[^0-9_!¡?÷?¿/\\+=@#$%ˆ&*(){}|~<>;:[\]]{1,}$"
            phraseRegex = "^[a-zA-Z0-9- ',.;:!]*$"
            alphaSpaceRegex = "^[a-zA-Z ]*$"
            
            #Compiled Regular Expressions
            cNameReg = re.compile(nameRegex)
            cPhraseReg = re.compile(phraseRegex)
            cAlphaSpaceReg = re.compile(alphaSpaceRegex)
              
   
             #Validation of inputs 
            if not aFName or not isinstance(aFName,str) or len(aFName)>20 or not re.search(cNameReg,aFName):
                return "First name given does not follow the constraints."

            if aMName:                
                if not isinstance(aMName,str) or len(aMName)>20 or not re.search(cNameReg,aMName):
                    return "Middle name given does not follow the constraints."

            if not aLName or not isinstance(aLName,str) or len(aLName)>40 or not re.search(cNameReg,aLName):#Still need to validates all the characters in the last name string.
                return "Last name given does not follow the constraints."

            if aBio:
                if not aBio or not isinstance(aBio,str) or len(aBio)>1000 or not re.search(cPhraseReg,aBio):
                    return "Athlete bio given does not follow the constraints."

            if aHeight:
                if not isinstance(float(aHeight),float) or aHeight < 48.0 or aHeight > 96.0:
                    return "Invalid value for height given."

            if aStudyProgram:
                if not isinstance(aStudyProgram,str) or not re.search(cAlphaSpaceReg,aStudyProgram):
                    return "The study program given does not follow the constraints."

            if aDateOfBirth:           
                try:#Date format validation
                    if not isinstance(aDateOfBirth,str):
                        return "The date of birth given is not valid."
                    parse(aDateOfBirth)
                except:
                    return "The date of birth given is not valid."


            if aSchoolOfPrecedence:
                if not isinstance(aSchoolOfPrecedence,str) or not re.search(cAlphaSpaceReg,aSchoolOfPrecedence):
                    return "The input given for school of precedence is incorrect."

            if aNumber:
                if not isinstance(int(aNumber),int) or aNumber < 0 or aNumber > 99:
                    return "The number of the athlete given is not valid."

            if aYearOfStudy:
                if not isinstance(int(aYearOfStudy),int) or aYearOfStudy < 1 or aYearOfStudy > 10:
                    return "The year of study given is not valid."

            if aYearsOfParticipation:
                if not isinstance(int(aYearsOfParticipation),int) or aYearsOfParticipation < 1 or aYearsOfParticipation > 4 :
                    return "The years of participation given is not valid."

            if aProfilePictureLink:
                if not isinstance(aProfilePictureLink,str):
                    return "The profile picture link given is not valid."

            if aPositions:            
                if not isinstance(aPositions,dict):
                    return "Positions given are not valid."

            if aCategories:
                if not isinstance(aCategories,dict):
                    return "Categories given are not valid"

            if aPositions and aCategories:
                return "An athlete can't have  both positions and categories in a sport."
        except:
            return "Bad arguments given."  

        return 1            



        

        
        
        






