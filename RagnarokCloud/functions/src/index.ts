import * as functions from 'firebase-functions';
import * as admin from 'firebase-admin'

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
class VoleyballStatsEntry {

    // Statistics of interest for volleyball.
    private killPoints: number = 0;
    private attackErrors: number = 0;
    private assists: number = 0;
    private aces: number = 0;
    private serviceErrors: number = 0;
    private digs: number = 0;
    private blocks: number = 0;
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
                "blocking_errors": this.blockingErrors,
                "reception_errors": this.receptionErrors
            }
        };
    }

}


// TODO -> Add function documentation.
export const volleyballGameSync = functions.database.ref("/v1/{game_id}/game-metadata/game-ended")
    .onUpdate(async (change, context) => {
        // Read the game id (event_id).
        const gameId = context.params.game_id;
        console.log("Change detected on game-id=" + gameId);

        // Read the latest data corrsponding to the state.
        let gameState: string = "";

        try {
            gameState = change.after.child("answer").val();
        } catch (error) {
            console.log("volleyballGameSync Error: " + error);
            return null;
        }

        // If the game is not over, ignore/return.
        if (gameState === "No") {
            console.log("Game is not over! " + gameState);
            return null;
        }

        // Read the sport value.
        let sport: string = "";

        // Attempt to obtain the sport value from game metadata.
        try {
            await admin.database().ref("/v1/" + gameId + "/game-metadata/sport").once('value').then((snapshot) => {
                sport = snapshot.val();
            }).catch(() => {
                console.log("ERROR: could not retrieve sport from game metadata.");
            });
        } catch (error) {
            console.log("volleyballGameSync Error: " + error);
            return null;
        }

        // Note: Even though for this phase only volleyball is implemented,
        //       it is important to validate that the sport is volleyball.
        //       This way, this function can work when other sports are added.
        if (sport !== "Voleibol") {
            console.log("Not a volleyball game! " + sport);
            return null;
        }

        // If the game is marked as over and is a volleyball game, start sync process.

        // Following Volleyball Game Sync Cloud Function Flowchart.
        // Refer to MJOLNIR's Progress Resport #1, figure F.1

        // Initialize Variables.
        let uprmPlayerStats: Map<string, VoleyballStatsEntry> = new Map();
        // let uprmStats: VoleyballStatsEntry = new VoleyballStatsEntry();

        // Retrieve UPRM roster from database and add them to uprmPlayerStats.
        admin.database().ref("/v1/" + gameId + "/uprm-roster").once('value').then((snapshot) => {
            //
            snapshot.forEach((athleteSnap) => {
                const athleteKey: string = <string>athleteSnap.key;
                console.log(athleteKey);
                uprmPlayerStats.set(athleteKey, new VoleyballStatsEntry());
            });
        }).catch(() => {
            console.log("It's broken...");
        });

        console.log(uprmPlayerStats.keys);

        const answer = "No"
        return change.after.ref.update({ answer });
    });