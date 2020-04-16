
// TODO -> Update these getter methods based on the new state.js.
export default {
    currentSet: state => state.currentSet,
    // UPRM Sets Score.
    uprmSet1: state => state.uprmSet1,
    uprmSet2: state => state.uprmSet2,
    uprmSet3: state => state.uprmSet3,
    uprmSet4: state => state.uprmSet4,
    uprmSet5: state => state.uprmSet5,
    // Opponent Team Current Score.
    oppSet1: state => state.oppSet1,
    oppSet2: state => state.oppSet2,
    oppSet3: state => state.oppSet3,
    oppSet4: state => state.oppSet4,
    oppSet5: state => state.oppSet5,

    uprmRoster: state => state.uprmRoster,
    oppRoster: state => state.oppRoster,
    gameOver: state => state.gameOver,
    oppColor: state => state.oppColor,
    gameActions: state => state.gameActions,
    // uprmScores: (state) => state.uprmScore,
    // oppScores: (state) => state.oppScore,
    // uprmStatistics: state => state.uprmStatistics,
    // uprmAthleteStatistics: state => state.uprmAthleteStatistics, 
    // oppStatistics: state => state.oppStatistics, 
    // oppAthleteStatistics: state => state.oppAthleteStatistics, 

}