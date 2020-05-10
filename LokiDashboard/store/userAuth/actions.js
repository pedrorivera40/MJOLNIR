const Cookie = process.client ? require('js-cookie') : undefined 
export default {
  /**
   * Action  to log a user into the system, and set their data in the store.
   * @param {*} param0 destructuring of the vuex context object
   * @param {*} credentials credentials passed in for the user.
   */
  async login({ commit, dispatch }, credentials) {
    try {
      commit("SET_LOADING")
      const response = await this.$auth.loginWith('local', { data: credentials }) //returns auth data as json.
      const user = await this.$axios.post('users/username/', credentials) //call get user by username to set auth user.
      await this.$auth.setUser(user.data.User) // Set auth user.
      Cookie.set('user', JSON.stringify({username:user.data.User.username}))
      dispatch('getUserPermissions', response.data.auth.token)
      dispatch('notifications/setSnackbar', { text: 'Login Exitoso!' }, { root: true })
      commit("SET_USER_DATA", response.data)
    } catch (error) {
      if (!!error.response) {
        dispatch('notifications/setSnackbar', { text: error.response.data.Error, color: 'error' }, { root: true })
        commit("DONE_LOADING")
      } else {
        dispatch('notifications/setSnackbar', { text: error.message, color: 'error' }, { root: true })
        commit("DONE_LOADING")
      }
    }
  },

  /**
   * Action to rehydrate a user's information after a reload.
   * @param {*} param0 destructuring of vuex context object.
   */
  async setUser({ commit }) {
    const user = JSON.parse(localStorage.getItem('user'))
    await this.$auth.setUser(user)

    commit("SET_USER_DATA_ON_RELOAD")
  },

  /**
   * Action to activate an inactive acount by using a temporary password. 
   * @param {*} param0 destructuring of vuex context object
   * @param {*} credentials credentials passed in for the user.
   */
  async activateAccount({ commit, dispatch }, credentials) {
    try {
      commit("SET_LOADING")
      await this.$axios.patch(`users/activate`, { username: credentials.username, password: credentials.password, new_password: credentials.new_password }) //call get user by username to set auth user.
      commit("DONE_LOADING")
      dispatch('login', { username: credentials.username, password: credentials.new_password })
      dispatch('notifications/setSnackbar', { text: 'Cambio de contraseña exitoso! Iniciando sesión...' }, { root: true })
    } catch (error) {
      if (!!error.response) {
        dispatch('notifications/setSnackbar', { text: error.response.data.Error, color: 'error' }, { root: true })
        commit("DONE_LOADING")
      } else {
        dispatch('notifications/setSnackbar', { text: error.message, color: 'error' }, { root: true })
      }
    }

  },

  /**
   * Action to get the logged in user's system permissions.
   * @param {*} param0 destructuring of vuex context object
   * @param {*} token Logged in user's auth token
   */
  async getUserPermissions({ commit, dispatch }, token) {
    try {
      // Extract permissions from jwt
      const permissions = JSON.parse(atob(token.split('.')[1])).permissions
      
      Cookie.set('permissions', permissions)

      commit("SET_USER_PERMISSIONS", permissions)
    } catch (error) {
      if (!!error.response) {
        dispatch('notifications/setSnackbar', { text: error.response.data.Error, color: 'error' }, { root: true })
      } else {
        dispatch('notifications/setSnackbar', { text: error.message, color: 'error' }, { root: true })
      }
    }
  },

  /**
   * Action to logout a user from the system and clear their data.
   * @param {*} param0 destructuring of vuex context object
   */
  logout({ commit }) {
    commit("CLEAR_USER_DATA")
  }
}