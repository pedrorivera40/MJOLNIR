from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import datetime
from handler.user import UserHandler
from handler.athlete import AthleteHandler
from auth import verifyHash, generateToken, verifyToken, getTokenInfo
from customSession import CustomSession
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
from handler.match_based_event import MatchBasedEventHandler
from handler.team import TeamHandler
from handler.event_result import EventResultHandler
from handler.medal_based_event import MedalBasedEventHandler


# Load environment variables
load_dotenv()


app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')
customSession = CustomSession()
CORS(app)


def token_check(func):
    """
    Midleware to verify the request is authorized.

    Midleware function used to protect routes from unauthorized request
    by verifying each request provides a valid token.
    """
    @wraps(func)
    def decorated(*args, **kwargs):

        if request.headers.get('Authorization') == None:
            return jsonify(Error='Token is missing'), 403

        # Extract token from auth header.
        token = request.headers.get('Authorization').split(' ')[1]

        if not token:
            return jsonify(Error='Token is missing'), 403

        if not verifyToken(token):
            return jsonify(Error="Token is invalid"), 403
        else:
            return func(*args, **kwargs)
    return decorated


def extractUserInfoFormToken():
    token = request.headers.get('Authorization').split(' ')[1]
    return getTokenInfo(token)

def validateRequestPermissions(token, permissionNumber):
    def switch(permissionNumber):
        return {
            '13': 0,
            '14': 1,
            '15': 2,
            '16': 3,
            '17': 4,
            '18': 5,
            '19': 6,
            '20': 7,
            '21': 8,
            '22': 9,
            '23': 10,
            '24': 11,
            '25': 12,
            '26': 13,
            '27': 14,
        }[permissionNumber]
    index = switch(permissionNumber)
    print('index',index)
    print('Permission Number',permissionNumber)
    print('All permissions',token['permissions'])
    print('Permissions being checked',token['permissions'][index][permissionNumber])
    print('Permission check',token['permissions'][index][permissionNumber]==False)
    return(token['permissions'][index][permissionNumber]==False)

#--------- Athlete Routes ---------#
@app.route("/athletes/", methods=['GET', 'POST'])
def athletes():
    handler = AthleteHandler()
    if request.method == 'POST':
        json = request.json
        if not 'sID' in json or not 'attributes' in json:
            return jsonify(Error="Argumentos dados son incorrectos."), 400

        return handler.addAthlete(json['sID'], json['attributes'])

    elif request.method == 'GET':
        json = request.args
        if not json:
            return handler.getAllAthletes()

        if not 'sID' in json or not 'tID' in json:
            return jsonify(Error="Argumentos dados son incorrectos."), 400

        return handler.getAthletesBySportAndNotInTeam(json['sID'], json['tID'])

@app.route("/athletes/details/", methods = ['GET'])
def athletesDetailed():
    if request.method == 'GET':
        return AthleteHandler().getAllAthletesDetailed()
    


@app.route("/athletes/<int:aid>/", methods=['GET', 'PUT', 'DELETE'])
def athleteByID(aid):
    handler = AthleteHandler()
    if request.method == 'GET':
        return handler.getAthleteByID(aid)
    elif request.method == 'PUT':
        json = request.json
        if 'attributes' not in json:
            return jsonify(Error="Argumentos dados son incorrectos."), 400

        return handler.editAthlete(aid, json['attributes'])

    elif request.method == 'DELETE':
        return handler.removeAthlete(aid)


###########################################
#--------- Authentication Routes ---------#
###########################################
@app.route("/auth/", methods=['POST'])
def auth():
    if request.json == None:
        return jsonify(Error='Bad Request.'), 400
    if request.method == 'POST':
        handler = UserHandler()
        req = request.json
        if 'username' not in req or 'password' not in req:
            return jsonify(Error='Bad Request.'), 400

        username = req['username']
        password = req['password']  # TODO: AES Encryption
        return handler.login(username, password, customSession)

@app.route("/logout", methods=['POST'])
def logout():
    if request.json == None:
        return jsonify(Error='Bad Request.'), 400
    if request.method == 'POST':
        req = request.json

        username = req['username']
        if(customSession.logout(username)):
            return jsonify(Message='Logout exitoso!'), 200
        return jsonify(Error='Problemas con el logout.'), 400

###########################################
#--------- Dashboard User Routes ---------#
###########################################
@app.route("/users/", methods=['GET', 'POST'])
@token_check
def allUsers():
    token = extractUserInfoFormToken()
    loggedUser = customSession.isLoggedIn(token['user'])
    print(loggedUser)
    if(loggedUser == None):
        return jsonify(Error='Invalid Session'), 401
        
    if(validateRequestPermissions(token,'21') or
    validateRequestPermissions(token,'22') or
    validateRequestPermissions(token,'23')):
        return jsonify(Error='User does not have permissions to acces this resource.'), 403
    handler = UserHandler()
    if request.method == 'GET':
        # For user list display
        return handler.getAllDashUsers()
    if request.method == 'POST':
        if request.json == None:
            return jsonify(Error='Bad Request.'), 400
        req = request.json
        # Check the request contains the right structure.
        if 'username' not in req or 'full_name' not in req or 'email' not in req or 'password' not in req:
            return jsonify(Error='Bad Request.'), 400

        # For account creation
        return handler.addDashUser(req['username'], req['full_name'], req['email'], req['password'])


@app.route("/users/<int:duid>", methods=['GET', 'PATCH'])
# @token_check
def userByID(duid):
    handler = UserHandler()
    req = request.json
    if request.method == 'GET':
        # For managing specific users
        return handler.getDashUserByID(duid)
    if request.method == 'PATCH':
        if request.json == None:
            return jsonify(Error='Bad Request.'), 400
        # For username change
        # Check the request contains the right structure.
        if 'username' not in req or 'full_name' not in req or 'email' not in req or 'is_active' not in req:
            return jsonify(Error='Bad Request.'), 400

        return handler.updateDashUserInfo(duid, req['username'], req['full_name'], req['email'], req['is_active'])


@app.route("/users/username/", methods=['POST'])
# @token_check
def getUserByUsername():
    if request.json == None:
        return jsonify(Error='Bad Request.'), 400
    if request.method == 'POST':
        handler = UserHandler()
        req = request.json
        # Check the request contains the right structure.
        if 'username' not in req:
            return jsonify(Error='Bad Request.'), 400

        return handler.getDashUserByUsername(req['username'])


@app.route("/users/email/", methods=['POST'])
# @token_check
def getUserByEmail():
    if request.json == None:
        return jsonify(Error='Bad Request.'), 400
    if request.method == 'POST':
        handler = UserHandler()
        req = request.json
        # Check the request contains the right structure.
        if 'email' not in req:
            return jsonify(Error='Bad Request.'), 400
        return handler.getDashUserByEmail(req['email'])


@app.route("/users/<int:duid>/reset", methods=['PATCH'])
# @token_check
def passwordReset(duid):
    if request.json == None:
        return jsonify(Error='Bad Request.'), 400
    handler = UserHandler()
    req = request.json
    if request.method == 'PATCH':
        # For password reset
        # Check the request contains the right structure.
        if 'password' not in req:
            return jsonify(Error='Bad Request.'), 400
        return handler.updateDashUserPassword(duid, req['password'])


@app.route("/users/activate", methods=['PATCH'])
def accountUnlock():
    if request.json == None:
        return jsonify(Error='Bad Request.'), 400
    req = request.json
    handler = UserHandler()
    if request.method == 'PATCH':
        # For acount unlock
        # Check the request contains the right structure.
        if 'username' not in req or 'password' not in req or 'new_password' not in req:
            return jsonify(Error='Bad Request.'), 400
        return handler.unlockDashUserAccount(req['username'], req['password'], req['new_password'])


# TODO: id's that are sanwdiwch must be converted to string
@app.route("/users/<string:duid>/toggleActive", methods=['PATCH'])
# @token_check
def toggleActive(duid):
    handler = UserHandler()
    if request.method == 'PATCH':
        return handler.toggleDashUserActive(duid)


# TODO: id's that are sanwdiwch must be converted to string
@app.route("/users/<string:duid>/remove", methods=['PATCH'])
# @token_check
def removeUser(duid):
    handler = UserHandler()
    if request.method == 'PATCH':
        return handler.removeDashUser(duid)


@app.route("/users/<string:duid>/permissions",  methods=['GET', 'PATCH'])
# @token_check
def userPermissions(duid):

    handler = UserHandler()
    if request.method == 'GET':
        return handler.getUserPermissions(duid, 'request')
    if request.method == 'PATCH':
        if request.json == None:
            return jsonify(Error='Bad Request.'), 400
        req = request.json
        # Check the request contains the right structure.
        if 'permissions' not in req:
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
            return jsonify(Error="Argumentos dados son incorrectos."), 400
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
        if not json or 'attributes' not in json:
            return jsonify(Error="Argumentos dados son incorrectos."), 400
        return handler.addEvent(tID, json['attributes'])


#--------- Sports/Categories/Positions Routes ---------#
'''
    TODO ***************************************** TODO
        1. Add routes documentation.
        2. Validate that the format matches with other routes.
        3. Verify if it is necessary to validate request.method=='GET'.
        4. Tests, tests, and more tests...
'''


