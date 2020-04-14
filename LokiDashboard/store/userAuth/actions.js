export default {
  async login({ commit, dispatch }, credentials) {
    try {
      commit("SET_LOADING")
      const response = await this.$auth.loginWith('local', { data: credentials }) //returns auth data as json.
      const user = await this.$axios.post('users/username/', credentials) //call get user by username to set auth user.
      await this.$auth.setUser(user.data.User) // Set auth user.
      
      dispatch('getUserPermissions', user.data.User.id)
      dispatch('notifications/setSnackbar', { text: 'Login Sucessfully' }, { root: true })
      commit("SET_USER_DATA", response.data)
    } catch (error) {
      if (!!error.response) {
        dispatch('notifications/setSnackbar', { text: error.response.data.Error, color: 'error' }, { root: true })
        commit("DONE_LOADING")
      } else {
        dispatch('notifications/setSnackbar', { text: error.message, color: 'error' }, { root: true })
      }
    }
  },
  async setUser({ commit }) {
    const user = JSON.parse(localStorage.getItem('user'))

    const permissions = JSON.parse(localStorage.getItem('permissions'))
    await this.$auth.setUser(user)

    commit("SET_USER_DATA_ON_RELOAD", permissions)
  },

  async activateAccount({ commit, dispatch }, credentials) {
    try {
      commit("SET_LOADING")
      await this.$axios.patch(`users/activate`, { username: credentials.username, password: credentials.password, new_password: credentials.new_password }) //call get user by username to set auth user.
      commit("DONE_LOADING")
      dispatch('login', { username: credentials.username, password: credentials.new_password })
      dispatch('notifications/setSnackbar', { text: 'Password changed successfully! Loggin in...' }, { root: true })
    } catch (error) {
      if (!!error.response) {
        dispatch('notifications/setSnackbar', { text: error.response.data.Error, color: 'error' }, { root: true })
        commit("DONE_LOADING")
      } else {
        dispatch('notifications/setSnackbar', { text: error.message, color: 'error' }, { root: true })
      }
    }

  },

  async getUserPermissions({ commit, dispatch }, userID) {
    try {
      const response = await this.$axios.get(`/users/${userID}/permissions`)
      commit("SET_USER_PERMISSIONS", response.data.Permissions)
    } catch (error) {
      if (!!error.response) {
        dispatch('notifications/setSnackbar', { text: error.response.data.Error, color: 'error' }, { root: true })
      } else {
        dispatch('notifications/setSnackbar', { text: error.message, color: 'error' }, { root: true })
      }
    }
  },
  logout({ commit }) {
    commit("CLEAR_USER_DATA")
  }
}