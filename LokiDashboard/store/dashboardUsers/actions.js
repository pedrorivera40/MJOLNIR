export default {
  async getUsers({ commit, dispatch }) {
    try {
      commit("SET_LOADING")
      const response = await this.$axios.get('users/')
      commit("SET_USERS", response.data.Users )
      commit("DONE_LOADING")

    } catch (error) {
      dispatch('notifications/setSnackbar', {text: error.response.data.Error, color: 'error'}, {root: true})
      commit("DONE_LOADING")
    }
  },
  
  logout({ commit }) {
    commit("CLEAR_USER_DATA")
  }
}