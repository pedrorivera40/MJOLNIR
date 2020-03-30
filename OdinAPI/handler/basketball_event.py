from flask import jsonify
from .dao.basketball_event import BasketballEventDAO


class BasketballEventHandler:
    
# getAllStatisticsByBasketballEventID(eID)//Instantiates a Basketball Event DAO in order to complete the desired get request and it returns a JSON with the desired information or with an error message.
# getAllAthleteStatisticsByBasketballEventId(eID,aID)//Instantiates a Basketball Event DAO in order to complete the desired get request and it returns a JSON with the desired information or with an error message
# addStatistics(eID, aID, attributes)//Instantiates a Basketball Event DAO in order to complete the desired post request and it returns a JSON with either a confirmation or error message.
# editStatistics(eID, aID,attributes)//Instantiates a Basketball Event DAO in order to complete the desired put request and it returns a JSON with either a confirmation or error message.
# removesStatistics(eID, aID)//Instantiates a Basketball Event DAO in order to complete the desired put request and it returns a JSON with either a confirmation or error message.
# mapBasketballEventToDict(record)//Maps a Basketball Event record to a dictionary and returns it.


    #TODO:(herbert comment) typo with athelete in the method
    def mapBasketballEventToDict(self,record):
        
        athlete_info = {}
        stat_info = {}
        athlete_info['athlete_id'] = record[0]
        athlete_info['first_name'] = record[1]
        athlete_info['middle_name'] = record[2]
        athlete_info['last_names'] = record[3]      
        athlete_info['number'] = record[4]
        athlete_info['profile_image_link'] = record[5]
        stat_info['points'] = record[6]
        stat_info['rebounds'] = record[7]
        stat_info['assists'] = record[8]
        stat_info['steals'] = record[9]
        stat_info['blocks'] = record[10]
        stat_info['turnovers'] = record[11]
        stat_info['field_goal_attempt'] = record[12]
        stat_info['successful_field_goal'] = record[13]
        stat_info['three_point_attempt'] = record[14]
        stat_info['successful_three_point'] = record[15]
        stat_info['free_throw_attempt'] = record[16]
        stat_info['successful_free_throw'] = record[17]
        stat_info['field_goal_percentage'] = float(record[18])
        stat_info['free_throw_percentage'] = float(record[19])
        stat_info['three_point_percentage'] = float(record[20])
        result = dict(Athlete = athlete_info, Event_Statistics = stat_info)
        return result
    
    def getAllStatisticsByBasketballEventID(self,eID):
        dao = BasketballEventDAO()
        result = dao.getAllStatisticsByEventID(eID)
        if not result:
            return jsonify(Error = "Basketball Event Statistics not found for the event: {}.".format(eID)),404
        mappedResult = []
        for athlete_statistics in result:                        
            mappedResult.append(self.mapBasketballEventToDict(athlete_statistics))
        #print(mappedResult)
        return jsonify(Basketball_Event_Statistics = mappedResult), 200
#===================================SAMPLING ATHLETES BELOW======================================
    # def getAthleteByID(self,aID):
    #     dao = AthleteDAO()
    #     result = dao.getAthleteByID(aID)
    #     if not result:
    #         return jsonify(Error = "Athlete with aID:{} not found.".format(aID)),404
    #     mappedResult = self.mapAtheleteToDict(result);
    #     return jsonify(Athlete = mappedResult), 200
    
    # def getAthleteByName(self,aFName,aMName,aLName):
    #     dao = AthleteDAO()
    #     result = dao.getAthleteByName(aFName,aMName,aLName)
    #     if not result:
    #         return jsonify(Error = "Athletes not found with the name: {} {} {}.".format(aFName,aMName,aLName)),404
    #     mappedResult = []
    #     for athlete in result:
    #         mappedResult.append(self.mapAtheleteToDict(athlete))
    #     return jsonify(Athletes = mappedResult), 200

    # def addAthlete(self,sID,attributes):
    #     dao = AthleteDAO()
    #     result = dao.addAthlete(sID,attributes[0],attributes[1],attributes[2],attributes[3],attributes[4],attributes[5],attributes[6],attributes[7],attributes[8],attributes[9])
    #     if not result:
    #         return jsonify(Error = "Problem inserting new athlete."),500
    #     return jsonify(Athlete = "Added new athlete with id:{}.".format(result)),201

    # def editAthlete(self,aID,attributes):
    #     dao = AthleteDAO()
    #     result = dao.editAthlete(aID,attributes[0],attributes[1],attributes[2],attributes[3],attributes[4],attributes[5],attributes[6],attributes[7],attributes[8],attributes[9],attributes[10])
    #     if not result:
    #         return jsonify(Error = "Athlete not found with id:{}.".format(aID)),404
    #     mappedResult = self.mapAtheleteToDict(result)
    #     return jsonify(Athlete = mappedResult),200
    
    # def removeAthlete(self,aID):
    #     dao = AthleteDAO()
    #     result = dao.removeAthlete(aID)
    #     if not result:
    #         return jsonify(Error = "Athlete not found with id:{} for the sport:{}.".format(sID,aID)),404
    #     return jsonify(Athlete = "Removed athlete with id:{}.".format(result)),200
    




