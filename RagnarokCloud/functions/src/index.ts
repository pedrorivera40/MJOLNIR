import * as functions from 'firebase-functions';
import * as admin from 'firebase-admin';
import { encode, TAlgorithm } from "jwt-simple";

// Add axios library for interacting with Odin API via HTTP.	
const axios: any = require('axios').default;

/*
    This file contains the Cloud Functions required for the development of Huella Deportiva Web.
    @author Pedro Luis Rivera Gomez - pedrorivera40
*/

// Initialize app to use Admin Priviledges.	
admin.initializeApp(functions.config().firebase);

// This function is written for learning purposes.
// Its goal is to react to changes in a path of the Realtime Database, to simulate
// rejecting the change (if a new value is present, replace it by the old value).
// In this case that is performed over the game_ended child inside the metadata
// corresponding to a game. For details, refer to the NoSQL structure in the progress
// report #1 for MJOLNIR.

// Prototype...
// export const sampleCloudFunction = functions.database.instance("mjolnir-pbp-v1").ref("/v1/{game_id}/game-metadata/game-ended")	
//     .onUpdate((change, context) => {	
//         // Read the game id for the change. It will be logged for quick testing purposes.	
//         // const gameId = context.params.game_id	
//         // console.log("Change detected on game-id=" + gameId)	

//         // Read the latest data corrsponding to the state.	
//         const gameState = change.after.child("answer").val()	

//         // If the game is not over, ignore/return.	
//         if (gameState === "No") {	
//             // console.log("Game is not over!")	
//             return null	
//         }	

//         // If the game is marked as over, reject that change by re-writting in the database "No".	
//         const answer = "No"	
//         return change.after.ref.update({ answer });	

//     });

// TODO -> Add class documentation.	
export class VolleyballStatsEntry {

    // Statistics of interest for volleyball.	
    private killPoints: number = 0;
    private attackErrors: number = 0;
    private assists: number = 0;
    private aces: number = 0;
    private serviceErrors: number = 0;
    private digs: number = 0;
    private blocks: number = 0;
    private blockPoints: number = 0;
    private blockingErrors: number = 0;
    private receptionErrors: number = 0;

    /**	
     * Empty constructor for a VolleyballStatsEntry instance.	
     */
    // constructor() { }	

    // Instance variables mutator methods.	
    // Used to add actions corresponding to events of a volleyball game that	
    // are considered for statistical purposes.	

    // Add a kill play.	
    kill(): void {
        this.killPoints++;
    }

    // Add an attack error play.	
    attackError(): void {
        this.attackErrors++;
    }

    // Add an assist play.	
    assist(): void {
        this.assists++;
    }

    // Add an ace play.	
    ace(): void {
        this.aces++;
    }

    // Add a service error play.	
    serviceError(): void {
        this.serviceErrors++;
    }

    // Add a dig play.	
    dig(): void {
        this.digs++;
    }

    // Add a block play.	
    block(): void {
        this.blocks++;
    }

    // Add a block point play.
    blockPoint(): void {
        this.blockPoints++;
        this.blocks++;
    }

    // Add a blocking error play.	
    blockingError(): void {
        this.blockingErrors++;
    }

    // Add a reception error play.	
    receptionError(): void {
        this.receptionErrors++;
    }

    // Entry getter method.	
    // This method converts a VolleybalStatEntry into its JSON representation.	
    getJSON(): JSON {
        // Organize output in the following structure:	
        //      { volleyball_statistics : { "stat1" : stat1_val, ... } }	
        return <JSON><unknown>{
            "volleybal_statistics": {
                "kill_points": this.killPoints,
                "attack_errors": this.attackErrors,
                "assists": this.assists,
                "aces": this.aces,
                "service_errors": this.serviceErrors,
                "digs": this.digs,
                "blocks": this.blocks,
                "blocking_points": this.blockPoints,
                "blocking_errors": this.blockingErrors,
                "reception_errors": this.receptionErrors
            }
        };
    }

}

export const enum VolleyballPlays {
    KillPoint = "KillPoint",
    AttackError = "AttackError",
    Assist = "Assist",
    Ace = "Ace",
    ServiceError = "ServiceError",
    Dig = "Dig",
    Block = "Block",
    BlockPoint = "BlockPoint",
    BlockingError = "BlockingError",
    ReceptionError = "ReceptionError"
}

