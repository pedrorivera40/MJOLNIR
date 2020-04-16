export default {

    // Modify UPRM Set Scores.
    UPDATE_UPRM_SET(state, entry) {
        state.uprmSets.splice(entry.set - 1, 1, entry.score);
    },

    // Modify opponent Set Scores.
    UPDATE_OPP_SET(state, entry) {
        state.oppSets.splice(entry.set - 1, 1, entry.score);
    },

    // Update current set value.
    UPDATE_CURRENT_SET(state, set) {
        state.currentSet = set
    },

    // Insert athlete entry into UPRM roster.
    ADD_UPRM_ROSTER(state, athlete) {
        state.uprmRoster.push(athlete);
    },

    // Update athlete entry from UPRM roster.
    UPDATE_UPRM_ROSTER(state, athlete) {
        for (let index in state.oppRoster) {
            if (state.uprmRoster[index].key === key) {
                state.uprmRoster.splice(index, 1, athlete);
                break;
            }
        }
    },

    // Remove athlete entry from UPRM roster.
    REMOVE_UPRM_ROSTER(state, key) {
        for (let index in state.oppRoster) {
            if (state.uprmRoster[index].key === key) {
                state.uprmRoster.splice(index, 1);
                break;
            }
        }
    },

    // Insert athlete entry into opponent roster.
    ADD_OPP_ROSTER(state, athlete) {
        state.oppRoster.push(athlete);
    },

    // Update athlete entry from opponent roster.
    UPDATE_OPP_ROSTER(state, athlete) {
        for (let index in state.oppRoster) {
            if (state.oppRoster[index].key === key) {
                state.oppRoster.splice(index, 1, athlete);
                break;
            }
        }
    },

    // Remove athlete entry from opponent roster.
    REMOVE_OPP_ROSTER(state, key) {
        for (let index in state.oppRoster) {
            if (state.oppRoster[index].key === key) {
                state.oppRoster.splice(index, 1);
                break;
            }
        }
    },

    // Update game over state.
    SET_GAME_OVER(state, isOver) {
        state.gameOver = isOver
    },

    // Update opponent color.
    SET_OPP_COLOR(state, color) {
        state.oppColor = color
    },

    // Insert game action into actions list.
    ADD_GAME_ACTION(state, action) {
        state.gameActions.unshift(action);
    },

    // Update value of existing action.
    UPDATE_GAME_ACTION(state, action) {
        for (let index in state.gameActions) {
            if (state.gameActions[index].key === action.key) {
                state.gameActions.splice(index, 1, action);
                break;
            }
        }
    },

    // Remove entry from existing game actions.
    REMOVE_GAME_ACTION(state, key) {
        for (let index in state.gameActions) {
            if (state.gameActions[index].key === key) {
                state.gameActions.splice(index, 1);
                break;
            }
        }
    },

    // Update UPRM team statistics based on the game actions list.
    UPDATE_UPRM_STATISTICS(state) {
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

        state.uprmStatistics = result;
    },

    // Update opponent team statistics based on the game actions list.
    UPDATE_OPP_STATISTICS(state) {
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

        state.oppStatistics = result;
    },

    // Update UPRM athlete statistics based on the game actions list.
    UPDATE_UPRM_ATHLETE_STATISTICS(state) {
        let result = [];

        for (let athlete in state.uprmRoster) {
            result.push(
                {
                    athlete_number: athlete.number,
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
                }
            );
        }

        for (let index in state.gameActions) {
            let currentAction = state.gameActions[index];
            if (currentAction.team !== "uprm") {
                continue;
            }
            let athlete_index = -1;
            for (let athlete in state.uprmRoster) {
                if (state.uprmRoster[athlete].number === currentAction.number) {
                    athlete_index = athlete;
                    break;
                }
            }
            switch (currentAction.action_type) {
                case "KillPoint":
                    result[athlete_index].killPoints++;
                    break;

                case "Ace":
                    result[athlete_index].aces++;
                    break;

                case "BlockPoint":
                    result[athlete_index].blockPoints++;
                    break;

                case "Assist":
                    result[athlete_index].assists++;
                    break;

                case "Block":
                    result[athlete_index].blocks++;
                    break;

                case "Dig":
                    result[athlete_index].digs++;
                    break;

                case "AttackError":
                    result[athlete_index].attackErrors++;
                    break;

                case "ServiceError":
                    result[athlete_index].serviceErrors++;
                    break;

                case "BlockingError":
                    result[athlete_index].blockingErrors++;
                    break;

                case "ReceptionError":
                    result[athlete_index].receptionErrors++;
                    break;

                default:
                    break;
            }
        }

        state.uprmAthleteStatistics = result;
    },

    // Update opponent athlete statistics based on the game actions list.
    UPDATE_OPP_ATHLETE_STATISTICS(state) {
        let result = [];

        for (let athlete in state.oppRoster) {
            result.push(
                {
                    athlete_number: athlete.number,
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
                }
            );
        }

        for (let index in state.gameActions) {
            let currentAction = state.gameActions[index];
            if (currentAction.team !== "opponent") {
                continue;
            }
            let athlete_index = -1;
            for (let athlete in state.oppRoster) {
                if (state.oppRoster[athlete].number === currentAction.number) {
                    athlete_index = athlete;
                    break;
                }
            }
            switch (currentAction.action_type) {
                case "KillPoint":
                    result[athlete_index].killPoints++;
                    break;

                case "Ace":
                    result[athlete_index].aces++;
                    break;

                case "BlockPoint":
                    result[athlete_index].blockPoints++;
                    break;

                case "Assist":
                    result[athlete_index].assists++;
                    break;

                case "Block":
                    result[athlete_index].blocks++;
                    break;

                case "Dig":
                    result[athlete_index].digs++;
                    break;

                case "AttackError":
                    result[athlete_index].attackErrors++;
                    break;

                case "ServiceError":
                    result[athlete_index].serviceErrors++;
                    break;

                case "BlockingError":
                    result[athlete_index].blockingErrors++;
                    break;

                case "ReceptionError":
                    result[athlete_index].receptionErrors++;
                    break;

                default:
                    break;
            }
        }

        state.uprmAthleteStatistics = result;
    },
}