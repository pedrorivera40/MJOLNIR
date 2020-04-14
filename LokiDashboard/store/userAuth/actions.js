export default {
  async login({ commit, dispatch }, credentials) {
    try {
      commit("SET_LOADING")
      const response = await this.$auth.loginWith('local', { data: credentials }) //returns the desired data as json.
      const user = await this.$axios.post('users/username/', credentials) //call get user by username to set auth user.
      await this.$auth.setUser(user.data.User) // Set auth user.
      dispatch('notifications/setSnackbar', { text: 'Login Sucessfully' }, { root: true })
      commit("SET_USER_DATA", response.data.User)
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
    try {
      commit("SET_LOADING")
      await this.$axios.patch(`users/activate`, { username: credentials.username, password: credentials.password, new_password: credentials.new_password }) //call get user by username to set auth user.
      commit("DONE_LOADING")
      dispatch('login',{ username: credentials.username, password: credentials.new_password})
      dispatch('notifications/setSnackbar', { text: 'Password changed successfully! Loggin in...' }, { root: true })
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