# ===================================================================================
# =======================//BASKETBALL RESULTS ROUTES//===============================
# ===================================================================================
# TODO: (Herbert) verify route naming/division
# TODO: (Herbert) validate JSON request arguments

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
@app.route("/results/basketball/", methods=['GET', 'POST'])
def basketballStatistics():
    if request.method == 'GET':
        json = request.args
    else:
        json = request.json
    if json is None:
        return jsonify(Error='Bad Request'), 400
    handler = BasketballEventHandler()
    if request.method == 'GET':
        # Validate Request for GET
        if 'event_id' not in json:
            return jsonify(Error='Bad Request'), 400
        event_id = request.args.get('event_id', type=int)
        return handler.getAllStatisticsByEventID(event_id)
    if request.method == 'POST':
        # Validate General IDs for POST
        if ('event_id' not in json or 'team_statistics' not in json or 'athlete_statistics'
                not in json or 'uprm_score' not in json or 'opponent_score' not in json):
            return jsonify(Error='Bad Request'), 400
        # Validate Team Statistics Request
        team_statistics = json['team_statistics']
        if ('basketball_statistics' not in team_statistics):
            return jsonify(Error='Bad Request'), 400
        specific_stats = team_statistics['basketball_statistics']
        if ('points' not in specific_stats or 'rebounds' not in specific_stats or 'assists' not in specific_stats
            or 'steals' not in specific_stats or 'blocks' not in specific_stats or 'turnovers' not in specific_stats
            or 'field_goal_attempt' not in specific_stats or 'successful_field_goal' not in specific_stats
            or 'three_point_attempt' not in specific_stats or 'successful_three_point' not in specific_stats
                or 'free_throw_attempt' not in specific_stats or 'successful_free_throw' not in specific_stats):
            return jsonify(Error='Bad Request'), 400
        # Validate Each Athlete's Statistics Request
        athlete_statistics = json['athlete_statistics']
        for athlete_json in athlete_statistics:
            if ('statistics' not in athlete_json or 'athlete_id' not in athlete_json):
                return jsonify(Error='Bad Request'), 400
            athlete_json_sport = athlete_json['statistics']
            if ('basketball_statistics' not in athlete_json_sport):
                return jsonify(Error='Bad Request'), 400
            specific_stats = athlete_json_sport['basketball_statistics']
            if ('points' not in specific_stats or 'rebounds' not in specific_stats or 'assists' not in specific_stats
                or 'steals' not in specific_stats or 'blocks' not in specific_stats or 'turnovers' not in specific_stats
                or 'field_goal_attempt' not in specific_stats or 'successful_field_goal' not in specific_stats
                or 'three_point_attempt' not in specific_stats or 'successful_three_point' not in specific_stats
                    or 'free_throw_attempt' not in specific_stats or 'successful_free_throw' not in specific_stats):
                return jsonify(Error='Bad Request'), 400

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
@app.route("/results/basketball/individual/", methods=['GET', 'POST', 'PUT', 'DELETE'])
def basketballAthleteStatistics():
    if request.method == 'GET' or request.method == 'DELETE':
        json = request.args
    else:
        json = request.json
    if json is None:
        return jsonify(Error='Bad Request'), 400
    handler = BasketballEventHandler()

    if request.method == 'GET' or request.method == 'DELETE':
        # Validate GET/REMOVE requests
        if ('event_id' not in json or 'athlete_id' not in json):
            return jsonify(Error='Bad Request'), 400
        # Carry on with request
        if request.method == 'GET':
            event_id = request.args.get('event_id', type=int)
            athlete_id = request.args.get('athlete_id', type=int)
            return handler.getAllAthleteStatisticsByEventId(event_id, athlete_id)
        if request.method == 'DELETE':
            return handler.removeStatistics(json['event_id'], json['athlete_id'])

    if request.method == 'POST' or request.method == 'PUT':
        # Validate POST/PUT Requests
        # Validate Basic IDs
        if ('event_id' not in json or 'athlete_id' not in json or 'attributes' not in json):
            return jsonify(Error='Bad Request'), 400
        # Validate Specific Statistics
        specific_stats = json['attributes']
        if ('points' not in specific_stats or 'rebounds' not in specific_stats or 'assists' not in specific_stats
            or 'steals' not in specific_stats or 'blocks' not in specific_stats or 'turnovers' not in specific_stats
            or 'field_goal_attempt' not in specific_stats or 'successful_field_goal' not in specific_stats
            or 'three_point_attempt' not in specific_stats or 'successful_three_point' not in specific_stats
                or 'free_throw_attempt' not in specific_stats or 'successful_free_throw' not in specific_stats):
            return jsonify(Error='Bad Request'), 400
        # Carry On With Request
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
@app.route("/results/basketball/team/", methods=['GET', 'POST', 'PUT', 'DELETE'])
def basketballTeamStatistics():
    if request.method == 'GET' or request.method == 'DELETE':
        json = request.args
    else:
        json = request.json
    if json is None:
        return jsonify(Error='Bad Request'), 400
    handler = BasketballEventHandler()
    if request.method == 'GET' or request.method == 'DELETE' or request.method == 'PUT':
        # Validate GET/REMOVE/PUT requests
        if ('event_id' not in json):
            return jsonify(Error='Bad Request'), 400
        # Carry on with request
        if request.method == 'GET':
            event_id = request.args.get('event_id', type=int)
            return handler.getAllTeamStatisticsByEventId(event_id)
        if request.method == 'DELETE':
            return handler.removeTeamStatistics(json['event_id'])
        if request.method == 'PUT':
            return handler.editTeamStatistics(json['event_id'])
    if request.method == 'POST':
        # Validate POST Requests
        # Validate Basic IDs
        if ('event_id' not in json or 'add_type' not in json or 'attributes' not in json):
            return jsonify(Error='Bad Request'), 400
        # Validate Specific Statistics
        specific_stats = json['attributes']
        if ('points' not in specific_stats or 'rebounds' not in specific_stats or 'assists' not in specific_stats
            or 'steals' not in specific_stats or 'blocks' not in specific_stats or 'turnovers' not in specific_stats
            or 'field_goal_attempt' not in specific_stats or 'successful_field_goal' not in specific_stats
            or 'three_point_attempt' not in specific_stats or 'successful_three_point' not in specific_stats
                or 'free_throw_attempt' not in specific_stats or 'successful_free_throw' not in specific_stats):
            return jsonify(Error='Bad Request'), 400
        # Carry On With Request
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
@app.route("/results/basketball/score/", methods=['GET', 'POST', 'PUT', 'DELETE'])
def basketballFinalScores():
    if request.method == 'GET' or request.method == 'DELETE':
        json = request.args
    else:
        json = request.json
    if json is None:
        return jsonify(Error='Bad Request'), 400
    handler = BasketballEventHandler()
    if request.method == 'GET' or request.method == 'DELETE':
        # Validate GET/REMOVE requests
        if ('event_id' not in json):
            return jsonify(Error='Bad Request'), 400
        # Carry on with request
        if request.method == 'GET':
            event_id = request.args.get('event_id', type=int)
            return handler.getFinalScore(event_id)
        if request.method == 'DELETE':
            return handler.removeFinalScore(json['event_id'])
    if request.method == 'POST' or request.method == 'PUT':
        # Validate POST/PUT Requests
        # Validate Basic IDs
        if ('event_id' not in json or 'attributes' not in json):
            return jsonify(Error='Bad Request'), 400
        # Validate Specific Statistics
        specific_stats = json['attributes']
        if ('uprm_score' not in specific_stats or 'opponent_score' not in specific_stats):
            return jsonify(Error='Bad Request'), 400
        # Carry On With Request
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
# TODO: (Herbert) need to prepare a request schema for this one. just aid and seasonYear
@app.route("/results/basketball/season/athlete_games/", methods=['GET'])
def basketballSeasonAthleteStatistics():
    if request.method == 'GET':
        json = request.args
    else:
        json = request.json
    if json is None:
        return jsonify(Error='Bad Request'), 400
    handler = BasketballEventHandler()
    if request.method == 'GET':
        # Validate GET requests
        if ('athlete_id' not in json or 'season_year' not in json):
            return jsonify(Error='Bad Request'), 400
        season_year = request.args.get('season_year', type=int)
        athlete_id = request.args.get('athlete_id', type=int)
        # Carry on with request
        return handler.getAllAthleteStatisticsPerSeason(athlete_id, season_year)
    else:
        return jsonify(Error="Method not allowed."), 405


# {
#     "athlete_id":1,
#     "season_year":2020
# }
@app.route("/results/basketball/season/athlete_aggregate/", methods=['GET'])
def basketballAggregateAthleteStatistics():
    if request.method == 'GET':
        json = request.args
    else:
        json = request.json
    if json is None:
        return jsonify(Error='Bad Request'), 400
    handler = BasketballEventHandler()
    if request.method == 'GET':
        # Validate GET requests
        if ('athlete_id' not in json or 'season_year' not in json):
            return jsonify(Error='Bad Request'), 400
        season_year = request.args.get('season_year', type=int)
        athlete_id = request.args.get('athlete_id', type=int)
        # Carry on with request
        return handler.getAggregatedAthleteStatisticsPerSeason(athlete_id, season_year)
    else:
        return jsonify(Error="Method not allowed."), 405

# {
#     "sport_id":1,
#     "season_year":2020
# }
@app.route("/results/basketball/season/all_athletes_aggregate/", methods=['GET'])
def basketballAggregateAllAthleteStatistics():
    if request.method == 'GET':
        json = request.args
    else:
        json = request.json
    if json is None:
        return jsonify(Error='Bad Request'), 400
    handler = BasketballEventHandler()
    if request.method == 'GET':
        # Validate GET requests
        if ('sport_id' not in json or 'season_year' not in json):
            return jsonify(Error='Bad Request'), 400
        season_year = request.args.get('season_year', type=int)
        sport_id = request.args.get('sport_id', type=int)
        # Carry on with request
        return handler.getAllAggregatedAthleteStatisticsPerSeason(sport_id, season_year)
    else:
        return jsonify(Error="Method not allowed."), 405

