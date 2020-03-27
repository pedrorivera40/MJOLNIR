from .config.sqlconfig import db_config
from flask import jsonify
import psycopg2

class AthleteDAO:
    def __init__(self):
        connection_url = "dbname={} user={} password={} host ={} ".format(
        db_config['database'],
        db_config['username'],
        db_config['password'],
        db_config['host']
        )
        self.conn = psycopg2.connect(connection_url)


    def getAtheletes(self):
        atheletes = []
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT first_name, last_names, short_bio, number, sport_id, id from athlete;"
        )
        db_athletes = cursor.fetchall()

        for row in db_athletes:
            atheletes.append({
                'first_name': row[0],               
                'last_names' : row[1],
                'short_bio': row[2],               
                'number': row[3],                
                'sport_id': row[4],
                'id':row[5]
            })
        #print(db_athletes)
        return jsonify(Athletes = atheletes),201

