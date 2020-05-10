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
            
        }catch(error){
            console.log("ERROR GETTING ALL EVENT STATS",stat_params,error)
            commit("SET_RESULTS_PAYLOAD",null)
        }
    },
    async getEventInfo({commit},event_id){
        try{
            //console.log("At the request level we have:",event_id)
            const response = await this.$axios.get('/events/'+event_id)
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
}

