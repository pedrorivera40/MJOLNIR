export default {
  async login({ commit }, credentials) {
    try {
      const response = await this.$auth.loginWith('local',{ data: credentials }) //returns the desired data as json.
      const user = await this.$axios.post('users/username/', credentials) //call get user by username to set auth user.
      await this.$auth.setUser(user.data) // Set auth user.
      commit("SET_USER_DATA", response.data.User) 
    } catch (error) {
      console.log("Trouble fetching events.", error)
    }
  },
  logout({ commit }) {
    commit("CLEAR_USER_DATA")
  }
}