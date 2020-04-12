export default {
  async getUsers({ commit, dispatch }) {
    try {
      commit("SET_LOADING", 'users')
      const response = await this.$axios.get('users/')
      commit("SET_USERS", response.data.Users )
      commit("DONE_LOADING", 'users')

    } catch (error) {
      dispatch('notifications/setSnackbar', {text: error.response.data.Error, color: 'error'}, {root: true})
      commit("DONE_LOADING", 'users')
    }
  },

  async getPermissions({ commit, dispatch }, userID) {
    try {
      commit("SET_LOADING", 'permissions')
      const response = await this.$axios.get(`users/${userID}/permissions`)
      commit("SET_PERMISSIONS", response.data.Permissions )
      commit("DONE_LOADING", 'permissions')

    } catch (error) {
      dispatch('notifications/setSnackbar', {text: error.response.data.Error, color: 'error'}, {root: true})
      commit("DONE_LOADING", 'permissions')
    }
  },
  
  async setPermissions({ commit, dispatch }, userID) {
    try {
      commit("SET_LOADING", 'permissions')
      const response = await this.$axios.patch(`users/${userID}/permissions`)
      commit("SET_PERMISSIONS", response.data.Permissions )
      commit("DONE_LOADING", 'permissions')

    } catch (error) {
      dispatch('notifications/setSnackbar', {text: error.response.data.Error, color: 'error'}, {root: true})
      commit("DONE_LOADING", 'permissions')
    }
  },
  
  logout({ commit }) {
    commit("CLEAR_USER_DATA")
  }
}