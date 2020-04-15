from flask import Flask, request, jsonify, session

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
from handler.pbp_handler import VolleyballPBPHandler

from handler.team import TeamHandler


## Load environment variables
load_dotenv()


app = Flask(__name__)
app.secret_key = 'any random string'

CORS(app)


def token_check(func):
    """
    Midleware to verify the request is authorized.

    Midleware function used to protect routes from unauthorized request
    by verifying each request provides a valid token.
    """
    @wraps(func)
    def decorated(*args, **kwargs):

        # Extract token from auth header.
        token = request.headers.get('Authorization').split(' ')[1]

        if not token:
            return jsonify(Error='Token is missing'), 403

        if not verifyToken(token):
            return jsonify(Error="Token is invalid"), 403
        else:
            return func(*args, **kwargs)
    return decorated


#--------- Athlete Routes ---------#
@app.route("/athletes/", methods=['GET', 'POST'])
def athletes():
    handler = AthleteHandler()
    if request.method == 'POST':
        json = request.json
        if not 'sID' in json or not 'attributes' in json:
            return jsonify(Error = "Bad Request"),400

        return handler.addAthlete(json['sID'], json['attributes'])

    elif request.method == 'GET':
        json = request.json
        if not 'sID' in json:
            return jsonify(Error = "Bad Request"),400

        return handler.getAthletesBySport(json['sID'])


@app.route("/athletes/<int:aid>/", methods=['GET', 'POST', 'PUT', 'DELETE'])
def athleteByID(aid):
    handler = AthleteHandler()
    if request.method == 'GET':
        return handler.getAthleteByID(aid)
    elif request.method == 'PUT':
        json = request.json
        if 'attributes' not in json:
            return jsonify(Error = "Bad Request"),400

        return handler.editAthlete(aid, json['attributes'])
        
    elif request.method == 'DELETE':        
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
        req = request.json
        if 'username' not in req or 'password' not in req:
            return jsonify(Error='Bad Request'), 400
            
        username = req['username']
        password = req['password'] # TODO: AES Encryption
        return handler.login(username, password)
        

###########################################
#--------- Dashboard User Routes ---------#
###########################################
@app.route("/users/", methods=['GET', 'POST'])
@token_check
def allUsers():
    handler = UserHandler()
    if request.method == 'GET':
        # For user list display
        return handler.getAllDashUsers()
    if request.method == 'POST':
        req = request.json

        ## Check the request contains the right structure.
        if 'username' not in req or 'full_name' not in req or 'email' not in req or 'password' not in req:
            return jsonify(Error='Bad Request'), 400

        # For account creation
        return handler.addDashUser(req['username'], req['full_name'], req['email'], req['password'])


@app.route("/users/<int:duid>", methods=['GET', 'PATCH'])
@token_check
def userByID(duid):
    handler = UserHandler()
    req = request.json
    if request.method == 'GET':
        # For managing specific users
        return handler.getDashUserByID(duid)
    if request.method == 'PATCH':
        ## For username change
        ## Check the request contains the right structure.
        if 'username' not in req or 'full_name' not in req or 'email' not in req or 'is_active' not in req :
            return jsonify(Error='Bad Request'), 400

        return handler.updateDashUserInfo(duid, req['username'],req['full_name'], req['email'], req['is_active'])


@app.route("/users/username/", methods=['POST'])
@token_check
def getUserByUsername():
    if request.method == 'POST':
        handler = UserHandler()
        req = request.json
        ## Check the request contains the right structure.
        if 'username' not in req :
            return jsonify(Error='Bad Request'), 400

        return handler.getDashUserByUsername(req['username'])


@app.route("/users/email/", methods=['POST'])
@token_check
def getUserByEmail():
    if request.method == 'POST':
        handler = UserHandler()
        req = request.json
        ## Check the request contains the right structure.
        if 'email' not in req :
            return jsonify(Error='Bad Request'), 400
        return handler.getDashUserByEmail(req['email'])


@app.route("/users/<int:duid>/reset", methods=['PATCH'])
@token_check
def passwordReset(duid):
    handler = UserHandler()
    req = request.json
    if request.method == 'PATCH':
        ## For password reset
        ## Check the request contains the right structure.
        if 'password' not in req :
            return jsonify(Error='Bad Request'), 400
        return handler.updateDashUserPassword(duid, req['password'])

@app.route("/users/activate", methods=['PATCH'])
@token_check
def accountUnlock():
    handler = UserHandler()
    req = request.json
    if request.method == 'PATCH':
        ## For acount unlock
        ## Check the request contains the right structure.
        if 'username' not in req or 'password' not in req or 'new_password' not in req :
            return jsonify(Error='Bad Request'), 400
        return handler.unlockDashUserAccount(req['username'], req['password'], req['new_password'])


# TODO: id's that are sanwdiwch must be converted to string
@app.route("/users/<string:duid>/toggleActive", methods=['PATCH'])
@token_check
def toggleActive(duid):
    handler = UserHandler()
    if request.method == 'PATCH':
        return handler.toggleDashUserActive(duid)


# TODO: id's that are sanwdiwch must be converted to string
@app.route("/users/<string:duid>/remove", methods=['PATCH'])
@token_check
def removeUser(duid):
    handler = UserHandler()
    if request.method == 'PATCH':
        return handler.removeDashUser(duid)


@app.route("/users/<string:duid>/permissions",  methods=['GET', 'PATCH'])
@token_check
def userPermissions(duid):
    handler = UserHandler()
    if request.method == 'GET':
        return handler.getUserPermissions(duid)
    if request.method == 'PATCH':
        req = request.json
        ## Check the request contains the right structure.
        if 'permissions' not in req :
            return jsonify(Error='Bad Request.'), 400
        if req['permissions'] == None:
            return jsonify(Error='Permissions cant be empty.'), 400
        handler = UserHandler()
        return handler.setUserPermissions(duid, req['permissions'])


#--------- Event Routes ---------#
@app.route("/events/", methods=['GET'])
def events():
    handler = EventHandler()
    if request.method == 'GET':
        return handler.getAllEvents()


@app.route("/events/<int:eID>/", methods=['GET', 'PUT', 'DELETE'])
def eventsById(eID):
    handler = EventHandler()
    if request.method == 'GET':
        return handler.getEventByID(eID)
    elif request.method == 'PUT':
        json = request.json        
        if 'attributes' not in json:
            return jsonify(Error = "Bad arguments"),400            
        return handler.editEvent(eID, json['attributes'])
    elif request.method == 'DELETE':
        return handler.removeEvent(eID)


