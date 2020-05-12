export default{

    /**
     * Action to fetch all athletes from the database with 
     * detailed information like their positions and categories.
     * @param {*} param0  destructuring of vuex context object
     */
    async getAthletes( {commit,dispatch} ){
        try{
           
            const response = await this.$axios.get('athletes/details/')
            commit("SET_ATHLETES",response.data.Athletes)            

        }catch(error){
            if(!!error.response.data){
                dispatch('notifications/setSnackbar', {text: error.response.data.Error, color: 'error'}, {root: true})
            }else{
                dispatch('notifications/setSnackbar', {text: error.message, color: 'error'}, {root: true})
            }
        }
    },

    /**
     * Action to fetch an athlete by their id from the database.
     * @param {*} param0 destructuring of vuex context object
     * @param {*} aid id of the athlete being fetched
     */
    async getAthleteByID({commit,dispatch},aid){
        try{
            
            const response = await this.$axios.get('athletes/'+aid+'/public/')
            commit("SET_ATHLETE",response.data.Athlete)
            
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
     * Action to fetch the sports with their positions and categories
     * from the database.
     * @param {*} param0 destructuring of vuex context object
     */
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

    /**
     * Action to add a new athlete to the system given the information
     * in the athlete creation form
     * @param {*} param0 destructuring of vuex context object
     * @param {*} athleteJSON Object containing the information of the athlete to be added.
     */
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

    /**
     * Action to edit an athlete's information by their id and information given
     * in the athlete edit form.
     * @param {*} param0 destructuring of vuex context object
     * @param {*} athleteJSON Object containing the information of athlete to be edited.
     */
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

    /**
     * Action to remove an athlete from the system given their id.
     * @param {*} param0 destructuring of vuex context object
     * @param {*} athleteID id of the athlete being removed
     */
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

    /**
     * Action to fetch the season statistics by event for an athlete given
     * their id and season.
     * @param {*} param0 destructring of vuex context object
     * @param {*} stats_params Object containing the route parameters for the request
     */
    async getAthleteSeasonStats({commit,dispatch},stats_params){
        try{
            const response = await this.$axios.get('results/'+stats_params.sport_name+'/season/athlete_games/?athlete_id='+stats_params.athlete_id+'&season_year='+stats_params.season_year)
            //console.log(response.data)
            commit("SET_SEASON_STATS",response.data)            
        }catch(error){
            console.log(error)
            if(!!error.response.data){
                dispatch('notifications/setSnackbar', {text: error.response.data.Error, color: 'error'}, {root: true})
                return 'error'
            }else{
                dispatch('notifications/setSnackbar', {text: error.message, color: 'error'}, {root: true})
            }
        }

    },

    /**
     * Action to fetch the aggregate season statistics for an athlete given 
     * their id and season.
     * @param {*} param0 destructuring of vuex context object
     * @param {*} stats_params Object containing the route parameters for the request
     */
    async getAthleteAggregateSeasonStats({commit,dispatch},stats_params){
        try{
            const response = await this.$axios.get('results/'+stats_params.sport_name+'/season/athlete_aggregate/?athlete_id='+stats_params.athlete_id+'&season_year='+stats_params.season_year)
            //console.log(response.data)
            commit("SET_AGGREGATE_SEASON_STATS",response.data)            
        }catch(error){
            console.log(error)
            if(!!error.response.data){
                dispatch('notifications/setSnackbar', {text: error.response.data.Error, color: 'error'}, {root: true})
                return 'error'
            }else{
                dispatch('notifications/setSnackbar', {text: error.message, color: 'error'}, {root: true})
            }
        }

    },
}