# {
#     "sport_id":1,
#     "season_year":2020
# }
@app.route("/results/basketball/season/team_aggregate/", methods=['GET'])
def basketballAggregateTeamStatistics():
    if request.method == 'GET':
        json = request.args
    else:
        json = request.json
    if json is None:
        return jsonify(Error='Bad Request'), 400
    handler = BasketballEventHandler()
    if request.method == 'GET':
        # Validate GET requests
        if ('sport_id' not in json or 'season_year' not in json):
            return jsonify(Error='Bad Request'), 400
        season_year = request.args.get('season_year', type=int)
        sport_id = request.args.get('sport_id', type=int)
        # Carry on with request
        return handler.getAggregatedTeamStatisticsPerSeason(sport_id, season_year)
    else:
        return jsonify(Error="Method not allowed."), 405

# ===================================================================================
# ===================//END BASKETBALL RESULTS ROUTES//===============================
# ===================================================================================


#--------- PBP Routes ---------#
@app.route("/pbp/<string:sport>", methods=['POST', 'DELETE'])
def pbp_sequence(sport):

    body = request.get_json()
    args = request.args
    handler = None
    event_id = None

    # Assign proper handler.
    if sport == "Voleibol":
        handler = VolleyballPBPHandler()
    else:
        return jsonify(ERROR="El deporte seleccionado no tiene cobertura jugada a jugada."), 400

    if request.method == 'DELETE':
        if len(args) != 1 or "event_id" not in args or len(body) != 0:
            return jsonify(ERROR="Error en la petición. Solo debe proveerse un argumento en el cuerpo."), 400

        event_id = args["event_id"]

    else:
        if len(body) != 1 or "event_id" not in body or len(args) != 0:
            return jsonify(ERROR="Error en la petición. Solo debe proveerse un argumento en el cuerpo."), 400

        event_id = body["event_id"]

    if request.method == 'POST':
        return handler.startPBPSequence(event_id)

    return handler.removePBPSequence(event_id)


@app.route("/pbp/<string:sport>/set", methods=['PUT'])
def volleyball_pbp_set_current_set(sport):
    body = request.get_json()
    args = request.args
    handler = None

    if len(args) != 0:
        return jsonify(ERROR="No se aceptan argumentos en esta ruta."), 400

    # Assign proper handler.
    if sport == "Voleibol":
        handler = VolleyballPBPHandler()
    else:
        return jsonify(ERROR="El deporte seleccionado no tiene cobertura jugada a jugada."), 400

    if len(body) == 2 and "adjust" in body and "event_id" in body:
        return handler.adjustCurrentSet(body["event_id"], body["adjust"])

    return jsonify(ERROR="Error en la solicitud. Se debe enviar ambos ID del evento y cantidad a ser ajustada."), 400


@app.route("/pbp/<string:sport>/color", methods=['PUT'])
def pbp_set_color(sport):
    body = request.get_json()
    args = request.args
    handler = None

    if len(args) != 0:
        return jsonify(ERROR="No se aceptan argumentos en esta ruta."), 400

    # Assign proper handler.
    if sport == "Voleibol":
        handler = VolleyballPBPHandler()
    else:
        return jsonify(ERROR="El deporte seleccionado no tiene cobertura jugada a jugada."), 400

    if len(body) == 2 and "color" in body and "event_id" in body:
        return handler.setOpponentColor(body["event_id"], body["color"])

    return jsonify(ERROR="Error en la solicitud. Se debe enviar ambos ID del evento y color en formato HEX."), 400


@app.route("/pbp/<string:sport>/roster", methods=['POST', 'DELETE'])
def pbp_roster(sport):
    # ADD, REMOVE & EDIT TEAM ROSTERS FOR A PBP SEQUENCE
    body = request.get_json()
    args = request.args
    handler = None
    team = None
    event_id = None

    # Assign proper handler.
    if sport == "Voleibol":
        handler = VolleyballPBPHandler()
    else:
        return jsonify(ERROR="El deporte seleccionado no tiene cobertura jugada a jugada."), 400

    if request.method == 'DELETE':
        # Validate team is given within request body.
        if not "team" in args or not "event_id" in args or len(body) != 0:
            return jsonify(ERROR="Error en la solicitud. Se debe enviar ambos ID del evento y nombre de equipo como argumentos."), 400

        team = args["team"]
        event_id = args["event_id"]

    else:

        # Validate team is given within request body.
        if not "team" in body or not "event_id" in body or len(args) != 0:
            return jsonify(ERROR="Error en la solicitud. Se debe enviar ambos ID del evento y nombre de equipo en el cuerpo."), 400

        team = body["team"]
        event_id = body["event_id"]

    if request.method == 'POST':
        # Validate data is present in body.
        if len(body) != 3 or not "data" in body:
            return jsonify(ERROR="Error en la solicitud. Se debe enviar el ID del evento, nombre de equipo, y data."), 400

        data = body["data"]

        # For UPRM, data is the athlete_id.
        if team == "uprm":
            return handler.setUPRMPlayer(event_id, data)

        if team == "opponent":
            return handler.setOppPlayer(event_id, data)

        # Team not recognized.
        return jsonify(ERROR="Error en la solicitud. Nombre de equipo es invalido."), 400

    # Validate athlete id is given.
    if len(args) != 3 or "athlete_id" not in args:
        return jsonify(ERROR="Error en la solicitud. Valores para nombre de equipo, ID del evento, y ID de atleta deben ser proporcionados."), 400

    athlete_id = args["athlete_id"]

    if team == "uprm":
        return handler.removeUPRMPlayer(event_id, athlete_id)

    if team == "opponent":
        return handler.removeOppPlayer(event_id, athlete_id)

    # Team not recognized.
    return jsonify(ERROR="Error en la solicitud. Nombre de equipo es invalido."), 400


@app.route("/pbp/<string:sport>/actions", methods=['POST', 'PUT', 'DELETE'])
def pbp_actions(sport):
    # ADD, REMOVE & EDIT GAME ACTIONS FOR A PBP SEQUENCE
    body = request.get_json()
    args = request.args

    event_id = None

    if request.method == 'DELETE':
        # Validate event id is present in args.
        if "event_id" not in args:
            return jsonify(ERROR="Error en la solicitud. No se encontró valor de ID del evento."), 400

        event_id = args["event_id"]

    else:

        # Validate event id is present in body.
        if "event_id" not in body:
            return jsonify(ERROR="Error en la solicitud. No se encontró valor de ID del evento."), 400

        event_id = body["event_id"]

    # Assign proper handler.
    if sport == "Voleibol":
        handler = VolleyballPBPHandler()
    else:
        return jsonify(ERROR="El deporte seleccionado no tiene cobertura jugada a jugada."), 400

    if request.method == 'POST':
        # Validate action data is present in request body.
        if len(body) != 2 or "data" not in body:
            return jsonify(ERROR="Error en la solicitud. Se deben incluir el ID del evento y el valor de data en el cuerpo."), 400

        return handler.addPBPAction(event_id, body["data"])

    if request.method == 'PUT':
        # Validate data and action id are present in request body.
        if len(body) != 3 or "data" not in body or "action_id" not in body or len(args) != 0:
            return jsonify(ERROR="Error en la solicitud. Se deben incluir el ID del evento, ID de la acción y el valor de data en el cuerpo."), 400

        return handler.editPBPAction(event_id, body["action_id"], body["data"])

    # For delete, validate action id is present in body.
    if len(args) != 2 or "action_id" not in args or len(body) != 0:
        return jsonify(ERROR="Error en la solicitud. Se deben incluir el ID del evento y el ID de la acción como argumentos."), 400

    return handler.removePlayPBPAction(event_id, args["action_id"])