@app.route("/events/team/<int:tID>/", methods=['GET', 'POST'])
def teamEvents(tID):
    handler = EventHandler()
    if request.method == 'GET':
        return handler.getEventsByTeam(tID)
    elif request.method == 'POST':
        json = request.json
        if 'attributes' not in json:
            return jsonify(Error = "Bad arguments"),400
        return handler.addEvent(tID, json['attributes'])


#--------- Sports/Categories/Positions Routes ---------#
'''
    TODO ***************************************** TODO
        1. Add routes documentation.
        2. Validate that the format matches with other routes.
        3. Verify if it is necessary to validate request.method=='GET'.
        4. Tests, tests, and more tests...
'''


#===================================================================================
#=======================//BASKETBALL RESULTS ROUTES//===============================
#===================================================================================
#TODO: (Herbert) verify route naming/division 
#TODO: (Herbert) validate JSON request arguments

# REQUEST FORMAT FOR ROUTE:
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
# }
@app.route("/results/basketball/", methods = ['GET','POST'])
def basketballStatistics():
    json = request.json
    handler = BasketballEventHandler()
    if request.method == 'GET':
        #Validate Request for GET
        if 'event_id' not in json:
            return jsonify(Error='Bad Request'), 400
        return handler.getAllStatisticsByEventID(json['event_id'])
    if request.method == 'POST':
        #Validate General IDs for POST
        if ('event_id' not in json or 'team_statistics' not in json or 'athlete_statistics'
        not in json or 'uprm_score' not in json or 'opponent_score' not in json):
            return jsonify(Error='Bad Request'), 400
        #Validate Team Statistics Request
        team_statistics = json['team_statistics']
        if ('basketball_statistics' not in team_statistics):
            return jsonify(Error='Bad Request'),400
        specific_stats = team_statistics['basketball_statistics']
        if ('points' not in specific_stats or 'rebounds' not in specific_stats or 'assists' not in specific_stats 
            or 'steals' not in specific_stats or 'blocks' not in specific_stats or 'turnovers' not in specific_stats 
            or 'field_goal_attempt' not in specific_stats or 'successful_field_goal' not in specific_stats 
            or 'three_point_attempt' not in specific_stats or 'successful_three_point' not in specific_stats 
            or 'free_throw_attempt' not in specific_stats or 'successful_free_throw' not in specific_stats):
                return jsonify(Error='Bad Request'),400
        #Validate Each Athlete's Statistics Request
        athlete_statistics = json['athlete_statistics']
        for athlete_json in athlete_statistics:
            if ('statistics' not in athlete_json or 'athlete_id' not in athlete_json):
                return jsonify(Error='Bad Request'),400
            athlete_json_sport = athlete_json['statistics']
            if ('basketball_statistics' not in athlete_json_sport):
                return jsonify(Error='Bad Request'),400
            specific_stats = athlete_json_sport['basketball_statistics']
            if ('points' not in specific_stats or 'rebounds' not in specific_stats or 'assists' not in specific_stats 
            or 'steals' not in specific_stats or 'blocks' not in specific_stats or 'turnovers' not in specific_stats 
            or 'field_goal_attempt' not in specific_stats or 'successful_field_goal' not in specific_stats 
            or 'three_point_attempt' not in specific_stats or 'successful_three_point' not in specific_stats 
            or 'free_throw_attempt' not in specific_stats or 'successful_free_throw' not in specific_stats):
                return jsonify(Error='Bad Request'),400
                
        return handler.addAllEventStatistics(json['event_id'], json)
        
        # return jsonify(json),200
    else:
        return jsonify("Method not allowed."), 405

# FORMAT FOR REQUEST:
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
@app.route("/results/basketball/individual/", methods = ['GET','POST','PUT','DELETE'])
def basketballAthleteStatistics():
    json = request.json
    handler = BasketballEventHandler()
    
    if request.method == 'GET' or request.method == 'DELETE':
        #Validate GET/REMOVE requests
        if ('event_id' not in json or 'athlete_id' not in json):
            return jsonify(Error='Bad Request'),400
        #Carry on with request
        if request.method == 'GET':
            return handler.getAllAthleteStatisticsByEventId(json['event_id'], json['athlete_id'])
        if request.method == 'DELETE':
            return handler.removeStatistics(json['event_id'], json['athlete_id'])
    
    if request.method == 'POST' or request.method == 'PUT':
        #Validate POST/PUT Requests
        #Validate Basic IDs
        if ('event_id' not in json or 'athlete_id' not in json or 'attributes' not in json):
            return jsonify(Error='Bad Request'),400
        #Validate Specific Statistics
        specific_stats = json['attributes']
        if ('points' not in specific_stats or 'rebounds' not in specific_stats or 'assists' not in specific_stats 
            or 'steals' not in specific_stats or 'blocks' not in specific_stats or 'turnovers' not in specific_stats 
            or 'field_goal_attempt' not in specific_stats or 'successful_field_goal' not in specific_stats 
            or 'three_point_attempt' not in specific_stats or 'successful_three_point' not in specific_stats 
            or 'free_throw_attempt' not in specific_stats or 'successful_free_throw' not in specific_stats):
                return jsonify(Error='Bad Request'),400
        #Carry On With Request
        if request.method == 'POST':
            return handler.addStatistics(json['event_id'], json['athlete_id'], json['attributes'])
        if request.method == 'PUT':
            returnable = handler.editStatistics(
                json['event_id'], json['athlete_id'], json['attributes'])
            return returnable
    
    else:
        return jsonify(Error="Method not allowed."), 405

# FORMAT FOR REQUEST:
# {"add_type":"manual",
# "event_id":1,
# "attributes":
#   {
#   "points":2, "rebounds":2, "assists":2, "steals":2, "blocks":2, "turnovers":2, "field_goal_attempt":2,
#   "successful_field_goal":2, "three_point_attempt":2, "successful_three_point":2, "free_throw_attempt":2,
#   "successful_free_throw":2
#   }
# }
@app.route("/results/basketball/team/", methods = ['GET','POST','PUT','DELETE'])
def basketballTeamStatistics():
    json = request.json
    handler = BasketballEventHandler()
    if request.method == 'GET' or request.method == 'DELETE' or request.method == 'PUT':
        #Validate GET/REMOVE/PUT requests
        if ('event_id' not in json):
            return jsonify(Error='Bad Request'),400
        #Carry on with request
        if request.method == 'GET':
            return handler.getAllTeamStatisticsByEventId(json['event_id'])
        if request.method == 'DELETE':
            return handler.removeTeamStatistics(json['event_id'])
        if request.method == 'PUT':
            return handler.editTeamStatistics(json['event_id'])
    if request.method == 'POST':
        #Validate POST Requests
        #Validate Basic IDs
        if ('event_id' not in json or 'add_type' not in json or 'attributes' not in json):
            return jsonify(Error='Bad Request'),400
        #Validate Specific Statistics
        specific_stats = json['attributes']
        if ('points' not in specific_stats or 'rebounds' not in specific_stats or 'assists' not in specific_stats 
            or 'steals' not in specific_stats or 'blocks' not in specific_stats or 'turnovers' not in specific_stats 
            or 'field_goal_attempt' not in specific_stats or 'successful_field_goal' not in specific_stats 
            or 'three_point_attempt' not in specific_stats or 'successful_three_point' not in specific_stats 
            or 'free_throw_attempt' not in specific_stats or 'successful_free_throw' not in specific_stats):
                return jsonify(Error='Bad Request'),400
        #Carry On With Request
        if json['add_type'] == 'AUTO':
            return handler.addTeamStatisticsAuto(json['event_id'])
        if json['add_type'] == 'MANUAL':
            return handler.addTeamStatistics(json['event_id'], json['attributes'])
        else:
            return jsonify(Error="Bad Request, Must specify valid add_type"), 400
    else:
        return jsonify(Error="Method not allowed."), 405

