import * as functions from 'firebase-functions';

/*
    This file contains the Cloud Functions required for the development of Huella Deportiva Web.
    @author Pedro Luis Rivera Gomez - pedrorivera40
*/

// This function is written for learning purposes.
// Its goal is to react to changes in a path of the Realtime Database, to simulate
// rejecting the change (if a new value is present, replace it by the old value).
// In this case that is performed over the game_ended child inside the metadata
// corresponding to a game. For details, refer to the NoSQL structure in the progress
// report #1 for MJOLNIR.
// export const sampleCloudFunction = functions.database.ref("/v1/{game_id}/game-metadata/game-ended")
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

enum EntryType {
    TeamEntry,
    AthleteEntry,
}

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
    constructor() { }

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

// class VolleyballAthlete {

//     // Instance variables.

//     // Player ID - This allows the system to identify a volleyball athlete
//     //             from the Odin API perspective after the sync request is sent.
//     private athleteId: string;

//     // Keeps track of a volleyball athlete statistics for the current game.
//     private athleteStats: VoleyballStatsEntry;


//     /**
//      * Initializes a VolleyballAthlete instance given its athlete identifier.
//      */
//     constructor(athleteId: string) {
//         this.athleteId = athleteId;
//         this.athleteStats = new VoleyballStatsEntry();
//     }
// }


export const volleyballGameSync = functions.database.ref("/v1/{game_id}/game-metadata/game-ended")
    .onUpdate((change, context) => {
        // Read the game id (event_id).
        const gameId = context.params.game_id;
        console.log("Change detected on game-id=" + gameId);

        // Read the latest data corrsponding to the state.
        const gameState = change.after.child("answer").val();

        // Read the sport value.
        const sport = change.after.child("sport").val();
        console.log(sport);

        // If the game is not over, ignore/return.
        if (gameState === "No") {
            console.log("Game is not over!");
            return null;
        }

        // Note: Even though for this phase only volleyball is implemented,
        //       it is important to validate that the sport is volleyball.
        //       This way, this function can work when other sports are added.
        if (sport !== "Voleibol") {
            console.log("Not a volleyball game!");
            return null;
        }

        // If the game is marked as over and is a volleyball game, start sync process.






        const answer = "No"
        return change.after.ref.update({ answer });

    });