export default {

    UPDATE_UPRM_SET(state, entry) {
        state.uprmSets.splice(entry.set - 1, 1, entry.score);
    },

    UPDATE_OPP_SET(state, entry) {
        state.oppSets.splice(entry.set - 1, 1, entry.score);
    },

    // UPDATE_UPRM_SET1(state, score) {
    //     state.uprmSet1 = score;
    // },

    // UPDATE_UPRM_SET2(state, score) {
    //     state.uprmSet2 = score;
    // },

    // UPDATE_UPRM_SET3(state, score) {
    //     state.uprmSet3 = score;
    // },

    // UPDATE_UPRM_SET4(state, score) {
    //     state.uprmSet4 = score;
    // },

    // UPDATE_UPRM_SET5(state, score) {
    //     state.uprmSet5 = score;
    // },

    // UPDATE_OPP_SET1(state, score) {
    //     state.oppSet1 = score;
    // },

    // UPDATE_OPP_SET2(state, score) {
    //     state.oppSet2 = score;
    // },

    // UPDATE_OPP_SET3(state, score) {
    //     state.oppSet3 = score;
    // },

    // UPDATE_OPP_SET4(state, score) {
    //     state.oppSet4 = score;
    // },

    // UPDATE_OPP_SET5(state, score) {
    //     state.oppSet5 = score;
    // },

    UPDATE_CURRENT_SET(state, set) {
        state.currentSet = set
    },

    ADD_UPRM_ROSTER(state, athlete) {
        state.uprmRoster.push(athlete);
    },

    UPDATE_UPRM_ROSTER(state, athlete) {
        for (let index in state.oppRoster) {
            if (state.uprmRoster[index].key === key) {
                state.uprmRoster.splice(index, 1, athlete);
                break;
            }
        }
    },

    REMOVE_UPRM_ROSTER(state, key) {
        for (let index in state.oppRoster) {
            if (state.uprmRoster[index].key === key) {
                state.uprmRoster.splice(index, 1);
                break;
            }
        }
    },

    ADD_OPP_ROSTER(state, athlete) {
        state.oppRoster.push(athlete);
    },

    UPDATE_OPP_ROSTER(state, athlete) {
        for (let index in state.oppRoster) {
            if (state.oppRoster[index].key === key) {
                state.oppRoster.splice(index, 1, athlete);
                break;
            }
        }
    },

    REMOVE_OPP_ROSTER(state, key) {
        for (let index in state.oppRoster) {
            if (state.oppRoster[index].key === key) {
                state.oppRoster.splice(index, 1);
                break;
            }
        }
    },

    SET_GAME_OVER(state, isOver) {
        state.gameOver = isOver
    },

    SET_OPP_COLOR(state, color) {
        state.oppColor = color
    },

    ADD_GAME_ACTION(state, action) {
        state.gameActions.unshift(action);
    },

    UPDATE_GAME_ACTION(state, action) {
        for (let index in state.gameActions) {
            if (state.gameActions[index].key === action.key) {
                state.gameActions.splice(index, 1, action);
                break;
            }
        }
    },

    REMOVE_GAME_ACTION(state, key) {
        for (let index in state.gameActions) {
            if (state.gameActions[index].key === key) {
                state.gameActions.splice(index, 1);
                break;
            }
        }
    },
}