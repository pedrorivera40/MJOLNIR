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
        

#--------- Dashboard User Routes ---------#
@app.route("/users/", methods = ['GET'])
def users():
    if request.method == 'GET':
        handler = UserHandler()

        return handler.getAllDashUsers()


#Launch app.
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')