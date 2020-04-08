from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import datetime
from handler.user import UserHandler
from handler.athlete import AthleteHandler
from auth import verifyHash, generateToken, verifyToken
from functools import wraps
from dotenv import load_dotenv
import os
from handler.position import PositionHandler
from handler.event import EventHandler
from handler.basketball_event import BasketballEventHandler
from handler.volleyball_event import VolleyballEventHandler
from handler.soccer_event import SoccerEventHandler
from handler.baseball_event import BaseballEventHandler
from handler.sport import SportHandler



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

        # Extract token from auth header.
        token = request.headers.get('Authorization').split(' ')[1]

        if not token:
            return jsonify(Error='Token is missing'), 403

        if not verifyToken(token):
            return jsonify(Error="Token is invalid"), 403
        else:
            return func()
    return decorated


@app.route("/")
@token_check
def hello():
    return jsonify("Hi, this is a route that will be eliminated xD")

#--------- Athlete Routes ---------#
@app.route("/athletes/", methods=['GET', 'POST'])
def athletes():
    handler = AthleteHandler()
    if request.method == 'POST':
        json = request.json
        return handler.addAthlete(json['sID'], json['attributes'])
    elif request.method == 'GET':
        json = request.json

        return handler.getAthletesBySport(json['sID'])


@app.route("/athletes/<int:aid>/", methods=['GET', 'POST', 'PUT', 'DELETE'])
def athleteByID(aid):
    handler = AthleteHandler()
    if request.method == 'GET':
        return handler.getAthleteByID(aid)
    elif request.method == 'PUT':
        json = request.json
        return handler.editAthlete(aid, json['attributes'])
    elif request.method == 'DELETE':
        json = request.json
        return handler.removeAthlete(aid)

#--------- Position Routes ---------#
@app.route("/positions/", methods=['GET', 'DELETE'])
def position():
    handler = PositionHandler()
    if request.method == 'GET':
        return handler.getPositionByName(request.json['psName'])
    elif request.method == 'DELETE':
        return handler.removeAthletePosition(request.json['apID'])


@app.route("/positions/<int:sid>", methods=['GET'])
def sportPositions(sid):
    handler = PositionHandler()
    if request.method == 'GET':
        return handler.getPositions(sid)


@app.route("/positions/<int:sid>/<int:aid>", methods=['GET', 'POST', 'PUT'])
def athletePositions(sid, aid):
    handler = PositionHandler()
    if request.method == 'GET':
        return handler.getAthletePositionInSport(sid, aid)
    if request.method == 'POST':
        return handler.addAthletePosition(request.json['psID'], aid)
    if request.method == 'PUT':
        return handler.editAthletePosition(request.json['apID'], request.json['psID'], aid)

###########################################
#--------- Authentication Routes ---------#
###########################################
@app.route("/auth/", methods=['POST'])
def auth():
    if request.method == 'POST':
        handler = UserHandler() 

        if request.json['username'] == None or request.json['password'] == None:
            return jsonify(Error='Bad Request'), 400
            
        username = request.json['username']
        password = request.json['password'] # TODO: AES Encryption
        
        return handler.login(username, password)
        
@app.route("/test/", methods=['get'])
def test():
    if request.method == 'get':
        handler = UserHandler() 

        if request.json['username'] == None or request.json['password'] == None:
            return jsonify(Error='Bad Request'), 400
            
        username = request.json['username']
        password = request.json['password'] # TODO: AES Encryption
        
        return handler.login(username, password)

###########################################
#--------- Dashboard User Routes ---------#
###########################################
@app.route("/users/", methods = ['GET','POST'])
def allUsers():
    handler = UserHandler()
    if request.method == 'GET':
        ## For user list display
        return handler.getAllDashUsers() 
    if request.method == 'POST':
        req = request.json

        ## Check the request contains the right structure.
        if req['username'] == None or req['full_name'] == None or req['email'] == None or req['password'] == None:
            return jsonify(Error='Bad Request'), 400

        ## For account creation
        return handler.addDashUser(req['username'],req['full_name'], req['email'], req['password'])