// TODO -> Add documentation & TESTS.	
export const updateVolleyballStats = function (actionType: string, playerStats:
    VolleyballStatsEntry, teamStats: VolleyballStatsEntry): void {

    // Update player and team statistics based on the given action type.	
    switch (actionType) {

        case VolleyballPlays.KillPoint:
            playerStats.kill();
            teamStats.kill();
            break;

        case VolleyballPlays.AttackError:
            playerStats.attackError();
            teamStats.attackError();
            break;

        case VolleyballPlays.Assist:
            playerStats.assist();
            teamStats.assist();
            break;

        case VolleyballPlays.Ace:
            playerStats.ace();
            teamStats.ace();
            break;

        case VolleyballPlays.ServiceError:
            playerStats.serviceError();
            teamStats.serviceError();
            break;

        case VolleyballPlays.Dig:
            playerStats.dig();
            teamStats.dig();
            break;

        case VolleyballPlays.Block:
            playerStats.block();
            teamStats.block();
            break;

        case VolleyballPlays.BlockPoint:
            playerStats.blockPoint();
            teamStats.blockPoint();
            break;

        case VolleyballPlays.BlockingError:
            playerStats.blockingError();
            teamStats.blockingError();
            break;

        case VolleyballPlays.ReceptionError:
            playerStats.receptionError();
            teamStats.receptionError();
            break;

        default:
            console.log("volleyballGameSync Error: Non-statistics current action " + actionType);
            break;
    }

    return;
}

export const postVolleyballResults = async function (gameStatistics: JSON) {
    // Prepare for POST request to Odin API with volleyball results.	
    const volleyballPath = "https://white-smile-272204.ue.r.appspot.com/results/volleyball/";
    // Handling permissions as required for using Odin API.
    const permissions = [
        { "13": false },
        { "14": false },
        { "15": false },
        { "16": false },
        { "17": false },
        { "18": false },
        { "19": true },
        { "20": false },
        { "21": false },
        { "22": false },
        { "23": false },
        { "24": false },
        { "25": false },
        { "26": false },
        { "27": false }
    ];

    const payload = {
        'permissions': permissions,
    }

    const algorithm: TAlgorithm = "HS256";
    const SECRET_KEY: string = "LALALALALALALA";

    let token: string = encode(payload, SECRET_KEY, algorithm);
    console.log(token);

    // Given the token, send statistics to Odin API.	
    await axios({
        method: 'post',
        url: volleyballPath,
        responseType: 'application/json',
        data: gameStatistics,
        headers: {
            'Authorization': "Bearer " + token
        }
    }).then(function (response: any) {
        console.log(response.data);
        return true;
    }).catch((error: any) => {
        console.log("postVolleyballResults posting results error: " + error);
    });

    return false;
}

