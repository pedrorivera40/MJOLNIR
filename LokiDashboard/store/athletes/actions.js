export default{
    async getAthletes( {commit} ){
        try{
           
            const response = await this.$axios.get('athletes/')
            commit("SET_ATHLETES",response.data.Athletes)
            commit("SET_ATHLETE",null)

        }catch(error){
            console.log(error.response.data.Error)
           
        }
    },

    async getAthleteByID({commit},aid){
        try{
            
            const response = await this.$axios.get('athletes/'+aid+'/')
            commit("SET_ATHLETE",response.data.Athlete)
            
        }catch(error){
            console.log(error.response.data.Error)
            
        }
    }
}

