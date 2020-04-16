export default {

    UPDATE_UPRM_SET_SCORES(state, set, score) {
        state.setScores.uprm[set] = score;
    },

    UPDATE_OPP_SET_SCORES(state, set, score) {
        state.setScores.opp[set] = score;
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
}