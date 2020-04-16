
// TODO -> Update these getter methods based on the new state.js.
export default {
    currentSet: state => state.currentSet,
    // UPRM Sets Score.
    uprmSets: state => state.uprmSets,
    // Opponent Team Current Score.
    oppSets: state => state.oppSets,
    uprmRoster: state => state.uprmRoster,
    oppRoster: state => state.oppRoster,
    gameOver: state => state.gameOver,
    oppColor: state => state.oppColor,
    gameActions: state => state.gameActions,
    currentUPRMSet: state => {
        if (state.currentSet === 0) {
            return 0;
        } else {
            return state.uprmSets[state.currentSet - 1];
        }
    },
    currentOppSet: state => {
        if (state.currentSet === 0) {
            return 0;
        } else {
            return state.oppSets[state.currentSet - 1];
        }
    },
    // uprmScore: (state) => {
    //     state.uprmScore
    // },
    // oppScore: (state) => { state.oppScore },
    // uprmStatistics: state => state.uprmStatistics,
    // uprmAthleteStatistics: state => state.uprmAthleteStatistics, 
    // oppStatistics: state => state.oppStatistics, 
    // oppAthleteStatistics: state => state.oppAthleteStatistics, 

}