@app.route("/users/<int:duid>", methods = ['GET','PATCH'])
def userByID(duid):
    handler = UserHandler()
    req = request.json
    if request.method == 'GET':
        ## For managing specific users
        return handler.getDashUserByID(duid)
    if request.method == 'PATCH':
        ## For username change
        ## Check the request contains the right structure.
        if req['username'] == None:
            return jsonify(Error='Bad Request'), 400

        return handler.updateDashUserUsername(duid,req['username'])

@app.route("/users/username/", methods = ['POST'])
def getUserByUsername():
    if request.method == 'POST':
        handler = UserHandler()
        req = request.json
        ## Check the request contains the right structure.
        if req['username'] == None:
            return jsonify(Error='Bad Request'), 400

        return handler.getDashUserByUsername(req['username'])


@app.route("/users/email/", methods = ['POST'])
def getUserByEmail():
    if request.method == 'POST':
        handler = UserHandler()
        req = request.json
        ## Check the request contains the right structure.
        if req['email'] == None:
            return jsonify(Error='Bad Request'), 400
        return handler.getDashUserByEmail(req['email'])

@app.route("/users/<int:duid>/reset", methods = ['PATCH'])
def passwordReset(duid):
    handler = UserHandler()
    req = request.json
    if request.method == 'PATCH':
        ## For password reset
        ## Check the request contains the right structure.
        if req['password'] == None:
            return jsonify(Error='Bad Request'), 400
        return handler.updateDashUserPassword(duid,req['password'])

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

@app.route("/users/<string:duid>/permissions",  methods = [ 'GET','PATCH'])
def userPermissions(duid):
    handler = UserHandler()
    if request.method == 'GET':
        return  handler.getUserPermissions(duid)
    if request.method == 'PATCH':
        req = request.json
        ## Check the request contains the right structure.
        if req['permissions'] == None:
            return jsonify(Error='Bad Request'), 400
        handler = UserHandler()
        return  handler.setUserPermissions(duid, req['permissions'])


#--------- Event Routes ---------#
@app.route("/events/",methods = ['GET'])
def events():
    handler = EventHandler()
    if request.method == 'GET':
        return handler.getAllEvents()
    

@app.route("/events/<int:eID>/",methods =['GET','PUT','DELETE'])
def eventsById(eID):
    handler = EventHandler()
    if request.method == 'GET':
        return handler.getEventByID(eID)
    elif request.method == 'PUT':
        json = request.json
        return handler.editEvent(eID,json['attributes'])
    elif request.method == 'DELETE':
        return handler.removeEvent(eID)

@app.route("/events/team/<int:tID>/", methods = ['GET','POST'])
def teamEvents(tID):
    handler = EventHandler()
    if request.method == 'GET':
        return handler.getEventsByTeam(tID)
    elif request.method == 'POST':
        json = request.json
        return handler.addEvent(tID,json['attributes'])



#--------- Sports/Categories/Positions Routes ---------#

'''
    TODO ***************************************** TODO
        1. Add routes documentation.
        2. Validate that the format matches with other routes.
        3. Verify if it is necessary to validate request.method=='GET'.
        4. Tests, tests, and more tests...
'''



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
#   "opponent_score": 0,
#   "opponent_name": "name_here",
#   "opponent_color": "#HEX_VAL_HERE" 
# }

# TODO: validate JSON request arguments somehow
# @app.route("/results/basketball/<int:eid>/", methods = ['GET','POST'])
@app.route("/results/basketball/", methods = ['GET','POST'])
def basketballStatistics():
    json = request.json
    handler = BasketballEventHandler()
    if request.method == 'GET':
        return handler.getAllStatisticsByEventID(json['event_id'])
        #Removed call for version with only athlete stats list, new version returns all
        #return handler.getAllStatisticsByEventID(eid)
    if request.method == 'POST':
        return handler.addAllEventStatistics(json['event_id'],json)
        #return jsonify(json),200
    else:
        return jsonify("Method not allowed."), 405