# FORMAT FOR REQUEST:
# { "event_id":3,
#   "attributes":
#   {
#   "uprm_score":2, "opponent_score":2
#   }
# }
@app.route("/results/basketball/score/", methods = ['GET','POST','PUT','DELETE'])
def basketballFinalScores():
    json = request.json
    handler = BasketballEventHandler()
    if request.method == 'GET' or request.method == 'DELETE':
        #Validate GET/REMOVE requests
        if ('event_id' not in json):
            return jsonify(Error='Bad Request'),400
        #Carry on with request
        if request.method == 'GET':
            return handler.getFinalScore(json['event_id'])
        if request.method == 'DELETE':
            return handler.removeFinalScore(json['event_id'])
    if request.method == 'POST' or request.method == 'PUT':
        #Validate POST/PUT Requests
        #Validate Basic IDs
        if ('event_id' not in json or 'attributes' not in json):
            return jsonify(Error='Bad Request'),400
        #Validate Specific Statistics
        specific_stats = json['attributes']
        if ('uprm_score' not in specific_stats or 'opponent_score' not in specific_stats):
                return jsonify(Error='Bad Request'),400
        #Carry On With Request
        if request.method == 'POST':
            return handler.addFinalScore(json['event_id'], json['attributes'])
        if request.method == 'PUT':
            return handler.editFinalScore(json['event_id'], json['attributes'])
    else:
        return jsonify(Error="Method not allowed."), 405

# {
#     "athlete_id":1,
#     "season_year":2020
# }
#TODO: (Herbert) need to prepare a request schema for this one. just aid and seasonYear
@app.route("/results/basketball/season/athlete_games/", methods = ['GET'])
def basketballSeasonAthleteStatistics():
    json = request.json
    handler = BasketballEventHandler()
    if request.method == 'GET':
        #Validate GET requests
        if ('athlete_id' not in json or 'season_year' not in json):
            return jsonify(Error='Bad Request'),400
        #Carry on with request
        return handler.getAllAthleteStatisticsPerSeason(json['athlete_id'], json['season_year'])
    else:
        return jsonify(Error="Method not allowed."), 405


# {
#     "athlete_id":1,
#     "season_year":2020
# }
@app.route("/results/basketball/season/athlete_aggregate/", methods = ['GET'])
def basketballAggregateAthleteStatistics():
    json = request.json
    handler = BasketballEventHandler()
    if request.method == 'GET':
        #Validate GET requests
        if ('athlete_id' not in json or 'season_year' not in json):
            return jsonify(Error='Bad Request'),400
        #Carry on with request
        return handler.getAggregatedAthleteStatisticsPerSeason(json['athlete_id'], json['season_year'])
    else:
        return jsonify(Error="Method not allowed."), 405

# {
#     "sport_id":1,
#     "season_year":2020
# }
@app.route("/results/basketball/season/all_athletes_aggregate/", methods = ['GET'])
def basketballAggregateAllAthleteStatistics():
    json = request.json
    handler = BasketballEventHandler()
    if request.method == 'GET':
        #Validate GET requests
        if ('sport_id' not in json or 'season_year' not in json):
            return jsonify(Error='Bad Request'),400
        #Carry on with request
        return handler.getAllAggregatedAthleteStatisticsPerSeason(json['sport_id'], json['season_year'])
    else:
        return jsonify(Error="Method not allowed."), 405

# {
#     "sport_id":1,
#     "season_year":2020
# }
@app.route("/results/basketball/season/team_aggregate/", methods = ['GET'])
def basketballAggregateTeamStatistics():
    json = request.json
    handler = BasketballEventHandler()
    if request.method == 'GET':
        #Validate GET requests
        if ('sport_id' not in json or 'season_year' not in json):
            return jsonify(Error='Bad Request'),400
        #Carry on with request
        return handler.getAggregatedTeamStatisticsPerSeason(json['sport_id'], json['season_year'])
    else:
        return jsonify(Error="Method not allowed."), 405

#===================================================================================
#===================//END BASKETBALL RESULTS ROUTES//===============================
#===================================================================================
#--------- PBP Routes ---------#
@app.route("/pbp", methods=['POST', 'DELETE'])
def pbp_sequence():

    body = request.get_json()
    if len(body) != 1 or "event_id" not in body:
        return jsonify("Bad request. ")

    handler = VolleyballPBPHandler()
    event_id = body["event_id"]
    if request.method == 'POST':
        return handler.startPBPSequence(event_id)

    return handler.removePBPSequence(event_id)


@app.route("/pbp/color", methods=['POST', 'PUT'])
def pbp_set_color():
    body = request.get_json()
    if len(body) == 2 and "color" in body and "event_id" in body:
        return VolleyballPBPHandler().setOpponentColor(body["event_id"], body["color"])

    return jsonify(ERROR="Bad request, client must pass both event id and color within request body."), 400


@app.route("/pbp/roster", methods=['POST', 'PUT', 'DELETE'])
def pbp_roster():
    # ADD, REMOVE & EDIT TEAM ROSTERS FOR A PBP SEQUENCE
    body = request.get_json()

    # Validate team is given within request body.
    if not "team" in body or not "event_id" in body:
        return jsonify(ERROR="Bad request. Values for team and event id must be included in request body."), 400

    handler = VolleyballPBPHandler()
    team = body["team"]
    event_id = body["event_id"]

    if request.method == 'POST' or request.method == 'PUT':
        # Validate data is present in body.
        if len(body) != 3 or not "data" in body:
            return jsonify(ERROR="Bad request. Values for team, event id, and data must be included in request body."), 400

        data = body["data"]
        if team == "uprm":
            return handler.setUPRMPlayer(event_id, data)

        if team == "opponent":
            return handler.setOppPlayer(event_id, data)

        # Team not recognized.
        return jsonify(ERROR="Bad request. Team value invalid."), 400

    # Validate athlete id is given.
    if len(body) != 3 or "athlete_id" not in body:
        return jsonify(ERROR="Bad request. Values for team, event id, and athlete id must be provided."), 400

    athlete_id = body["athlete_id"]

    if team == "uprm":
        return handler.removeUPRMPlayer(event_id, athlete_id)

    if team == "opponent":
        return handler.removeOppPlayer(event_id, athlete_id)

    # Team not recognized.
    return jsonify(ERROR="Bad request. Team value invalid."), 400


