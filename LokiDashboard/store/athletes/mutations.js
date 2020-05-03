export default{

    SET_ATHLETE(state,athlete){
        state.athlete = athlete
    },

    SET_ATHLETES(state,athletes){
        state.athletes = athletes
    },

    SET_ATHLETE_SPORTS(state,athlete_sports){
        state.athlete_sports = athlete_sports
    },

    DELETE_ATHLETE(state,id){
        state.athletes = state.athletes.filter(athletes => athletes.id !== id)
    },

    ADD_ATHLETE(state,athlete){
        state.athletes.push(athlete)
    },


    UPDATE_ATHLETE(state,athlete){
        const index = state.athletes.findIndex(arrathlete => arrathlete.id === athlete.id)
        if(index !== -1){
            state.athletes.splice(index,1,athlete)
        }
    }
}