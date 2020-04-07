from flask import jsonify
from .dao.position_dao import PositionDAO

class PositionHandler:


    def mapPositionToDict(self,record):
        result = {}
        result['id'] = record[0]
        result['name'] = record[1]
        return result

    def mapAthleteSportPositionToDict(self,record):
        result = {}
        result['apID'] = record[0]
        result['pID'] = record[1]
        result['psName'] = record[2]
        return result
    
    def mapAthletePositionToDict(self,record):
        result = {}
        result['id'] = record[0]
        result['position_id'] = record[1]
        result['athlete_id'] = record[2]
        return result


    def getPositions(self,sID):
        dao = PositionDAO()
        result = dao.getPositions(sID)
        if not result:
            return jsonify(Error = "Positions for the sport with id:  {} not found.".format(sID)), 404
        mappedResult = []
        for position in result:
            mappedResult.append(self.mapPositionToDict(position))
        return jsonify(Positions = mappedResult), 200
    
    def getPositionByName(self,psName):
        dao = PositionDAO()
        result = dao.getPositionByName(psName)
        if not result:
            return jsonify(Error = "Position with the name:{} not found.".format(psName)), 404
        mappedResult = self.mapPositionToDict(result)
        return jsonify(Position = mappedResult), 200
    
    def getAthletePositionInSport(self,sID,aID):
        dao = PositionDAO()
        result = dao.getAthletePositionInSport(sID,aID)
        if not result:
            return jsonify(Error = "Position not found  for the sport with id:{} and athlete with id:{} not found.".format(sID,aID)),404
        mappedResult = self.mapAthleteSportPositionToDict(result)
        return jsonify(AthletePosition = mappedResult), 200

    def addAthletePosition(self,psID,aID):
        dao = PositionDAO()
        result = dao.addAthletePosition(psID,aID)
        if not result:
            return jsonify(Error = "Position could not be added."), 404
        
        return jsonify(Position = "Added new position for the athlete with id:{}.".format(result)), 201
    
    def editAthletePosition(self,apID,psID,aID):
        dao = PositionDAO()
        result = dao.editAthletePosition(apID,psID,aID)
        if not result:
            return jsonify(Error = "Position to edit was not found."), 404
        mappedResult = self.mapAthletePositionToDict(result)
        return jsonify(EditedPosition = mappedResult), 200
    
    def removeAthletePosition(self,apID):
        dao = PositionDAO()
        result = dao.removeAthletePosition(apID)
        if not result:
            return jsonify(Error = "Position to remove was not found."), 404
        return jsonify(Position = "Position for the athlete with id:{} was removed.".format(result)), 200

        
    




