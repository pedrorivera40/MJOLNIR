export default {

    // Queries all sports from Odin API.
    async getAllSports({ commit, dispatch }) {
        try {
            commit("CLEAR_SPORTS")
            const response = await this.$axios.get('sports');
            const sports = response.data.SPORTS
            const sportsMasculino = sports.filter(sport => sport.branch_name === "Masculino");
            const sportsFemenino = sports.filter(sport => sport.branch_name === "Femenino");
            const sportsExhibicion = sports.filter(sport => sport.branch_name === "Exhibición");
            commit("SET_SPORTS", sports);
            commit("SET_SPORTS_MASCULINO", sportsMasculino);
            commit("SET_SPORTS_FEMENINO", sportsFemenino);
            commit("SET_SPORTS_EXHIBICION", sportsExhibicion);
        } catch (error) {
            if (!!error.response) {
                dispatch('notifications/setSnackbar', { text: error.response.data.Error, color: 'error' }, { root: true })
            } else {
                dispatch('notifications/setSnackbar', { text: error.message, color: 'error' }, { root: true })
            }
        }
    },

    // Queries all sports corresponding to the male branch.
    async getSportsMasculino({ commit, dispatch }) {
        try {
            commit("CLEAR_SPORTS")
            const response = await this.$axios.get('sports?branch=Masculino');
            commit("SET_SPORTS", response.data.SPORTS)
        } catch (error) {
            if (!!error.response) {
                dispatch('notifications/setSnackbar', { text: error.response.data.Error, color: 'error' }, { root: true })
            } else {
                dispatch('notifications/setSnackbar', { text: error.message, color: 'error' }, { root: true })
            }
        }
    },

    // Queries all sports corresponding to the female branch.
    async getSportsFemenino({ commit, dispatch }) {
        try {
            const response = await this.$axios.get('sports?branch=Femenino');
            commit("SET_SPORTS", response.data.SPORTS)
        } catch (error) {
            if (!!error.response) {
                dispatch('notifications/setSnackbar', { text: error.response.data.Error, color: 'error' }, { root: true })
            } else {
                dispatch('notifications/setSnackbar', { text: error.message, color: 'error' }, { root: true })
            }
        }
    },

    // Queries all sports corresponding to the exhibition branch.
    async getSportsExhibicion({ commit, dispatch }) {
        try {
            const response = await this.$axios.get('sports?branch=Exhibicion');
            commit("SET_SPORTS", response.data.SPORTS)
        } catch (error) {
            if (!!error.response) {
                dispatch('notifications/setSnackbar', { text: error.response.data.Error, color: 'error' }, { root: true })
            } else {
                dispatch('notifications/setSnackbar', { text: error.message, color: 'error' }, { root: true })
            }
        }
    },

}