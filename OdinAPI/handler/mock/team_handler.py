from flask import Flask, jsonify


class _mockTeamHandler:

    def __init__(self):
        '''
        Initialize collection for the Team Handler mock class.
        '''
        self.records = {4: [
            {
                "team_members_id": 26,
                "athlete_id": 12,
                "first_name": "Elena",
                "middle_name": "Marie",
                "last_names": "Quiñones",
                "number": 12,
                "profile_image_link": "Here goes an image",
                "height_inches": "5'08",
                "study_program": "Computer Sciences",
                "school_of_precedence": "Tasis",
                "years_of_participation": 3,
                "positions": ["libero"],
                "categories": []
            },
            {
                "team_members_id": 26,
                "athlete_id": 14,
                "first_name": "Justina",
                "middle_name": "",
                "last_names": "Barreros Marte",
                "number": 15,
                "profile_image_link": "Here goes an image",
                "height_inches": "5'08",
                "study_program": "Computer Sciences",
                "school_of_precedence": "Tasis",
                "years_of_participation": 3,
                "positions": ["libero"],
                "categories": []
            },
            {
                "team_members_id": 26,
                "athlete_id": 26,
                "first_name": "Jennifer",
                "middle_name": "",
                "last_names": "Castro",
                "number": 1,
                "profile_image_link": "Here goes an image",
                "height_inches": "5'08",
                "study_program": "Computer Sciences",
                "school_of_precedence": "Tasis",
                "years_of_participation": 3,
                "positions": ["libero"],
                "categories": []
            },
            {
                "team_members_id": 26,
                "athlete_id": 80,
                "first_name": "Maria",
                "middle_name": "Marie",
                "last_names": "Martinez",
                "number": 7,
                "profile_image_link": "Here goes an image",
                "height_inches": "5'08",
                "study_program": "Computer Sciences",
                "school_of_precedence": "Tasis",
                "years_of_participation": 3,
                "positions": ["libero"],
                "categories": []
            },
            {
                "team_members_id": 26,
                "athlete_id": 99,
                "first_name": "Esther",
                "middle_name": "",
                "last_names": "Laboy",
                "number": 5,
                "profile_image_link": "Here goes an image",
                "height_inches": "5'08",
                "study_program": "Computer Sciences",
                "school_of_precedence": "Tasis",
                "years_of_participation": 3,
                "positions": ["libero"],
                "categories": []
            },
        ]}

    def getTeamMembersByID(self, team_id):
        if self.records.get(team_id):
            return jsonify(TEAM=self.records.get(team_id)), 200

        return jsonify(ERROR="Team not found"), 400
