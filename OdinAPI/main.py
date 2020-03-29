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
@app.route("/athletes/<int:aid>/", methods = ['GET','POST','PUT','DELETE'])
def athleteByID(aid):
    handler = AthleteHandler()
    if request.method == 'GET':
        return handler.getAthleteByID(aid)
    elif request.method == 'POST':
        json = request.json
        return handler.addAthlete(json['sID'],json['attributes'])
    elif request.method == 'PUT':
        json = request.json
        return handler.editAthlete(aid,json['attributes'])
    elif request.method == 'DELETE':
        json = request.json
        return handler.removeAthlete(aid)
        
###########################################
#--------- Dashboard User Routes ---------#
###########################################
@app.route("/users/", methods = ['GET','POST'])
def allUsers():
    handler = UserHandler()
    req = request.json
    if request.method == 'GET':
        return handler.getAllDashUsers()
    if request.method == 'POST':
        password = createHash(req['password'])
        return handler.addDashUser(req['username'],req['fullName'], req['email'], password)

@app.route("/users/<int:duid>", methods = ['GET','PATCH','DELETE'])
def userByID(duid):
    handler = UserHandler()
    req = request.json
    if request.method == 'GET':
        return handler.getDashUserByID(duid)
    if request.method == 'PATCH':
        return handler.updateDashUserUsername(duid,req['username'])

@app.route("/users/<int:duid>/reset", methods = ['PATCH'])
def passwordReset(duid):
    handler = UserHandler()
    req = request.json
    if request.method == 'PATCH':
        password = createHash(req['password'])
        return handler.updateDashUserPassword(duid,password)
    


@app.route("/users/<string:username>", methods = ['GET'])
def userByUsername(username):
    if request.method == 'GET':
        handler = UserHandler()

        return handler.getDashUserByUsername(username)

@app.route("/users/email/<string:email>", methods = ['GET'])
def userByEmail(email):
    print (email)
    if request.method == 'GET':
        handler = UserHandler()

        return handler.getDashUserByEmail(email)


#Launch app.
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
    