// TODO -> Add cloud function documentation.	
export const volleyballGameSync = functions.database.ref("/v1/{game_id}/game-metadata/game-over")
    .onUpdate(async (change, context) => {

        /* 	
            <Section 1> 	
                This section represents the first input block from the flowchart	
                in figure F.1 of MJOLNIR's progress report #1. In this part, meta-data,	
                uprm-roster, game actions, and game score is retrieved.	
        */

        // Read the game id (event_id).	
        const gameId = context.params.game_id;
        console.log("Change detected on game-id=" + gameId);

        // Read the latest data corrsponding to the state.
        let gameState: string = "";
        let prevGameState: string = "";

        try {
            gameState = change.after.child("answer").val();
            prevGameState = change.before.child("answer").val();
        } catch (error) {
            console.log("volleyballGameSync Error: " + error);
            return null;
        }

        // If the game is not over, ignore/return.	
        if (gameState === "No") {
            // console.log("Game is not over!")	
            return null
        }

        // If the game is not over, ignore/return.
        if (gameState === "No") {
            console.log("volleyballGameSync: Game is not over! " + gameState);
            return null;
        }

        if (gameState === prevGameState) {
            console.log("volleyballGameSync: Already sync! " + prevGameState);
            return null;
        }

        // Read the sport value.	
        let sport: string = "";

        // Obtain the sport value from game metadata.	
        await admin.database().ref("/v1/" + gameId + "/game-metadata/sport").once('value').then((snapshot) => {
            sport = snapshot.val();
        }).catch(() => {
            console.log("volleyballGameSync Errpr: could not retrieve sport from game metadata.");
            return null;
        });


        // Note: Even though for this phase only volleyball is implemented,	
        //       it is important to validate that the sport is volleyball.	
        //       This way, this function can work when other sports are added.	
        if (sport !== "Voleibol") {
            console.log("volleyballGameSync Error: Not a volleyball game! (" + sport + ")");
            return null;
        }

        // Obtain game score based on sets won by each team.
        let uprmScore: number = 0;
        let opponentScore: number = 0;

        await admin.database().ref("/v1/" + gameId + "/score").once('value').then((snapshot) => {
            // Find the score on each quarter and calculate the number of quarter won by each team.	
            for (let i = 1; i <= 5; i++) {

                const uprmPoints: number = snapshot.child("set" + i + "-uprm").val();
                const opponentPoints: number = snapshot.child("set" + i + "-opponent").val();

                if (uprmPoints > opponentPoints) {
                    uprmScore++;
                }

                if (uprmPoints < opponentPoints) {
                    opponentScore++;
                }
            }
        }).catch(() => {
            console.log("volleyballGameSync Error: Unable to retrieve score.");
            return null;
        });

        // If the game is marked as over and is a volleyball game, start sync process.	

        /*	
            <Section 2>	
                This section represents the first process block of the flowchart in which	
                uprm-player-stats (uprmPlayerStats in code) and uprm-stats (uprmStats) are	
                initialized. Note that in this implementation, when the game actions are	
                retrieved, uprmPlayerStats and uprmStats collections are being modified.	
        */

        // Initialize Variables.	
        let uprmPlayerStats: VolleyballStatsEntry[] = [];
        let uprmPlayerKeys: string[] = [];
        let uprmStats: VolleyballStatsEntry = new VolleyballStatsEntry();

        // Retrieve UPRM roster from RTDB.	
        await admin.database().ref("/v1/" + gameId + "/uprm-roster").once('value').then((snapshot) => {
            // Insert athlete VolleyballStatsEntry into the uprmPlayerStats map.	
            snapshot.forEach((athleteSnap) => {
                const athleteKey: string = <string>athleteSnap.key;
                uprmPlayerKeys.push(athleteKey);
                uprmPlayerStats.push(new VolleyballStatsEntry());
            });
        }).catch(() => {
            console.log("volleyballGameSync Error: Unable to retrieve UPRM roster.");
            return null;
        });

        console.log(uprmPlayerStats);

        // Retrieve game actions and per each game action modify uprmPlayerStats and uprmStats.	
        // The conditional branches in the following code segment follow the flowchart for the	
        // Volleyball Game Sync process specified in progress report #1 for MJOLNIR.	
        await admin.database().ref("/v1/" + gameId + "/game-actions").once('value').then((snapshot) => {
            // Update uprmPlayerStats and uprmStats based on each volleyball play (from game actions).	
            snapshot.forEach((gameAction) => {

                const actionType: string = <string>gameAction.child("action_type").val();

                // Update statistics only if it is a play corresponding to UPRM team.	
                if (actionType !== "Notification") {
                    const team: string = <string>gameAction.child("team").val();

                    if (team === "uprm") {
                        const player: string = <string>gameAction.child("athlete_id").val();
                        let index = -1;
                        for (let i = 0; i < uprmPlayerKeys.length; i++) {
                            if (uprmPlayerKeys[i] == player) {
                                index = i;
                            }
                        }
                        if (index >= 0) {
                            updateVolleyballStats(actionType, uprmPlayerStats[index], uprmStats);
                        } else {
                            console.log("ATHLETE NOT FOUND " + player);
                        }
                    }
                }
            });
        }).catch(() => {
            console.log("volleyballGameSync Error: Unable to retrieve game actions.");
            return null;
        });

        // Prepare uprmPlayerStats to be added into the request payload.	
        let athleteStats: any = [];
        for (let i = 0; i < uprmPlayerKeys.length; i++) {
            athleteStats.push(
                {
                    "athlete_id": uprmPlayerKeys[i],
                    "statistics": uprmPlayerStats[i].getJSON()
                }
            );
        }

        /*	
            <Section 3>	
                In this section, all the statistics have been calculated. The only	
                missing task is to build the JSON payload and send the HTTPS request	
                to Odin API.	
        */

        // Prepare payload.	
        const gameStatistics = <JSON><unknown>{
            "event_id": gameId,
            "team_statistics": uprmStats.getJSON(),
            "athlete_statistics": JSON.stringify(athleteStats),
            "uprm_score": uprmScore,
            "opponent_score": opponentScore
        };

        console.log(gameStatistics);

        // Send game statistics to Odin API.	
        postVolleyballResults(gameStatistics).then(() => {
            console.log("POSTED");
        }).catch(error => {
            console.log(error);
        })

        // End of volleyballGameSync process.	
        return;
    });

// postVolleyballResults(JSON.parse("{ \"val_1\": 23 }"));