@app.route("/pbp/<string:sport>/end", methods=['POST'])
def pbp_end(sport):
    body = request.get_json()
    args = request.args
    handler = None

    if len(args) != 0:
        return jsonify(ERROR="No se aceptan argumentos en esta ruta."), 400

    # Assign proper PBP handler.
    if sport == "Voleibol":
        handler = VolleyballPBPHandler()
    else:
        return jsonify(ERROR="El deporte seleccionado no tiene cobertura jugada a jugada."), 400

    if len(body) == 1 and "event_id" in body:
        return handler.setPBPSequenceOver(body["event_id"])

    return jsonify(ERROR="Error en la solicitud. Se debe incluir solamente el ID del evento."), 400


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
@app.route("/results/volleyball/", methods=['GET', 'POST'])
def volleyballStatistics():
    if request.method == 'GET':
        json = request.args
    else:
        json = request.json
    if json is None:
        return jsonify(Error='Bad Request'), 400
    handler = VolleyballEventHandler()
    if request.method == 'GET':
        # Validate Request for GET
        if 'event_id' not in json:
            return jsonify(Error='Bad Request'), 400
        event_id = request.args.get('event_id', type=int)
        return handler.getAllStatisticsByEventID(event_id)
    if request.method == 'POST':
        # Validate General IDs for POST
        if ('event_id' not in json or 'team_statistics' not in json or 'athlete_statistics'
                not in json or 'uprm_score' not in json or 'opponent_score' not in json):
            return jsonify(Error='Bad Request'), 400
        # Validate Team Statistics Request
        team_statistics = json['team_statistics']
        if ('volleyball_statistics' not in team_statistics):
            return jsonify(Error='Bad Request'), 400
        specific_stats = team_statistics['volleyball_statistics']
        if ('kill_points' not in specific_stats or 'attack_errors' not in specific_stats or 'assists' not in specific_stats
            or 'aces' not in specific_stats or 'service_errors' not in specific_stats or 'digs' not in specific_stats
                or 'blocks' not in specific_stats or 'blocking_errors' not in specific_stats or 'reception_errors' not in specific_stats):
            return jsonify(Error='Bad Request'), 400
        # Validate Each Athlete's Statistics Request
        athlete_statistics = json['athlete_statistics']
        for athlete_json in athlete_statistics:
            if ('statistics' not in athlete_json or 'athlete_id' not in athlete_json):
                return jsonify(Error='Bad Request'), 400
            athlete_json_sport = athlete_json['statistics']
            if ('volleyball_statistics' not in athlete_json_sport):
                return jsonify(Error='Bad Request'), 400
            specific_stats = athlete_json_sport['volleyball_statistics']
            if ('kill_points' not in specific_stats or 'attack_errors' not in specific_stats or 'assists' not in specific_stats
                or 'aces' not in specific_stats or 'service_errors' not in specific_stats or 'digs' not in specific_stats
                    or 'blocks' not in specific_stats or 'blocking_errors' not in specific_stats or 'reception_errors' not in specific_stats):
                return jsonify(Error='Bad Request'), 400
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
@app.route("/results/volleyball/individual/", methods=['GET', 'POST', 'PUT', 'DELETE'])
def volleyballAthleteStatistics():
    if request.method == 'GET' or request.method == 'DELETE':
        json = request.args
    else:
        json = request.json
    if json is None:
        return jsonify(Error='Bad Request'), 400
    handler = VolleyballEventHandler()
    if request.method == 'GET' or request.method == 'DELETE':
        # Validate GET/REMOVE requests
        if ('event_id' not in json or 'athlete_id' not in json):
            return jsonify(Error='Bad Request'), 400
        # Carry on with request
        if request.method == 'GET':
            event_id = request.args.get('event_id', type=int)
            athlete_id = request.args.get('athlete_id', type=int)
            return handler.getAllAthleteStatisticsByEventId(event_id, athlete_id)
        if request.method == 'DELETE':
            return handler.removeStatistics(json['event_id'], json['athlete_id'])
    if request.method == 'POST' or request.method == 'PUT':
        # Validate POST/PUT Requests
        # Validate Basic IDs
        if ('event_id' not in json or 'athlete_id' not in json or 'attributes' not in json):
            return jsonify(Error='Bad Request'), 400
        # Validate Specific Statistics
        specific_stats = json['attributes']
        if ('kill_points' not in specific_stats or 'attack_errors' not in specific_stats or 'assists' not in specific_stats
            or 'aces' not in specific_stats or 'service_errors' not in specific_stats or 'digs' not in specific_stats
                or 'blocks' not in specific_stats or 'blocking_errors' not in specific_stats or 'reception_errors' not in specific_stats):
            return jsonify(Error='Bad Request'), 400
        # Carry On With Request
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
@app.route("/results/volleyball/team/", methods=['GET', 'POST', 'PUT', 'DELETE'])
def volleyballTeamStatistics():
    if request.method == 'GET' or request.method == 'DELETE':
        json = request.args
    else:
        json = request.json
    if json is None:
        return jsonify(Error='Bad Request'), 400
    handler = VolleyballEventHandler()
    if request.method == 'GET' or request.method == 'DELETE' or request.method == 'PUT':
        # Validate GET/REMOVE/PUT requests
        if ('event_id' not in json):
            return jsonify(Error='Bad Request'), 400
        # Carry on with request
        if request.method == 'GET':
            event_id = request.args.get('event_id', type=int)
            return handler.getAllTeamStatisticsByEventId(event_id)
        if request.method == 'PUT':
            return handler.editTeamStatistics(json['event_id'])
        if request.method == 'DELETE':
            return handler.removeTeamStatistics(json['event_id'])
    if request.method == 'POST':
        # Validate POST Requests
        # Validate Basic IDs
        if ('event_id' not in json or 'add_type' not in json or 'attributes' not in json):
            return jsonify(Error='Bad Request'), 400
        # Validate Specific Statistics
        specific_stats = json['attributes']
        if ('kill_points' not in specific_stats or 'attack_errors' not in specific_stats or 'assists' not in specific_stats
            or 'aces' not in specific_stats or 'service_errors' not in specific_stats or 'digs' not in specific_stats
                or 'blocks' not in specific_stats or 'blocking_errors' not in specific_stats or 'reception_errors' not in specific_stats):
            return jsonify(Error='Bad Request'), 400
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
@app.route("/results/volleyball/score/", methods=['GET', 'POST', 'PUT', 'DELETE'])
def volleyballFinalScores():
    if request.method == 'GET' or request.method == 'DELETE':
        json = request.args
    else:
        json = request.json
    if json is None:
        return jsonify(Error='Bad Request'), 400
    handler = VolleyballEventHandler()
    if request.method == 'GET' or request.method == 'DELETE':
        # Validate GET/REMOVE requests
        if ('event_id' not in json):
            return jsonify(Error='Bad Request'), 400
        # Carry on with request
        if request.method == 'GET':
            event_id = request.args.get('event_id', type=int)
            return handler.getFinalScore(event_id)
        if request.method == 'DELETE':
            return handler.removeFinalScore(json['event_id'])
    if request.method == 'POST' or request.method == 'PUT':
        # Validate POST/PUT Requests
        # Validate Basic IDs
        if ('event_id' not in json or 'attributes' not in json):
            return jsonify(Error='Bad Request'), 400
        # Validate Specific Statistics
        specific_stats = json['attributes']
        if ('uprm_score' not in specific_stats or 'opponent_score' not in specific_stats):
            return jsonify(Error='Bad Request'), 400
        # Carry On With Request
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
# TODO: (Herbert) need to prepare a request schema for this one. just aid and seasonYear
@app.route("/results/volleyball/season/athlete_games/", methods=['GET'])
def volleyballSeasonAthleteStatistics():
    if request.method == 'GET':
        json = request.args
    else:
        json = request.json
    if json is None:
        return jsonify(Error='Bad Request'), 400
    handler = VolleyballEventHandler()
    if request.method == 'GET':
        # Validate GET requests
        if ('athlete_id' not in json or 'season_year' not in json):
            return jsonify(Error='Bad Request'), 400
        season_year = request.args.get('season_year', type=int)
        athlete_id = request.args.get('athlete_id', type=int)
        # Carry on with request
        return handler.getAllAthleteStatisticsPerSeason(athlete_id, season_year)
    else:
        return jsonify(Error="Method not allowed."), 405


# {
#     "athlete_id":1,
#     "season_year":2020
# }
@app.route("/results/volleyball/season/athlete_aggregate/", methods=['GET'])
def volleyballAggregateAthleteStatistics():
    if request.method == 'GET':
        json = request.args
    else:
        json = request.json
    if json is None:
        return jsonify(Error='Bad Request'), 400
    handler = VolleyballEventHandler()
    if request.method == 'GET':
        # Validate GET requests
        if ('athlete_id' not in json or 'season_year' not in json):
            return jsonify(Error='Bad Request'), 400
        season_year = request.args.get('season_year', type=int)
        athlete_id = request.args.get('athlete_id', type=int)
        # Carry on with request
        return handler.getAggregatedAthleteStatisticsPerSeason(athlete_id, season_year)
    else:
        return jsonify(Error="Method not allowed."), 405

# {
#     "sport_id":1,
#     "season_year":2020
# }
@app.route("/results/volleyball/season/all_athletes_aggregate/", methods=['GET'])
def volleyballAggregateAllAthleteStatistics():
    if request.method == 'GET':
        json = request.args
    else:
        json = request.json
    if json is None:
        return jsonify(Error='Bad Request'), 400
    handler = VolleyballEventHandler()
    if request.method == 'GET':
        # Validate GET requests
        if ('sport_id' not in json or 'season_year' not in json):
            return jsonify(Error='Bad Request'), 400
        season_year = request.args.get('season_year', type=int)
        sport_id = request.args.get('sport_id', type=int)
        # Carry on with request
        return handler.getAllAggregatedAthleteStatisticsPerSeason(sport_id, season_year)
    else:
        return jsonify(Error="Method not allowed."), 405

