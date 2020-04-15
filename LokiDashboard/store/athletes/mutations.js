export default{

    SET_ATHLETE(state,athlete){
			state.athlete = athlete
    },

    SET_ATHLETES(state,athletes){
			state.athletes = athletes
    },

    SET_LOADING(state){
			state.isLoadingA = true
    },

    DONE_LOADING(state){
			state.isLoadingA = false
    }
}