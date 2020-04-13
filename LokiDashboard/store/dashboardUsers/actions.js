export default {
  async getUsers({ commit, dispatch }) {
    try {
      commit("SET_LOADING", 'users')
      const response = await this.$axios.get('users/')
      commit("SET_USERS", response.data.Users )
      commit("DONE_LOADING", 'users')

    } catch (error) {
      if(!!error.response.data){
        dispatch('notifications/setSnackbar', {text: error.response.data.Error, color: 'error'}, {root: true})
      } else {
        dispatch('notifications/setSnackbar', {text: error.message, color: 'error'}, {root: true})
      }

      commit("DONE_LOADING", 'users')
    }
  },

  async getPermissions({ commit, dispatch }, userID) {
    try {
      commit("SET_LOADING", 'permission')
      const response = await this.$axios.get(`users/${userID}/permissions`)
      commit("SET_PERMISSIONS", response.data.Permissions )
      commit("DONE_LOADING", 'permission')

    } catch (error) {
      if(!!error.response.data){
        dispatch('notifications/setSnackbar', {text: error.response.data.Error, color: 'error'}, {root: true})
      } else {
        dispatch('notifications/setSnackbar', {text: error.message, color: 'error'}, {root: true})
      }

      commit("DONE_LOADING", 'permission')
    }
  },
  
  async setPermissions({ commit, dispatch },payload) {
    try {
      await this.$axios.patch(`users/${payload.id}/permissions`, {permissions: payload.permissions})
      dispatch('notifications/setSnackbar', {text: 'User Permissions Saved.', color: 'primary lighten-1'}, {root: true})

    } catch (error) {
      if(!!error.response.data){
        dispatch('notifications/setSnackbar', {text: error.response.data.Error, color: 'error'}, {root: true})
      } else {
        dispatch('notifications/setSnackbar', {text: error.message, color: 'error'}, {root: true})
      }

      commit("DONE_LOADING", 'permission')
    }
  },

  async deleteUser({ commit, dispatch },payload) {
    try {
      await this.$axios.patch(`users/${payload.id}/remove`,)
      commit("DELETE_USER", payload.id)
      dispatch('notifications/setSnackbar', {text: `${payload.username} has been deleted.`, color: 'primary lighten-1'}, {root: true})

    } catch (error) {
      if(!!error.response.data){
        dispatch('notifications/setSnackbar', {text: error.response.data.Error, color: 'error'}, {root: true})
      } else {
        dispatch('notifications/setSnackbar', {text: error.message, color: 'error'}, {root: true})
      }

      commit("DONE_LOADING", 'permission')
    }
  },

  async addUser({ commit, dispatch }, payload) {
    try {
      const response = await this.$axios.post(`users/`, payload)
      commit("ADD_USER", response.data.User)
      dispatch('notifications/setSnackbar', {text: `${payload.username} has been added to the system..`, color: 'primary lighten-1'}, {root: true})

    } catch (error) {
      if(!!error.response.data){
        dispatch('notifications/setSnackbar', {text: error.response.data.Error, color: 'error'}, {root: true})
        return 'error' //so modal does not close when an error happens.
      } else {
        dispatch('notifications/setSnackbar', {text: error.message, color: 'error'}, {root: true})
      }

      commit("DONE_LOADING", 'permission')
    }
  },
  
  logout({ commit }) {
    commit("CLEAR_USER_DATA")
  }
}