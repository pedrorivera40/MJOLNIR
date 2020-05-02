export default {
    // Queries all sports from Odin API.
    async getAllSports({ commit }) {
        try {
            commit("CLEAR_SPORTS")
            const response = await this.$axios.get('sports');
            commit("SET_SPORTS", response.data.SPORTS)
        } catch (error) {
            console.log(error.response.data.ERROR);
        }
    },

    // Queries all sports corresponding to the male branch.
    async getSportsMasculino({ commit }) {
        try {
            commit("CLEAR_SPORTS")
            const response = await this.$axios.get('sports?branch=Masculino');
            commit("SET_SPORTS", response.data.SPORTS)
        } catch (error) {
            console.log(error.response.data.ERROR);
        }
    },

    // Queries all sports corresponding to the female branch.
    async getSportsFemenino({ commit }) {
        try {
            commit("CLEAR_SPORTS")
            const response = await this.$axios.get('sports?branch=Femenino');
            commit("SET_SPORTS", response.data.SPORTS)
        } catch (error) {
            console.log(error.response.data.ERROR);
        }
    },

    // Queries all sports corresponding to the exhibition branch.
    async getSportsExhibicion({ commit }) {
        try {
            commit("CLEAR_SPORTS")
            const response = await this.$axios.get('sports?branch=Exhibicion');
            commit("SET_SPORTS", response.data.SPORTS)
        } catch (error) {
            console.log(error.response.data.ERROR);
        }
    },
}