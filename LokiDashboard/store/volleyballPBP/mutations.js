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
}