export default {
    /**
     * Action to fetch all events from the datadase
     * @param {*} param0 destructuring of vuex context object
     */
    async getEvents({commit,dispatch}) {
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
    async getEventByID({commit,dispatch},eid) {
        try{
            const response = await this.$axios.get('events/'+eid+'/public/')
            commit("SET_EVENT",response.data.Event)            

        }catch(error){
            if(!!error.response.data){
                dispatch('notifications/setSnackbar', {text: error.response.data.Error, color: 'error'}, {root: true})
            }else{
                dispatch('notifications/setSnackbar', {text: error.message, color: 'error'}, {root: true})
            }
        }
    },

    /**
     * Action to fetch the teams in the database with their information.
     * @param {*} param0 destructuring of vuex context object
     */
    async getEventTeams({commit,dispatch}) {
        try{
            const response = await this.$axios.get('teams/all/')
            commit("SET_EVENT_TEAMS",response.data.Teams)            

        }catch(error){
            if(!!error.response.data){
                dispatch('notifications/setSnackbar', {text: error.response.data.Error, color: 'error'}, {root: true})
            }else{
                dispatch('notifications/setSnackbar', {text: error.message, color: 'error'}, {root: true})
            }
        }
    },

    /**
     * Action to add a new event to the system givent the information
     * in the event creation form
     * @param {*} param0 destructuring of vuex context object
     * @param {*} eventJSON Object containing the information of the event to be added.
     */
    async addEvent({commit,dispatch},eventJSON){
        try{         
            
            const response = await this.$axios.post('events/team/'+eventJSON.team_id+'/',eventJSON)            
            commit("ADD_EVENT",response.data.Event)
            dispatch('notifications/setSnackbar', {text: "Se añadió un nuevo evento exitosamente", color: 'success'}, {root: true})
            
        }catch(error){            
            if(!!error.response.data){               
                dispatch('notifications/setSnackbar', {text: error.response.data.Error, color: 'error'}, {root: true})
                return 'error'
            }else{
                dispatch('notifications/setSnackbar', {text: error.message, color: 'error'}, {root: true})
            }
        }
    },

    /**
     * Action to edit an event's information by their id and information given
     * in the event edit form
     * @param {*} param0 destructuring of a vuex context object
     * @param {*} eventJSON Object containing the information of the event to be edited.
     */
    async editEvent({commit,dispatch},eventJSON){
        try{
           
            const response = await this.$axios.put('events/'+eventJSON.event_id+'/',eventJSON)
            commit("UPDATE_EVENT",response.data.Event)
            dispatch('notifications/setSnackbar', {text: `El evento con identificador:${eventJSON.event_id} ha sido editado.`, color: 'success'}, {root: true})
            
        }catch(error){
            
            if(!!error.response.data){
                
                dispatch('notifications/setSnackbar', {text: error.response.data.Error, color: 'error'}, {root: true})
                return 'error'
            }else{
                dispatch('notifications/setSnackbar', {text: error.message, color: 'error'}, {root: true})
            }
        }
    },

    /**
     * Action to remove an event from the system given their id
     * @param {*} param0 destructuring of vuex context object
     * @param {*} eventID id of the event being removed
     */
    async removeEvent({commit,dispatch},eventID){
        try{          
            const response = await this.$axios.delete('events/'+eventID+'/')
            commit("DELETE_EVENT",eventID)
            dispatch('notifications/setSnackbar', {text: `El evento con identificador:${eventID} ha sido removido.`, color: 'success'}, {root: true})
            
        }catch(error){
            if(!!error.response.data){
                dispatch('notifications/setSnackbar', {text: error.response.data.Error, color: 'error'}, {root: true})
                return 'error'
            }else{
                dispatch('notifications/setSnackbar', {text: error.message, color: 'error'}, {root: true})
            }
        }
    },

    /**
     * Action to start a pbp sequence for an event in the system.
     * @param {*} param0 destructuring of vuex context object
     * @param {*} eventJSON Object containing the route parameters for the request.
     */
    async startPBPSequence({commit,dispatch},eventJSON){
        try{
            
            commit("SET_EVENTS",[])
            
            const response = await this.$axios.post('pbp/'+eventJSON.sport_name,{event_id:eventJSON.event_id})
            
            dispatch('notifications/setSnackbar', {text: response.data.MSG, color: 'success'}, {root: true})
            this.$router.push('/jugadas-voleibol/'+eventJSON.event_id)
        }catch(error){
            if(!!error.response.data){
                dispatch('notifications/setSnackbar', {text: error.response.data.ERROR, color: 'error'}, {root: true})
            }else{
                dispatch('notifications/setSnackbar', {text: error.message, color: 'error'}, {root: true})
            }
        }
        
    }
    
    
     
}