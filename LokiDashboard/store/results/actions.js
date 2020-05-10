export default{
    async getAllEventStatistics({commit, dispatch},stat_params){
        try{
            console.log("At the request level we have the stat params ",stat_params)
            let event_id = stat_params.event_id
            let sport_route = stat_params.sport_route
            //console.log("At the request level we have:",event_id)
            const response = await this.$axios.get('/results/'+sport_route+'/public/?event_id='+event_id)
            //console.log("GET ALL EVENT STATS",response)
            console.log("GET ALL EVENT STATS",response.data)
            commit("SET_RESULTS_PAYLOAD",response.data)
            commit("SET_QUERY_DONE")
            
        }catch(error){
            console.log("ERROR GETTING ALL EVENT STATS",stat_params,error)
            commit("SET_RESULTS_PAYLOAD",null)
            commit("SET_QUERY_DONE")
            // if(!!error.response.data){
            //     dispatch('notifications/setSnackbar', {text: error.response.data.Error, color: 'error'}, {root: true})
            // }else{
            //     dispatch('notifications/setSnackbar', {text: error.message, color: 'error'}, {root: true})
            // }
        }
    },
    async getEventInfo({commit, dispatch},event_id){
        try{
            //console.log("At the request level we have:",event_id)
            const response = await this.$axios.get('/events/'+event_id+'/public/')
            //console.log("GET EVENT INFO",response)
            console.log("GET EVENT INFO",response.data)
            commit("SET_EVENT_INFO",response.data.Event)
            commit("SET_QUERY_DONE")
            
        }catch(error){
            console.log("ERROR GETTING EVENT INFO",event_id,error)
            commit("SET_EVENT_INFO",null)
            commit("SET_QUERY_DONE")
            if(!!error.response.data){
                dispatch('notifications/setSnackbar', {text: error.response.data.Error, color: 'error'}, {root: true})
            }else{
                dispatch('notifications/setSnackbar', {text: error.message, color: 'error'}, {root: true})
            }
        }
    },
    async clearAllStats({commit, dispatch}){
        try{
            commit("SET_RESULTS_PAYLOAD",null)
        }catch(error){
            console.log("ERROR SETTING RESULTS PAYLOAD TO NULL",error)
            if(!!error.response.data){
                dispatch('notifications/setSnackbar', {text: error.response.data.Error, color: 'error'}, {root: true})
            }else{
                dispatch('notifications/setSnackbar', {text: error.message, color: 'error'}, {root: true})
            }
        }
    },
    async clearIndividualStats({commit, dispatch}){
        try{
            commit("SET_INDIVIDUAL_STATS",null)
        }catch(error){
            console.log("ERROR SETTING INDIVIDUAL STATS PAYLOAD TO NULL",error)
            if(!!error.response.data){
                dispatch('notifications/setSnackbar', {text: error.response.data.Error, color: 'error'}, {root: true})
            }else{
                dispatch('notifications/setSnackbar', {text: error.message, color: 'error'}, {root: true})
            }
        }
    },
    async clearEventInfo({commit, dispatch}){
        try{
            commit("SET_EVENT_INFO",null)
        }catch(error){
            console.log("ERROR SETTING EVENT INFO TO NULL",error)
            if(!!error.response.data){
                dispatch('notifications/setSnackbar', {text: error.response.data.Error, color: 'error'}, {root: true})
            }else{
                dispatch('notifications/setSnackbar', {text: error.message, color: 'error'}, {root: true})
            }
        }
    },
    //NEW ACTIONS FOR THE DASHBOARD INTEGRATION
    //GENERAL USE
    async setQueryLoading({commit, dispatch}){
        try{
            commit("SET_QUERY_LOADING")
        }catch(error){
            console.log("ERROR SETTING STATE VARIABLE FOR LOADING QUERY",error)
            if(!!error.response.data){
                dispatch('notifications/setSnackbar', {text: error.response.data.Error, color: 'error'}, {root: true})
            }else{
                dispatch('notifications/setSnackbar', {text: error.message, color: 'error'}, {root: true})
            }
        }
    },
    //FINAL SCORE ACTIONS
    async addFinalScore({commit,dispatch},scoreJSON){
        try{
            let sport_route = scoreJSON.sport_route
            let statistics = scoreJSON.statistics
            const response = await this.$axios.post('/results/'+sport_route+'/score/',statistics)
            commit("SET_QUERY_DONE")
            dispatch('notifications/setSnackbar', {text: "Se añadio nuevo record de Puntuacion Final de manera exitosa.", color: 'success'}, {root: true})
        }catch(error){
            commit("SET_QUERY_DONE")
            console.log("ERROR POSTING FINAL SCORE",scoreJSON,error)
            if(!!error.response.data){
                dispatch('notifications/setSnackbar', {text: error.response.data.Error, color: 'error'}, {root: true})
            }else{
                dispatch('notifications/setSnackbar', {text: error.message, color: 'error'}, {root: true})
            }
        }
    },
    async editFinalScore({commit,dispatch},scoreJSON){
        try{
            let sport_route = scoreJSON.sport_route
            let statistics = scoreJSON.statistics
            const response = await this.$axios.put('/results/'+sport_route+'/score/',statistics)
            commit("SET_QUERY_DONE")
            dispatch('notifications/setSnackbar', {text: "Se edito record de Puntuacion Final de manera exitosa.", color: 'success'}, {root: true})
        }catch(error){
            commit("SET_QUERY_DONE")
            console.log("ERROR POSTING FINAL SCORE",scoreJSON,error)
            if(!!error.response.data){
                dispatch('notifications/setSnackbar', {text: error.response.data.Error, color: 'error'}, {root: true})
            }else{
                dispatch('notifications/setSnackbar', {text: error.message, color: 'error'}, {root: true})
            }
        }
    },
    async getFinalScore({commit,dispatch},scoreJSON){
        try{
            let sport_route = scoreJSON.sport_route
            let event_id = scoreJSON.event_id
            const response = await this.$axios.get('/results/'+sport_route+'/score/public/?event_id='+event_id)
            console.log("GET FINAL SCORE",response.data)
            commit("SET_FINAL_SCORE",response.data)
            	
        }catch(error){
            commit("SET_FINAL_SCORE",null)
            console.log("ERROR GETTING FINAL SCORE",scoreJSON,error)
        }
    },
    //GENERAL ACTIONS
    async setQueryLoading({commit, dispatch}){
        try{
            commit("SET_QUERY_LOADING")
        }catch(error){
            console.log("ERROR SETTING STATE VARIABLE FOR LOADING QUERY",error)
            if(!!error.response.data){
                dispatch('notifications/setSnackbar', {text: error.response.data.Error, color: 'error'}, {root: true})
            }else{
                dispatch('notifications/setSnackbar', {text: error.message, color: 'error'}, {root: true})
            }
        }
    },
    //TEAM MEMBERS
    async getTeamMembers({commit, dispatch},team_id){
        try{
            //console.log("GET MEMBERS: At actions level we have:",team_id)
            const response = await this.$axios.get('/teams/members/public/?team_id='+team_id)
            
            //console.log("GET MEMBERS:",response)
            console.log("GET MEMBERS:",response.data)
            commit("SET_TEAM_MEMBERS",response.data.Team)
            //TODO: LIKELY MOVE FROM HERE SINCE DASHBOARD ENDS EARLIER
            commit("SET_QUERY_DONE")
            
        }catch(error){
            console.log("ERROR GETTING TEAM MEMBERS",team_id,error)
            commit("SET_TEAM_MEMBERS",null)
            commit("SET_QUERY_DONE")
            if(!!error.response.data){
                dispatch('notifications/setSnackbar', {text: error.response.data.Error, color: 'error'}, {root: true})
            }else{
                dispatch('notifications/setSnackbar', {text: error.message, color: 'error'}, {root: true})
            }
        }
    },
    async setNullTeamMembers({commit, dispatch}){
        try{
            commit("SET_TEAM_MEMBERS",null)
        }catch(error){
            console.log("ERROR SETTING NULLIFYING TEAM MEMBERS",error)
            if(!!error.response.data){
                dispatch('notifications/setSnackbar', {text: error.response.data.Error, color: 'error'}, {root: true})
            }else{
                dispatch('notifications/setSnackbar', {text: error.message, color: 'error'}, {root: true})
            }
        }
    },
    //INDIVIDUAL STATS
    async addIndividualStatistics({commit,dispatch},statsJSON){
        try{
            let sport_route = statsJSON.sport_route
            console.log("[ADDSTATS-INDEX->ROUTE]",sport_route)
            let statistics = statsJSON.statistics
            console.log("[ADDSTATS-INDEX->STATISTICS]",statistics)
            const response = await this.$axios.post('/results/'+sport_route+'/individual/',statistics)
            commit("SET_QUERY_DONE")
            dispatch('notifications/setSnackbar', {text: "Se añadio nuevo record de Estadisticas de Atleta de manera exitosa.", color: 'success'}, {root: true})
        }catch(error){
            commit("SET_QUERY_DONE")
            console.log("ERROR POSTING INDIVIDUAL STATS",statsJSON,error)
            if(!!error.response.data){
                dispatch('notifications/setSnackbar', {text: error.response.data.Error, color: 'error'}, {root: true})
            }else{
                dispatch('notifications/setSnackbar', {text: error.message, color: 'error'}, {root: true})
            }
        }
    },
    async editIndividualStatistics({commit,dispatch},statsJSON){
        try{
            console.log("[EDIT STATS SUBMIT] STRAIGHT FROM ACTIONS, PARAMS ARE",statsJSON)
            let sport_route = statsJSON.sport_route
            let statistics = statsJSON.statistics
            const response = await this.$axios.put('/results/'+sport_route+'/individual/',statistics)
            commit("SET_QUERY_DONE")
            dispatch('notifications/setSnackbar', {text: "Se edito record de Estadisticas de Atleta de manera exitosa.", color: 'success'}, {root: true})
        }catch(error){
            commit("SET_QUERY_DONE")
            console.log("ERROR UPDATING INDIVIDUAL STATS",statsJSON,error)
            if(!!error.response.data){
                dispatch('notifications/setSnackbar', {text: error.response.data.Error, color: 'error'}, {root: true})
            }else{
                dispatch('notifications/setSnackbar', {text: error.message, color: 'error'}, {root: true})
            }
        }
    },
    async getIndividualStatistics({commit,dispatch},statsJSON){
        try{
            console.log("[EDIT STATS] STRAIGHT FROM ACTIONS, PARAMS ARE",statsJSON)
            let sport_route = statsJSON.sport_route
            // let statistics = statsJSON.statistics
            let event_id = statsJSON.event_id
            let athlete_id = statsJSON.athlete_id
            if(statsJSON.category_id){
                let category_id = statsJSON.category_id
                const response1 = await this.$axios.get('/results/'+sport_route+'/individual/public/?event_id='+event_id+'&athlete_id='+athlete_id+'&category_id='+category_id)
                console.log("GET INDIVIDUAL STATS",response1.data)
                commit("SET_INDIVIDUAL_STATS",response1.data)
            }
            else{
                const response2 = await this.$axios.get('/results/'+sport_route+'/individual/public/?event_id='+event_id+'&athlete_id='+athlete_id)
                console.log("GET INDIVIDUAL STATS",response2.data)
                commit("SET_INDIVIDUAL_STATS",response2.data)
                
            }
           
            commit("SET_QUERY_DONE")
      
        }catch(error){
            commit("SET_INDIVIDUAL_STATS",null)
            commit("SET_QUERY_DONE")
            console.log("ERROR GETTING INDIVIDUAL STATS",statsJSON,error)
            if(!!error.response.data){
                dispatch('notifications/setSnackbar', {text: error.response.data.Error, color: 'error'}, {root: true})
            }else{
                dispatch('notifications/setSnackbar', {text: error.message, color: 'error'}, {root: true})
            }
        }
    },
    async removeIndividualStatistics({commit,dispatch},statsJSON){
        try{
            let sport_route = statsJSON.sport_route
            // let statistics = statsJSON.statistics
            let event_id = statsJSON.event_id
            let athlete_id = statsJSON.athlete_id
            if(statsJSON.category_id){
                let category_id = statsJSON.category_id
                const response1 = await this.$axios.delete('/results/'+sport_route+'/individual/?event_id='+event_id+'&athlete_id='+athlete_id+'&category_id='+category_id)
            }
            else{
                const response2 = await this.$axios.delete('/results/'+sport_route+'/individual/?event_id='+event_id+'&athlete_id='+athlete_id)
            }
            commit("SET_QUERY_DONE")
            dispatch('notifications/setSnackbar', {text: "Se removio record de Estadisticas de Atleta de manera exitosa.", color: 'success'}, {root: true})
        }catch(error){
            commit("SET_QUERY_DONE")
            console.log("ERROR REMOVING INDIVIDUAL STATS",statsJSON,error)
            if(!!error.response.data){
                dispatch('notifications/setSnackbar', {text: error.response.data.Error, color: 'error'}, {root: true})
            }else{
                dispatch('notifications/setSnackbar', {text: error.message, color: 'error'}, {root: true})
            }
        }
    },
}

