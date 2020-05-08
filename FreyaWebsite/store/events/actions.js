export default {
    /**
     * Action to fetch all events from the datadase
     * @param {*} param0 destructuring of vuex context object
     */
    async getEvents({ commit}) {
        try {
            const response = await this.$axios.get('events/')
            commit("SET_EVENTS", response.data.Events)
            commit("SET_EVENT",null)

        }catch(error){
            if(!!error.response.data){
                dispatch('notifications/setSnackbar', {text: error.response.data.Error, color: 'error'}, {root: true})
            }else{
                dispatch('notifications/setSnackbar', {text: error.message, color: 'error'}, {root: true})
            }

        }
    },

    /**
     * Action to fetch an event by their id from the database
     * @param {*} param0 destructuring of vuex context object
     * @param {*} eid id of the event being fetched
     */
    async getEventByID({commit},eid) {
        try{
            const response = await this.$axios.get('events/'+eid+'/')
            commit("SET_EVENT",response.data.Event)            

        }catch(error){
            if(!!error.response.data){
                dispatch('notifications/setSnackbar', {text: error.response.data.Error, color: 'error'}, {root: true})
            }else{
                dispatch('notifications/setSnackbar', {text: error.message, color: 'error'}, {root: true})
            }
        }
    },
    
     
}