# {
#     "sport_id":1,
#     "season_year":2020
# }
@app.route("/results/volleyball/season/team_aggregate/", methods=['GET'])
def volleyballAggregateTeamStatistics():
    if request.method == 'GET':
        json = request.args
    else:
        json = request.json
    if json is None:
        return jsonify(Error='Bad Request'), 400
    handler = VolleyballEventHandler()
    if request.method == 'GET':
        # Validate GET requests
        if ('sport_id' not in json or 'season_year' not in json):
            return jsonify(Error='Bad Request'), 400
        season_year = request.args.get('season_year', type=int)
        sport_id = request.args.get('sport_id', type=int)
        # Carry on with request
        return handler.getAggregatedTeamStatisticsPerSeason(sport_id, season_year)
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
@app.route("/results/soccer/", methods=['GET', 'POST'])
def soccerStatistics():
    if request.method == 'GET':
        json = request.args
    else:
        json = request.json
    if json is None:
        return jsonify(Error='Bad Request'), 400
    handler = SoccerEventHandler()
    if request.method == 'GET':
        # Validate Request for GET
        if 'event_id' not in json:
            return jsonify(Error='Bad Request'), 400
        event_id = request.args.get('event_id', type=int)
        return handler.getAllStatisticsByEventID(event_id)
    if request.method == 'POST':
        # Validate General IDs for POST
        if ('event_id' not in json or 'team_statistics' not in json or 'athlete_statistics'
                not in json or 'uprm_score' not in json or 'opponent_score' not in json):
            return jsonify(Error='Bad Request'), 400
        # Validate Team Statistics Request
        team_statistics = json['team_statistics']
        if ('soccer_statistics' not in team_statistics):
            return jsonify(Error='Bad Request'), 400
        specific_stats = team_statistics['soccer_statistics']
        if ('goal_attempts' not in specific_stats or 'assists' not in specific_stats or 'fouls' not in specific_stats
                or 'cards' not in specific_stats or 'successful_goals' not in specific_stats or 'tackles' not in specific_stats):
            return jsonify(Error='Bad Request'), 400
        # Validate Each Athlete's Statistics Request
        athlete_statistics = json['athlete_statistics']
        for athlete_json in athlete_statistics:
            if ('statistics' not in athlete_json or 'athlete_id' not in athlete_json):
                return jsonify(Error='Bad Request'), 400
            athlete_json_sport = athlete_json['statistics']
            if ('soccer_statistics' not in athlete_json_sport):
                return jsonify(Error='Bad Request'), 400
            specific_stats = athlete_json_sport['soccer_statistics']
            if ('goal_attempts' not in specific_stats or 'assists' not in specific_stats or 'fouls' not in specific_stats
                    or 'cards' not in specific_stats or 'successful_goals' not in specific_stats or 'tackles' not in specific_stats):
                return jsonify(Error='Bad Request'), 400
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
@app.route("/results/soccer/individual/", methods=['GET', 'POST', 'PUT', 'DELETE'])
def soccerAthleteStatistics():
    if request.method == 'GET' or request.method == 'DELETE':
        json = request.args
    else:
        json = request.json
    if json is None:
        return jsonify(Error='Bad Request'), 400
    handler = SoccerEventHandler()
    if request.method == 'GET' or request.method == 'DELETE':
        # Validate GET/REMOVE requests
        if ('event_id' not in json or 'athlete_id' not in json):
            return jsonify(Error='Bad Request'), 400
        # Carry on with request
        if request.method == 'GET':
            event_id = request.args.get('event_id', type=int)
            athlete_id = request.args.get('athlete_id', type=int)
            return handler.getAllAthleteStatisticsByEventId(event_id, athlete_id)
        if request.method == 'DELETE':
            return handler.removeStatistics(json['event_id'], json['athlete_id'])
    if request.method == 'POST' or request.method == 'PUT':
        # Validate POST/PUT Requests
        # Validate Basic IDs
        if ('event_id' not in json or 'athlete_id' not in json or 'attributes' not in json):
            return jsonify(Error='Bad Request'), 400
        # Validate Specific Statistics
        specific_stats = json['attributes']
        if ('goal_attempts' not in specific_stats or 'assists' not in specific_stats or 'fouls' not in specific_stats
                or 'cards' not in specific_stats or 'successful_goals' not in specific_stats or 'tackles' not in specific_stats):
            return jsonify(Error='Bad Request'), 400
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
@app.route("/results/soccer/team/", methods=['GET', 'POST', 'PUT', 'DELETE'])
def soccerTeamStatistics():
    if request.method == 'GET' or request.method == 'DELETE':
        json = request.args
    else:
        json = request.json
    if json is None:
        return jsonify(Error='Bad Request'), 400
    handler = SoccerEventHandler()
    if request.method == 'GET' or request.method == 'DELETE' or request.method == 'PUT':
        # Validate GET/REMOVE/PUT requests
        if ('event_id' not in json):
            return jsonify(Error='Bad Request'), 400
        # Carry on with request
        if request.method == 'GET':
            event_id = request.args.get('event_id', type=int)
            return handler.getAllTeamStatisticsByEventId(event_id)
        if request.method == 'PUT':
            return handler.editTeamStatistics(json['event_id'])
        if request.method == 'DELETE':
            return handler.removeTeamStatistics(json['event_id'])
    if request.method == 'POST':
        # Validate POST Requests
        # Validate Basic IDs
        if ('event_id' not in json or 'add_type' not in json or 'attributes' not in json):
            return jsonify(Error='Bad Request'), 400
        # Validate Specific Statistics
        specific_stats = json['attributes']
        if ('goal_attempts' not in specific_stats or 'assists' not in specific_stats or 'fouls' not in specific_stats
                or 'cards' not in specific_stats or 'successful_goals' not in specific_stats or 'tackles' not in specific_stats):
            return jsonify(Error='Bad Request'), 400
        # Carry On With Request
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
@app.route("/results/soccer/score/", methods=['GET', 'POST', 'PUT', 'DELETE'])
def soccerFinalScores():
    if request.method == 'GET' or request.method == 'DELETE':
        json = request.args
    else:
        json = request.json
    if json is None:
        return jsonify(Error='Bad Request'), 400
    handler = SoccerEventHandler()
    if request.method == 'GET' or request.method == 'DELETE':
        # Validate GET/REMOVE requests
        if ('event_id' not in json):
            return jsonify(Error='Bad Request'), 400
        # Carry on with request
        if request.method == 'GET':
            event_id = request.args.get('event_id', type=int)
            return handler.getFinalScore(event_id)
        if request.method == 'DELETE':
            return handler.removeFinalScore(json['event_id'])
    if request.method == 'POST' or request.method == 'PUT':
        # Validate POST/PUT Requests
        # Validate Basic IDs
        if ('event_id' not in json or 'attributes' not in json):
            return jsonify(Error='Bad Request'), 400
        # Validate Specific Statistics
        specific_stats = json['attributes']
        if ('uprm_score' not in specific_stats or 'opponent_score' not in specific_stats):
            return jsonify(Error='Bad Request'), 400
        # Carry On With Request
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
# TODO: (Herbert) need to prepare a request schema for this one. just aid and seasonYear
@app.route("/results/soccer/season/athlete_games/", methods=['GET'])
def soccerSeasonAthleteStatistics():
    if request.method == 'GET':
        json = request.args
    else:
        json = request.json
    if json is None:
        return jsonify(Error='Bad Request'), 400
    handler = SoccerEventHandler()
    if request.method == 'GET':
        # Validate GET requests
        if ('athlete_id' not in json or 'season_year' not in json):
            return jsonify(Error='Bad Request'), 400
        season_year = request.args.get('season_year', type=int)
        athlete_id = request.args.get('athlete_id', type=int)
        # Carry on with request
        return handler.getAllAthleteStatisticsPerSeason(athlete_id, season_year)
    else:
        return jsonify(Error="Method not allowed."), 405

# {
#     "athlete_id":1,
#     "season_year":2020
# }
@app.route("/results/soccer/season/athlete_aggregate/", methods=['GET'])
def soccerAggregateAthleteStatistics():
    if request.method == 'GET':
        json = request.args
    else:
        json = request.json
    if json is None:
        return jsonify(Error='Bad Request'), 400
    handler = SoccerEventHandler()
    if request.method == 'GET':
        # Validate GET requests
        if ('athlete_id' not in json or 'season_year' not in json):
            return jsonify(Error='Bad Request'), 400
        season_year = request.args.get('season_year', type=int)
        athlete_id = request.args.get('athlete_id', type=int)
        # Carry on with request
        return handler.getAggregatedAthleteStatisticsPerSeason(athlete_id, season_year)
    else:
        return jsonify(Error="Method not allowed."), 405

# {
#     "sport_id":1,
#     "season_year":2020
# }
@app.route("/results/soccer/season/all_athletes_aggregate/", methods=['GET'])
def soccerAggregateAllAthleteStatistics():
    if request.method == 'GET':
        json = request.args
    else:
        json = request.json
    if json is None:
        return jsonify(Error='Bad Request'), 400
    handler = SoccerEventHandler()
    if request.method == 'GET':
        # Validate GET requests
        if ('sport_id' not in json or 'season_year' not in json):
            return jsonify(Error='Bad Request'), 400
        season_year = request.args.get('season_year', type=int)
        sport_id = request.args.get('sport_id', type=int)
        # Carry on with request
        return handler.getAllAggregatedAthleteStatisticsPerSeason(sport_id, season_year)
    else:
        return jsonify(Error="Method not allowed."), 405

