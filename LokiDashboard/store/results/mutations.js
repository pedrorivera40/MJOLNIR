export default{
    SET_RESULTS_PAYLOAD(state,results_payload){
        state.results_payload = results_payload
    },
  
    SET_EVENT_INFO(state,event_info){
        state.event_info = event_info
    },

    //LOADING QUERY STATUS
    SET_QUERY_LOADING(state){
        state.loadingQuery = true
    },
    SET_QUERY_DONE(state){
        state.loadingQuery = false
    },

    //FINAL SCORE
    SET_FINAL_SCORE(state,final_score){
        state.final_score = final_score
    }

}