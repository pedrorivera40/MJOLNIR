import { rtdb } from '~/services/firebaseInit.js'

export default {

    // Set async function for handling Firebase set scores updates (each team has 5 set scores).
    async handleSetScores({ commit, dispatch }, event_id) {
        try {

            for (let i = 1; i <= 5; i++) {
                // Async functions for UPRM scores.
                await rtdb().ref("/v1/" + event_id + "/score/set" + i + "-uprm").on('value', function (snapshot) {
                    let entry = { set: i, score: snapshot.val() };
                    commit("UPDATE_UPRM_SET", entry)
                });
                // Async functions for opponent scores.
                await rtdb().ref("/v1/" + event_id + "/score/set" + i + "-opponent").on('value', function (snapshot) {
                    let entry = { set: i, score: snapshot.val() };
                    commit("UPDATE_OPP_SET", entry)
                });
            }

        } catch (error) {
            dispatch('notifications/setSnackbar', { text: "Unable to retrieve scores from RTDB.", color: "error" }, { root: true });
        }
    },

    // Set async function for handling Firebase current set updates.
    async handleCurrentSet({ commit, dispatch }, event_id) {
        try {

            await rtdb().ref("/v1/" + event_id + "/game-metadata/current-set").on('value', function (snapshot) {
                commit("UPDATE_CURRENT_SET", snapshot.val());
            });

        } catch (error) {
            dispatch('notifications/setSnackbar', { text: "Unable to retrieve current set from RTDB.", color: "error" }, { root: true });
        }
    },

    // Set async function for handling Firebase UPRM roster updates.
    async handleUPRMRoster({ commit, dispatch }, event_id) {
        try {

            // Handle roster additions.
            await rtdb().ref("/v1/" + event_id + "/uprm-roster").on('child_added', function (snapshot) {
                let athlete = snapshot.val();
                athlete.key = snapshot.key;
                commit("ADD_UPRM_ROSTER", athlete);
                commit("UPDATE_UPRM_ATHLETE_STATISTICS");
            });

            // Handle roster updates.
            await rtdb().ref("/v1/" + event_id + "/uprm-roster").on('child_changed', function (snapshot) {
                let athlete = snapshot.val();
                athlete.key = snapshot.key;
                commit("UPDATE_UPRM_ROSTER", athlete);
                commit("UPDATE_UPRM_ATHLETE_STATISTICS");
            });

            // Handle roster removals.
            await rtdb().ref("/v1/" + event_id + "/uprm-roster").on('child_removed', function (snapshot) {
                commit("REMOVE_UPRM_ROSTER", snapshot.key);
                commit("UPDATE_UPRM_ATHLETE_STATISTICS");
            });

        } catch (error) {
            dispatch('notifications/setSnackbar', { text: "Error retrieving UPRM roster update from RTDB.", color: "error" }, { root: true });
        }
    },

    // Set async function for handling Firebase opponent roster updates.
    async handleOPPRoster({ commit, dispatch }, event_id) {
        try {

            // Handle roster additions.
            await rtdb().ref("/v1/" + event_id + "/opponent-roster").on('child_added', function (snapshot) {
                let athlete = snapshot.val();
                athlete.key = snapshot.key;
                commit("ADD_OPP_ROSTER", athlete);
                commit("UPDATE_OPP_ATHLETE_STATISTICS");
            });

            // Handle roster updates.
            await rtdb().ref("/v1/" + event_id + "/opponent-roster").on('child_changed', function (snapshot) {
                let athlete = snapshot.val();
                athlete.key = snapshot.key;
                commit("UPDATE_OPP_ROSTER", athlete);
                commit("UPDATE_OPP_ATHLETE_STATISTICS");
            });

            // Handle roster removals.
            await rtdb().ref("/v1/" + event_id + "/opponent-roster").on('child_removed', function (snapshot) {
                commit("REMOVE_OPP_ROSTER", snapshot.key);
                commit("UPDATE_OPP_ATHLETE_STATISTICS");
            });

        } catch (error) {
            dispatch('notifications/setSnackbar', { text: "Error retrieving opponent roster update from RTDB.", color: "error" }, { root: true });
        }
    },

    // Set async function for handling Firebase game-over updates.
    async handleGameOver({ commit, dispatch }, event_id) {
        try {

            await rtdb().ref("/v1/" + event_id + "/game-metadata/game-over").on('value', function (snapshot) {
                commit("SET_GAME_OVER", snapshot.val())
            });

        } catch (error) {
            dispatch('notifications/setSnackbar', { text: "Unable to retrieve game over from RTDB.", color: "error" }, { root: true });
        }
    },

    // Set async function for handling Firebase opponent color updates.
    async handleOppColor({ commit, dispatch }, event_id) {
        try {

            await rtdb().ref("/v1/" + event_id + "/game-metadata/opp-color").on('value', function (snapshot) {
                commit("SET_OPP_COLOR", snapshot.val())
            });

        } catch (error) {
            dispatch('notifications/setSnackbar', { text: "Unable to retrieve opponent color from RTDB.", color: "error" }, { root: true });
        }
    },

    // Set async function for handling Firebase game action updates.
    async handleGameActions({ commit, dispatch }, event_id) {
        try {

            // Handle roster additions.
            await rtdb().ref("/v1/" + event_id + "/game-actions").on('child_added', function (snapshot) {
                let action = snapshot.val();
                action.key = snapshot.key;
                commit("ADD_GAME_ACTION", action);
                commit("UPDATE_UPRM_STATISTICS");
                commit("UPDATE_OPP_STATISTICS");
                commit("UPDATE_UPRM_ATHLETE_STATISTICS");
                commit("UPDATE_OPP_ATHLETE_STATISTICS");
            });

            // Handle roster updates.
            await rtdb().ref("/v1/" + event_id + "/game-actions").on('child_changed', function (snapshot) {
                let action = snapshot.val();
                action.key = snapshot.key;
                commit("UPDATE_GAME_ACTION", action);
                commit("UPDATE_UPRM_STATISTICS");
                commit("UPDATE_OPP_STATISTICS");
                commit("UPDATE_UPRM_ATHLETE_STATISTICS");
                commit("UPDATE_OPP_ATHLETE_STATISTICS");
            });

            // Handle roster removals.
            await rtdb().ref("/v1/" + event_id + "/game-actions").on('child_removed', function (snapshot) {
                commit("REMOVE_GAME_ACTION", snapshot.key);
                commit("UPDATE_UPRM_STATISTICS");
                commit("UPDATE_OPP_STATISTICS");
                commit("UPDATE_UPRM_ATHLETE_STATISTICS");
                commit("UPDATE_OPP_ATHLETE_STATISTICS");
            });

        } catch (error) {
            dispatch('notifications/setSnackbar', { text: "Error retrieving game actions update from RTDB.", color: "error" }, { root: true });
        }
    },

    // Detach async function for handling Firebase set scores updates (each team has 5 set scores).
    async detachSetScores({ commit, dispatch }, event_id) {
        try {
            for (let i = 1; i <= 5; i++) {
                // Async functions for UPRM scores.
                await rtdb().ref("/v1/" + event_id + "/score/set" + i + "-uprm").off();
                // Async functions for opponent scores.
                await rtdb().ref("/v1/" + event_id + "/score/set" + i + "-opponent").off();
            }

        } catch (error) {
            dispatch('notifications/setSnackbar', { text: "Unable to retrieve scores from RTDB.", color: "error" }, { root: true });
        }
    },

    // Detach async function for handling Firebase current set updates.
    async detachCurrentSet({ commit, dispatch }, event_id) {
        try {

            await rtdb().ref("/v1/" + event_id + "/game-metadata/current-set").on('value', function (snapshot) {
                commit("UPDATE_CURRENT_SET", snapshot.val());
            });

        } catch (error) {
            dispatch('notifications/setSnackbar', { text: "Unable to retrieve current set from RTDB.", color: "error" }, { root: true });
        }
    },

    // Detach async function for handling Firebase UPRM roster updates.
    async detachUPRMRoster({ commit, dispatch }, event_id) {
        try {

            // Handle roster additions.
            await rtdb().ref("/v1/" + event_id + "/uprm-roster").off();

        } catch (error) {
            dispatch('notifications/setSnackbar', { text: "Error detaching UPRM roster update from RTDB.", color: "error" }, { root: true });
        }
    },

    // Detach async function for handling Firebase opponent roster updates.
    async detachOPPRoster({ commit, dispatch }, event_id) {
        try {

            // Handle roster additions.
            await rtdb().ref("/v1/" + event_id + "/opponent-roster").off();

        } catch (error) {
            dispatch('notifications/setSnackbar', { text: "Error detaching opponent roster update from RTDB.", color: "error" }, { root: true });
        }
    },

    // Detach async function for handling Firebase game-over updates.
    async detachGameOver({ commit, dispatch }, event_id) {
        try {

            await rtdb().ref("/v1/" + event_id + "/game-metadata/game-over").off();

        } catch (error) {
            dispatch('notifications/setSnackbar', { text: "Unable to detach game over from RTDB.", color: "error" }, { root: true });
        }
    },

    // Detach async function for handling Firebase opponent color updates.
    async detachOppColor({ commit, dispatch }, event_id) {
        try {

            await rtdb().ref("/v1/" + event_id + "/game-metadata/opp-color").off();;

        } catch (error) {
            dispatch('notifications/setSnackbar', { text: "Unable detaching opponent color from RTDB.", color: "error" }, { root: true });
        }
    },

    // Detach async function for handling Firebase game action updates.
    async detachGameActions({ commit, dispatch }, event_id) {
        try {

            await rtdb().ref("/v1/" + event_id + "/game-actions").off();

        } catch (error) {
            dispatch('notifications/setSnackbar', { text: "Error detaching game actions updates from RTDB.", color: "error" }, { root: true });
        }
    },

    async getEvent({ commit, dispatch }, event_id) {
        try {
            const response = await this.$axios.get(`/events/${event_id}/public/`);
            commit("SET_HAS_PBP", response.data.Event.hasPBP);
            commit("SET_TEAM_ID", response.data.Event.team_id);
            commit("SET_BRANCH", response.data.Event.branch);
            commit("SET_OPPONENT_NAME", response.data.Event.opponent_name);
            commit("SET_SPORT_NAME", response.data.Event.sport_name);
            return true;
        } catch (error) {
            if (!!error.response) {
                dispatch('notifications/setSnackbar', { text: error.response.data.Error, color: 'error' }, { root: true })
            } else {
                dispatch('notifications/setSnackbar', { text: error.message, color: 'error' }, { root: true })
            }
            return false;
        }
    },

    async getValidUPRMRoster({ commit, dispatch }, team_id) {
        try {
            const response = await this.$axios.get(`/teams/members/public/?team_id=${team_id}`);
            commit("SET_VALID_UPRM_ROSTER", response.data.Team.team_members);
        } catch (error) {
            if (!!error.response) {
                dispatch('notifications/setSnackbar', { text: error.response.data.Error, color: 'error' }, { root: true })
            } else {
                dispatch('notifications/setSnackbar', { text: error.message, color: 'error' }, { root: true })
            }
        }
    },

    async sendSetAdjust({ commit, dispatch }, payload) {
        try {

            const response = await this.$axios.put(`/pbp/Voleibol/set`, payload);
            dispatch('notifications/setSnackbar', { text: response.data.MSG, color: 'success' }, { root: true })
        } catch (error) {
            if (!!error.response) {
                dispatch('notifications/setSnackbar', { text: error.response.data.Error, color: 'error' }, { root: true })
            } else {
                dispatch('notifications/setSnackbar', { text: error.message, color: 'error' }, { root: true })
            }
        }
    },

    async sendGameAction({ commit, dispatch }, payload) {
        try {

            const response = await this.$axios.post(`/pbp/Voleibol/actions`, payload);
            dispatch('notifications/setSnackbar', { text: response.data.MSG, color: 'success' }, { root: true })
            return true;
        } catch (error) {
            console.log(error.response.data)
            if (!!error.response.data.Error) {
                dispatch('notifications/setSnackbar', { text: error.response.data.Error, color: 'error' }, { root: true })
            }
            else {
                dispatch('notifications/setSnackbar', { text: error.message, color: 'error' }, { root: true })
            }
            return false;
        }
    },

    async updateGameAction({ commit, dispatch }, payload) {
        try {

            const response = await this.$axios.put(`/pbp/Voleibol/actions`, payload);
            dispatch('notifications/setSnackbar', { text: response.data.MSG, color: 'success' }, { root: true })
            return true;
        } catch (error) {
            if (!!error.response) {
                dispatch('notifications/setSnackbar', { text: error.response.data.Error, color: 'error' }, { root: true })
            } else {
                dispatch('notifications/setSnackbar', { text: error.message, color: 'error' }, { root: true })
            }
            return false;
        }
    },

    async removeGameAction({ commit, dispatch }, payload) {
        try {
            const response = await this.$axios.delete(`/pbp/Voleibol/actions?event_id=${payload.event_id}&action_id=${payload.action_id}`);
            dispatch('notifications/setSnackbar', { text: response.data.MSG, color: 'success' }, { root: true })
            return true;
        } catch (error) {
            if (!!error.response) {
                dispatch('notifications/setSnackbar', { text: error.response.data.Error, color: 'error' }, { root: true })
            } else {
                dispatch('notifications/setSnackbar', { text: error.message, color: 'error' }, { root: true })
            }
            return false;
        }
    },

    // Send a notification in case athlete is selected without previously having a game action chosen.
    notifyNotActionSelected({ commit, dispatch }) {
        dispatch('notifications/setSnackbar', { text: "Debe seleccionar el tipo de jugada antes de escoger un jugador.", color: 'error' }, { root: true });
    },

    // Set end to a PBP sequence.
    async endPBPSequence({ commit, dispatch }, payload) {
        try {
            const response = await this.$axios.post(`/pbp/Voleibol/end`, payload);
            dispatch('notifications/setSnackbar', { text: response.data.MSG, color: 'success' }, { root: true })
        } catch (error) {
            if (!!error.response) {
                dispatch('notifications/setSnackbar', { text: error.response.data.Error, color: 'error' }, { root: true })
            } else {
                dispatch('notifications/setSnackbar', { text: error.message, color: 'error' }, { root: true })
            }
        }
    },

    // Clear app state regarding PBP sequence data.
    clearPBPState({ commit, dispatch }) {
        try {
            commit("CLEAR_STATE");
        } catch (error) {
            dispatch('notifications/setSnackbar', { text: error, color: 'error' }, { root: true })
        }
    },

    // Update opponent color in the RTDB via Odin.
    async updateOpponentColor({ commit, dispatch }, payload) {
        try {
            const response = await this.$axios.put(`/pbp/Voleibol/color`, payload);
            dispatch('notifications/setSnackbar', { text: response.data.MSG, color: 'success' }, { root: true })
            return true;
        } catch (error) {
            if (!!error.response) {
                dispatch('notifications/setSnackbar', { text: error.response.data.Error, color: 'error' }, { root: true })
            } else {
                dispatch('notifications/setSnackbar', { text: error.message, color: 'error' }, { root: true })
            }
            return false;
        }
    },

    // Add PBP player into game roster.
    async addPBPAthlete({ commit, dispatch }, payload) {
        try {
            const response = await this.$axios.post(`/pbp/Voleibol/roster`, payload);
            dispatch('notifications/setSnackbar', { text: response.data.MSG, color: 'success' }, { root: true })
            return true;
        } catch (error) {
            if (!!error.response) {
                dispatch('notifications/setSnackbar', { text: error.response.data.Error, color: 'error' }, { root: true })
            } else {
                dispatch('notifications/setSnackbar', { text: error.message, color: 'error' }, { root: true })
            }
            return false;
        }
    },

    // Update opponent PBP player.
    // Add PBP player into game roster.
    async updateOppAthlete({ commit, dispatch }, payload) {
        try {
            const response = await this.$axios.put(`/pbp/Voleibol/roster`, payload);
            dispatch('notifications/setSnackbar', { text: response.data.MSG, color: 'success' }, { root: true })
            return true;
        } catch (error) {
            if (!!error.response) {
                dispatch('notifications/setSnackbar', { text: error.response.data.Error, color: 'error' }, { root: true })
            } else {
                dispatch('notifications/setSnackbar', { text: error.message, color: 'error' }, { root: true })
            }
            return false;
        }
    },

    // Remove player from game roster.
    async removeAthlete({ commit, dispatch }, args) {
        try {
            const response = await this.$axios.delete(`/pbp/Voleibol/roster?${args}`);
            dispatch('notifications/setSnackbar', { text: response.data.MSG, color: 'success' }, { root: true })
            return true;
        } catch (error) {
            if (!!error.response) {
                dispatch('notifications/setSnackbar', { text: error.response.data.Error, color: 'error' }, { root: true })
            } else {
                dispatch('notifications/setSnackbar', { text: error.message, color: 'error' }, { root: true })
            }
            return false;
        }
    }

}