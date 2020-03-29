from flask import jsonify
from .dao.position import PositionDAO

class PositionHandler:


    def mapPositionToDict(self,record):
        result = {}
        result['id'] = record[0]
        result['name'] = record[1]
        return result

    def getPositions(self,sID):
        dao = PositionDAO()
        result = dao.getPositions(sID)
        if not result:
            return jsonify(Error = "Positions for the sport with id:  {} not found.".format(sID)), 404
        mappedResult = []
        for position in result:
            mappedResult = self.mapPositionToDict(position)
        return jsonify(Positions = mappedResult), 201
    
    def getPositionByName(self,psName):
        dao = PositionDAO()
        result = dao.getPositionByName(psName)
        if not result:
            return jsonify(Error = "Position with the name:{} not found.".format(psName)), 404
        mappedResult = self.mapPositionToDict(result)
        return jsonify(Position = mappedResult), 201
    
    def getPositionByAID(self,sID,aID):
        dao = PositionDAO()
        result = dao.getPositionByAID(sID,aID)
        if not result:
            return jsonify(Error = "Position not found  for the sport with id:{} and athlete with id:{} not found.".format(sID,aID)),404
        mappedResult = self.mapPositionToDict(result)
        return jsonify(AthletePosition = mappedResult), 201

    def addPosition(self,sID,aID,psName):
        dao = PositionDAO()
        result = dao.addPosition(sID,aID,psName)
        if not result:
            return jsonify(Error = "Position could not be added."), 404
        
        return jsonify(Position = "Added new position for the athlete with id:{}.".format(result)), 201
    
    def editPosition(self,pID,sID,aID,psName):
        dao = PositionDAO()
        result = dao.editPosition(pID,sID,aID,psName)
        if not result:
            return jsonify(Error = "Position to edit was not found."), 404
        mappedResult = self.mapPositionToDict(result)
        return jsonify(Position = mappedResult), 201
    
    def removePosition(self,pID,sID,aID):
        dao = PositionDAO()
        result = dao.removePosition(pID,sID,aID)
        if not result:
            return jsonify(Error = "Position to remove was not found."), 404
        return jsonify(Position = "Position for the athlete with id:{} was removed.".format(result)), 201

        
    