#FORMAT FOR REQUEST:
# {
#   "event_id": 2,
#   "athlete_id":2,
#   "attributes":
#   {
#   "points":2, "rebounds":2, "assists":2, "steals":2, "blocks":2, "turnovers":2, "field_goal_attempt":2,
#   "successful_field_goal":2, "three_point_attempt":2, "successful_three_point":2, "free_throw_attempt":2,
#   "successful_free_throw":2
#   }
# }

# @app.route("/results/basketball/<int:eid>/<int:aid>/", methods = ['GET','POST','PUT','DELETE'])
@app.route("/results/basketball/individual/", methods = ['GET','POST','PUT','DELETE'])
def basketballAthleteStatistics():
    json = request.json
    handler = BasketballEventHandler()
    if request.method == 'GET':
        return handler.getAllAthleteStatisticsByEventId(json['event_id'],json['athlete_id'])
    if request.method == 'POST':
        return handler.addStatistics(json['event_id'],json['athlete_id'],json['attributes'])
    if request.method == 'PUT':
        returnable = handler.editStatistics(json['event_id'],json['athlete_id'],json['attributes'])
        return returnable
    if request.method == 'DELETE':
        return handler.removeStatistics(json['event_id'],json['athlete_id'])
    else:
        return jsonify(Error="Method not allowed."), 405

#FORMAT FOR REQUEST:
# {"add_type":"manual",
# "event_id":1,
# "attributes":
#   {
#   "points":2, "rebounds":2, "assists":2, "steals":2, "blocks":2, "turnovers":2, "field_goal_attempt":2,
#   "successful_field_goal":2, "three_point_attempt":2, "successful_three_point":2, "free_throw_attempt":2,
#   "successful_free_throw":2
#   }
# }

# @app.route("/results/basketball/<int:eid>/team/", methods = ['GET','POST','PUT','DELETE'])
@app.route("/results/basketball/team/", methods = ['GET','POST','PUT','DELETE'])
def basketballTeamStatistics():
    json = request.json
    handler = BasketballEventHandler()
    if request.method == 'GET':
        return handler.getAllTeamStatisticsByEventId(json['event_id'])
    if request.method == 'POST':
        if json['add_type'] == 'AUTO':
            return handler.addTeamStatisticsAuto(json['event_id'])
        if json['add_type'] == 'MANUAL':
            return handler.addTeamStatistics(json['event_id'],json['attributes'])
        else: 
            return jsonify(Error= "Method not allowed, Must specify valid add_type"),405
    if request.method == 'PUT':
        return handler.editTeamStatistics(json['event_id'])
    if request.method == 'DELETE':
        return handler.removeTeamStatistics(json['event_id'])
    else:
        return jsonify(Error="Method not allowed."), 405



#FORMAT FOR REQUEST:
# { "event_id":3,
#   "attributes":
#   {
#   "local_score":2, "opponent_score":2,
#   "opponent_name": "name_here",
#   "opponent_color": "#HEX_VAL_HERE"  
#   }
# }

# @app.route("/results/basketball/<int:eid>/score/", methods = ['GET','POST','PUT','DELETE'])
@app.route("/results/basketball/score/", methods = ['GET','POST','PUT','DELETE'])
def basketballFinalScores():
    json = request.json
    handler = BasketballEventHandler()
    if request.method == 'GET':
        return handler.getFinalScore(json['event_id'])
    if request.method == 'POST':
        return handler.addFinalScore(json['event_id'],json['attributes'])
    if request.method == 'PUT':
        return handler.editFinalScore(json['event_id'],json['attributes'])
    if request.method == 'DELETE':
        return handler.removeFinalScore(json['event_id'])
    else:
        return jsonify(Error="Method not allowed."), 405

