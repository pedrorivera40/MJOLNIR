
export default{
    //this one is meant to be done in order with the other set of queries
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
            commit("SET_QUERY_DONE")
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
            commit("SET_QUERY_DONE")
        }
    },
    //THe diffrence is in that query is done after getting team and thats it
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
            // commit("SET_ATHLETES",[])
            const response = await this.$axios.put('teams/',teamJSON)
            // dispatch('notifications/setSnackbar', {text: response.data.Athlete, color: 'success'}, {root: true})
            
            let sport_id = teamJSON.sport_id
            commit("SET_QUERY_DONE")
            // this.$router.push('/equipo/'+sport_id)
        }catch(error){
            commit("SET_QUERY_DONE")
            console.log("ERROR PUTTING TEAM",teamJSON,error)
            
            // if(!!error.response.data){
            //     dispatch('notifications/setSnackbar', {text: error.response.data.Error, color: 'error'}, {root: true})
            // }else{
            //     dispatch('notifications/setSnackbar', {text: error.message, color: 'error'}, {root: true})
            // }
        }
    },
    async postTeam({commit,dispatch},teamJSON){
        try{
            // commit("SET_ATHLETES",[])
            const response = await this.$axios.post('teams/',teamJSON)
            // dispatch('notifications/setSnackbar', {text: response.data.Athlete, color: 'success'}, {root: true})
            
            let sport_id = teamJSON.sport_id
            commit("SET_QUERY_DONE")
            // this.$router.push('/equipo/'+sport_id)
        }catch(error){
            commit("SET_QUERY_DONE")
            console.log("ERROR POSTING TEAM",teamJSON,error)
            // if(!!error.response.data){
            //     dispatch('notifications/setSnackbar', {text: error.response.data.Error, color: 'error'}, {root: true})
            // }else{
            //     dispatch('notifications/setSnackbar', {text: error.message, color: 'error'}, {root: true})
            // }
        }
    },
    async addMembers({commit,dispatch},membersJSON){
        try{
            // {
            //     "team_id":1,
            //     "athlete_id":8
            // }
            // commit("SET_ATHLETES",[])
            const response = await this.$axios.post('teams/members/',membersJSON)
            // dispatch('notifications/setSnackbar', {text: response.data.Athlete, color: 'success'}, {root: true})
            
            //TODO: how to dynamically check the sport id if not a param? it'd have to be a param, would 
            //be a json inside a json or something. oh well. 
            let sport_id = 1
            // let sport_id = memberJSON.sport_id
            commit("SET_QUERY_DONE")
            // this.$router.push('/equipo/'+sport_id)
        }catch(error){
            commit("SET_QUERY_DONE")
            console.log("ERROR POSTING TEAM MEMBERS",membersJSON,error)
            // if(!!error.response.data){
            //     dispatch('notifications/setSnackbar', {text: error.response.data.Error, color: 'error'}, {root: true})
            // }else{
            //     dispatch('notifications/setSnackbar', {text: error.message, color: 'error'}, {root: true})
            // }
        }
    },
    async getSportAthletes({commit},athlete_params){
        try{
            let sport_id = athlete_params.sport_id
            let team_id = athlete_params.team_id
            console.log("GET ATHLETES: At actions level we have:",athlete_params)
            console.log("At the request level we have:",athlete_params)
            const response = await this.$axios.get('athletes/?sID='+sport_id+'&tID='+team_id)
            console.log("GET ATHLETES",response)
            console.log("GET ATHLETES",response.data)
            commit("SET_SPORT_ATHLETES",response.data.Athletes)
            commit("SET_QUERY_DONE")
            
        }catch(error){
            console.log("ERROR GETTING SPORT ATHLETES",athlete_params,error)
            commit("SET_SPORT_ATHLETES",null)
            commit("SET_QUERY_DONE")
        }
    },
    async setSportAthletesNull({commit}){
        try{
            commit("SET_SPORT_ATHLETES",null)
            commit("SET_QUERY_DONE")
            
        }catch(error){
            console.log("ERROR SETTING SPORT ATHLETES NULL",error)
            commit("SET_SPORT_ATHLETES",null)
            commit("SET_QUERY_DONE")
        }
    },
    async removeTeam({commit},teamJSON){
        try{
            let sport_id = teamJSON.sport_id
            let season_year = teamJSON.season_year
            console.log("REMOVE ATHLETES: At actions level we have:",teamJSON)
            const response = await this.$axios.delete('teams/?sport_id='+sport_id+'&season_year='+season_year)
            // console.log("REMOVE ATHLETES",response)
            // console.log("REMOVE ATHLETES",response.data)
            // commit("SET_TEAM",null)
            commit("SET_QUERY_DONE")
            
        }catch(error){
            console.log("ERROR REMOVING TEAM",teamJSON,error)
            // commit("SET_TEAM",null)
            commit("SET_QUERY_DONE")
        }
    },
    async removeTeamMember({commit},memberJSON){
        try{
            let athlete_id = memberJSON.athlete_id
            let team_id = memberJSON.team_id
            console.log("REMOVE ATHLETES: At actions level we have:",memberJSON)
            const response = await this.$axios.delete('teams/member/?athlete_id='+athlete_id+'&team_id='+team_id)
            // console.log("REMOVE ATHLETES",response)
            // console.log("REMOVE ATHLETES",response.data)
            // commit("SET_TEAM_MEMBER",null)
            commit("SET_QUERY_DONE")
            
        }catch(error){
            console.log("ERROR REMOVING TEAM MEMBER",memberJSON,error)
            // commit("SET_TEAM_MEMBER",null)
            commit("SET_QUERY_DONE")
        }
    },
    
}

