export default{
    async getTeamByYear({commit},team_params){
        try{
            console.log("GET TEAM: At actions level we have:",team_params)
            // var json_parsed = JSON.parse(team_params);
            let sport_id = team_params.sport_id
            let season_year = team_params.season_year
            console.log("At the request level we have:",sport_id,season_year)
            const response = await this.$axios.get('teams/?sport_id='+sport_id+'&season_year='+season_year)
            console.log("GET TEAM",response)
            console.log("GET TEAM",response.data)
            commit("SET_TEAM",response.data.Team)
            commit("SET_READY_MEMBERS")
            
        }catch(error){
            // Verify if this is automatic or if this is only because of Luis' formatting?
            // console.log(error.response.data.Error)
            console.log("SOME FUCKING TEAM ERROR WHAT?",team_params,error)
            commit("SET_TEAM",null)
            commit("SET_TEAM_MEMBERS",null)
        }
    },
    async getTeamMembers({commit},team_id){
        try{
            console.log("GET MEMBERS: At actions level we have:",team_id)
            const response = await this.$axios.get('teams/members/?team_id='+team_id)
            
            console.log("GET MEMBERS:",response)
            console.log("GET MEMBERS:",response.data)
            commit("SET_TEAM_MEMBERS",response.data.Team)
            
        }catch(error){
            // Verify if this is automatic or if this is only because of Luis' formatting?
            // console.log(error.response.data.Error)
            console.log("SOME FUCKING MEMBERS ERROR WHAT?",team_id,error)
            commit("SET_TEAM_MEMBERS",null)
        }
    },
    async stopGetMembers({commit}){
        try{
            commit("SET_WAITING_MEMBERS")
        }catch(error){
            console.log("SOME FUCKING SETTINGGET ERROR WHAT?",error)
        }
    },



    
    // async getAthletes( {commit} ){
    //     try{
           
    //         const response = await this.$axios.get('athletes/')
    //         commit("SET_ATHLETES",response.data.Athletes)
    //         commit("SET_ATHLETE",null)

    //     }catch(error){
    //         console.log(error.response.data.Error)

    //         commit("DONE_LOADING",'users')
    //     }
    // },

    // async getAthleteByID({commit},aid){
    //     try{
            
    //         const response = await this.$axios.get('athletes/'+aid+'/')
    //         commit("SET_ATHLETE",response.data.Athlete)
            
    //     }catch(error){
    //         console.log(error.response.data.Error)
            
    //     }
    // }
}

