import { VolleyballStatsEntry } from './index';

const stats = [
    3, // kills
    7, // attackErrors
    5, // assists
    11, // aces
    13, // serviceErrors
    2, // digs
    19, // blocks
    17, // blockPoints
    23, // blockingErrors
    31 // receptionErrors
];

const expectedOutput = JSON.stringify({
    "volleybal_statistics": {
        "kill_points": stats[0],
        "attack_errors": stats[1],
        "assists": stats[2],
        "aces": stats[3],
        "service_errors": stats[4],
        "digs": stats[5],
        "blocks": stats[6] + stats[7],
        "blocking_points": stats[7],
        "blocking_errors": stats[8],
        "reception_errors": stats[9]
    }
});

let entry: VolleyballStatsEntry = new VolleyballStatsEntry();

for (let i = 0; i < stats[0]; i++) {
    entry.kill();
}

for (let i = 0; i < stats[1]; i++) {
    entry.attackError();
}

for (let i = 0; i < stats[2]; i++) {
    entry.assist();
}

for (let i = 0; i < stats[3]; i++) {
    entry.ace();
}

for (let i = 0; i < stats[4]; i++) {
    entry.serviceError();
}

for (let i = 0; i < stats[5]; i++) {
    entry.dig();
}

for (let i = 0; i < stats[6]; i++) {
    entry.block();
}

for (let i = 0; i < stats[7]; i++) {
    entry.blockPoint();
}

for (let i = 0; i < stats[8]; i++) {
    entry.blockingError();
}

for (let i = 0; i < stats[9]; i++) {
    entry.receptionError();
}

// Get actual output and display expected vs actual outputs.
const actualOutput = JSON.stringify(entry.getJSON());
console.log("VolleyballStatsEntryTester: EXPECTED_OUTPUT = " + expectedOutput);
console.log("VolleyballStatsEntryTester: ACTUAL_OUTPUT = " + actualOutput);

// Display Test Result.
if (actualOutput === expectedOutput) {
    console.log("VolleyballStatsEntryTester: PASSED");
} else {
    console.log("VolleyballStatsEntryTester: FAILED");
}
