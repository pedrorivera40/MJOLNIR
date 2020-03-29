from flask import Flask,request,jsonify
from flask_cors import CORS
import os
import datetime
<<<<<<< HEAD
# from handler.dao.athlete import AthleteDAO
from handler.user import UserHandler
=======
from handler.athlete import AthleteHandler
>>>>>>> 591ad7b2d3ad8a0d1bc781b6a2d152da9a5b43c1





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
def users():
    if request.method == 'GET':
        handler = UserHandler()

        return handler.getAllDashUsers()


#Launch app.
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')