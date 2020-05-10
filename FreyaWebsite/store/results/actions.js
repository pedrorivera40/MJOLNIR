export default{
    async getAllEventStatistics({commit},stat_params){
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
        }
    },
    async getEventInfo({commit},event_id){
        try{
            //console.log("At the request level we have:",event_id)
            const response = await this.$axios.get('/events/'+event_id+'/public/')
            //console.log("GET EVENT INFO",response)
            console.log("GET EVENT INFO",response.data)
            commit("SET_EVENT_INFO",response.data.Event)
            // commit("SET_QUERY_DONE")
            
        }catch(error){
            console.log("ERROR GETTING EVENT INFO",event_id,error)
            commit("SET_EVENT_INFO",null)
            commit("SET_QUERY_DONE")
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
}

