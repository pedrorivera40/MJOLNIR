export default {
  async login({ commit, dispatch }, credentials) {
    try {
      commit("SET_LOADING")
      const response = await this.$auth.loginWith('local', { data: credentials }) //returns the desired data as json.
      const user = await this.$axios.post('users/username/', credentials) //call get user by username to set auth user.
      await this.$auth.setUser(user.data.User) // Set auth user.
      commit("SET_USER_DATA", response.data.User)
      dispatch('notifications/setSnackbar', { text: 'Login Sucessfully' }, { root: true })
    } catch (error) {
      if (!!error.response) {
        dispatch('notifications/setSnackbar', { text: error.response.data.Error, color: 'error' }, { root: true })
        commit("DONE_LOADING")
      }
    }
  },
  async setUser({ commit }) {
    const user = JSON.parse(localStorage.getItem('user'))
    await this.$auth.setUser(user)

    commit("SET_USER_DATA_ON_RELOAD")
  },

  async activateAccount({ commit, dispatch }, credentials) {
    let id = ''
    try {
      commit("SET_LOADING")
      const user = await this.$axios.post('users/username/', { username: credentials.username }) //call get user by username to set auth user.
      id = user.data.User.id

    } catch (error) {
      if (!!error.response) {
        dispatch('notifications/setSnackbar', { text: error.response.data.Error, color: 'error' }, { root: true })
        commit("DONE_LOADING")
      }
    }
    try {
      await this.$axios.patch(`users/${id}/reset`, { username: credentials.username, password: credentials.password }) //call get user by username to set auth user.
      commit("DONE_LOADING")
      dispatch('notifications/setSnackbar', { text: 'Password changed successfully! Please login.' }, { root: true })
    } catch (error) {
      if (!!error.response) {
        dispatch('notifications/setSnackbar', { text: error.response.data.Error, color: 'error' }, { root: true })
        commit("DONE_LOADING")
      }
    }
  },
  logout({ commit }) {
    commit("CLEAR_USER_DATA")
  }
}