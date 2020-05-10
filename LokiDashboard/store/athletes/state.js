export default() =>({
    /**
     * Loaded athlete
     */
    athlete: null, //Used in the single athlete viewer page.
    /**
     * List of all athletes.
     */
    athletes: [],//Used in in the all athletes viewer page.
    /**
     * Athlete sports
     */
    athlete_sports:[],//Used for athlete creation form.
    /**
     * Loaded athelete statistics per season state
     */
    athlete_stats_per_season:null,//Used in the athlete viewer page.
    /**
     * Loaded athlete aggregate statistics per season
     */
    athlete_aggregate_stats_per_season:null,//Used in the athlete viewer page.
})