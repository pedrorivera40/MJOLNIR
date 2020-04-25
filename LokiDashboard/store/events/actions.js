export default {
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

    async addEvent({commit,dispatch},eventJSON){
        try{
            commit("SET_EVENTS",[])
            
            const response = await this.$axios.post('events/team/'+eventJSON.team_id+'/',eventJSON)
            dispatch('notifications/setSnackbar', {text: response.data.Event, color: 'success'}, {root: true})
            //this.$router.push('/eventos/')
        }catch(error){
            if(!!error.response.data){
                dispatch('notifications/setSnackbar', {text: error.response.data.Error, color: 'error'}, {root: true})
            }else{
                dispatch('notifications/setSnackbar', {text: error.message, color: 'error'}, {root: true})
            }
        }
    },

    async editEvent({commit,dispatch},eventJSON){
        try{
            commit("SET_EVENTS",[])
            
            const response = await this.$axios.put('events/'+eventJSON.event_id+'/',eventJSON)
            dispatch('notifications/setSnackbar', {text: response.data.Event, color: 'success'}, {root: true})
            this.$router.push('/eventos/')
        }catch(error){
            if(!!error.response.data){
                dispatch('notifications/setSnackbar', {text: error.response.data.Error, color: 'error'}, {root: true})
            }else{
                dispatch('notifications/setSnackbar', {text: error.message, color: 'error'}, {root: true})
            }
        }
    },

    async removeEvent({commit,dispatch},eventID){
        try{
            commit("SET_EVENTS",[])
            
            const response = await this.$axios.delete('events/'+eventID+'/')
            dispatch('notifications/setSnackbar', {text: response.data.Event, color: 'success'}, {root: true})
            this.$router.go()
        }catch(error){
            if(!!error.response.data){
                dispatch('notifications/setSnackbar', {text: error.response.data.Error, color: 'error'}, {root: true})
            }else{
                dispatch('notifications/setSnackbar', {text: error.message, color: 'error'}, {root: true})
            }
        }
    }
    
    
     
}