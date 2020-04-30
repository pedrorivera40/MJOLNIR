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
            commit("SET_READY_STATS")
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
    //NEW ACTIONS FOR THE INTEGRATION OF POST/PUT/DELETE:
    async getTeamMembers({commit},team_id){
        try{
            //console.log("GET MEMBERS: At actions level we have:",team_id)
            const response = await this.$axios.get('teams/members/?team_id='+team_id)
            
            //console.log("GET MEMBERS:",response)
            console.log("GET MEMBERS:",response.data)
            commit("SET_TEAM_MEMBERS",response.data.Team)
            //TODO: LIKELY MOVE FROM HERE SINCE DASHBOARD ENDS EARLIER
            commit("SET_QUERY_DONE")
            
        }catch(error){
            console.log("ERROR GETTING TEAM MEMBERS",team_id,error)
            commit("SET_TEAM_MEMBERS",null)
            commit("SET_QUERY_DONE")
        }
    },
    async setNullTeamMembers({commit}){
        try{
            commit("SET_TEAM_MEMBERS",null)
        }catch(error){
            console.log("ERROR SETTING NULLIFYING TEAM MEMBERS",error)
        }
    },
    async setQueryLoading({commit}){
        try{
            commit("SET_QUERY_LOADING")
        }catch(error){
            console.log("ERROR SETTING STATE VARIABLE FOR LOADING QUERY",error)
        }
    },
    async addIndividualStatistics({commit,dispatch},statsJSON){
        try{
            let sports_route = statsJSON.sports_route
            let statistics = statsJSON.statistics
            const response = await this.$axios.post('results/'+sports_route+'/individual/',statistics)
        }catch(error){
            console.log("ERROR POSTING INDIVIDUAL STATS",statsJSON,error)
        }
    },
    async editIndividualStatistics({commit,dispatch},statsJSON){
        try{
            let sports_route = statsJSON.sports_route
            let statistics = statsJSON.statistics
            const response = await this.$axios.put('results/'+sports_route+'/individual/',statistics)
      
        }catch(error){
  
            console.log("ERROR UPDATING INDIVIDUAL STATS",statsJSON,error)
        }
    },
    async getIndividualStatistics({commit,dispatch},statsJSON){
        try{
            let sports_route = statsJSON.sports_route
            let statistics = statsJSON.statistics
            let event_id = statistics.event_id
            let athlete_id = statistics.athlete_id
            const response = await this.$axios.put('results/'+sports_route+'/individual/?event_id='+event_id+'&athlete_id='+athlete_id)
            console.log("GET INDIVIDUAL STATS",response.data)
            commit("SET_INDIVIDUAL_STATS",response.data)
      
        }catch(error){
            commit("SET_INDIVIDUAL_STATS",null)
      
            console.log("ERROR GETTING INDIVIDUAL STATS",statsJSON,error)
        }
    },
    async removeIndividualStatistics({commit,dispatch},statsJSON){
        try{
            let sports_route = statsJSON.sports_route
            let statistics = statsJSON.statistics
            let event_id = statistics.event_id
            let athlete_id = statistics.athlete_id
            const response = await this.$axios.delete('results/'+sports_route+'/individual/?event_id='+event_id+'&athlete_id='+athlete_id)
          
        }catch(error){
  
            console.log("ERROR REMOVING INDIVIDUAL STATS",statsJSON,error)
        }
    },
    async addFinalScore({commit,dispatch},scoreJSON){
        try{
            let sports_route = scoreJSON.sports_route
            let statistics = scoreJSON.statistics
            const response = await this.$axios.post('results/'+sports_route+'/individual/',statistics)
          
        }catch(error){
     
            console.log("ERROR POSTING FINAL SCORE",scoreJSON,error)
        }
    },
    async editFinalScore({commit,dispatch},scoreJSON){
        try{
            let sports_route = scoreJSON.sports_route
            let statistics = scoreJSON.statistics
            const response = await this.$axios.put('results/'+sports_route+'/individual/',statistics)
  
        }catch(error){
         
            console.log("ERROR UPDATING FINAL SCORE",statsJSON,error)
        }
    },
    async getFinalScore({commit,dispatch},scoreJSON){
        try{
            let sports_route = scoreJSON.sports_route
            let statistics = scoreJSON.statistics
            let event_id = statistics.event_id
            let athlete_id = statistics.athlete_id
            const response = await this.$axios.put('results/'+sports_route+'/score/?event_id='+event_id)
            console.log("GET FINAL SCORE",response.data)
            commit("SET_FINAL_SCORE",response.data)
      
        }catch(error){
            commit("SET_FINAL_SCORE",null)
      
            console.log("ERROR GETTING FINAL SCORE",statsJSON,error)
        }
    },
    async stopGetMembers({commit}){
        try{
            commit("SET_WAITING_MEMBERS")
        }catch(error){
            console.log("ERROR SETTING STATE VARIABLE FOR TEAM MEMBERS",error)
        }
    },
    async setReadyStats({commit}){
        try{
            commit("SET_READY_STATS")
        }catch(error){
            console.log("ERROR SETTING STATE VARIABLE FOR STATS",error)
        }
    },
    async stopGetStats({commit}){
        try{
            commit("SET_WAITING_STATS")
        }catch(error){
            console.log("ERROR SETTING STATE VARIABLE FOR STATS",error)
        }
    },
}

