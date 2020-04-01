from flask import Flask,request,jsonify
from flask_cors import CORS
import os
import datetime
from handler.user import UserHandler
from handler.athlete import AthleteHandler
from handler.position import PositionHandler
from handler.basketball_event import BasketballEventHandler





app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})


@app.route("/")
def hello():
    return jsonify("Hi, this is a route that will be eliminated xD")

#--------- Athlete Routes ---------#
@app.route("/athletes/",methods = ['GET','POST'])
def athletes():
    handler = AthleteHandler()
    if request.method == 'POST':
        json = request.json
        return handler.addAthlete(json['sID'],json['attributes'])
    elif request.method == 'GET':
        json = request.json
        return handler.getAtheletesBySport(json['sID'],json['branch'])

@app.route("/athletes/<int:aid>/", methods = ['GET','POST','PUT','DELETE'])
def athleteByID(aid):
    handler = AthleteHandler()
    if request.method == 'GET':
        return handler.getAthleteByID(aid)   
    elif request.method == 'PUT':
        json = request.json
        return handler.editAthlete(aid,json['attributes'])
    elif request.method == 'DELETE':
        json = request.json
        return handler.removeAthlete(aid)

#--------- Position Routes ---------# 
@app.route("/positions/", methods = ['GET','DELETE'])
def position():
    handler = PositionHandler()
    if request.method == 'GET':
        return handler.getPositionByName(request.json['psName'])
    elif request.method == 'DELETE':
        return handler.removeAthletePosition(request.json['apID'])
    

@app.route("/positions/<int:sid>", methods = ['GET'])
def sportPositions(sid):
    handler = PositionHandler()
    if request.method == 'GET':
        return handler.getPositions(sid)
@app.route("/positions/<int:sid>/<int:aid>", methods = ['GET','POST','PUT'])
def athletePositions(sid,aid):
    handler = PositionHandler()
    if request.method == 'GET':
        return handler.getAthletePositionInSport(sid,aid)
    if request.method == 'POST':
        return handler.addAthletePosition(request.json['psID'],aid)
    if request.method == 'PUT':
        return handler.editAthletePosition(request.json['apID'],request.json['psID'],aid)


#--------- Dashboard User Routes ---------#
@app.route("/users/", methods = ['GET'])
def users():
    if request.method == 'GET':
        handler = UserHandler()

        return handler.getAllDashUsers()

#TODO: WORK ON THIS (Herbert) -> Improve route naming, base on args...
#--------- Result Routes ---------#
#TODO: Route Error Management, how does it not explode while saying error message?
@app.route("/results/basketball/<int:eid>", methods = ['GET'])
def basketballStatistics(eid):
    if request.method == 'GET':
        handler = BasketballEventHandler()
        return handler.getAllStatisticsByBasketballEventID(eid)
    else:
        return jsonify("Method not allowed."), 405

@app.route("/results/basketball/<int:eid>/<int:aid>/", methods = ['GET','POST','PUT','DELETE'])
def basketballAthleteStatistics(eid,aid):
    json = request.json
    if request.method == 'GET':
        handler = BasketballEventHandler()
        return handler.getAllAthleteStatisticsByBasketballEventId(eid,aid)
    if request.method == 'POST':
        handler = BasketballEventHandler()
        return handler.addStatistics(eid,aid,json['attributes'])
    if request.method == 'PUT':
        handler = BasketballEventHandler()
        returnable = handler.editStatistics(eid,aid,json['attributes'])
        # TODO: somehow manage to prevent this from executing if errors
        handler.editTeamStatistics(eid) 
        return returnable
    if request.method == 'DELETE':
        handler = BasketballEventHandler()
        return handler.removeStatistics(eid,aid)
    else:
        return jsonify(Error="Method not allowed."), 405

@app.route("/results/basketball/<int:eid>/team/", methods = ['GET','POST','PUT','DELETE'])
def basketballTeamStatistics(eid):
    json = request.json
    if request.method == 'GET':
        handler = BasketballEventHandler()
        return handler.getAllTeamStatisticsByBasketballEventId(eid)
    if request.method == 'POST':
        handler = BasketballEventHandler()
        if json['add_type'] == 'AUTO':
            return handler.addTeamStatisticsAuto(eid)
        else:
            return handler.addTeamStatistics(eid,json['attributes'])
    if request.method == 'PUT':
        handler = BasketballEventHandler()
        return handler.editTeamStatistics(eid)
    if request.method == 'DELETE':
        handler = BasketballEventHandler()
        return handler.removeTeamStatistics(eid)
    else:
        return jsonify(Error="Method not allowed."), 405

@app.route("/results/basketball/season/<int:seasonYear>/<int:aid>/", methods = ['GET'])
def basketballSeasonAthleteStatistics(aid,seasonYear):
    json = request.json
    if request.method == 'GET':
        handler = BasketballEventHandler()
        return handler.getAllAthleteStatisticsPerSeason(aid,seasonYear)
    else:
        return jsonify(Error="Method not allowed."), 405



#Launch app.
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')