export default {
  async login({ commit, dispatch }, credentials) {
    try {
      commit("SET_LOADING")
      const response = await this.$auth.loginWith('local',{ data: credentials }) //returns the desired data as json.
      const user = await this.$axios.post('users/username/', credentials) //call get user by username to set auth user.
      await this.$auth.setUser(user.data.User) // Set auth user.
      commit("SET_USER_DATA", response.data.User) 
      dispatch('notifications/setSnackbar', {text: 'Login Sucessfully'}, {root: true})
    } catch (error) {
      // dispatch('notifications/setSnackbar', {text: error.response.data.Error, color: 'error'}, {root: true})
      commit("DONE_LOADING")
    }
  },
  async setUser({commit}){
    const user = JSON.parse(localStorage.getItem('user'))
    await this.$auth.setUser(user)
    
    commit("SET_USER_DATA_ON_RELOAD")
  },
  async reset({commit}, credentials){
    let id = ''
    try {
      const user = await this.$axios.post('users/username/', {username: credentials.username}) //call get user by username to set auth user.
      id = user.data.User.id
    
    } catch (error) {
      console.log(error.response.data.Error)
    }
    try {
      await this.$axios.patch(`users/${id}/reset`, {username: credentials.username, password: credentials.password}) //call get user by username to set auth user.
    } catch (error) {
      console.log(error.response.data.Error)
    }
  },
  logout({ commit }) {
    commit("CLEAR_USER_DATA")
  }
}