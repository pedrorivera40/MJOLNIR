export default {
    SET_SPORTS(state, sports) {
        state.sports = sports;
    },

    SET_SPORTS_MASCULINO(state, sports) {
        state.sportsMasculino = sports;
    },

    SET_SPORTS_FEMENINO(state, sports) {
        state.sportsFemenino = sports;
    },

    SET_SPORTS_EXHIBICION(state, sports) {
        state.sportsExhibicion = sports;
    },

    CLEAR_SPORTS(state) {
        state.sports = [];
        state.sportsMasculino = [];
        state.sportsFemenino = [];
        state.sportsExhibicion = [];
    },
}