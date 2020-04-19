import { VolleyballStatsEntry } from './index';
import { updateVolleyballStats } from './index';

// For this test non valid plays will be sent to the updateVolleyballStats function.
// Therefore, the expected output is all statistics set to 0.
const expectedOutput = JSON.stringify({
    "volleybal_statistics": {
        "kill_points": 0,
        "attack_errors": 0,
        "assists": 0,
        "aces": 0,
        "service_errors": 0,
        "digs": 0,
        "blocks": 0,
        "block_points": 0,
        "blocking_errors": 0,
        "reception_errors": 0
    }
});

let athlete1: VolleyballStatsEntry = new VolleyballStatsEntry();
let teamStats: VolleyballStatsEntry = new VolleyballStatsEntry();

// Insert an invalid game action, and a notification. 
updateVolleyballStats("AN_INVALID_GAME_ACTION", athlete1, teamStats);
updateVolleyballStats("Notification", athlete1, teamStats);

// Obtain and display outputs of athlete1 and teamStats.
const athlete1Output = athlete1.getJSON();
const teamStatsOutput = teamStats.getJSON();

console.log(athlete1Output);
console.log(teamStatsOutput);

// Validate if the test passes.
if (JSON.stringify(athlete1Output) === expectedOutput && JSON.stringify(teamStatsOutput) === expectedOutput) {
    console.log("UpdateVolleyballStatsBADTest: PASSED");
} else {
    console.log("UpdateVolleyballStatsBADTest: FAILED");
}