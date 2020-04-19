from flask import Flask, jsonify

class _mockEventHandler:

    def __init__(self):
        '''
        Initialize mock collection for the EventDAO mock class.
        '''
        self.records = {
            28: {
                "branch": "femenino",  # col 0 -> event date
                "is_local": "true",  # col 1 -> is local value
                "opponent-name": "UPR-RP",  # col 2 -> opponent name
                "sport_name": "Voleibol",  # col 3 -> sport name
                "venue": "Coliseo Rafael Mangual",  # col 4 -> venue
                "date": "28-may-2020"  # col 5 -> date
            },
            29: {
                "branch": "femenino",  # col 0 -> event date
                "is_local": "true",  # col 1 -> is local value
                "opponent-name": "UPR-RP",  # col 2 -> opponent name
                "sport_name": "Voleibol",  # col 3 -> sport name
                "venue": "Coliseo Rafael Mangual",  # col 4 -> venue
                "date": "28-may-2020"  # col 5 -> date
            },
        }

    def getEventById(self, id):
        if self.records.get(id):
            return jsonify(EVENT=self.records.get(id)), 200

        return jsonify(ERROR="Event not found"), 400