# {
#     "sport_id":1,
#     "season_year":2020
# }
@app.route("/results/soccer/season/team_aggregate/", methods=['GET'])
def soccerAggregateTeamStatistics():
    if request.method == 'GET':
        json = request.args
    else:
        json = request.json
    if json is None:
        return jsonify(Error='Bad Request'), 400
    handler = SoccerEventHandler()
    if request.method == 'GET':
        # Validate GET requests
        if ('sport_id' not in json or 'season_year' not in json):
            return jsonify(Error='Bad Request'), 400
        season_year = request.args.get('season_year', type=int)
        sport_id = request.args.get('sport_id', type=int)
        # Carry on with request
        return handler.getAggregatedTeamStatisticsPerSeason(sport_id, season_year)
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
@app.route("/results/baseball/", methods=['GET', 'POST'])
def baseballStatistics():
    if request.method == 'GET':
        json = request.args
    else:
        json = request.json
    if json is None:
        return jsonify(Error='Bad Request'), 400
    handler = BaseballEventHandler()
    if request.method == 'GET':
        # Validate Request for GET
        if 'event_id' not in json:
            return jsonify(Error='Bad Request'), 400
        event_id = request.args.get('event_id', type=int)
        return handler.getAllStatisticsByEventID(event_id)
    if request.method == 'POST':
        # Validate General IDs for POST
        if ('event_id' not in json or 'team_statistics' not in json or 'athlete_statistics'
                not in json or 'uprm_score' not in json or 'opponent_score' not in json):
            return jsonify(Error='Bad Request'), 400
        # Validate Team Statistics Request
        team_statistics = json['team_statistics']
        if ('baseball_statistics' not in team_statistics):
            return jsonify(Error='Bad Request'), 400
        specific_stats = team_statistics['baseball_statistics']
        if ('at_bats' not in specific_stats or 'runs' not in specific_stats or 'hits' not in specific_stats
            or 'runs_batted_in' not in specific_stats or 'base_on_balls' not in specific_stats or 'strikeouts' not in specific_stats
                or 'left_on_base' not in specific_stats):
            return jsonify(Error='Bad Request'), 400
        # Validate Each Athlete's Statistics Request
        athlete_statistics = json['athlete_statistics']
        for athlete_json in athlete_statistics:
            if ('statistics' not in athlete_json or 'athlete_id' not in athlete_json):
                return jsonify(Error='Bad Request'), 400
            athlete_json_sport = athlete_json['statistics']
            if ('baseball_statistics' not in athlete_json_sport):
                return jsonify(Error='Bad Request'), 400
            specific_stats = athlete_json_sport['baseball_statistics']
            if ('at_bats' not in specific_stats or 'runs' not in specific_stats or 'hits' not in specific_stats
                or 'runs_batted_in' not in specific_stats or 'base_on_balls' not in specific_stats or 'strikeouts' not in specific_stats
                    or 'left_on_base' not in specific_stats):
                return jsonify(Error='Bad Request'), 400
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
@app.route("/results/baseball/individual/", methods=['GET', 'POST', 'PUT', 'DELETE'])
def baseballAthleteStatistics():
    if request.method == 'GET' or request.method == 'DELETE':
        json = request.args
    else:
        json = request.json
    if json is None:
        return jsonify(Error='Bad Request'), 400
    handler = BaseballEventHandler()
    if request.method == 'GET' or request.method == 'DELETE':
        # Validate GET/REMOVE requests
        if ('event_id' not in json or 'athlete_id' not in json):
            return jsonify(Error='Bad Request'), 400
        # Carry on with request
        if request.method == 'GET':
            event_id = request.args.get('event_id', type=int)
            athlete_id = request.args.get('athlete_id', type=int)
            return handler.getAllAthleteStatisticsByEventId(event_id, athlete_id)
        if request.method == 'DELETE':
            return handler.removeStatistics(json['event_id'], json['athlete_id'])
    if request.method == 'POST' or request.method == 'PUT':
        # Validate POST/PUT Requests
        # Validate Basic IDs
        if ('event_id' not in json or 'athlete_id' not in json or 'attributes' not in json):
            return jsonify(Error='Bad Request'), 400
        # Validate Specific Statistics
        specific_stats = json['attributes']
        if ('at_bats' not in specific_stats or 'runs' not in specific_stats or 'hits' not in specific_stats
            or 'runs_batted_in' not in specific_stats or 'base_on_balls' not in specific_stats or 'strikeouts' not in specific_stats
                or 'left_on_base' not in specific_stats):
            return jsonify(Error='Bad Request'), 400
        # Carry On With Request
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
@app.route("/results/baseball/team/", methods=['GET', 'POST', 'PUT', 'DELETE'])
def baseballTeamStatistics():
    if request.method == 'GET' or request.method == 'DELETE':
        json = request.args
    else:
        json = request.json
    if json is None:
        return jsonify(Error='Bad Request'), 400
    handler = BaseballEventHandler()
    if request.method == 'GET' or request.method == 'DELETE' or request.method == 'PUT':
        # Validate GET/REMOVE/PUT requests
        if ('event_id' not in json):
            return jsonify(Error='Bad Request'), 400
        # Carry on with request
        if request.method == 'GET':
            event_id = request.args.get('event_id', type=int)
            return handler.getAllTeamStatisticsByEventId(event_id)
        if request.method == 'PUT':
            return handler.editTeamStatistics(json['event_id'])
        if request.method == 'DELETE':
            return handler.removeTeamStatistics(json['event_id'])
    if request.method == 'POST':
        # Validate POST Requests
        # Validate Basic IDs
        if ('event_id' not in json or 'add_type' not in json or 'attributes' not in json):
            return jsonify(Error='Bad Request'), 400
        # Validate Specific Statistics
        specific_stats = json['attributes']
        if ('at_bats' not in specific_stats or 'runs' not in specific_stats or 'hits' not in specific_stats
            or 'runs_batted_in' not in specific_stats or 'base_on_balls' not in specific_stats or 'strikeouts' not in specific_stats
                or 'left_on_base' not in specific_stats):
            return jsonify(Error='Bad Request'), 400
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
@app.route("/results/baseball/score/", methods=['GET', 'POST', 'PUT', 'DELETE'])
def baseballFinalScores():
    if request.method == 'GET' or request.method == 'DELETE':
        json = request.args
    else:
        json = request.json
    if json is None:
        return jsonify(Error='Bad Request'), 400
    handler = BaseballEventHandler()
    if request.method == 'GET' or request.method == 'DELETE':
        # Validate GET/REMOVE requests
        if ('event_id' not in json):
            return jsonify(Error='Bad Request'), 400
        # Carry on with request
        if request.method == 'GET':
            event_id = request.args.get('event_id', type=int)
            return handler.getFinalScore(event_id)
        if request.method == 'DELETE':
            return handler.removeFinalScore(json['event_id'])
    if request.method == 'POST' or request.method == 'PUT':
        # Validate POST/PUT Requests
        # Validate Basic IDs
        if ('event_id' not in json or 'attributes' not in json):
            return jsonify(Error='Bad Request'), 400
        # Validate Specific Statistics
        specific_stats = json['attributes']
        if ('uprm_score' not in specific_stats or 'opponent_score' not in specific_stats):
            return jsonify(Error='Bad Request'), 400
        # Carry On With Request
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
# TODO: (Herbert) need to prepare a request schema for this one. just aid and seasonYear
@app.route("/results/baseball/season/athlete_games/", methods=['GET'])
def baseballSeasonAthleteStatistics():
    if request.method == 'GET':
        json = request.args
    else:
        json = request.json
    if json is None:
        return jsonify(Error='Bad Request'), 400
    handler = BaseballEventHandler()
    if request.method == 'GET':
        # Validate GET requests
        if ('athlete_id' not in json or 'season_year' not in json):
            return jsonify(Error='Bad Request'), 400
        season_year = request.args.get('season_year', type=int)
        athlete_id = request.args.get('athlete_id', type=int)
        # Carry on with request
        return handler.getAllAthleteStatisticsPerSeason(athlete_id, season_year)
    else:
        return jsonify(Error="Method not allowed."), 405


# {
#     "athlete_id":1,
#     "season_year":2020
# }
@app.route("/results/baseball/season/athlete_aggregate/", methods=['GET'])
def baseballAggregateAthleteStatistics():
    if request.method == 'GET':
        json = request.args
    else:
        json = request.json
    if json is None:
        return jsonify(Error='Bad Request'), 400
    handler = BaseballEventHandler()
    if request.method == 'GET':
        # Validate GET requests
        if ('athlete_id' not in json or 'season_year' not in json):
            return jsonify(Error='Bad Request'), 400
        season_year = request.args.get('season_year', type=int)
        athlete_id = request.args.get('athlete_id', type=int)
        # Carry on with request
        return handler.getAggregatedAthleteStatisticsPerSeason(athlete_id, season_year)
    else:
        return jsonify(Error="Method not allowed."), 405

# {
#     "sport_id":1,
#     "season_year":2020
# }
@app.route("/results/baseball/season/all_athletes_aggregate/", methods=['GET'])
def baseballAggregateAllAthleteStatistics():
    if request.method == 'GET':
        json = request.args
    else:
        json = request.json
    if json is None:
        return jsonify(Error='Bad Request'), 400
    handler = BaseballEventHandler()
    if request.method == 'GET':
        # Validate GET requests
        if ('sport_id' not in json or 'season_year' not in json):
            return jsonify(Error='Bad Request'), 400
        season_year = request.args.get('season_year', type=int)
        sport_id = request.args.get('sport_id', type=int)
        # Carry on with request
        return handler.getAllAggregatedAthleteStatisticsPerSeason(sport_id, season_year)
    else:
        return jsonify(Error="Method not allowed."), 405

# {
#     "sport_id":1,
#     "season_year":2020
# }
@app.route("/results/baseball/season/team_aggregate/", methods=['GET'])
def baseballAggregateTeamStatistics():
    if request.method == 'GET':
        json = request.args
    else:
        json = request.json
    if json is None:
        return jsonify(Error='Bad Request'), 400
    handler = BaseballEventHandler()
    if request.method == 'GET':
        # Validate GET requests
        if ('sport_id' not in json or 'season_year' not in json):
            return jsonify(Error='Bad Request'), 400
        season_year = request.args.get('season_year', type=int)
        sport_id = request.args.get('sport_id', type=int)
        # Carry on with request
        return handler.getAggregatedTeamStatisticsPerSeason(sport_id, season_year)
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
        args = request.args
        handler = SportHandler()

        if body:
            return jsonify(ERROR="No se aceptan parámetros."), 400

        if len(args) == 0:
            return handler.getAllSports()

        if len(args) == 1:

            if 'branch' in args:
                # Validate branch type.
                if not isinstance(args['branch'], str):
                    return jsonify(ERROR="Error en la solicitud. La rama deportiva debe ser una secuencia de caracteres."), 400

                return handler.getSportsByBranch(args['branch'])

            if 'sport_name' in args:
                # Validate sport_name type.
                if not isinstance(args['sport_name'], str):
                    return jsonify(ERROR="Error en la solicitud. El nombre del deporte debe ser una secuencia de caracteres."), 400

                return handler.getSportByName(args['sport_name'])

            if 'sport_id' in args:
                # Validate sport_name type.
                if not args['sport_id'].isdigit():
                    return jsonify(ERROR="Error en la solicitud. El ID del deporte debe ser un entero."), 400

                return handler.getSportById(args['sport_id'])

        return jsonify(ERROR="Error en la solicitud. Debe proveerse un valor (rama deportiva o nombre del deporte) como argumento."), 400

    return jsonify(ERROR="Método HTTP no autorizado."), 405


