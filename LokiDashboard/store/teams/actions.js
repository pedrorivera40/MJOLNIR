
export default{
    async getTeamByYear({commit},team_params){
        try{
            //console.log("GET TEAM: At actions level we have:",team_params)
            let sport_id = team_params.sport_id
            let season_year = team_params.season_year
            //console.log("At the request level we have:",sport_id,season_year)
            const response = await this.$axios.get('teams/?sport_id='+sport_id+'&season_year='+season_year)
            //console.log("GET TEAM",response)
            console.log("GET TEAM",response.data)
            commit("SET_TEAM",response.data.Team)
            commit("SET_READY_MEMBERS")
            // commit("SET_ATHLETE",null,{root:true})
            
        }catch(error){
            console.log("ERROR GETTING TEAM",team_params,error)
            commit("SET_TEAM",null)
            commit("SET_TEAM_MEMBERS",null)
            commit("SET_QUERY_DONE")
        }
    },
    async getTeamMembers({commit},team_id){
        try{
            //console.log("GET MEMBERS: At actions level we have:",team_id)
            const response = await this.$axios.get('teams/members/?team_id='+team_id)
            
            //console.log("GET MEMBERS:",response)
            console.log("GET MEMBERS:",response.data)
            commit("SET_TEAM_MEMBERS",response.data.Team)
            commit("SET_READY_MEMBER_STATS")
            //TODO: LIKELY MOVE FROM HERE SINCE DASHBOARD ENDS EARLIER
            commit("SET_QUERY_DONE")
            
        }catch(error){
            console.log("ERROR GETTING TEAM MEMBERS",team_id,error)
            commit("SET_TEAM_MEMBERS",null)
            commit("SET_WAITING_MEMBERS")
            commit("SET_QUERY_DONE")
        }
    },
    async stopGetMembers({commit}){
        try{
            commit("SET_WAITING_MEMBERS")
        }catch(error){
            console.log("ERROR SETTING STATE VARIABLE FOR TEAM MEMBERS",error)
        }
    },
    async stopGetMemberStats({commit}){
        try{
            commit("SET_WAITING_MEMBER_STATS")
        }catch(error){
            console.log("ERROR SETTING STATE VARIABLE FOR TEAM MEMBER STATS",error)
        }
    },
    async stopGetTeamStats({commit}){
        try{
            commit("SET_WAITING_TEAM_STATS")
        }catch(error){
            console.log("ERROR SETTING STATE VARIABLE FOR TEAM STATS",error)
        }
    },
    async setQueryLoading({commit}){
        try{
            commit("SET_QUERY_LOADING")
        }catch(error){
            console.log("ERROR SETTING STATE VARIABLE FOR LOADING QUERY",error)
        }
    },
    async setNullTeam({commit}){
        try{
            commit("SET_TEAM",null)
        }catch(error){
            console.log("ERROR SETTING NULLIFYING TEAM",error)
        }
    },
    async setNullTeamMembers({commit}){
        try{
            commit("SET_TEAM_MEMBERS",null)
        }catch(error){
            console.log("ERROR SETTING NULLIFYING TEAM MEMBERS",error)
        }
    },
    async setNullMemberStats({commit}){
        try{
            commit("SET_MEMBER_STATISTICS",null)
        }catch(error){
            console.log("ERROR SETTING NULLIFYING MEMBER STATS",error)
        }
    },
    async setNullTeamStats({commit}){
        try{
            commit("SET_TEAM_STATISTICS",null)
        }catch(error){
            console.log("ERROR SETTING NULLIFYING TEAM STATS",error)
        }
    },
    async getMemberStatistics({commit},team_params){
        try{
            //console.log("GET MEMBER STATS: At actions level we have:",team_params)
           
            let sport_id = team_params.sport_id
            let season_year = team_params.season_year
            let sport_route = team_params.sport_route
            //console.log("At the request level we have:",sport_id,season_year)
            const response = await this.$axios.get('/results/'+sport_route+'/season/all_athletes_aggregate/?sport_id='+sport_id+'&season_year='+season_year)
            //console.log("GET MEMBER STATS:",response)
            console.log("GET MEMBER STATS:",response.data)
            commit("SET_MEMBER_STATISTICS",response.data)
            commit("SET_READY_TEAM_STATS")
            
        }catch(error){
         
            console.log("ERROR GETTING MEMBER STATISTICS",team_params,error)
            commit("SET_MEMBER_STATISTICS",null)
        }
    },
    async getTeamStatistics({commit},team_params){
        try{
            //console.log("GET TEAM STATS: At actions level we have:",team_params)
         
            let sport_id = team_params.sport_id
            let season_year = team_params.season_year
            let sport_route = team_params.sport_route
            //console.log("At the request level we have:",sport_id,season_year)
            const response = await this.$axios.get('/results/'+sport_route+'/season/team_aggregate/?sport_id='+sport_id+'&season_year='+season_year)
            //console.log("GET TEAM STATS:",response)
            console.log("GET TEAM STATS:",response.data)
            commit("SET_TEAM_STATISTICS",response.data)
            
        }catch(error){
      
            console.log("ERROR GETTING TEAM STATISTICS",team_params,error)
            commit("SET_TEAM_STATISTICS",null)
        }
    },
    async getTeamByYearSimple({commit},team_params){
        try{
            console.log("GET TEAM: At actions level we have:",team_params)
            let sport_id = team_params.sport_id
            let season_year = team_params.season_year
            console.log("At the request level we have:",sport_id,season_year)
            const response = await this.$axios.get('teams/?sport_id='+sport_id+'&season_year='+season_year)
            console.log("GET TEAM",response)
            console.log("GET TEAM",response.data)
            commit("SET_TEAM",response.data.Team)
            commit("SET_QUERY_DONE")
            
        }catch(error){
            console.log("ERROR GETTING TEAM",team_params,error)
            commit("SET_TEAM",null)
            commit("SET_QUERY_DONE")
        }
    },
    async editTeam({commit,dispatch},teamJSON){
        try{
            // {
            //     "sport_id":1,
            //     "season_year":"1942",
            //     "team_image_url":"https://comicvine1.cbsistatic.com/uploads/original/11138/111387409/7081408-8787124231-d9pmk.png",
            //     "about_team": "I was Updated Yay!"
            //     }
            // commit("SET_ATHLETES",[])
            const response = await this.$axios.put('teams/',teamJSON)
            // dispatch('notifications/setSnackbar', {text: response.data.Athlete, color: 'success'}, {root: true})
            
            //TODO: need to check how to get route params from here (sport_id), it's not working.
            // --> basically, cant do the route params form here of course, but can pass them as a modified json? 
            // --> should not be neccessary. the source is the same anyway
            let sport_id = teamJSON.sport_id
            this.$router.push('/equipo/'+sport_id)
        }catch(error){
            console.log("ERROR GETTING TEAM",teamJSON,error)
            // if(!!error.response.data){
            //     dispatch('notifications/setSnackbar', {text: error.response.data.Error, color: 'error'}, {root: true})
            // }else{
            //     dispatch('notifications/setSnackbar', {text: error.message, color: 'error'}, {root: true})
            // }
        }
    },
}