#TODO: need to prepare a reuquest schema for this one. just aid and seasonYear
@app.route("/results/basketball/season/<int:seasonYear>/<int:aid>/", methods = ['GET'])
def basketballSeasonAthleteStatistics(aid,seasonYear):
    json = request.json
    handler = BasketballEventHandler()
    if request.method == 'GET':
        return handler.getAllAthleteStatisticsPerSeason(aid,seasonYear)
    else:
        return jsonify(Error="Method not allowed."), 405


#===================================================================================
#=======================//VOLLEYBALL RESULTS ROUTES//===============================
#===================================================================================

# REQUEST FORMAT FOR ROUTE:
# { "event_id": 5,
#   "team_statistics": 
#    { "volleyball_statistics": 
#       { 
#         "kill_points": 1,
#         "attack_errors":1,
#         "assists":1,
#         "aces":1,
#         "service_errors":1,
#         "digs":1,
#         "blocks":1,
#         "blocking_errors":1,
#         "reception_errors":1
#       } 
#    },
#   "athlete_statistics": 
#   [
#   	{"athlete_id":4,
#   	"statistics":
# 	  	{"volleyball_statistics":
# 		  	{
#             "kill_points": 1,
#             "attack_errors":1,
#             "assists":1,
#             "aces":1,
#             "service_errors":1,
#             "digs":1,
#             "blocks":1,
#             "blocking_errors":1,
#             "reception_errors":1
# 		  	}
# 	  	}
#   	},
#   	{"athlete_id":8,
#   	"statistics":
# 	  	{"volleyball_statistics":
# 		  	{
#             "kill_points": 1,
#             "attack_errors":1,
#             "assists":1,
#             "aces":1,
#             "service_errors":1,
#             "digs":1,
#             "blocks":1,
#             "blocking_errors":1,
#             "reception_errors":1
# 		  	}
# 	  	}
#   	}
#   	],
#   "uprm_score": 0,
#   "opponent_score": 0,
#   "opponent_name": "name_here",
#   "opponent_color": "#HEX_VAL_HERE" 
# }

# TODO: validate JSON request arguments somehow
# @app.route("/results/volleyball/<int:eid>/", methods = ['GET','POST'])
@app.route("/results/volleyball/", methods = ['GET','POST'])
def volleyballStatistics():
    json = request.json
    handler = VolleyballEventHandler()
    if request.method == 'GET':
        return handler.getAllStatisticsByEventID(json['event_id'])
    if request.method == 'POST':
        return handler.addAllEventStatistics(json['event_id'],json)
        #return jsonify(json),200
    else:
        return jsonify("Method not allowed."), 405

# FORMAT FOR REQUEST:
# {
#   "event_id": 2,
#   "athlete_id":2,
#   "attributes":
#   {
#     "kill_points": 1,
#     "attack_errors":1,
#     "assists":1,
#     "aces":1,
#     "service_errors":1,
#     "digs":1,
#     "blocks":1,
#     "blocking_errors":1,
#     "reception_errors":1
#   }
# }

# @app.route("/results/volleyball/<int:eid>/<int:aid>/", methods = ['GET','POST','PUT','DELETE'])
@app.route("/results/volleyball/individual/", methods = ['GET','POST','PUT','DELETE'])
def volleyballAthleteStatistics():
    json = request.json
    handler = VolleyballEventHandler()
    if request.method == 'GET':
        return handler.getAllAthleteStatisticsByEventId(json['event_id'],json['athlete_id'])
    if request.method == 'POST':
        return handler.addStatistics(json['event_id'],json['athlete_id'],json['attributes'])
    if request.method == 'PUT':
        returnable = handler.editStatistics(json['event_id'],json['athlete_id'],json['attributes'])
        return returnable
    if request.method == 'DELETE':
        return handler.removeStatistics(json['event_id'],json['athlete_id'])
    else:
        return jsonify(Error="Method not allowed."), 405

# FORMAT FOR REQUEST:
# {
# "add_type":"manual",
# "event_id":1,
# "attributes":
#   {
#     "kill_points": 1,
#     "attack_errors":1,
#     "assists":1,
#     "aces":1,
#     "service_errors":1,
#     "digs":1,
#     "blocks":1,
#     "blocking_errors":1,
#     "reception_errors":1
#   }
# }