@app.route("/sports/details", methods=['GET'])
def get_sport_info():
    if request.method == 'GET':
        args = request.args
        body = request.get_json()
        if not body and not args:
            return SportHandler().getSportCategoriesPositions()

        return jsonify(ERROR="Error en la solicitud. No se permiten parámetros."), 400

    return jsonify(ERROR="Método HTTP no autorizado."), 405


# ===================================================================================
# ===================//START TEAM RESULTS ROUTES//===================================
# ===================================================================================
# {
# "sport_id":1,
# "season_year":"2020",
# "team_image_url":"www.google.com",
# "about_team":"hello we are cool"
# }
@app.route("/teams/", methods=['GET', 'POST', 'PUT', 'DELETE'])
def teamByYear():
    if request.method == 'GET' or request.method == 'DELETE':
        json = request.args
    else:
        json = request.json
    if json is None:
        return jsonify(Error='Bad Request'), 400
    handler = TeamHandler()
    if (request.method == 'GET' or request.method == 'DELETE'):
        # Validate GET/DELETE Request Body
        if ('sport_id' not in json or 'season_year' not in json):
            return jsonify(Error='Bad Request'), 400
        if request.method == 'GET':
            sport_id = request.args.get('sport_id', type=int)
            season_year = request.args.get('season_year', type=int)
            return handler.getTeamByYear(sport_id, season_year)
        if request.method == 'DELETE':
            return handler.removeTeamByYear(json['sport_id'], json['season_year'])
    if (request.method == 'POST' or request.method == 'PUT'):
        # Validate POST/PUT Request Body
        if ('sport_id' not in json or 'season_year' not in json or 'team_image_url' not in json or 'about_team' not in json):
            return jsonify(Error='Bad Request'), 400
        if request.method == 'POST':
            return handler.addTeam(json['sport_id'], json['season_year'], json['team_image_url'], json['about_team'])
        if request.method == 'PUT':
            return handler.editTeamByYear(json['sport_id'], json['season_year'], json['team_image_url'], json['about_team'])

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
@app.route("/teams/members/", methods=['GET', 'POST'])
def teamMembers():
    if request.method == 'GET':
        json = request.args
    else:
        json = request.json
    if json is None:
        return jsonify(Error='Bad Request'), 400
    handler = TeamHandler()
    if request.method == 'GET':
        # Validate GET Request Body
        if ('team_id' not in json):
            return jsonify(Error='Bad Request'), 400
        team_id = request.args.get('team_id', type=int)
        return handler.getTeamMembersByID(team_id)
    if request.method == 'POST':
        # Validate POST Request Body
        if ('team_id' not in json or 'team_members' not in json):
            return jsonify(Error='Bad Request'), 400
        members_to_add = json['team_members']
        # Validate Each Added Member ID
        for member in members_to_add:
            if ('athlete_id' not in member):
                return jsonify(Error='Bad Request'), 400
        return handler.addTeamMembers(json['team_id'], json['team_members'])
    else:
        return jsonify(Error="Method not allowed."), 405


# {
#     "team_id":1,
#     "athlete_id":1
# }
# TODO: (Herbert) Check if need to remove route due to redundancy, wait for front end
@app.route("/teams/member/", methods=['GET', 'POST', 'DELETE'])
def teamMemberByIDs():
    if request.method == 'GET' or request.method == 'DELETE':
        json = request.args
    else:
        json = request.json
    if json is None:
        return jsonify(Error='Bad Request'), 400
    handler = TeamHandler()
    if request.method == 'GET' or request.method == 'POST' or request.method == 'DELETE':
        # Validate GET/POST/DELETE Request Body
        if ('team_id' not in json or 'athlete_id' not in json):
            return jsonify(Error='Bad Request'), 400
        if request.method == 'GET':
            athlete_id = request.args.get('athlete_id', type=int)
            team_id = request.args.get('team_id', type=int)
            return handler.getTeamMemberByIDs(athlete_id, team_id)
        if request.method == 'POST':
            return handler.addTeamMember(json['athlete_id'], json['team_id'])
        if request.method == 'DELETE':
            return handler.removeTeamMember(json['athlete_id'], json['team_id'])
    else:
        return jsonify(Error="Method not allowed."), 405


@app.route("/teams/all/", methods=['GET', 'POST', 'DELETE'])
def getAllTeams():
    handler = TeamHandler()
    if request.method == 'GET':
        return handler.getAllTeams()
    else:
        return jsonify(Error="Method not allowed."), 405

# ===================================================================================
# ===================//END TEAM RESULTS ROUTES//=====================================
# ===================================================================================

# ===================================================================================
# =======================//MATCH BASED RESULTS ROUTES//===============================
# ===================================================================================


@app.route("/results/matchbased/", methods=['GET', 'POST'])
def matchbasedStatistics():
    json = None
    if request.method == 'GET':
        json = request.args
    elif request.method == 'POST':
        json = request.json

    if not json or 'event_id' not in json:
        return jsonify(Error="Bad arguments"), 400

    handler = MatchBasedEventHandler()
    if request.method == 'GET':
        try:
            return handler.getAllStatisticsByEventID(int(json['event_id']))
        except:
            return jsonify(Error="Bad arguments"), 400

    if request.method == 'POST':
        return handler.addAllEventStatistics(json['event_id'], json)

    else:
        return jsonify("Method not allowed."), 405


@app.route("/results/matchbased/individual/", methods=['GET', 'POST', 'PUT', 'DELETE'])
def matchbasedAthleteStatistics():
    json = None
    if request.method == 'GET' or request.method == 'DELETE':
        json = request.args
    else:
        json = request.json

    if not json or 'event_id' not in json or 'athlete_id' not in json:
        return jsonify(Error="Bad arguments"), 400

    handler = MatchBasedEventHandler()

    if request.method == 'GET':
        try:
            return handler.getAllAthleteStatisticsByEventIdAndCategoryId(int(json['event_id']), int(json['athlete_id']), int(json['category_id']))
        except:
            return jsonify(Error="Bad arguments"), 400

    if request.method == 'POST':
        if 'attributes' not in json:
            return jsonify(Error="Bad arguments"), 400

        return handler.addStatistics(json['event_id'], json['athlete_id'], json['attributes'])

    if request.method == 'PUT':
        if 'attributes' not in json:
            return jsonify(Error="Bad arguments"), 400
        return handler.editStatistics(json['event_id'], json['athlete_id'], json['attributes'])

    if request.method == 'DELETE':
        if 'category_id' not in json:           
            return jsonify(Error="Bad arguments"), 400
        try:
            return handler.removeStatistics(int(json['event_id']), int(json['athlete_id']), int(json['category_id']))
        except:
            return jsonify(Error = "Bad arguments"),400


@app.route("/results/matchbased/team/", methods=['GET', 'POST', 'PUT', 'DELETE'])
def matchbasedTeamStatistics():
    json = None
    if request.method == 'GET' or request.method == 'DELETE':
        json = request.args
    else:
        json = request.json

    if not json or 'event_id' not in json:
        return jsonify(Error="Bad arguments"), 400

    handler = MatchBasedEventHandler()

    if request.method == 'GET':
        try:
            return handler.getAllTeamStatisticsByEventIdAndCategoryId(int(json['event_id']), int(json['category_id']))
        except:
            return jsonify(Error="Bad arguments"), 400

    if request.method == 'POST':
        if 'attributes' not in json:
            return jsonify(Error="Bad arguments"), 400
        return handler.addTeamStatistics(json['event_id'], json['attributes'])

    if request.method == 'PUT':
        if 'category_id' not in json:
            return jsonify(Error="Bad arguments"), 400

        return handler.editTeamStatistics(json['event_id'], json['category_id'])

    if request.method == 'DELETE':
        if 'category_id' not in json:
            return jsonify(Error="Bad arguments"), 400
        try:
            return handler.removeTeamStatistics(int(json['event_id']), int(json['category_id']))
        except:
            return jsonify(Error="Bad arguments"), 400

@app.route("/results/matchbased/score/", methods=['GET', 'POST', 'PUT', 'DELETE'])
def matchbasedFinalScores():
    json = None
    if request.method == 'GET' or request.method == 'DELETE':
        json = request.args
    else:
        json = request.json

    if json is None:
        return jsonify(Error='Bad Request'), 400

    handler = EventResultHandler()

    if request.method == 'GET' or request.method == 'DELETE':

        if 'event_id' not in json:
            return jsonify(Error='Bad Request'), 400
        try:
            if request.method == 'GET':
                return handler.getFinalScore(int(json['event_id']))
            if request.method == 'DELETE':
                return handler.removeFinalScore(int(json['event_id']))
        except:
            return jsonify(Error="Bad arguments"), 400
    if request.method == 'POST' or request.method == 'PUT':

        if 'event_id' not in json or 'attributes' not in json:
            return jsonify(Error='Bad Request'), 400

        specific_stats = json['attributes']

        if ('uprm_score' not in specific_stats or 'opponent_score' not in specific_stats):
            return jsonify(Error='Bad Request'), 400
        try:
            if request.method == 'POST':
                return handler.addFinalScore(json['event_id'], json['attributes'])
            if request.method == 'PUT':
                return handler.editFinalScore(json['event_id'], json['attributes'])
        except:
            return jsonify(Error="Bad arguments"), 400


