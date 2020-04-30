export default{
    SET_RESULTS_PAYLOAD(state,results_payload){
        state.results_payload = results_payload
    },
    SET_EVENT_INFO(state,event_info){
        state.event_info = event_info
    },
    SET_INDIVIDUAL_STATS(state,individual_stats){
        state.individual_stats = individual_stats
    },
    SET_FINAL_SCORE(state,final_score){
        state.final_score = final_score
    },
    SET_QUERY_LOADING(state){
        state.loadingQuery = true
    },
    SET_QUERY_DONE(state){
        state.loadingQuery = false
    },
    SET_READY_MEMBERS(state){
        state.readyForMembers = true
    },
    SET_WAITING_MEMBERS(state){
        state.readyForMembers = false
    },
    SET_TEAM_MEMBERS(state,team_members){
        state.team_members = team_members
    },
    SET_WAITING_STATS(state){
        state.readyForStats = false
    },
    SET_READY_STATS(state){
        state.readyForStats = true
    }
}