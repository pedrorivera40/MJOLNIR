
// TODO -> Add default team statistics JSON.
export default () => ({
    uprmSet1: 0,
    oppSet1: 0,
    // uprmScore: [0, 0, 0, 0, 0], // JSON object containing the set scores for UPRM team.
    // oppScore: [0, 0, 0, 0, 0], // JSON object containing the set scores for opponent team.
    currentSet: 0, // Current Volleyball game set (1, 2, 3, 4, 5).
    uprmRoster: [], // List of UPRM athletes for this match.
    oppRoster: [], // List of opponent athletes for this match.
    gameOver: false, // Denotes if the game is over.
    oppColor: "", // Keeps track of the opponent team color (for UI purposes).
    gameActions: [], // List of game actions (notifications and plays...)

    // uprmStatistics: {}, // Keep collective UPRM statistics for this match.
    // uprmAthleteStatistics: {}, // For each UPRM athlete, keeps their individual stats for this match.
    // oppStatistics: {}, // Keep collective opponent statistics for this match.
    // oppAthleteStatistics: {}, // For each opponent athlete, keeps their individual stats for this match.
})