@app.route("/pbp/actions", methods=['POST', 'PUT', 'DELETE'])
def pbp_actions():
    # ADD, REMOVE & EDIT GAME ACTIONS FOR A PBP SEQUENCE
    body = request.get_json()

    # Validate event id is present in body.
    if "event_id" not in body:
        return jsonify(ERROR="Bad request. Not event id found."), 400

    event_id = body["event_id"]
    handler = VolleyballPBPHandler()
    if request.method == 'POST':
        # Validate action data is present in request body.
        if len(body) != 2 or "data" not in body:
            return jsonify(ERROR="Bad request. Must send both event id and data within request body."), 400

        return handler.addPBPAction(event_id, body["data"])

    if request.method == 'PUT':
        # Validate data and action id are present in request body.
        if len(body) != 3 or "data" not in body or "action_id" not in body:
            return jsonify(ERROR="Bad request. Must send both event id and data within request body."), 400

        return handler.editPBPAction(event_id, body["action_id"], body["data"])

    # For delete, validate action id is present in body.
    if len(body) != 2 or "action_id" not in body:
        return jsonify(ERROR="Bad request. Must send both event id and action id within request body."), 400

    return handler.removePlayPBPAction(event_id, body["action_id"])


@app.route("/pbp/end", methods=['POST'])
def pbp_end():
    body = request.get_json()
    if len(body) == 1 and "event_id" in body:
        return VolleyballPBPHandler().setPBPSequenceOver(body["event_id"])

    return jsonify(ERROR="Bad request, client must pass event_id only, within the body."), 400

# ===================================================================================
# =======================//VOLLEYBALL RESULTS ROUTES//===============================
# ===================================================================================

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
#   "opponent_score": 0
# }
@app.route("/results/volleyball/", methods = ['GET','POST'])
def volleyballStatistics():
    json = request.json
    handler = VolleyballEventHandler()
    if request.method == 'GET':
        #Validate Request for GET
        if 'event_id' not in json:
            return jsonify(Error='Bad Request'), 400
        return handler.getAllStatisticsByEventID(json['event_id'])
    if request.method == 'POST':
        #Validate General IDs for POST
        if ('event_id' not in json or 'team_statistics' not in json or 'athlete_statistics'
        not in json or 'uprm_score' not in json or 'opponent_score' not in json):
            return jsonify(Error='Bad Request'), 400
        #Validate Team Statistics Request
        team_statistics = json['team_statistics']
        if ('volleyball_statistics' not in team_statistics):
            return jsonify(Error='Bad Request'),400
        specific_stats = team_statistics['volleyball_statistics']
        if ('kill_points' not in specific_stats or 'attack_errors' not in specific_stats or 'assists' not in specific_stats 
            or 'aces' not in specific_stats or 'service_errors' not in specific_stats or 'digs' not in specific_stats 
            or 'blocks' not in specific_stats or 'blocking_errors' not in specific_stats or 'reception_errors' not in specific_stats):
                return jsonify(Error='Bad Request'),400
        #Validate Each Athlete's Statistics Request
        athlete_statistics = json['athlete_statistics']
        for athlete_json in athlete_statistics:
            if ('statistics' not in athlete_json or 'athlete_id' not in athlete_json):
                return jsonify(Error='Bad Request'),400
            athlete_json_sport = athlete_json['statistics']
            if ('volleyball_statistics' not in athlete_json_sport):
                return jsonify(Error='Bad Request'),400
            specific_stats = athlete_json_sport['volleyball_statistics']
            if ('kill_points' not in specific_stats or 'attack_errors' not in specific_stats or 'assists' not in specific_stats 
            or 'aces' not in specific_stats or 'service_errors' not in specific_stats or 'digs' not in specific_stats 
            or 'blocks' not in specific_stats or 'blocking_errors' not in specific_stats or 'reception_errors' not in specific_stats):
                return jsonify(Error='Bad Request'),400
        return handler.addAllEventStatistics(json['event_id'], json)
        # return jsonify(json),200
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
@app.route("/results/volleyball/individual/", methods = ['GET','POST','PUT','DELETE'])
def volleyballAthleteStatistics():
    json = request.json
    handler = VolleyballEventHandler()
    if request.method == 'GET' or request.method == 'DELETE':
        #Validate GET/REMOVE requests
        if ('event_id' not in json or 'athlete_id' not in json):
            return jsonify(Error='Bad Request'),400
        #Carry on with request
        if request.method == 'GET':
            return handler.getAllAthleteStatisticsByEventId(json['event_id'], json['athlete_id'])
        if request.method == 'DELETE':
            return handler.removeStatistics(json['event_id'], json['athlete_id'])
    if request.method == 'POST' or request.method == 'PUT':
        #Validate POST/PUT Requests
        #Validate Basic IDs
        if ('event_id' not in json or 'athlete_id' not in json or 'attributes' not in json):
            return jsonify(Error='Bad Request'),400
        #Validate Specific Statistics
        specific_stats = json['attributes']
        if ('kill_points' not in specific_stats or 'attack_errors' not in specific_stats or 'assists' not in specific_stats 
            or 'aces' not in specific_stats or 'service_errors' not in specific_stats or 'digs' not in specific_stats 
            or 'blocks' not in specific_stats or 'blocking_errors' not in specific_stats or 'reception_errors' not in specific_stats):
                return jsonify(Error='Bad Request'),400
        #Carry On With Request
        if request.method == 'POST':
            return handler.addStatistics(json['event_id'], json['athlete_id'], json['attributes'])
        if request.method == 'PUT':
            returnable = handler.editStatistics(
                json['event_id'], json['athlete_id'], json['attributes'])
        return returnable
    
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
@app.route("/results/volleyball/team/", methods = ['GET','POST','PUT','DELETE'])
def volleyballTeamStatistics():
    json = request.json
    handler = VolleyballEventHandler()
    if request.method == 'GET' or request.method == 'DELETE' or request.method == 'PUT':
        #Validate GET/REMOVE/PUT requests
        if ('event_id' not in json):
            return jsonify(Error='Bad Request'),400
        #Carry on with request
        if request.method == 'GET':
            return handler.getAllTeamStatisticsByEventId(json['event_id'])
        if request.method == 'PUT':
            return handler.editTeamStatistics(json['event_id'])
        if request.method == 'DELETE':
            return handler.removeTeamStatistics(json['event_id'])
    if request.method == 'POST':
        #Validate POST Requests
        #Validate Basic IDs
        if ('event_id' not in json or 'add_type' not in json or 'attributes' not in json):
            return jsonify(Error='Bad Request'),400
        #Validate Specific Statistics
        specific_stats = json['attributes']
        if ('kill_points' not in specific_stats or 'attack_errors' not in specific_stats or 'assists' not in specific_stats 
            or 'aces' not in specific_stats or 'service_errors' not in specific_stats or 'digs' not in specific_stats 
            or 'blocks' not in specific_stats or 'blocking_errors' not in specific_stats or 'reception_errors' not in specific_stats):
                return jsonify(Error='Bad Request'),400
        if json['add_type'] == 'AUTO':
            return handler.addTeamStatisticsAuto(json['event_id'])
        if json['add_type'] == 'MANUAL':
            return handler.addTeamStatistics(json['event_id'], json['attributes'])
        else:
            return jsonify(Error="Method not allowed, Must specify valid add_type"), 405
    else:
        return jsonify(Error="Method not allowed."), 405