# @app.route("/results/volleyball/<int:eid>/team/", methods = ['GET','POST','PUT','DELETE'])
@app.route("/results/volleyball/team/", methods = ['GET','POST','PUT','DELETE'])
def volleyballTeamStatistics():
    json = request.json
    handler = VolleyballEventHandler()
    if request.method == 'GET':
        return handler.getAllTeamStatisticsByEventId(json['event_id'])
    if request.method == 'POST':
        if json['add_type'] == 'AUTO':
            return handler.addTeamStatisticsAuto(json['event_id'])
        if json['add_type'] == 'MANUAL':
            return handler.addTeamStatistics(json['event_id'],json['attributes'])
        else: 
            return jsonify(Error= "Method not allowed, Must specify valid add_type"),405
    if request.method == 'PUT':
        return handler.editTeamStatistics(json['event_id'])
    if request.method == 'DELETE':
        return handler.removeTeamStatistics(json['event_id'])
    else:
        return jsonify(Error="Method not allowed."), 405



#FORMAT FOR REQUEST:
# { "event_id":3,
#   "attributes":
#   {
#   "local_score":2, "opponent_score":2,
#   "opponent_name": "name_here",
#   "opponent_color": "#HEX_VAL_HERE"  
#   }
# }

# @app.route("/results/volleyball/<int:eid>/score/", methods = ['GET','POST','PUT','DELETE'])
@app.route("/results/volleyball/score/", methods = ['GET','POST','PUT','DELETE'])
def volleyballFinalScores():
    json = request.json
    handler = VolleyballEventHandler()
    if request.method == 'GET':
        return handler.getFinalScore(json['event_id'])
    if request.method == 'POST':
        return handler.addFinalScore(json['event_id'],json['attributes'])
    if request.method == 'PUT':
        return handler.editFinalScore(json['event_id'],json['attributes'])
    if request.method == 'DELETE':
        return handler.removeFinalScore(json['event_id'])
    else:
        return jsonify(Error="Method not allowed."), 405

#TODO: need to prepare a reuquest schema for this one. just aid and seasonYear
@app.route("/results/volleyball/season/<int:seasonYear>/<int:aid>/", methods = ['GET'])
def volleyballSeasonAthleteStatistics(aid,seasonYear):
    json = request.json
    handler = VolleyballEventHandler()
    if request.method == 'GET':
        return handler.getAllAthleteStatisticsPerSeason(aid,seasonYear)
    else:
        return jsonify(Error="Method not allowed."), 405


#===================================================================================
#===================//END VOLLEYBALL RESULTS ROUTES//===============================
#===================================================================================


#===================================================================================
#=======================//SOCCER RESULTS ROUTES//===============================
#===================================================================================

# REQUEST FORMAT FOR ROUTE:
# { "event_id": 5,
#   "team_statistics": 
#    { "soccer_statistics": 
#       { 
#         "goal_attempts":1, 
#         "assists":1,
#         "fouls":1,
#         "cards":1,
#         "successful_goals":1,
#         "tackles":1
#       } 
#    },
#   "athlete_statistics": 
#   [
#   	{"athlete_id":4,
#   	"statistics":
# 	  	{"soccer_statistics":
# 		  	{
#             "goal_attempts":1, 
#             "assists":1,
#             "fouls":1,
#             "cards":1,
#             "successful_goals":1,
#             "tackles":1
# 		  	}
# 	  	}
#   	},
#   	{"athlete_id":8,
#   	"statistics":
# 	  	{"soccer_statistics":
# 		  	{
#             "goal_attempts":1, 
#             "assists":1,
#             "fouls":1,
#             "cards":1,
#             "successful_goals":1,
#             "tackles":1
# 		  	}
# 	  	}
#   	}
#   	],
#   "uprm_score": 0,
#   "opponent_score": 0,
#   "opponent_name": "name_here",
#   "opponent_color": "#HEX_VAL_HERE" 
# }