@app.route("/results/matchbased/season/athlete_games/", methods=['GET'])
def matchbasedSeasonAthleteStatistics():
    json = request.args
    if not json or 'athlete_id' not in json or 'season_year' not in json:
        return jsonify("Error = Bad arguments"), 400

    if request.method == 'GET':
        try:
            return MatchBasedEventHandler().getAllAthleteStatisticsPerSeason(int(json['athlete_id']), int(json['season_year']))
        except:
            return jsonify(Error="Bad arguments"), 400


@app.route("/results/matchbased/season/athlete_aggregate/", methods=['GET'])
def matchbasedAggregateAthleteStatistics():
    json = request.args
    if not json or 'athlete_id' not in json or 'season_year' not in json:
        return jsonify(Error="Bad arguments"), 400

    if request.method == 'GET':
        try:
            return MatchBasedEventHandler().getAggregatedAthleteStatisticsPerSeason(int(json['athlete_id']), int(json['season_year']))
        except:
            return jsonify(Error="Bad arguments"), 400


@app.route("/results/matchbased/season/all_athletes_aggregate/", methods=['GET'])
def matchbasedAggregateAllAthleteStatistics():
    json = request.args
    if not json or 'sport_id' not in json or 'season_year' not in json:
        return jsonify(Error="Bad arguments"), 400

    if request.method == 'GET':
        try:
            return MatchBasedEventHandler().getAllAggregatedAthleteStatisticsPerSeason(int(json['sport_id']), int(json['season_year']))
        except:
            return jsonify(Error="Bad arguments"), 400


@app.route("/results/matchbased/season/team_aggregate/", methods=['GET'])
def matchbasedAggregateTeamStatistics():
    json = request.args
    if not json or 'sport_id' not in json or 'season_year' not in json:
        return jsonify(Error="Bad arguments"), 400

    if request.method == 'GET':
        try:
            return MatchBasedEventHandler().getAggregatedTeamStatisticsPerSeason(int(json['sport_id']), int(json['season_year']))
        except:
            return jsonify(Error="Bad arguments"), 400


# ===================================================================================
# ===================//END MATCH BASED RESULTS ROUTES//===============================
# ===================================================================================


# ===================================================================================
# =======================//MEDAL BASED RESULTS ROUTES//===============================
# ===================================================================================

@app.route("/results/medalbased/", methods=['GET', 'POST'])
def medalbasedStatistics():
    json = None
    if request.method == 'GET':
        json = request.args
    elif request.method == 'POST':
        json = request.json

    if not json or 'event_id' not in json:
        return jsonify(Error="Bad arguments"), 400

    handler = MedalBasedEventHandler()
    if request.method == 'GET':
        try:
            return handler.getAllStatisticsByEventID(int(json['event_id']))
        except:
            return jsonify(Error="Bad arguments"), 400

    if request.method == 'POST':
        return handler.addAllEventStatistics(json['event_id'], json)

    else:
        return jsonify("Method not allowed."), 405


@app.route("/results/medalbased/individual/", methods=['GET', 'POST', 'PUT', 'DELETE'])
def medalbasedAthleteStatistics():
    json = None
    if request.method == 'GET' or request.method == 'DELETE':
        json = request.args
    else:
        json = request.json

    if not json or 'event_id' not in json or 'athlete_id' not in json:
        return jsonify(Error="Bad arguments"), 400

    handler = MedalBasedEventHandler()

    if request.method == 'GET':
        try:
            return handler.getAllAthleteStatisticsByEventIdAndCategoryId(int(json['event_id']), int(json['athlete_id']), int(json['category_id']))
        except:
            return jsonify(Error="Bad arguments"), 400

    if request.method == 'POST':
        if 'attributes' not in json:
            return jsonify(Error="Bad arguments"), 400

        return handler.addStatistics(json['event_id'], json['athlete_id'], json['attributes'])

    if request.method == 'PUT':
        if 'attributes' not in json:
            return jsonify(Error="Bad arguments"), 400
        return handler.editStatistics(json['event_id'], json['athlete_id'], json['attributes'])

    if request.method == 'DELETE':
        if 'category_id' not in json:
            return jsonify(Error="Bad arguments"), 400
        try:
            return handler.removeStatistics(int(json['event_id']),int(json['athlete_id']),int(json['category_id']))
        except:
            return jsonify(Error = "Bad arguments"),400


@app.route("/results/medalbased/team/", methods=['GET', 'POST', 'PUT', 'DELETE'])
def medalbasedTeamStatistics():
    json = None
    if request.method == 'GET' or request.method == "DELETE":
        json = request.args
    else:
        json = request.json

    if not json or 'event_id' not in json:
        return jsonify(Error="Bad arguments"), 400

    handler = MedalBasedEventHandler()

    if request.method == 'GET':
        try:
            return handler.getAllTeamStatisticsByEventIdAndCategoryId(int(json['event_id']), int(json['category_id']))
        except:
            return jsonify(Error="Bad arguments"), 400

    if request.method == 'POST':
        if 'attributes' not in json:
            return jsonify(Error="Bad arguments"), 400
        return handler.addTeamStatistics(json['event_id'], json['attributes'])

    if request.method == 'PUT':
        if 'category_id' not in json:
            return jsonify(Error="Bad arguments"), 400

        return handler.editTeamStatistics(json['event_id'], json['category_id'])

    if request.method == 'DELETE':
        if 'category_id' not in json:
            return jsonify(Error="Bad arguments"), 400
        try:
            return handler.removeTeamStatistics(int(json['event_id']), int(json['category_id']))
        except:
            return jsonify(Error="Bad arguments"), 400


@app.route("/results/medalbased/score/", methods=['GET', 'POST', 'PUT', 'DELETE'])
def medalbasedFinalScores():
    json = None
    if request.method == 'GET' or request.method == 'DELETE':
        json = request.args
    else:
        json = request.json

    if json is None:
        return jsonify(Error='Bad Request'), 400

    handler = EventResultHandler()

    if request.method == 'GET' or request.method == 'DELETE':

        if 'event_id' not in json:
            return jsonify(Error='Bad Request'), 400
        try:
            if request.method == 'GET':
                return handler.getFinalScore(int(json['event_id']))
            if request.method == 'DELETE':
                return handler.removeFinalScore(int(json['event_id']))
        except:
            return jsonify(Error="Bad arguments"), 400
    if request.method == 'POST' or request.method == 'PUT':

        if 'event_id' not in json or 'attributes' not in json:
            return jsonify(Error='Bad Request'), 400

        specific_stats = json['attributes']

        if ('uprm_score' not in specific_stats or 'opponent_score' not in specific_stats):
            return jsonify(Error='Bad Request'), 400
        try:
            if request.method == 'POST':
                return handler.addFinalScore(json['event_id'], json['attributes'])
            if request.method == 'PUT':
                return handler.editFinalScore(json['event_id'], json['attributes'])
        except:
            return jsonify(Error="Bad arguments"), 400


@app.route("/results/medalbased/season/athlete_games/", methods=['GET'])
def medalbasedSeasonAthleteStatistics():
    json = request.args
    if not json or 'athlete_id' not in json or 'season_year' not in json:
        return jsonify("Error = Bad arguments"), 400

    if request.method == 'GET':
        try:
            return MedalBasedEventHandler().getAllAthleteStatisticsPerSeason(int(json['athlete_id']), int(json['season_year']))
        except:
            return jsonify(Error="Bad arguments"), 400


@app.route("/results/medalbased/season/athlete_aggregate/", methods=['GET'])
def medalbasedAggregateAthleteStatistics():
    json = request.args
    if not json or 'athlete_id' not in json or 'season_year' not in json:
        return jsonify(Error="Bad arguments"), 400

    if request.method == 'GET':
        try:
            return MedalBasedEventHandler().getAggregatedAthleteStatisticsPerSeason(int(json['athlete_id']), int(json['season_year']))
        except:
            return jsonify(Error="Bad arguments"), 400


@app.route("/results/medalbased/season/all_athletes_aggregate/", methods=['GET'])
def medalbasedAggregateAllAthleteStatistics():
    json = request.args
    if not json or 'sport_id' not in json or 'season_year' not in json:
        return jsonify(Error="Bad arguments"), 400

    if request.method == 'GET':
        try:
            return MedalBasedEventHandler().getAllAggregatedAthleteStatisticsPerSeason(int(json['sport_id']), int(json['season_year']))
        except:
            return jsonify(Error="Bad arguments"), 400


@app.route("/results/medalbased/season/team_aggregate/", methods=['GET'])
def medalbasedAggregateTeamStatistics():
    json = request.args
    if not json or 'sport_id' not in json or 'season_year' not in json:
        return jsonify(Error="Bad arguments"), 400

    if request.method == 'GET':
        try:
            return MedalBasedEventHandler().getAggregatedTeamStatisticsPerSeason(int(json['sport_id']), int(json['season_year']))
        except:
            return jsonify(Error="Bad arguments"), 400


# ===================================================================================
# ===================//END MEDAL BASED RESULTS ROUTES//===============================
# ===================================================================================


# Launch app.
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
