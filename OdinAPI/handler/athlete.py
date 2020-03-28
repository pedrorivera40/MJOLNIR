from flask import jsonify
from .dao.athlete import AthleteDAO

class AthleteHandler:
    
    def mapAtheleteToDict(self,record):
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
    
    def getAtheletesBySport(self,sID,aBranch):
        dao = AthleteDAO()
        result = dao.getAtheletesBySport(sID,aBranch)
        if result == None:
            return jsonify(Error = "Athletes not found for the sport: {sID} and branch: {aBranch}."),404
        mappedResult = []
        for athlete in result:
            mappedResult.append(self.mapAtheleteToDict(athlete))
        return jsonify(Atheletes = mappedResult), 201
    
    def getAthleteByID(self,aID):
        dao = AthleteDAO()
        result = dao.getAthleteByID(aID)
        if result == None:
            return jsonify(Error = "Athlete with aID:{aID} not found."),404
        mappedResult = self.mapAtheleteToDict(result);
        return jsonify(Athlete = mappedResult), 201
    
    def getAthleteByName(self,aFName,aMName,aLName):
        dao = AthleteDAO()
        result = dao.getAthleteByName()
        if result == None:
            return jsonify(Error = "Athletes not found with the name: {aFName} {aMName} {aLName}."),404
        mappedResult = []
        for athlete in result:
            mappedResult.append(self.mapAtheleteToDict(athlete))
        return jsonify(Athletes = mappedResult), 201

    def addAthlete(self,sID, attributes):
        dao = AthleteDAO()
        result = dao.addAthlete(sID,attributes[0],attributes[1],attributes[2],attributes[3],attributes[4],attributes[5],attributes[6],attributes[7],attributes[8],attributes[9])
        if result == None:
            return jsonify(Error = "Problem inserting new athlete."),500
        return jsonify(Athlete = "Added new athlete with id:{result}."),201

    def editAthlete(self,sID,aID,attributes):
        dao = AthleteDAO()
        result = dao.addAthlete(sID,aID,attributes[0],attributes[1],attributes[2],attributes[3],attributes[4],attributes[5],attributes[6],attributes[7],attributes[8],attributes[9])
        if result == None:
            return jsonify(Error = "Athlete not found with id:{aID} for the sport:{sID}."),404
        mappedResult == self.mapAtheleteToDict(result)
        return jsonify(Athlete = mappedResult),201
    
    def removeAthlete(self,sID,aID):
        dao = AthleteDAO()
        result = dao.removeAthlete(sID,aID)
        if result == None:
            return jsonify(Error = "Athlete not found with id:{aID} for the sport:{sID}."),404
        return jsonify(Athlete = "Removed athlete with id:{result}."),201
    




