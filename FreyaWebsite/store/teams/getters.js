export default{
    team: state => state.team,
    teams: state => state.teams,
    team_members: state => state.team_members,
    team_member: state => state.team_member,
    member_statistics: state => state.member_statistics,
    team_statistics: state => state.team_statistics,
    isLoadingT: state => state.isLoadingT,
    readyForMembers: state => state.readyForMembers,
    readyForMemberStats: state => state.readyForMemberStats,
    readyForTeamStats: state => state.readyForTeamStats,
    loadingQuery: state => state.loadingQuery
    // athlete: state => state.athlete,
    // athletes: state => state.athletes,
    // isLoadingA: state => state.isLoadingA,
}