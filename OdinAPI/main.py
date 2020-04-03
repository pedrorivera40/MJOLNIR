from flask import Flask, request, jsonify


app = Flask(__name__)


#--------- PBP Routes ---------#
@app.route("/pbp/", methods=['POST', 'PUT', 'DELETE'])
def pbp_sequence():
    # CREATE PBP SEQUENCE & EDIT METADATA. (ALSO DELETE)
    return 1


@app.route("/pbp/rosters", methods=['POST', 'PUT', 'DELETE'])
def pbp_roster():
    # ADD, REMOVE & EDIT TEAM ROSTERS FOR A PBP SEQUENCE
    return 1


@app.route("/pbp/actions", methods=['POST', 'PUT', 'DELETE'])
def pbp_actions():
    # ADD, REMOVE & EDIT GAME ACTIONS FOR A PBP SEQUENCE
    return 1


@app.route("/pbp/end", methods=['POST'])
def pbp_end():
    # END PBP SEQUENCE
    return 1


    # Launch app.
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
