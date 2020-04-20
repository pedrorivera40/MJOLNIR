import { VolleyballStatsEntry } from './index';
import { updateVolleyballStats } from './index';
import { VolleyballPlays } from './index';

const stats = [
    3, // kills
    7, // attackErrors
    5, // assists
    11, // aces
    13, // serviceErrors
    2, // digs
    19, // blocks (Note: this represents the blocks of that player in a game, however the function will return this value plus the number of block points.)
    17, // blockPoints
    23, // blockingErrors
    31 // receptionErrors
];

// Derive statistics for athletes. 
// Statistics are based in the stats array.
// For athlete 1, all the values are subtracted by 2.
// For athlete 2, all the values are added 2.
let stats1: number[] = [];
let stats2: number[] = [];

for (let i = 0; i < stats.length; i++) {
    stats1[i] = stats[i] - 2;
    stats2[i] = stats[i] + 2;
}

const expectedAthlete1 = JSON.stringify({
    "volleybal_statistics": {
        "kill_points": stats[0] - 2,
        "attack_errors": stats[1] - 2,
        "assists": stats[2] - 2,
        "aces": stats[3] - 2,
        "service_errors": stats[4] - 2,
        "digs": stats[5] - 2,
        "blocks": (stats[6] + stats[7]) - 4,
        "block_points": stats[7] - 2,
        "blocking_errors": stats[8] - 2,
        "reception_errors": stats[9] - 2
    }
});

const expectedAthlete2 = JSON.stringify({
    "volleybal_statistics": {
        "kill_points": stats[0] + 2,
        "attack_errors": stats[1] + 2,
        "assists": stats[2] + 2,
        "aces": stats[3] + 2,
        "service_errors": stats[4] + 2,
        "digs": stats[5] + 2,
        "blocks": (stats[6] + stats[7]) + 4,
        "block_points": stats[7] + 2,
        "blocking_errors": stats[8] + 2,
        "reception_errors": stats[9] + 2
    }
});

const expectedTeam = JSON.stringify({
    "volleybal_statistics": {
        "kill_points": stats[0] * 2,
        "attack_errors": stats[1] * 2,
        "assists": stats[2] * 2,
        "aces": stats[3] * 2,
        "service_errors": stats[4] * 2,
        "digs": stats[5] * 2,
        "blocks": (stats[6] + stats[7]) * 2,
        "block_points": stats[7] * 2,
        "blocking_errors": stats[8] * 2,
        "reception_errors": stats[9] * 2
    }
});

// Define variables for two athletes and their team.
let athlete1: VolleyballStatsEntry = new VolleyballStatsEntry();
let athlete2: VolleyballStatsEntry = new VolleyballStatsEntry();
let teamStats: VolleyballStatsEntry = new VolleyballStatsEntry();

// Assign statistics values for athlete1, athlete2, and team using the updateVolleyballStats method.
const assignStatistics = function (athleteEntry: VolleyballStatsEntry, teamEntry: VolleyballStatsEntry, statistics: any) {

    for (let i = 0; i < statistics[0]; i++) {
        updateVolleyballStats(VolleyballPlays.KillPoint, athleteEntry, teamEntry);
    }

    for (let i = 0; i < statistics[1]; i++) {
        updateVolleyballStats(VolleyballPlays.AttackError, athleteEntry, teamEntry);
    }

    for (let i = 0; i < statistics[2]; i++) {
        updateVolleyballStats(VolleyballPlays.Assist, athleteEntry, teamEntry);
    }

    for (let i = 0; i < statistics[3]; i++) {
        updateVolleyballStats(VolleyballPlays.Ace, athleteEntry, teamEntry);
    }

    for (let i = 0; i < statistics[4]; i++) {
        updateVolleyballStats(VolleyballPlays.ServiceError, athleteEntry, teamEntry);
    }

    for (let i = 0; i < statistics[5]; i++) {
        updateVolleyballStats(VolleyballPlays.Dig, athleteEntry, teamEntry);
    }

    for (let i = 0; i < statistics[6]; i++) {
        updateVolleyballStats(VolleyballPlays.Block, athleteEntry, teamEntry);
    }

    for (let i = 0; i < statistics[7]; i++) {
        updateVolleyballStats(VolleyballPlays.BlockPoint, athleteEntry, teamEntry);
    }

    for (let i = 0; i < statistics[8]; i++) {
        updateVolleyballStats(VolleyballPlays.BlockingError, athleteEntry, teamEntry);
    }

    for (let i = 0; i < statistics[9]; i++) {
        updateVolleyballStats(VolleyballPlays.ReceptionError, athleteEntry, teamEntry);
    }
}

// Assign each athlete their respective stats.
assignStatistics(athlete1, teamStats, stats1);
assignStatistics(athlete2, teamStats, stats2);

// Obtain and display each athlete and their team's JSON statistics.
const athlete1Output = athlete1.getJSON();
const athlete2Output = athlete2.getJSON();
const teamOutput = teamStats.getJSON();

console.log(athlete1.getJSON());
console.log(athlete2.getJSON());
console.log(teamStats.getJSON());

// Check if the test passes.
if (JSON.stringify(athlete1Output) === expectedAthlete1 && JSON.stringify(athlete2Output) === expectedAthlete2 && JSON.stringify(teamOutput) === expectedTeam) {
    console.log("UpdateVolleyballStatsTest: PASSED");
} else {
    console.log("UpdateVolleyballStatsTest: FAILED");
}