# FORMAT FOR REQUEST:
# { "event_id":3,
#   "attributes":
#   {
#   "uprm_score":2, "opponent_score":2
#   }
# }
@app.route("/results/volleyball/score/", methods = ['GET','POST','PUT','DELETE'])
def volleyballFinalScores():
    json = request.json
    handler = VolleyballEventHandler()
    if request.method == 'GET' or request.method == 'DELETE':
        #Validate GET/REMOVE requests
        if ('event_id' not in json):
            return jsonify(Error='Bad Request'),400
        #Carry on with request
        if request.method == 'GET':
            return handler.getFinalScore(json['event_id'])
        if request.method == 'DELETE':
            return handler.removeFinalScore(json['event_id'])
    if request.method == 'POST' or request.method == 'PUT':
        #Validate POST/PUT Requests
        #Validate Basic IDs
        if ('event_id' not in json or 'attributes' not in json):
            return jsonify(Error='Bad Request'),400
        #Validate Specific Statistics
        specific_stats = json['attributes']
        if ('uprm_score' not in specific_stats or 'opponent_score' not in specific_stats):
                return jsonify(Error='Bad Request'),400
        #Carry On With Request
        if request.method == 'POST':
            return handler.addFinalScore(json['event_id'], json['attributes'])
        if request.method == 'PUT':
            return handler.editFinalScore(json['event_id'], json['attributes'])
    else:
        return jsonify(Error="Method not allowed."), 405

# {
#     "athlete_id":1,
#     "season_year":2020
# }
#TODO: (Herbert) need to prepare a request schema for this one. just aid and seasonYear
@app.route("/results/volleyball/season/athlete_games/", methods = ['GET'])
def volleyballSeasonAthleteStatistics():
    json = request.json
    handler = VolleyballEventHandler()
    if request.method == 'GET':
        #Validate GET requests
        if ('athlete_id' not in json or 'season_year' not in json):
            return jsonify(Error='Bad Request'),400
        #Carry on with request
        return handler.getAllAthleteStatisticsPerSeason(json['athlete_id'], json['season_year'])
    else:
        return jsonify(Error="Method not allowed."), 405


# {
#     "athlete_id":1,
#     "season_year":2020
# }
@app.route("/results/volleyball/season/athlete_aggregate/", methods = ['GET'])
def volleyballAggregateAthleteStatistics():
    json = request.json
    handler = VolleyballEventHandler()
    if request.method == 'GET':
        #Validate GET requests
        if ('athlete_id' not in json or 'season_year' not in json):
            return jsonify(Error='Bad Request'),400
        #Carry on with request
        return handler.getAggregatedAthleteStatisticsPerSeason(json['athlete_id'], json['season_year'])
    else:
        return jsonify(Error="Method not allowed."), 405

# {
#     "sport_id":1,
#     "season_year":2020
# }
@app.route("/results/volleyball/season/all_athletes_aggregate/", methods = ['GET'])
def volleyballAggregateAllAthleteStatistics():
    json = request.json
    handler = VolleyballEventHandler()
    if request.method == 'GET':
        #Validate GET requests
        if ('sport_id' not in json or 'season_year' not in json):
            return jsonify(Error='Bad Request'),400
        #Carry on with request
        return handler.getAllAggregatedAthleteStatisticsPerSeason(json['sport_id'], json['season_year'])
    else:
        return jsonify(Error="Method not allowed."), 405

# {
#     "sport_id":1,
#     "season_year":2020
# }
@app.route("/results/volleyball/season/team_aggregate/", methods = ['GET'])
def volleyballAggregateTeamStatistics():
    json = request.json
    handler = VolleyballEventHandler()
    if request.method == 'GET':
        #Validate GET requests
        if ('sport_id' not in json or 'season_year' not in json):
            return jsonify(Error='Bad Request'),400
        #Carry on with request
        return handler.getAggregatedTeamStatisticsPerSeason(json['sport_id'], json['season_year'])
    else:
        return jsonify(Error="Method not allowed."), 405

# ===================================================================================
# ===================//END VOLLEYBALL RESULTS ROUTES//===============================
# ===================================================================================


