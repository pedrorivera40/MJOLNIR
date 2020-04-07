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

export const sampleCloudFunction = functions.database.ref("/v1/{game_id}/game-metadata/game-ended")
    .onUpdate((change, context) => {
        // Read the game id for the change. It will be logged for quick testing purposes.
        // const gameId = context.params.game_id
        // console.log("Change detected on game-id=" + gameId)

        // Read the latest data corrsponding to the state.
        const gameState = change.after.child("answer").val()

        // If the game is not over, ignore/return.
        if (gameState === "No") {
            // console.log("Game is not over!")
            return null
        }

        // If the game is marked as over, reject that change by re-writting in the database "No".
        const answer = "No"
        return change.after.ref.update({ answer });

    });