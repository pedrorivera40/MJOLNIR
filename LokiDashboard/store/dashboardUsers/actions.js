/**
 * Vuex store for sashboard users, with actions, mutations, getters and state.
 * @module dashboardUsers
 */

export default {

  /**
   * Action to fetch all the system users from the database.
   * @param {*} param0 destructuring of vuex context object
   */
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

  /**
   * Action to fetch user permissions given thir ID.
   * @param {*} param0 destructuring of vuex context object
   * @param {*} userID Id for the user whose permittions are being fetched.
   */
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
  
  /**
   * Action to set user permissions provided the user ID and a object with the permissions to be set.
   * @param {*} param0 destructuring of vuex context object
   * @param {*} payload Object containing user Id and user permissions to set.
   */
  async setPermissions({ commit, dispatch },payload) {
    try {
      await this.$axios.patch(`users/${payload.id}/permissions`, {permissions: payload.permissions})
      dispatch('notifications/setSnackbar', {text: 'Los permisos del usuario han sido guardados.', color: 'primary lighten-1'}, {root: true})

    } catch (error) {
      if(!!error.response.data){
        dispatch('notifications/setSnackbar', {text: error.response.data.Error, color: 'error'}, {root: true})
      } else {
        dispatch('notifications/setSnackbar', {text: error.message, color: 'error'}, {root: true})
      }

    }
  },

  /**
   * Action to delete a user from the system given their ID.
   * @param {*} param0 destructuring of vuex context object
   * @param {*} payload Object containing the user Id and their username.
   */
  async deleteUser({ commit, dispatch },payload) {
    try {
      await this.$axios.patch(`users/${payload.id}/remove`,)
      commit("DELETE_USER", payload.id)
      dispatch('notifications/setSnackbar', {text: `${payload.username} ha sido borrado.`, color: 'primary lighten-1'}, {root: true})

    } catch (error) {
      if(!!error.response.data){
        dispatch('notifications/setSnackbar', {text: error.response.data.Error, color: 'error'}, {root: true})
      } else {
        dispatch('notifications/setSnackbar', {text: error.message, color: 'error'}, {root: true})
      }

    }
  },

  /**
   * Action to add a new user to the system given their name, username, email, and password.
   * @param {*} param0 destructuring of vuex context object
   * @param {*} payload Object containing the information of the user to be added.
   */
  async addUser({ commit, dispatch }, payload) {
    try {
      const response = await this.$axios.post(`users/`, payload)
      commit("ADD_USER", response.data.User)
      dispatch('notifications/setSnackbar', {text: `${payload.username} ha sido añadido al sistema.`, color: 'primary lighten-1'}, {root: true})

    } catch (error) {
      if(!!error.response.data){
        dispatch('notifications/setSnackbar', {text: error.response.data.Error, color: 'error'}, {root: true})
        return 'error' //so modal does not close when an error happens.
      } else {
        dispatch('notifications/setSnackbar', {text: error.message, color: 'error'}, {root: true})
      }

    }
  },

  /**
   * Action to edit a user's information given their id, name, username, emaul, and account active status.
   * @param {*} param0 destructuring of vuex context object
   * @param {*} payload Object containing the information of the user to be edited.
   */
  async editUser({ commit, dispatch }, payload) {
    try {
      const response = await this.$axios.patch(`users/${payload.id}`, payload)
      commit("UPDATE_USER", response.data.User)
      dispatch('notifications/setSnackbar', {text: `La información de ${payload.username} ha sido actualizada!`, color: 'primary lighten-1'}, {root: true})

    } catch (error) {
      // console.log(error)
      if(!!error.response.data){
        dispatch('notifications/setSnackbar', {text: error.response.data.Error, color: 'error'}, {root: true})
        return 'error' //so modal does not close when an error happens.
      } else {
        dispatch('notifications/setSnackbar', {text: error.message, color: 'error'}, {root: true})
      }

    }
  },

  /**
   * Action that allows the admin to reset a user's password and set their active status to 0.
   * @param {*} param0 destructuring of vuex context object
   * @param {*} payload Object ontaining the Id of the user being reset and their new password.
   */
  async resetPasswordByAdmin({ commit, dispatch }, payload) {
    try {
      const response = await this.$axios.patch(`users/${payload.id}/reset`, payload)
      commit("UNLOCK_USER", response.data.User)
      dispatch('notifications/setSnackbar', {text: `La contraseña de ${payload.username} ha sido restablecida.`, color: 'primary lighten-1'}, {root: true})

    } catch (error) {
      if(!!error.response.data){
        dispatch('notifications/setSnackbar', {text: error.response.data.Error, color: 'error'}, {root: true})
        return 'error' //so modal does not close when an error happens.
      } else {
        dispatch('notifications/setSnackbar', {text: error.message, color: 'error'}, {root: true})
      }

    }
  },

}