export default {
  async login({ commit }, credentials) {
    try {
      const response = await this.$auth.loginWith('local',{ data: credentials }) //returns the desired data as json
      const user = await this.$axios.post('users/username/', credentials)
      const authUser = await this.$auth.setUser(user.data)
      console.log('authUser')
      console.log(authUser)
      commit("SET_USER_DATA", response.data) //Verify response json to make sure of the structure.
      this.$router.push('/inspire')
    } catch (error) {
      console.log("Trouble fetching events.", error)
    }
  },
  logout({ commit }) {
    commit("CLEAR_USER_DATA")
    this.$router.push('login')
  }
}