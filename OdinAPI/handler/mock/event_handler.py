from flask import Flask, jsonify

# NOTE: This mock has been deprecated during integration phase (April 30, 2020).


class _mockEventHandler:

    def __init__(self):
        '''
        Initialize collection for the Event Handler mock class.
        '''
        self.records = {
            28: {
                "id": 28,
                "event_date": "28-may-2020",
                "is_local": "true",
                "venue": "Coliseo Rafael Mangual",
                "team_id": 10,
                "opponent_name": "Jerezanas",
                "event_summary": "I do not want to write anything.",
                "sport_name": "Voleibol",
                "sport_img_url": "Here goes a photo",
                "branch": "femenino",
                "team_season_year": "2020"
            },
            29: {
                "id": 29,
                "event_date": "28-may-2020",
                "is_local": "true",
                "venue": "Coliseo Rafael Mangual",
                "team_id": 10,
                "opponent_name": "Jerezanas",
                "event_summary": "I do not want to write anything.",
                "sport_name": "Voleibol",
                "sport_img_url": "Here goes a photo",
                "branch": "femenino",
                "team_season_year": "2020"
            },
            19: {  # 4
                "id": 19,
                "event_date": "28-may-2020",
                "is_local": "true",
                "venue": "Coliseo Rafael Mangual",
                "team_id": 10,
                "opponent_name": "Jerezanas",
                "event_summary": "I do not want to write anything.",
                "sport_name": "Baloncesto",
                "sport_img_url": "Here goes a photo",
                "branch": "femenino",
                "team_season_year": "2020"
            },
        }

    def getEventById(self, id):
        if self.records.get(id):
            return jsonify(EVENT=self.records.get(id)), 200

        return jsonify(ERROR="Event not found"), 400
