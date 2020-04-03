from flask import Flask,request,jsonify
from flask_cors import CORS
import os
import datetime
from handler.user import UserHandler
from handler.athlete import AthleteHandler
from auth import createHash, verifyHash, generateToken, verifyToken
from functools import wraps
from dotenv import load_dotenv
import os
from handler.position import PositionHandler
from handler.basketball_event import BasketballEventHandler

## Load environment variables
load_dotenv()




app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})


def token_check(func):
    """
    Midleware to verify the request is authorized.

    Midleware function used to protect routes from unauthorized request
    by verifying each request provides a valid token.
    """
    @wraps(func)
    def decorated():

        token = request.headers.get('Authorization')
        print(token)
        print(request.headers)
        print(request.get_json())

        if not token:
            return jsonify(Error='Token is missing'), 403

        response = verifyToken(token, os.getenv('SECRET_KEY'))
        print(response, os.getenv('SECRET_KEY'))

        if response == False:
            return jsonify(Error="Token is invalid"), 403
        else:
            pass
        return func()
    return decorated


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

###########################################
#--------- Dashboard User Routes ---------#
###########################################
@app.route("/users/", methods = ['GET','POST'])
def allUsers():
    handler = UserHandler()
    req = request.json
    if request.method == 'GET':
        ## For user list display
        return handler.getAllDashUsers()
    if request.method == 'POST':
        ## For account creation
        password = createHash(req['password'])
        return handler.addDashUser(req['username'],req['full_name'], req['email'], password)

@app.route("/users/<int:duid>", methods = ['GET','PATCH'])
def userByID(duid):
    handler = UserHandler()
    req = request.json
    if request.method == 'GET':
        ## For managing specific users
        return handler.getDashUserByID(duid)
    if request.method == 'PATCH':
        ## For username change
        return handler.updateDashUserUsername(duid,req['username'])

@app.route("/users/username/", methods = ['POST'])
def getUserByUsername():
    if request.method == 'POST':
        handler = UserHandler()
        req = request.json
        return handler.getDashUserByUsername(req['username'])


@app.route("/users/email/", methods = ['POST'])
def getUserByEmail():
    if request.method == 'POST':
        handler = UserHandler()
        req = request.json
        return handler.getDashUserByEmail(req['email'])

@app.route("/users/<int:duid>/reset", methods = ['PATCH'])
def passwordReset(duid):
    handler = UserHandler()
    req = request.json
    if request.method == 'PATCH':
        ## For password reset
        password = createHash(req['password'])
        return handler.updateDashUserPassword(duid,password)

@app.route("/users/<string:duid>/toggleActive", methods = ['PATCH']) ## TODO: id's that are sanwdiwch must be converted to string
def toggleActive(duid):
    handler = UserHandler()
    if request.method == 'PATCH':
        return handler.toggleDashUserActive(duid)

@app.route("/users/<string:duid>/remove", methods = ['PATCH']) ## TODO: id's that are sanwdiwch must be converted to string
def removeUser(duid):
    handler = UserHandler()
    if request.method == 'PATCH':
        return handler.removeDashUser(duid)

@app.route("/users/<string:duid>/setPermissions",  methods = ['POST', 'PATCH'])
def addPermissions(duid):
    if request.method == 'POST':
        req = request.json
        handler = UserHandler()
        return  handler.addUserPermissions(duid, req['permissions'])



#TODO: WORK ON THIS (Herbert) -> Improve route naming, base on args...
#--------- Result Routes ---------#
#TODO: Route Error Management, how does it not explode while saying error message?


#REQUEST FORMAT FOR ROUTE:
# { "event_id": 5,
#   "team_statistics": 
#    { "basketball_statistics": 
#       { "points":500, "rebounds":500, "assists":500, "steals":500, "blocks":500, "turnovers":500, "field_goal_attempt":500,
# 		"successful_field_goal":500, "three_point_attempt":500, "successful_three_point":500, "free_throw_attempt":500,
# 		"successful_free_throw":500
#       } 
#    },
#   "athlete_statistics": 
#   [
#   	{"athlete_id":4,
#   	"statistics":
# 	  	{"basketball_statistics":
# 		  	{"points":2, "rebounds":2, "assists":2, "steals":2, "blocks":2, "turnovers":2, "field_goal_attempt":2, 
#             "successful_field_goal":2, "three_point_attempt":2, "successful_three_point":2, "free_throw_attempt":2, 
#             "successful_free_throw":2
# 		  	}
# 	  	}
#   	},
#   	{"athlete_id":8,
#   	"statistics":
# 	  	{"basketball_statistics":
# 		  	{"points":1, "rebounds":1, "assists":1, "steals":1, "blocks":1, "turnovers":1, "field_goal_attempt":1,
# 			"successful_field_goal":1, "three_point_attempt":1, "successful_three_point":1, "free_throw_attempt":1,
# 	        "successful_free_throw":1
# 		  	}
# 	  	}
#   	}
#   	],
#   "uprm_score": 0,
#   "opponent_score": 0
#   "opponent_name" = "name_here"
#   "opponent_color" = "#HEX_VAL_HERE" 
# }
@app.route("/results/basketball/<int:eid>/", methods = ['GET','POST'])
def basketballStatistics(eid):
    json = request.json
    handler = BasketballEventHandler()
    if request.method == 'GET':
        return handler.getAllStatisticsForEvent(eid)
        #Removed call for version with only athlete stats list, new version returns all
        #return handler.getAllStatisticsByBasketballEventID(eid)
    if request.method == 'POST':
        #TODO: change eID to json['event_id']
        return handler.addAllEventStatistics(eid,)
        #return jsonify(json),200
    else:
        return jsonify("Method not allowed."), 405

