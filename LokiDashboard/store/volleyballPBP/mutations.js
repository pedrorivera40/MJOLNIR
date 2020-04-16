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

    ADD_UPRM_ROSTER(state, athlete) {
        state.uprmRoster.push(athlete);
    },

    UPDATE_UPRM_ROSTER(state, athlete) {
        for (index in state.uprmRoster) {
            if (state.uprmRoster[index].id === athlete.id) {
                state.uprmRoster[index] = athlete;
                break;
            }
        }
    },

    REMOVE_UPRM_ROSTER(state, athlete) {
        for (index in state.uprmRoster) {
            if (state.uprmRoster[index].id === athlete.id) {
                state.uprmRoster = state.uprmRoster.splice(index, index + 1);
                break;
            }
        }
    },

    ADD_OPP_ROSTER(state, athlete) {
        state.oppRoster.push(athlete);
    },

    UPDATE_OPP_ROSTER(state, athlete) {
        for (index in state.oppRoster) {
            if (state.oppRoster[index].id === athlete.id) {
                state.oppRoster[index] = athlete;
                break;
            }
        }
    },

    REMOVE_OPP_ROSTER(state, athlete) {
        for (index in state.uprmRoster) {
            if (state.oppRoster[index].id === athlete.id) {
                state.oppRoster = state.oppRoster.splice(index, index + 1);
                break;
            }
        }
    },

    SET_GAME_OVER(state, isOver) {
        state.gameOver = isOver
    },

    // SET_OPP_COLOR(state, color) {
    //     state.oppColor = color
    // },
}