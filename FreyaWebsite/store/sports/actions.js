export default {

    // Queries all sports from Odin API.
    async getAllSports({ commit }) {
        try {
            commit("CLEAR_SPORTS")
            const response = await this.$axios.get('sports');
            const sports = response.data.SPORTS
            const sportsMasculino = sports.filter(sport => sport.branch_name === "Masculino");
            const sportsFemenino = sports.filter(sport => sport.branch_name === "Femenino");
            const sportsExhibicion = sports.filter(sport => sport.branch_name === "Exhibicion");
            commit("SET_SPORTS", sports);
            commit("SET_SPORTS_MASCULINO", sportsMasculino);
            commit("SET_SPORTS_FEMENINO", sportsFemenino);
            commit("SET_SPORTS_EXHIBICION", sportsExhibicion);
        } catch (error) {
            console.log(error);
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
            const response = await this.$axios.get('sports?branch=Femenino');
            commit("SET_SPORTS", response.data.SPORTS)
        } catch (error) {
            console.log(error.response.data.ERROR);
        }
    },

    // Queries all sports corresponding to the exhibition branch.
    async getSportsExhibicion({ commit }) {
        try {
            const response = await this.$axios.get('sports?branch=Exhibicion');
            commit("SET_SPORTS", response.data.SPORTS)
        } catch (error) {
            console.log(error.response.data.ERROR);
        }
    },

}