# TODO: validate JSON request arguments somehow
# @app.route("/results/soccer/<int:eid>/", methods = ['GET','POST'])
@app.route("/results/soccer/", methods = ['GET','POST'])
def soccerStatistics():
    json = request.json
    handler = SoccerEventHandler()
    if request.method == 'GET':
        return handler.getAllStatisticsByEventID(json['event_id'])
    if request.method == 'POST':
        return handler.addAllEventStatistics(json['event_id'],json)
        #return jsonify(json),200
    else:
        return jsonify("Method not allowed."), 405

# FORMAT FOR REQUEST:
# {
#   "event_id": 2,
#   "athlete_id":2,
#   "attributes":
#   {
#     "goal_attempts":1, 
#     "assists":1,
#     "fouls":1,
#     "cards":1,
#     "successful_goals":1,
#     "tackles":1
#   }
# }

# @app.route("/results/soccer/<int:eid>/<int:aid>/", methods = ['GET','POST','PUT','DELETE'])
@app.route("/results/soccer/individual/", methods = ['GET','POST','PUT','DELETE'])
def soccerAthleteStatistics():
    json = request.json
    handler = SoccerEventHandler()
    if request.method == 'GET':
        return handler.getAllAthleteStatisticsByEventId(json['event_id'],json['athlete_id'])
    if request.method == 'POST':
        return handler.addStatistics(json['event_id'],json['athlete_id'],json['attributes'])
    if request.method == 'PUT':
        returnable = handler.editStatistics(json['event_id'],json['athlete_id'],json['attributes'])
        return returnable
    if request.method == 'DELETE':
        return handler.removeStatistics(json['event_id'],json['athlete_id'])
    else:
        return jsonify(Error="Method not allowed."), 405

# FORMAT FOR REQUEST:
# {
# "add_type":"manual",
# "event_id":1,
# "attributes":
#   {
#     "goal_attempts":1, 
#     "assists":1,
#     "fouls":1,
#     "cards":1,
#     "successful_goals":1,
#     "tackles":1
#   }
# }

# @app.route("/results/soccer/<int:eid>/team/", methods = ['GET','POST','PUT','DELETE'])
@app.route("/results/soccer/team/", methods = ['GET','POST','PUT','DELETE'])
def soccerTeamStatistics():
    json = request.json
    handler = SoccerEventHandler()
    if request.method == 'GET':
        return handler.getAllTeamStatisticsByEventId(json['event_id'])
    if request.method == 'POST':
        if json['add_type'] == 'AUTO':
            return handler.addTeamStatisticsAuto(json['event_id'])
        if json['add_type'] == 'MANUAL':
            return handler.addTeamStatistics(json['event_id'],json['attributes'])
        else: 
            return jsonify(Error= "Method not allowed, Must specify valid add_type"),405
    if request.method == 'PUT':
        return handler.editTeamStatistics(json['event_id'])
    if request.method == 'DELETE':
        return handler.removeTeamStatistics(json['event_id'])
    else:
        return jsonify(Error="Method not allowed."), 405



#FORMAT FOR REQUEST:
# { "event_id":3,
#   "attributes":
#   {
#   "local_score":2, "opponent_score":2,
#   "opponent_name": "name_here",
#   "opponent_color": "#HEX_VAL_HERE"  
#   }
# }

# @app.route("/results/soccer/<int:eid>/score/", methods = ['GET','POST','PUT','DELETE'])
@app.route("/results/soccer/score/", methods = ['GET','POST','PUT','DELETE'])
def soccerFinalScores():
    json = request.json
    handler = SoccerEventHandler()
    if request.method == 'GET':
        return handler.getFinalScore(json['event_id'])
    if request.method == 'POST':
        return handler.addFinalScore(json['event_id'],json['attributes'])
    if request.method == 'PUT':
        return handler.editFinalScore(json['event_id'],json['attributes'])
    if request.method == 'DELETE':
        return handler.removeFinalScore(json['event_id'])
    else:
        return jsonify(Error="Method not allowed."), 405

