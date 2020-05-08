export default{

    /**
     * Action to fetch all athletes from the database 
     * @param {*} param0  destructuring of vuex context object
     */
    async getAthletes( {commit} ){
        try{
           
            const response = await this.$axios.get('athletes/')
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
    async getAthleteByID({commit},aid){
        try{
            
            const response = await this.$axios.get('athletes/'+aid+'/')
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

