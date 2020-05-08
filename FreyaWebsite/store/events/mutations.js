//These mutations allow you to modify the state of the application.
export default {
    
    /**
     * Mutation to set the loaded event's data in the state
     * @param {*} state vuex state object
     * @param {*} event loaded event object with data
     */
    SET_EVENT(state,event){
        //Set event data
        state.event = event
    },

    /**
     * Mutation to set loaded events list in the state.
     * @param {*} state vuex state object
     * @param {*} events loaded events list with objects containing event data
     */
    SET_EVENTS(state, events) {
        //Set loaded events list
        state.events = events
    },

}