export default {
    async getEvents({ commit}) {
        try {
            const response = await this.$axios.get('events/')
            commit("SET_EVENTS", response.data.Events)
            commit("SET_EVENT",null)

        }catch(error){
            console.log(error.response.data.Error)

        }
    },

    async getEventByID({commit},eid) {
        try{
            const response = await this.$axios.get('events/'+eid+'/')
            commit("SET_EVENT",response.data.Event)            

        }catch(error){
            console.log(error.response.data.Error)
        }
    },
    
     
}