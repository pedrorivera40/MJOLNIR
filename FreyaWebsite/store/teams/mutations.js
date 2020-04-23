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

    // SET_ATHLETE(state,athlete){
	// 		state.athlete = athlete
    // },

    // SET_ATHLETES(state,athletes){
	// 		state.athletes = athletes
    // },

    SET_LOADING(state){
			state.isLoadingT = true
    },

    DONE_LOADING(state){
			state.isLoadingT = false
    }
}