# ===================================================================================
# =======================//SOCCER RESULTS ROUTES//===============================
# ===================================================================================

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
#   "opponent_score": 0
# }
@app.route("/results/soccer/", methods = ['GET','POST'])
def soccerStatistics():
    json = request.json
    handler = SoccerEventHandler()
    if request.method == 'GET':
        #Validate Request for GET
        if 'event_id' not in json:
            return jsonify(Error='Bad Request'), 400
        return handler.getAllStatisticsByEventID(json['event_id'])
    if request.method == 'POST':
        #Validate General IDs for POST
        if ('event_id' not in json or 'team_statistics' not in json or 'athlete_statistics'
        not in json or 'uprm_score' not in json or 'opponent_score' not in json):
            return jsonify(Error='Bad Request'), 400
        #Validate Team Statistics Request
        team_statistics = json['team_statistics']
        if ('soccer_statistics' not in team_statistics):
            return jsonify(Error='Bad Request'),400
        specific_stats = team_statistics['soccer_statistics']
        if ('goal_attempts' not in specific_stats or 'assists' not in specific_stats or 'fouls' not in specific_stats 
            or 'cards' not in specific_stats or 'successful_goals' not in specific_stats or 'tackles' not in specific_stats):
            return jsonify(Error='Bad Request'),400
        #Validate Each Athlete's Statistics Request
        athlete_statistics = json['athlete_statistics']
        for athlete_json in athlete_statistics:
            if ('statistics' not in athlete_json or 'athlete_id' not in athlete_json):
                return jsonify(Error='Bad Request'),400
            athlete_json_sport = athlete_json['statistics']
            if ('soccer_statistics' not in athlete_json_sport):
                return jsonify(Error='Bad Request'),400
            specific_stats = athlete_json_sport['soccer_statistics']
            if ('goal_attempts' not in specific_stats or 'assists' not in specific_stats or 'fouls' not in specific_stats 
                or 'cards' not in specific_stats or 'successful_goals' not in specific_stats or 'tackles' not in specific_stats):
                return jsonify(Error='Bad Request'),400
        return handler.addAllEventStatistics(json['event_id'], json)
        # return jsonify(json),200
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
@app.route("/results/soccer/individual/", methods = ['GET','POST','PUT','DELETE'])
def soccerAthleteStatistics():
    json = request.json
    handler = SoccerEventHandler()
    if request.method == 'GET' or request.method == 'DELETE':
        #Validate GET/REMOVE requests
        if ('event_id' not in json or 'athlete_id' not in json):
            return jsonify(Error='Bad Request'),400
        #Carry on with request
        if request.method == 'GET':
            return handler.getAllAthleteStatisticsByEventId(json['event_id'], json['athlete_id'])
        if request.method == 'DELETE':
            return handler.removeStatistics(json['event_id'], json['athlete_id'])
    if request.method == 'POST' or request.method == 'PUT':
        #Validate POST/PUT Requests
        #Validate Basic IDs
        if ('event_id' not in json or 'athlete_id' not in json or 'attributes' not in json):
            return jsonify(Error='Bad Request'),400
        #Validate Specific Statistics
        specific_stats = json['attributes']
        if ('goal_attempts' not in specific_stats or 'assists' not in specific_stats or 'fouls' not in specific_stats 
                or 'cards' not in specific_stats or 'successful_goals' not in specific_stats or 'tackles' not in specific_stats):
                return jsonify(Error='Bad Request'),400
        if request.method == 'POST':
            return handler.addStatistics(json['event_id'], json['athlete_id'], json['attributes'])
        if request.method == 'PUT':
            returnable = handler.editStatistics(
                json['event_id'], json['athlete_id'], json['attributes'])
            return returnable
    
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
@app.route("/results/soccer/team/", methods = ['GET','POST','PUT','DELETE'])
def soccerTeamStatistics():
    json = request.json
    handler = SoccerEventHandler()
    if request.method == 'GET' or request.method == 'DELETE' or request.method == 'PUT':
        #Validate GET/REMOVE/PUT requests
        if ('event_id' not in json):
            return jsonify(Error='Bad Request'),400
        #Carry on with request
        if request.method == 'GET':
            return handler.getAllTeamStatisticsByEventId(json['event_id'])
        if request.method == 'PUT':
            return handler.editTeamStatistics(json['event_id'])
        if request.method == 'DELETE':
            return handler.removeTeamStatistics(json['event_id'])
    if request.method == 'POST':
        #Validate POST Requests
        #Validate Basic IDs
        if ('event_id' not in json or 'add_type' not in json or 'attributes' not in json):
            return jsonify(Error='Bad Request'),400
        #Validate Specific Statistics
        specific_stats = json['attributes']
        if ('goal_attempts' not in specific_stats or 'assists' not in specific_stats or 'fouls' not in specific_stats 
                or 'cards' not in specific_stats or 'successful_goals' not in specific_stats or 'tackles' not in specific_stats):
                return jsonify(Error='Bad Request'),400
        #Carry On With Request
        if json['add_type'] == 'AUTO':
            return handler.addTeamStatisticsAuto(json['event_id'])
        if json['add_type'] == 'MANUAL':
            return handler.addTeamStatistics(json['event_id'], json['attributes'])
        else:
            return jsonify(Error="Method not allowed, Must specify valid add_type"), 405
    else:
        return jsonify(Error="Method not allowed."), 405

# FORMAT FOR REQUEST:
# { "event_id":3,
#   "attributes":
#   {
#   "uprm_score":2, "opponent_score":2
#   }
# }
@app.route("/results/soccer/score/", methods = ['GET','POST','PUT','DELETE'])
def soccerFinalScores():
    json = request.json
    handler = SoccerEventHandler()
    if request.method == 'GET' or request.method == 'DELETE':
        #Validate GET/REMOVE requests
        if ('event_id' not in json):
            return jsonify(Error='Bad Request'),400
        #Carry on with request
        if request.method == 'GET':
            return handler.getFinalScore(json['event_id'])
        if request.method == 'DELETE':
            return handler.removeFinalScore(json['event_id'])
    if request.method == 'POST' or request.method == 'PUT':
        #Validate POST/PUT Requests
        #Validate Basic IDs
        if ('event_id' not in json or 'attributes' not in json):
            return jsonify(Error='Bad Request'),400
        #Validate Specific Statistics
        specific_stats = json['attributes']
        if ('uprm_score' not in specific_stats or 'opponent_score' not in specific_stats):
                return jsonify(Error='Bad Request'),400
        #Carry On With Request
        if request.method == 'POST':
            return handler.addFinalScore(json['event_id'], json['attributes'])
        if request.method == 'PUT':
            return handler.editFinalScore(json['event_id'], json['attributes'])
    else:
        return jsonify(Error="Method not allowed."), 405
# {
#     "athlete_id":1,
#     "season_year":2020
# }
#TODO: (Herbert) need to prepare a request schema for this one. just aid and seasonYear
@app.route("/results/soccer/season/athlete_games/", methods = ['GET'])
def soccerSeasonAthleteStatistics():
    json = request.json
    handler = SoccerEventHandler()
    if request.method == 'GET':
        #Validate GET requests
        if ('athlete_id' not in json or 'season_year' not in json):
            return jsonify(Error='Bad Request'),400
        #Carry on with request
        return handler.getAllAthleteStatisticsPerSeason(json['athlete_id'], json['season_year'])
    else:
        return jsonify(Error="Method not allowed."), 405

# {
#     "athlete_id":1,
#     "season_year":2020
# }
@app.route("/results/soccer/season/athlete_aggregate/", methods = ['GET'])
def soccerAggregateAthleteStatistics():
    json = request.json
    handler = SoccerEventHandler()
    if request.method == 'GET':
        #Validate GET requests
        if ('athlete_id' not in json or 'season_year' not in json):
            return jsonify(Error='Bad Request'),400
        #Carry on with request
        return handler.getAggregatedAthleteStatisticsPerSeason(json['athlete_id'], json['season_year'])
    else:
        return jsonify(Error="Method not allowed."), 405

