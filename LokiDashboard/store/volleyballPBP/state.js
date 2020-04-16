
// TODO -> Add default team statistics JSON.
export default () => ({
    currentSet: 0, // Current Volleyball game set (1, 2, 3, 4, 5).
    // UPRM set scores.
    uprmSet1: 0,
    uprmSet2: 0,
    uprmSet3: 0,
    uprmSet4: 0,
    uprmSet5: 0,
    // Opponent set scores.
    oppSet1: 0,
    oppSet2: 0,
    oppSet3: 0,
    oppSet4: 0,
    oppSet5: 0,

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