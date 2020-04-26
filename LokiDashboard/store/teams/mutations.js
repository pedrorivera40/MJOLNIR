export default{

    SET_TEAM(state,team){
        state.team = team
    },
    SET_TEAMS(state,teams){
        state.teams = teams
    },
    SET_TEAM_MEMBERS(state,team_members){
        state.team_members = team_members
    },
    SET_TEAM_MEMBER(state,team_member){
        state.team_member = team_member
    },
    SET_READY_MEMBERS(state){
        state.readyForMembers = true
    },
    SET_WAITING_MEMBERS(state){
        state.readyForMembers = false
    },
    SET_READY_MEMBER_STATS(state){
        state.readyForMemberStats = true
    },
    SET_WAITING_MEMBER_STATS(state){
        state.readyForMemberStats = false
    },
    SET_READY_TEAM_STATS(state){
        state.readyForTeamStats = true
    },
    SET_WAITING_TEAM_STATS(state){
        state.readyForTeamStats = false
    },
    SET_QUERY_LOADING(state){
        state.loadingQuery = true
    },
    SET_QUERY_DONE(state){
        state.loadingQuery = false
    },
    SET_MEMBER_STATISTICS(state,member_statistics){
        state.member_statistics = member_statistics
    },
    SET_TEAM_STATISTICS(state,team_statistics){
        state.team_statistics = team_statistics
    },
    SET_LOADING(state){
			state.isLoadingT = true
    },

    DONE_LOADING(state){
			state.isLoadingT = false
    }
}