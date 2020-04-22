export default{
    async getTeamByYear({commit},sport_id, season_year){
        try{
            const response = await this.$axios.get('teams/?sport_id='+1+'&season_year='+2020)
            commit("SET_TEAM",response.data.Team)
        }catch(error){
            // Verify if this is automatic or if this is only because of Luis' formatting?
            console.log(error.response.data.Error)
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

