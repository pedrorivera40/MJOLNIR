
// TODO -> Update these getter methods based on the new state.js.
export default {
    uprmSet1: state => state.uprmSet1,
    oppSet1: state => state.oppSet1,
    // uprmScores: (state) => state.uprmScore,
    // oppScores: (state) => state.oppScore,
    // uprmSetScore: (state, set) => state.setScores.uprm[set - 1],
    // oppSetScore: (state, set) => state.setScores.opp[set - 1],
    currentSet: state => state.currentSet,
    uprmRoster: state => state.uprmRoster,
    oppRoster: state => state.oppRoster,
    gameOver: state => state.gameOver,
    oppColor: state => state.oppColor,
    gameActions: state => state.gameActions,
    // uprmStatistics: state => state.uprmStatistics,
    // uprmAthleteStatistics: state => state.uprmAthleteStatistics, 
    // oppStatistics: state => state.oppStatistics, 
    // oppAthleteStatistics: state => state.oppAthleteStatistics, 

}