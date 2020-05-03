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
}