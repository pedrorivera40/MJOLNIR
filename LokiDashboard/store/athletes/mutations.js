//These mutations allow you to modify the state of the application.
export default{

    /**
     * Mutation to set the loaded athlete's data in the state.
     * @param {*} state vuex state object
     * @param {*} athlete loaded athlete object with data
     */
    SET_ATHLETE(state,athlete){
        //Set athlete data
        state.athlete = athlete
    },

    /**
     * Mutation to set the loaded athletes list in the state.
     * @param {*} state vuex state object
     * @param {*} athletes loaded athletes list with objects containing athlete data
     */

    SET_ATHLETES(state,athletes){
        //Set loadad athletes list
        state.athletes = athletes
    },

    /**
     * Mutation to set the loaded athlete sports list in the state.
     * @param {*} state vuex state object
     * @param {*} athlete_sports loaded athlete sports list with objects containing sport data
     */
    SET_ATHLETE_SPORTS(state,athlete_sports){
        //Set lodad athlete sports list
        state.athlete_sports = athlete_sports
    },

    /**
     * Mutation to filter the state's athletes effectively deleting them.
     * @param {*} state vuex state object
     * @param {*} id id of the athlete being deleted
     */
    DELETE_ATHLETE(state,id){
        state.athletes = state.athletes.filter(athletes => athletes.id !== id)
    },

    /**
     * Mutation to add a new athlete to the state's athletes list.
     * @param {*} state vuex state object
     * @param {*} athlete Object with the information of the athlete being added.
     */
    ADD_ATHLETE(state,athlete){
        state.athletes.push(athlete)
    },

    /**
     * Mutation to set the information of the updated athlete in the state's athletes list.
     * @param {*} state vuex state object
     * @param {*} athlete athlete Object with the information of the athlete being updated
     */
    UPDATE_ATHLETE(state,athlete){
        const index = state.athletes.findIndex(arrathlete => arrathlete.id === athlete.id)
        if(index !== -1){
            state.athletes.splice(index,1,athlete)
        }
    },

    /**
     * Mutation to set the statistics for a season of an athlete in the state's stats per season list.
     * @param {*} state vuex state object
     * @param {*} season_stats season statistics Object with the information of the statistics per event for an athlete in a season.
     */
    SET_SEASON_STATS(state,season_stats){
        state.athlete_stats_per_season = season_stats
    },

    /**
     * Mutation to set the aggregate statistics for a season of an athlete in the state's  aggregate stats per season list.
     * @param {*} state vuex state object
     * @param {*} aggregate_season_stats aggregate season statistics Object with the information of the statistics for an athlete in a season.
     */
    SET_AGGREGATE_SEASON_STATS(state,aggregate_season_stats){
        state.athlete_aggregate_stats_per_season = aggregate_season_stats
    }
}