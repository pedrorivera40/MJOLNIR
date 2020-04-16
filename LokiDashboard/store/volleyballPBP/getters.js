
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
                if (state.oppSets[i - 1] > state.uprmSets[i - 1]) {
                    score++;
                }
            }
            return score;
        }
    },
    uprmStatistics: state => {
        let result = {
            killPoints: 0,
            aces: 0,
            blockPoints: 0,
            assists: 0,
            blocks: 0,
            digs: 0,
            attackErrors: 0,
            serviceErrors: 0,
            blockingErrors: 0,
            receptionErrors: 0
        };

        for (let index in state.gameActions) {
            let currentAction = state.gameActions[index];
            if (currentAction.team !== "uprm") {
                continue;
            }
            switch (currentAction.action_type) {
                case "KillPoint":
                    result.killPoints++;
                    break;

                case "Ace":
                    result.aces++;
                    break;

                case "BlockPoint":
                    result.blockPoints++;
                    break;

                case "Assist":
                    result.assists++;
                    break;

                case "Block":
                    result.blocks++;
                    break;

                case "Dig":
                    result.digs++;
                    break;

                case "AttackError":
                    result.attackErrors++;
                    break;

                case "ServiceError":
                    result.serviceErrors++;
                    break;

                case "BlockingError":
                    result.blockingErrors++;
                    break;

                case "ReceptionError":
                    result.receptionErrors++;
                    break;

                default:
                    break;
            }
        }

        return result;
    },

    oppStatistics: state => {
        let result = {
            killPoints: 0,
            aces: 0,
            blockPoints: 0,
            assists: 0,
            blocks: 0,
            digs: 0,
            attackErrors: 0,
            serviceErrors: 0,
            blockingErrors: 0,
            receptionErrors: 0
        };

        for (let index in state.gameActions) {
            let currentAction = state.gameActions[index];
            if (currentAction.team !== "opponent") {
                continue;
            }
            switch (currentAction.action_type) {
                case "KillPoint":
                    result.killPoints++;
                    break;

                case "Ace":
                    result.aces++;
                    break;

                case "BlockPoint":
                    result.blockPoints++;
                    break;

                case "Assist":
                    result.assists++;
                    break;

                case "Block":
                    result.blocks++;
                    break;

                case "Dig":
                    result.digs++;
                    break;

                case "AttackError":
                    result.attackErrors++;
                    break;

                case "ServiceError":
                    result.serviceErrors++;
                    break;

                case "BlockingError":
                    result.blockingErrors++;
                    break;

                case "ReceptionError":
                    result.receptionErrors++;
                    break;

                default:
                    break;
            }
        }

        return result;
    },


    // uprmAthleteStatistics: state => state.uprmAthleteStatistics, 
    // oppStatistics: state => state.oppStatistics, 
    // oppAthleteStatistics: state => state.oppAthleteStatistics, 

}