export default {
    // Queries all sports from Odin API.
    async getAllSports({ commit, dispatch }) {
        try {
            commit("CLEAR_SPORTS")
            const response = await this.$axios.get('sports');
            commit("SET_SPORTS", response.data.SPORTS)
            return true;
        } catch (error) {
            if (!!error.response) {
                dispatch('notifications/setSnackbar', { text: error.response.data.Error, color: 'error' }, { root: true })
            } else {
                dispatch('notifications/setSnackbar', { text: error.message, color: 'error' }, { root: true })
            }
            return false;
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
            commit("CLEAR_SPORTS")
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
            commit("CLEAR_SPORTS")
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