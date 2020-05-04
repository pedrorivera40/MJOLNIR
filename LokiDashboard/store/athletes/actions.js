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
            const response = await this.$axios.post('athletes/',athleteJSON)
            commit("ADD_ATHLETE",response.data.Athlete)
            dispatch('notifications/setSnackbar', {text: "Se añadió un nuevo atleta exitosamente", color: 'success'}, {root: true})
            
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
            
            const response = await this.$axios.put('athletes/'+athleteJSON.athlete_id+'/',athleteJSON)
            commit("UPDATE_ATHLETE",response.data.Athlete)
            dispatch('notifications/setSnackbar', {text: `El atleta con identificador:${athleteJSON.athlete_id} ha sido editado.`, color: 'success'}, {root: true})
            
        }catch(error){
            console.log(error)
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
    },

    //Results related actions
    async getAthleteSeasonStats({commit,dispatch},stats_params){
        try{
            const response = await this.$axios.get('results/'+stats_params.sport_name+'/season/athlete_games/?athlete_id='+stats_params.athlete_id+'&season_year='+stats_params.season_year)
            //console.log(response.data)
            commit("SET_SEASON_STATS",response.data)
            dispatch('notifications/setSnackbar', {text: "Se recolectó exitosamente las estadísticas de la temporada.", color: 'success'}, {root: true})
        }catch(error){
            console.log(error)
            if(!!error.response.data){
                dispatch('notifications/setSnackbar', {text: 'Error', color: 'error'}, {root: true})
                return 'error'
            }else{
                dispatch('notifications/setSnackbar', {text: error.message, color: 'error'}, {root: true})
            }
        }

    },

    async getAthleteAggregateSeasonStats({commit,dispatch},stats_params){
        try{
            const response = await this.$axios.get('results/'+stats_params.sport_name+'/season/athlete_aggregate/?athlete_id='+stats_params.athlete_id+'&season_year='+stats_params.season_year)
            //console.log(response.data)
            commit("SET_AGGREGATE_SEASON_STATS",response.data)
            dispatch('notifications/setSnackbar', {text: "Se recolectó exitosamente las estadísticas agregadas de la temporada.", color: 'success'}, {root: true})
        }catch(error){
            console.log(error)
            if(!!error.response.data){
                dispatch('notifications/setSnackbar', {text: 'Error', color: 'error'}, {root: true})
                return 'error'
            }else{
                dispatch('notifications/setSnackbar', {text: error.message, color: 'error'}, {root: true})
            }
        }

    },
}

