
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
        }
        return state.oppSets[state.currentSet - 1];
    },
    uprmScore: (state) => {
        if (state.currentSet <= 1) {
            return 0;
        }
        else {
            let score = 0;
            let bound = state.currentSet;
            if (state.gameOver === true) {
                bound++;
            }
            for (let i = 1; i < bound; i++) {
                if (state.uprmSets[i - 1] > state.oppSets[i - 1]) {
                    score++;
                }
            }
            return score;
        }
    },
    oppScore: (state) => {
        if (state.currentSet <= 1) {
            return 0;
        }
        else {
            let score = 0;
            let bound = state.currentSet;
            if (state.gameOver === true) {
                bound++;
            }
            for (let i = 1; i < bound; i++) {
                console.log(i);
                if (state.oppSets[i - 1] > state.uprmSets[i - 1]) {
                    score++;
                }
            }
            return score;
        }
    },
    // uprmStatistics: state => state.uprmStatistics,
    // uprmAthleteStatistics: state => state.uprmAthleteStatistics, 
    // oppStatistics: state => state.oppStatistics, 
    // oppAthleteStatistics: state => state.oppAthleteStatistics, 

}