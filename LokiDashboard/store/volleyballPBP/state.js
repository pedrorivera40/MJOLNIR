
// TODO -> Add default team statistics JSON.
export default () => ({
    currentSet: 0, // Current Volleyball game set (1, 2, 3, 4, 5).
    uprmSets: [0, 0, 0, 0, 0], // UPRM set scores.
    oppSets: [0, 0, 0, 0, 0], // Opponent set scores.
    gameActions: [], // List of game actions (notifications and plays...)
    uprmRoster: [], // List of UPRM athletes for this match.
    oppRoster: [], // List of opponent athletes for this match.
    gameOver: false, // Denotes if the game is over.
    oppColor: "", // Keeps track of the opponent team color (for UI purposes).

    // uprmStatistics: {}, // Keep collective UPRM statistics for this match.
    // uprmAthleteStatistics: {}, // For each UPRM athlete, keeps their individual stats for this match.
    // oppStatistics: {}, // Keep collective opponent statistics for this match.
    // oppAthleteStatistics: {}, // For each opponent athlete, keeps their individual stats for this match.
})