#TODO: need to prepare a reuquest schema for this one. just aid and seasonYear
@app.route("/results/soccer/season/<int:seasonYear>/<int:aid>/", methods = ['GET'])
def soccerSeasonAthleteStatistics(aid,seasonYear):
    json = request.json
    handler = SoccerEventHandler()
    if request.method == 'GET':
        return handler.getAllAthleteStatisticsPerSeason(aid,seasonYear)
    else:
        return jsonify(Error="Method not allowed."), 405


#===================================================================================
#===================//END SOCCER RESULTS ROUTES//===============================
#===================================================================================

#===================================================================================
#=======================//BASEBALL RESULTS ROUTES//===============================
#===================================================================================

# REQUEST FORMAT FOR ROUTE:
# { "event_id": 5,
#   "team_statistics": 
#    { "baseball_statistics": 
#       { 
#         "at_bats":1,
#         "runs":1,
#         "hits":1,
#         "runs_batted_in":1,
#         "base_on_balls":1,
#         "strikeouts":1,
#         "left_on_base":1
#       } 
#    },
#   "athlete_statistics": 
#   [
#   	{"athlete_id":4,
#   	"statistics":
# 	  	{"baseball_statistics":
# 		  	{
#             "at_bats":1,
#             "runs":1,
#             "hits":1,
#             "runs_batted_in":1,
#             "base_on_balls":1,
#             "strikeouts":1,
#             "left_on_base":1
# 		  	}
# 	  	}
#   	},
#   	{"athlete_id":8,
#   	"statistics":
# 	  	{"baseball_statistics":
# 		  	{
#             "at_bats":1,
#             "runs":1,
#             "hits":1,
#             "runs_batted_in":1,
#             "base_on_balls":1,
#             "strikeouts":1,
#             "left_on_base":1
# 		  	}
# 	  	}
#   	}
#   	],
#   "uprm_score": 0,
#   "opponent_score": 0,
#   "opponent_name": "name_here",
#   "opponent_color": "#HEX_VAL_HERE" 
# }

# TODO: validate JSON request arguments somehow
# @app.route("/results/baseball/<int:eid>/", methods = ['GET','POST'])
@app.route("/results/baseball/", methods = ['GET','POST'])
def baseballStatistics():
    json = request.json
    handler = BaseballEventHandler()
    if request.method == 'GET':
        return handler.getAllStatisticsByEventID(json['event_id'])
    if request.method == 'POST':
        return handler.addAllEventStatistics(json['event_id'],json)
        #return jsonify(json),200
    else:
        return jsonify("Method not allowed."), 405

# FORMAT FOR REQUEST:
# {
#   "event_id": 2,
#   "athlete_id":2,
#   "attributes":
#   {
#     "at_bats":1,
#     "runs":1,
#     "hits":1,
#     "runs_batted_in":1,
#     "base_on_balls":1,
#     "strikeouts":1,
#     "left_on_base":1
#   }
# }

# @app.route("/results/baseball/<int:eid>/<int:aid>/", methods = ['GET','POST','PUT','DELETE'])
@app.route("/results/baseball/individual/", methods = ['GET','POST','PUT','DELETE'])
def baseballAthleteStatistics():
    json = request.json
    handler = BaseballEventHandler()
    if request.method == 'GET':
        return handler.getAllAthleteStatisticsByEventId(json['event_id'],json['athlete_id'])
    if request.method == 'POST':
        return handler.addStatistics(json['event_id'],json['athlete_id'],json['attributes'])
    if request.method == 'PUT':
        returnable = handler.editStatistics(json['event_id'],json['athlete_id'],json['attributes'])
        return returnable
    if request.method == 'DELETE':
        return handler.removeStatistics(json['event_id'],json['athlete_id'])
    else:
        return jsonify(Error="Method not allowed."), 405

