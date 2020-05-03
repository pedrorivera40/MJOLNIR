export default{
    async getAthletes( {commit,dispatch} ){
        try{
           
            const response = await this.$axios.get('athletes/')
            commit("SET_ATHLETES",response.data.Athletes)
            commit("SET_ATHLETE",null)

        }catch(error){
            if(!!error.response.data){
                dispatch('notifications/setSnackbar', {text: error.response.data.Error, color: 'error'}, {root: true})
            }else{
                dispatch('notifications/setSnackbar', {text: error.message, color: 'error'}, {root: true})
            }
        }
    },

    async getAthleteByID({commit,dispatch},aid){
        try{
            
            const response = await this.$axios.get('athletes/'+aid+'/')
            commit("SET_ATHLETE",response.data.Athlete)
            
        }catch(error){            
            if(!!error.response.data){
                dispatch('notifications/setSnackbar', {text: error.response.data.Error, color: 'error'}, {root: true})
            }else{
                dispatch('notifications/setSnackbar', {text: error.message, color: 'error'}, {root: true})
            }
        }
    },
    async getAthleteSports( {commit,dispatch} ){
        try{
           
            const response = await this.$axios.get('sports/details')
            commit("SET_ATHLETE_SPORTS",response.data.SPORTS)           

        }catch(error){
            if(!!error.response.data){
                dispatch('notifications/setSnackbar', {text: error.response.data.Error, color: 'error'}, {root: true})
            }else{
                dispatch('notifications/setSnackbar', {text: error.message, color: 'error'}, {root: true})
            }
        }
    },

    async addAthlete({commit,dispatch},athleteJSON){
        try{
            commit("SET_ATHLETES",[])
            
            const response = await this.$axios.post('athletes/',athleteJSON)
            dispatch('notifications/setSnackbar', {text: response.data.Athlete, color: 'success'}, {root: true})
            
        }catch(error){
            if(!!error.response.data){
                dispatch('notifications/setSnackbar', {text: error.response.data.Error, color: 'error'}, {root: true})
                return 'error'
            }else{
                dispatch('notifications/setSnackbar', {text: error.message, color: 'error'}, {root: true})
            }
        }
    },

    async editAthlete({commit,dispatch},athleteJSON){
        try{
            commit("SET_ATHLETES",[])
            
            const response = await this.$axios.put('athletes/'+athleteJSON.athlete_id+'/',athleteJSON)
            dispatch('notifications/setSnackbar', {text: response.data.Athlete, color: 'success'}, {root: true})
            
        }catch(error){
            if(!!error.response.data){
                dispatch('notifications/setSnackbar', {text: error.response.data.Error, color: 'error'}, {root: true})
                'return error'
            }else{
                dispatch('notifications/setSnackbar', {text: error.message, color: 'error'}, {root: true})
            }
        }
    },




    async removeAthlete({commit,dispatch},athleteID){
        try{           
            
            const response = await this.$axios.delete('athletes/'+athleteID+'/')
            commit("DELETE_ATHLETE",athleteID)
            dispatch('notifications/setSnackbar', {text: response.data.Athlete, color: 'success'}, {root: true})
            
        }catch(error){
            if(!!error.response.data){
                dispatch('notifications/setSnackbar', {text: error.response.data.Error, color: 'error'}, {root: true})
                return 'error'
            }else{
                dispatch('notifications/setSnackbar', {text: error.message, color: 'error'}, {root: true})
            }
        }
    }
}

