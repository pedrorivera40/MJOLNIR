export default{
    async getAllEventStatistics({commit},stat_params){
        try{
            console.log("At the request level we have the stat params ",stat_params)
            let event_id = stat_params.event_id
            let sport_route = stat_params.sport_route
            //console.log("At the request level we have:",event_id)
            const response = await this.$axios.get('results/'+sport_route+'/?event_id='+event_id)
            //console.log("GET ALL EVENT STATS",response)
            console.log("GET ALL EVENT STATS",response.data)
            commit("SET_RESULTS_PAYLOAD",response.data)
            
        }catch(error){
            console.log("ERROR GETTING ALL EVENT STATS",stat_params,error)
            commit("SET_RESULTS_PAYLOAD",null)
        }
    },
    async getEventInfo({commit},event_id){
        try{
            //console.log("At the request level we have:",event_id)
            const response = await this.$axios.get('http://localhost:5000/events/'+event_id+'/')
            //console.log("GET EVENT INFO",response)
            console.log("GET EVENT INFO",response.data)
            commit("SET_EVENT_INFO",response.data.Event)
            
        }catch(error){
            console.log("ERROR GETTING EVENT INFO",event_id,error)
            commit("SET_EVENT_INFO",null)
        }
    },
    async clearAllStats({commit}){
        try{
            commit("SET_RESULTS_PAYLOAD",null)
        }catch(error){
            console.log("ERROR SETTING RESULTS PAYLOAD TO NULL",error)
        }
    },
    async clearEventInfo({commit}){
        try{
            commit("SET_EVENT_INFO",null)
        }catch(error){
            console.log("ERROR SETTING EVENT INFO TO NULL",error)
        }
    },
    //NEW ACTIONS FOR THE DASHBOARD INTEGRATION
    //GENERAL USE
    async setQueryLoading({commit}){
        try{
            commit("SET_QUERY_LOADING")
        }catch(error){
            console.log("ERROR SETTING STATE VARIABLE FOR LOADING QUERY",error)
        }
    },
    //FINAL SCORE ACTIONS
    async addFinalScore({commit,dispatch},scoreJSON){
        try{
            let sport_route = scoreJSON.sport_route
            let statistics = scoreJSON.statistics
            const response = await this.$axios.post('results/'+sport_route+'/score/',statistics)
            commit("SET_QUERY_DONE")
        }catch(error){
            commit("SET_QUERY_DONE")
            console.log("ERROR POSTING FINAL SCORE",scoreJSON,error)
        }
    },
    // async postTeam({commit,dispatch},teamJSON){
    //     try{
    //         // commit("SET_ATHLETES",[])
    //         const response = await this.$axios.post('teams/',teamJSON)
    //         // dispatch('notifications/setSnackbar', {text: response.data.Athlete, color: 'success'}, {root: true})
            
    //         let sport_id = teamJSON.sport_id
    //         commit("SET_QUERY_DONE")
    //         // this.$router.push('/equipo/'+sport_id)
    //     }catch(error){
    //         commit("SET_QUERY_DONE")
    //         console.log("ERROR POSTING TEAM",teamJSON,error)
    //         // if(!!error.response.data){
    //         //     dispatch('notifications/setSnackbar', {text: error.response.data.Error, color: 'error'}, {root: true})
    //         // }else{
    //         //     dispatch('notifications/setSnackbar', {text: error.message, color: 'error'}, {root: true})
    //         // }
    //     }
    // },
    async editFinalScore({commit,dispatch},scoreJSON){
        try{
            let sport_route = scoreJSON.sport_route
            let statistics = scoreJSON.statistics
            const response = await this.$axios.put('results/'+sport_route+'/score/',statistics)
            commit("SET_QUERY_DONE")
        }catch(error){
            commit("SET_QUERY_DONE")
            console.log("ERROR POSTING FINAL SCORE",scoreJSON,error)
        }
    },
    async getFinalScore({commit,dispatch},scoreJSON){
        try{
            let sport_route = scoreJSON.sport_route
            let event_id = scoreJSON.event_id
            const response = await this.$axios.get('results/'+sport_route+'/score/?event_id='+event_id)
            console.log("GET FINAL SCORE",response.data)
            commit("SET_FINAL_SCORE",response.data)
            	
        }catch(error){
            commit("SET_FINAL_SCORE",null)
            console.log("ERROR GETTING FINAL SCORE",scoreJSON,error)
        }
    },
    //GENERAL ACTIONS
    async setQueryLoading({commit}){
        try{
            commit("SET_QUERY_LOADING")
        }catch(error){
            console.log("ERROR SETTING STATE VARIABLE FOR LOADING QUERY",error)
        }
    },
}

