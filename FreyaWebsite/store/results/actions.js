export default{
    async getAllEventStatistics({commit},event_id){
        try{
            //console.log("At the request level we have:",event_id)
            const response = await this.$axios.get('results/basketball/?event_id='+event_id)
            //console.log("GET ALL EVENT STATS",response)
            console.log("GET ALL EVENT STATS",response.data)
            commit("SET_RESULTS_PAYLOAD",response.data)
            
        }catch(error){
            console.log("ERROR GETTING ALL EVENT STATS",event_id,error)
            commit("SET_RESULTS_PAYLOAD",null)
        }
    },
    async getEventInfo({commit},event_id){
        try{
            //console.log("At the request level we have:",event_id)
            const response = await this.$axios.get('http://localhost:5000/events/'+event_id)
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
    


    // async stopGetTeamStats({commit}){
    //     try{
    //         commit("SET_WAITING_TEAM_STATS")
    //     }catch(error){
    //         console.log("ERROR SETTING STATE VARIABLE FOR TEAM STATS",error)
    //     }
    // },
}

