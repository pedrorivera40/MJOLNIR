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

    /**
     * Mutation to set event teams list in the state.
     * @param {*} state vuex state object
     * @param {*} event_teams loaded event teams list with objects containing team data
     */
    SET_EVENT_TEAMS(state,event_teams){
        state.event_teams = event_teams
    },

    /**
     * Mutation to filter the state's events effectively deleting them.
     * @param {*} state vuex state object
     * @param {*} id id of the event being deleted
     */
    DELETE_EVENT(state,id){
        state.events = state.events.filter(events => events.id !== id)
    },

    /**
     * Mutation to add a new event to the state's events list.
     * @param {*} state vuex state object
     * @param {*} event Object with the information of the event being added
     */
    ADD_EVENT(state,event){
        state.events.push(event)
    },

    /**
     * Mutation to set the information of the updated event in the state's events list.
     * @param {*} state vuex state object
     * @param {*} event Object with the information of the event being updated.
     */
    UPDATE_EVENT(state,event){
        const index = state.events.findIndex(arrevent => arrevent.id === event.id)
        if(index !== -1){
            state.events.splice(index,1,event)
        }
    }
    
}