export default {

    UPDATE_UPRM_SET1(state, score) {
        state.uprmSet1 = score;
    },

    UPDATE_UPRM_SET2(state, score) {
        state.uprmSet2 = score;
    },

    UPDATE_UPRM_SET3(state, score) {
        state.uprmSet3 = score;
    },

    UPDATE_UPRM_SET4(state, score) {
        state.uprmSet4 = score;
    },

    UPDATE_UPRM_SET5(state, score) {
        state.uprmSet5 = score;
    },

    UPDATE_OPP_SET1(state, score) {
        state.oppSet1 = score;
    },

    UPDATE_OPP_SET2(state, score) {
        state.oppSet2 = score;
    },

    UPDATE_OPP_SET3(state, score) {
        state.oppSet3 = score;
    },

    UPDATE_OPP_SET4(state, score) {
        state.oppSet4 = score;
    },

    UPDATE_OPP_SET5(state, score) {
        state.oppSet5 = score;
    },

    UPDATE_CURRENT_SET(state, set) {
        state.currentSet = set
    },

    ADD_UPRM_ROSTER(state, key, value) {
        state.uprmRoster.push([key, value]);
    },

    UPDATE_UPRM_ROSTER(state, key, value) {
        for (index in state.uprmRoster) {
            if (state.uprmRoster[index][0] === key) {
                state.uprmRoster[index][1] = value;
                break;
            }
        }
    },

    REMOVE_UPRM_ROSTER(state, key) {
        for (index in state.uprmRoster) {
            if (state.uprmRoster[index][0] === key) {
                state.uprmRoster = state.uprmRoster.splice(index, index + 1);
                break;
            }
        }
    },

    ADD_OPP_ROSTER(state, key, value) {
        state.oppRoster.push([key, value]);
    },

    UPDATE_OPP_ROSTER(state, key, value) {
        for (index in state.oppRoster) {
            if (state.oppRoster[index][0] === key) {
                state.oppRoster[index][1] = value;
                break;
            }
        }
    },

    REMOVE_OPP_ROSTER(state, key) {
        for (index in state.oppRoster) {
            if (state.oppRoster[index][0] === key) {
                state.oppRoster = state.oppRoster.splice(index, index + 1);
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

    ADD_GAME_ACTION(state, key, value) {
        state.gameActions.push([key, value]);
    },

    UPDATE_GAME_ACTION(state, key, value) {
        for (index in state.gameActions) {
            if (state.gameActions[index][0] === key) {
                state.gameActions[index][1] = value;
                break;
            }
        }
    },

    REMOVE_GAME_ACTION(state, key) {
        for (index in state.gameActions) {
            if (state.gameActions[index][0] === key) {
                state.gameActions = state.gameActions.splice(index, index + 1);
                break;
            }
        }
    },
}