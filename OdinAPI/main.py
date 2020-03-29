from flask import Flask,request,jsonify
from flask_cors import CORS
import os
import datetime
from handler.user import UserHandler
from handler.athlete import AthleteHandler





app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})


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
        

#--------- Dashboard User Routes ---------#
@app.route("/users/", methods = ['GET'])
def allUsers():
    if request.method == 'GET':
        handler = UserHandler()

        return handler.getAllDashUsers()

@app.route("/users/<int:duid>", methods = ['GET','POST','PUT','DELETE'])
def userByID(duid):
    if request.method == 'GET':
        handler = UserHandler()

        return handler.getDashUserByID(duid)

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