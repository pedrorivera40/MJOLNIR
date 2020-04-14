//Mutations are how you modify the state of the app.
export default {
  SET_USER_DATA(state, authData) {
    //Set user data
    state.user = this.$auth.user
    localStorage.setItem('user', JSON.stringify(state.user))

    //Set axios headers to contain the auth token by editing default axios config.
    this.$axios.defaults.headers.common['Authorization'] = `${authData.auth.token}`
  },

  SET_USER_PERMISSIONS(state, userPermissions) {
    //Set user data
    state.permissions = userPermissions
    localStorage.setItem('permissions', JSON.stringify(state.permissions))
  },
  SET_USER_DATA_ON_RELOAD(state) {
    //Set user data
    state.user = this.$auth.user

  },
  CLEAR_USER_DATA(state) {
    state.isLoading = false;
    this.$auth.logout()
    // //Clear userdata in local storage.
    localStorage.removeItem('user')
  },

  SET_LOADING(state){
    state.isLoading = true;
  },

  DONE_LOADING(state){
    state.isLoading = false;
  },

}