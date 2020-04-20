import { VolleyballStatsEntry } from './index';
import { updateVolleyballStats } from './index';
import { VolleyballPlays } from './index';


// For this test non valid plays will be sent to the updateVolleyballStats function (for athlete 1).
// Therefore, the expected output is all statistics set to 0.
const expectedAthelete1 = JSON.stringify({
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

// For this test, the case in which a second athlete makes two valid plays (kill points).
// Even though errors are issued, the remaining statistics are calculated.
const expectedTeamAthlete2 = JSON.stringify({
    "volleybal_statistics": {
        "kill_points": 2,
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
let athlete2: VolleyballStatsEntry = new VolleyballStatsEntry();
let teamStats: VolleyballStatsEntry = new VolleyballStatsEntry();

// Insert invalid game action, a notification, and two kill points.
updateVolleyballStats("AN_INVALID_GAME_ACTION", athlete1, teamStats);
updateVolleyballStats("Notification", athlete1, teamStats);
updateVolleyballStats("AN_INVALID_GAME_ACTION", athlete2, teamStats);
updateVolleyballStats(VolleyballPlays.KillPoint, athlete2, teamStats);
updateVolleyballStats("Notification", athlete2, teamStats);
updateVolleyballStats(VolleyballPlays.KillPoint, athlete2, teamStats);

// Obtain and display outputs of athlete1, athlete2 and teamStats.
const athlete1Output = athlete1.getJSON();
const athlete2Output = athlete2.getJSON();
const teamStatsOutput = teamStats.getJSON();

console.log(athlete1Output);
console.log(athlete2Output);
console.log(teamStatsOutput);

// Validate if the test passes.
if (JSON.stringify(athlete1Output) === expectedAthelete1 && JSON.stringify(teamStatsOutput) === expectedTeamAthlete2 && JSON.stringify(athlete2Output) === expectedTeamAthlete2) {
    console.log("UpdateVolleyballStatsMEDTest: PASSED");
} else {
    console.log("UpdateVolleyballStatsMEDTest: FAILED");
}