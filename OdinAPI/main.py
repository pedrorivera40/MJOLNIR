from flask import Flask,request,jsonify
from flask_cors import CORS
import os
import datetime
from handler.dao.athlete import AthleteDAO





app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})


@app.route("/")
def hello():
    return jsonify("Hi, this is a route that will be eliminated xD")


@app.route("/athletes/", methods = ['GET'])
def athleteProfiles():
    athlete = AthleteDAO()
    return athlete.getAtheletes()



#Launch app.
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')