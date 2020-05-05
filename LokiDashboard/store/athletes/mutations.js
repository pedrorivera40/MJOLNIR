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
    },

    SET_SEASON_STATS(state,season_stats){
        state.athlete_stats_per_season = season_stats
    },

    SET_AGGREGATE_SEASON_STATS(state,aggregate_season_stats){
        state.athlete_aggregate_stats_per_season = aggregate_season_stats
    }
}