# @app.route("/results/basketball/<int:eid>/all/", methods = ['GET'])
# def basketballAllStatistics(eid):
#     json = request.json
#     handler = BasketballEventHandler()
#     if request.method == 'GET':
#         return handler.getAllStatisticsForEvent(eid)
#     else:
#         return jsonify("Method not allowed."), 405


#FORMAT FOR REQUEST:
# {"attributes":
#   {
#   "points":2, "rebounds":2, "assists":2, "steals":2, "blocks":2, "turnovers":2, "field_goal_attempt":2,
#   "successful_field_goal":2, "three_point_attempt":2, "successful_three_point":2, "free_throw_attempt":2,
#   "successful_free_throw":2
#   }
# }
@app.route("/results/basketball/<int:eid>/<int:aid>/", methods = ['GET','POST','PUT','DELETE'])
def basketballAthleteStatistics(eid,aid):
    json = request.json
    handler = BasketballEventHandler()
    if request.method == 'GET':
        return handler.getAllAthleteStatisticsByBasketballEventId(eid,aid)
    if request.method == 'POST':
        return handler.addStatistics(eid,aid,json['attributes'])
    if request.method == 'PUT':
        returnable = handler.editStatistics(eid,aid,json['attributes'])
        return returnable
    if request.method == 'DELETE':
        return handler.removeStatistics(eid,aid)
    else:
        return jsonify(Error="Method not allowed."), 405

#FORMAT FOR REQUEST:
# {"add_type":"manual"
# "attributes":
#   {
#   "points":2, "rebounds":2, "assists":2, "steals":2, "blocks":2, "turnovers":2, "field_goal_attempt":2,
#   "successful_field_goal":2, "three_point_attempt":2, "successful_three_point":2, "free_throw_attempt":2,
#   "successful_free_throw":2
#   }
# }
@app.route("/results/basketball/<int:eid>/team/", methods = ['GET','POST','PUT','DELETE'])
def basketballTeamStatistics(eid):
    json = request.json
    handler = BasketballEventHandler()
    if request.method == 'GET':
        return handler.getAllTeamStatisticsByBasketballEventId(eid)
    if request.method == 'POST':
        if json['add_type'] == 'AUTO':
            return handler.addTeamStatisticsAuto(eid)
        if json['add_type'] == 'MANUAL':
            return handler.addTeamStatistics(eid,json['attributes'])
        else: 
            return jsonify(Error= "Method not allowed, Must specify valid add_type"),405
    if request.method == 'PUT':
        return handler.editTeamStatistics(eid)
    if request.method == 'DELETE':
        return handler.removeTeamStatistics(eid)
    else:
        return jsonify(Error="Method not allowed."), 405



#FORMAT FOR REQUEST:
# {"attributes":
#   {
#   "local_score":2, "opponent_score":2
#   "opponent_name" = "name_here"
#   "opponent_color" = "#HEX_VAL_HERE"  
#   }
# }
@app.route("/results/basketball/<int:eid>/score/", methods = ['GET','POST','PUT','DELETE'])
def basketballFinalScores(eid):
    json = request.json
    handler = BasketballEventHandler()
    if request.method == 'GET':
        return handler.getFinalScore(eid)
    if request.method == 'POST':
        return handler.addFinalScore(eid,json['attributes'])
    if request.method == 'PUT':
        return handler.editFinalScore(eid,json['attributes'])
    if request.method == 'DELETE':
        return handler.removeFinalScore(eid)
    else:
        return jsonify(Error="Method not allowed."), 405

@app.route("/results/basketball/season/<int:seasonYear>/<int:aid>/", methods = ['GET'])
def basketballSeasonAthleteStatistics(aid,seasonYear):
    json = request.json
    handler = BasketballEventHandler()
    if request.method == 'GET':
        return handler.getAllAthleteStatisticsPerSeason(aid,seasonYear)
    else:
        return jsonify(Error="Method not allowed."), 405

#Launch app.
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
    