# {
#     "sport_id":1,
#     "season_year":2020
# }
@app.route("/results/soccer/season/all_athletes_aggregate/", methods = ['GET'])
def soccerAggregateAllAthleteStatistics():
    json = request.json
    handler = SoccerEventHandler()
    if request.method == 'GET':
        #Validate GET requests
        if ('sport_id' not in json or 'season_year' not in json):
            return jsonify(Error='Bad Request'),400
        #Carry on with request
        return handler.getAllAggregatedAthleteStatisticsPerSeason(json['sport_id'], json['season_year'])
    else:
        return jsonify(Error="Method not allowed."), 405

# {
#     "sport_id":1,
#     "season_year":2020
# }
@app.route("/results/soccer/season/team_aggregate/", methods = ['GET'])
def soccerAggregateTeamStatistics():
    json = request.json
    handler = SoccerEventHandler()
    if request.method == 'GET':
        #Validate GET requests
        if ('sport_id' not in json or 'season_year' not in json):
            return jsonify(Error='Bad Request'),400
        #Carry on with request
        return handler.getAggregatedTeamStatisticsPerSeason(json['sport_id'], json['season_year'])
    else:
        return jsonify(Error="Method not allowed."), 405


# ===================================================================================
# ===================//END SOCCER RESULTS ROUTES//===============================
# ===================================================================================

# ===================================================================================
# =======================//BASEBALL RESULTS ROUTES//===============================
# ===================================================================================

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
#   "opponent_score": 0
# }
@app.route("/results/baseball/", methods = ['GET','POST'])
def baseballStatistics():
    json = request.json
    handler = BaseballEventHandler()
    if request.method == 'GET':
        #Validate Request for GET
        if 'event_id' not in json:
            return jsonify(Error='Bad Request'), 400
        return handler.getAllStatisticsByEventID(json['event_id'])
    if request.method == 'POST':
        #Validate General IDs for POST
        if ('event_id' not in json or 'team_statistics' not in json or 'athlete_statistics'
        not in json or 'uprm_score' not in json or 'opponent_score' not in json):
            return jsonify(Error='Bad Request'), 400
        #Validate Team Statistics Request
        team_statistics = json['team_statistics']
        if ('baseball_statistics' not in team_statistics):
            return jsonify(Error='Bad Request'),400
        specific_stats = team_statistics['baseball_statistics']
        if ('at_bats' not in specific_stats or 'runs' not in specific_stats or 'hits' not in specific_stats 
            or 'runs_batted_in' not in specific_stats or 'base_on_balls' not in specific_stats or 'strikeouts' not in specific_stats 
            or 'left_on_base' not in specific_stats):
                return jsonify(Error='Bad Request'),400
        #Validate Each Athlete's Statistics Request
        athlete_statistics = json['athlete_statistics']
        for athlete_json in athlete_statistics:
            if ('statistics' not in athlete_json or 'athlete_id' not in athlete_json):
                return jsonify(Error='Bad Request'),400
            athlete_json_sport = athlete_json['statistics']
            if ('baseball_statistics' not in athlete_json_sport):
                return jsonify(Error='Bad Request'),400
            specific_stats = athlete_json_sport['baseball_statistics']
            if ('at_bats' not in specific_stats or 'runs' not in specific_stats or 'hits' not in specific_stats 
            or 'runs_batted_in' not in specific_stats or 'base_on_balls' not in specific_stats or 'strikeouts' not in specific_stats 
            or 'left_on_base' not in specific_stats):
                return jsonify(Error='Bad Request'),400
        return handler.addAllEventStatistics(json['event_id'], json)
        # return jsonify(json),200
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
@app.route("/results/baseball/individual/", methods = ['GET','POST','PUT','DELETE'])
def baseballAthleteStatistics():
    json = request.json
    handler = BaseballEventHandler()
    if request.method == 'GET' or request.method == 'DELETE':
        #Validate GET/REMOVE requests
        if ('event_id' not in json or 'athlete_id' not in json):
            return jsonify(Error='Bad Request'),400
        #Carry on with request
        if request.method == 'GET':
            return handler.getAllAthleteStatisticsByEventId(json['event_id'], json['athlete_id'])
        if request.method == 'DELETE':
            return handler.removeStatistics(json['event_id'], json['athlete_id'])
    if request.method == 'POST' or request.method == 'PUT':
        #Validate POST/PUT Requests
        #Validate Basic IDs
        if ('event_id' not in json or 'athlete_id' not in json or 'attributes' not in json):
            return jsonify(Error='Bad Request'),400
        #Validate Specific Statistics
        specific_stats = json['attributes']
        if ('at_bats' not in specific_stats or 'runs' not in specific_stats or 'hits' not in specific_stats 
            or 'runs_batted_in' not in specific_stats or 'base_on_balls' not in specific_stats or 'strikeouts' not in specific_stats 
            or 'left_on_base' not in specific_stats):
                return jsonify(Error='Bad Request'),400
        #Carry On With Request
        if request.method == 'POST':
            return handler.addStatistics(json['event_id'], json['athlete_id'], json['attributes'])
        if request.method == 'PUT':
            returnable = handler.editStatistics(
                json['event_id'], json['athlete_id'], json['attributes'])
            return returnable
    
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
@app.route("/results/baseball/team/", methods = ['GET','POST','PUT','DELETE'])
def baseballTeamStatistics():
    json = request.json
    handler = BaseballEventHandler()
    if request.method == 'GET' or request.method == 'DELETE' or request.method == 'PUT':
        #Validate GET/REMOVE/PUT requests
        if ('event_id' not in json):
            return jsonify(Error='Bad Request'),400
        #Carry on with request
        if request.method == 'GET':
            return handler.getAllTeamStatisticsByEventId(json['event_id'])
        if request.method == 'PUT':
            return handler.editTeamStatistics(json['event_id'])
        if request.method == 'DELETE':
            return handler.removeTeamStatistics(json['event_id'])
    if request.method == 'POST':
        #Validate POST Requests
        #Validate Basic IDs
        if ('event_id' not in json or 'add_type' not in json or 'attributes' not in json):
            return jsonify(Error='Bad Request'),400
        #Validate Specific Statistics
        specific_stats = json['attributes']
        if ('at_bats' not in specific_stats or 'runs' not in specific_stats or 'hits' not in specific_stats 
            or 'runs_batted_in' not in specific_stats or 'base_on_balls' not in specific_stats or 'strikeouts' not in specific_stats 
            or 'left_on_base' not in specific_stats):
                return jsonify(Error='Bad Request'),400
        if json['add_type'] == 'AUTO':
            return handler.addTeamStatisticsAuto(json['event_id'])
        if json['add_type'] == 'MANUAL':
            return handler.addTeamStatistics(json['event_id'], json['attributes'])
        else:
            return jsonify(Error="Method not allowed, Must specify valid add_type"), 405
    else:
        return jsonify(Error="Method not allowed."), 405