# FORMAT FOR REQUEST:
# {
# "add_type":"manual",
# "event_id":1,
# "attributes":
#   {
#     "at_bats":1,
#     "runs":1,
#     "hits":1,
#     "runs_batted_in":1,
#     "base_on_balls":1,
#     "strikeouts":1,
#     "left_on_base":1
#   }
# }

# @app.route("/results/baseball/<int:eid>/team/", methods = ['GET','POST','PUT','DELETE'])
@app.route("/results/baseball/team/", methods = ['GET','POST','PUT','DELETE'])
def baseballTeamStatistics():
    json = request.json
    handler = BaseballEventHandler()
    if request.method == 'GET':
        return handler.getAllTeamStatisticsByEventId(json['event_id'])
    if request.method == 'POST':
        if json['add_type'] == 'AUTO':
            return handler.addTeamStatisticsAuto(json['event_id'])
        if json['add_type'] == 'MANUAL':
            return handler.addTeamStatistics(json['event_id'],json['attributes'])
        else: 
            return jsonify(Error= "Method not allowed, Must specify valid add_type"),405
    if request.method == 'PUT':
        return handler.editTeamStatistics(json['event_id'])
    if request.method == 'DELETE':
        return handler.removeTeamStatistics(json['event_id'])
    else:
        return jsonify(Error="Method not allowed."), 405



#FORMAT FOR REQUEST:
# { "event_id":3,
#   "attributes":
#   {
#   "local_score":2, "opponent_score":2,
#   "opponent_name": "name_here",
#   "opponent_color": "#HEX_VAL_HERE"  
#   }
# }

# @app.route("/results/baseball/<int:eid>/score/", methods = ['GET','POST','PUT','DELETE'])
@app.route("/results/baseball/score/", methods = ['GET','POST','PUT','DELETE'])
def baseballFinalScores():
    json = request.json
    handler = BaseballEventHandler()
    if request.method == 'GET':
        return handler.getFinalScore(json['event_id'])
    if request.method == 'POST':
        return handler.addFinalScore(json['event_id'],json['attributes'])
    if request.method == 'PUT':
        return handler.editFinalScore(json['event_id'],json['attributes'])
    if request.method == 'DELETE':
        return handler.removeFinalScore(json['event_id'])
    else:
        return jsonify(Error="Method not allowed."), 405

#TODO: need to prepare a reuquest schema for this one. just aid and seasonYear
@app.route("/results/baseball/season/<int:seasonYear>/<int:aid>/", methods = ['GET'])
def baseballSeasonAthleteStatistics(aid,seasonYear):
    json = request.json
    handler = BaseballEventHandler()
    if request.method == 'GET':
        return handler.getAllAthleteStatisticsPerSeason(aid,seasonYear)
    else:
        return jsonify(Error="Method not allowed."), 405


#===================================================================================
#===================//END BASEBALL RESULTS ROUTES//===============================
#===================================================================================

#Launch app.
@app.route("/sports", methods=['GET'])
def get_sports():
    if request.method == 'GET':
        body = request.get_json()
        handler = SportHandler()

        if not body:
            return handler.getAllSports()

        if len(body) == 1:

            if 'branch' in body:
                return handler.getSportsByBranch(body['branch'])

            if 'sport_name' in body:
                return handler.getSportByName(body['sport_name'])

            if 'sport_id' in body:
                return handler.getSportById(body['sport_id'])

        return jsonify(ERROR="Odin/sports: Malformed request, either branch or name is allowed."), 400

    return jsonify(ERROR="Odin/sports: HTTP verb not allowed."), 405


@app.route("/sports/details", methods=['GET'])
def get_sport_info():
    if request.method == 'GET':
        body = request.get_json()
        if not body:
            return SportHandler().getSportCategoriesPositions()

        return jsonify(ERROR="Odin/sports/details: Malformed request, no params allowed."), 400

    return jsonify(ERROR="Odin/sports: HTTP verb not allowed."), 405


# Launch app.
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
    

