
// TODO -> Update these getter methods based on the new state.js.
export default {
    uprmSetScore: (state, set) => state.setScores.uprm[set],
    oppSetScore: (state, set) => state.setScores.opp[set],
    currentSet: state => state.currentSet,
    uprmRoster: state => state.uprmRoster,
    oppRoster: state => state.oppRoster,
    gameOver: state => state.gameOver,
    oppColor: state => state.oppColor,
    // uprmStatistics: state => state.uprmStatistics,
    // uprmAthleteStatistics: state => state.uprmAthleteStatistics, 
    // oppStatistics: state => state.oppStatistics, 
    // oppAthleteStatistics: state => state.oppAthleteStatistics, 
    // gameActions: state => state.gameActions, 
}