# FORMAT FOR REQUEST:
# { "event_id":3,
#   "attributes":
#   {
#   "uprm_score":2, "opponent_score":2
#   }
# }
@app.route("/results/baseball/score/", methods = ['GET','POST','PUT','DELETE'])
def baseballFinalScores():
    json = request.json
    handler = BaseballEventHandler()
    if request.method == 'GET' or request.method == 'DELETE':
        #Validate GET/REMOVE requests
        if ('event_id' not in json):
            return jsonify(Error='Bad Request'),400
        #Carry on with request
        if request.method == 'GET':
            return handler.getFinalScore(json['event_id'])
        if request.method == 'DELETE':
            return handler.removeFinalScore(json['event_id'])
    if request.method == 'POST' or request.method == 'PUT':
        #Validate POST/PUT Requests
        #Validate Basic IDs
        if ('event_id' not in json or 'attributes' not in json):
            return jsonify(Error='Bad Request'),400
        #Validate Specific Statistics
        specific_stats = json['attributes']
        if ('uprm_score' not in specific_stats or 'opponent_score' not in specific_stats):
                return jsonify(Error='Bad Request'),400
        #Carry On With Request
        if request.method == 'POST':
            return handler.addFinalScore(json['event_id'], json['attributes'])
        if request.method == 'PUT':
            return handler.editFinalScore(json['event_id'], json['attributes'])
    else:
        return jsonify(Error="Method not allowed."), 405

# {
#     "athlete_id":1,
#     "season_year":2020
# }
#TODO: (Herbert) need to prepare a request schema for this one. just aid and seasonYear
@app.route("/results/baseball/season/athlete_games/", methods = ['GET'])
def baseballSeasonAthleteStatistics():
    json = request.json
    handler = BaseballEventHandler()
    if request.method == 'GET':
        #Validate GET requests
        if ('athlete_id' not in json or 'season_year' not in json):
            return jsonify(Error='Bad Request'),400
        #Carry on with request
        return handler.getAllAthleteStatisticsPerSeason(json['athlete_id'], json['season_year'])
    else:
        return jsonify(Error="Method not allowed."), 405



# {
#     "athlete_id":1,
#     "season_year":2020
# }
@app.route("/results/baseball/season/athlete_aggregate/", methods = ['GET'])
def baseballAggregateAthleteStatistics():
    json = request.json
    handler = BaseballEventHandler()
    if request.method == 'GET':
        #Validate GET requests
        if ('athlete_id' not in json or 'season_year' not in json):
            return jsonify(Error='Bad Request'),400
        #Carry on with request
        return handler.getAggregatedAthleteStatisticsPerSeason(json['athlete_id'], json['season_year'])
    else:
        return jsonify(Error="Method not allowed."), 405

# {
#     "sport_id":1,
#     "season_year":2020
# }
@app.route("/results/baseball/season/all_athletes_aggregate/", methods = ['GET'])
def baseballAggregateAllAthleteStatistics():
    json = request.json
    handler = BaseballEventHandler()
    if request.method == 'GET':
        #Validate GET requests
        if ('sport_id' not in json or 'season_year' not in json):
            return jsonify(Error='Bad Request'),400
        #Carry on with request
        return handler.getAllAggregatedAthleteStatisticsPerSeason(json['sport_id'], json['season_year'])
    else:
        return jsonify(Error="Method not allowed."), 405

# {
#     "sport_id":1,
#     "season_year":2020
# }
@app.route("/results/baseball/season/team_aggregate/", methods = ['GET'])
def baseballAggregateTeamStatistics():
    json = request.json
    handler = BaseballEventHandler()
    if request.method == 'GET':
        #Validate GET requests
        if ('sport_id' not in json or 'season_year' not in json):
            return jsonify(Error='Bad Request'),400
        #Carry on with request
        return handler.getAggregatedTeamStatisticsPerSeason(json['sport_id'], json['season_year'])
    else:
        return jsonify(Error="Method not allowed."), 405


# ===================================================================================
# ===================//END BASEBALL RESULTS ROUTES//===============================
# ===================================================================================

# Launch app.
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


#===================================================================================
#===================//START TEAM RESULTS ROUTES//===================================
#===================================================================================
# {
# "sport_id":1,
# "season_year":"2020",
# "team_image_url":"www.google.com"
# }
@app.route("/teams/", methods = ['GET','POST','PUT','DELETE'])
def teamByYear():
    json = request.json
    handler = TeamHandler()
    if request.method == 'GET':
        return handler.getTeamByYear(json['sport_id'],json['season_year'])
    if request.method == 'POST':
        return handler.addTeam(json['sport_id'],json['season_year'],json['team_image_url'])
    if request.method == 'PUT':
        return handler.editTeamByYear(json['sport_id'],json['season_year'],json['team_image_url'])
    if request.method == 'DELETE':
        return handler.removeTeamByYear(json['sport_id'],json['season_year'])
    else:
        return jsonify(Error="Method not allowed."), 405


# {
# "team_id":1,
# "team_members":[
#     { 
#         "athlete_id":1
#     },
#     {
#         "athlete_id":2
#     }
#     ]
# }
@app.route("/teams/members/", methods = ['GET','POST'])
def teamMembers():
    json = request.json
    handler = TeamHandler()
    if request.method == 'GET':
        return handler.getTeamMembersByID(json['team_id'])
    if request.method == 'POST':
        return handler.addTeamMembers(json['team_id'],json['team_members'])
    else:
        return jsonify(Error="Method not allowed."), 405


# {
#     "team_id":1,
#     "athlete_id":1
# }
#TODO: (Herbert) Check if need to remove route due to redundancy, wait for front end 
@app.route("/teams/member/", methods = ['GET','POST','DELETE'])
def teamMemberByIDs():
    json = request.json
    handler = TeamHandler()
    if request.method == 'GET':
        return handler.getTeamMemberByIDs(json['athlete_id'],json['team_id'])
    if request.method == 'POST':
        return handler.addTeamMember(json['athlete_id'],json['team_id'])
    if request.method == 'DELETE':
        return handler.removeTeamMember(json['athlete_id'],json['team_id'])
    else:
        return jsonify(Error="Method not allowed."), 405

#===================================================================================
#===================//END TEAM RESULTS ROUTES//=====================================
#===================================================================================


# Launch app.
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')