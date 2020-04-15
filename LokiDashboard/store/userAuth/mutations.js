//Mutations are how you modify the state of the app.
export default {
  SET_USER_DATA(state, authData) {
    //Set user data
    state.user = this.$auth.user

    //If some other user data needs to be persisted, it can be added here as a property.
    localStorage.setItem('user', JSON.stringify({
      username:state.user.username,
    }))

    //Set axios headers to contain the auth token by editing default axios config.
    this.$axios.defaults.headers.common['Authorization'] = `${authData.auth.token}`
  },

  SET_USER_PERMISSIONS(state, userPermissions) {
    //Set user data
    state.userPermissions = userPermissions
    localStorage.setItem('permissions', JSON.stringify(state.userPermissions))
  },
  SET_USER_DATA_ON_RELOAD(state, userPermissions) {
    //Set user data
    state.user = this.$auth.user
    state.userPermissions = userPermissions

  },
  CLEAR_USER_DATA(state) {
    state.isLoading = false;
    this.$auth.logout()

    //Clear userdata from local storage.
    localStorage.removeItem('user')
    localStorage.removeItem('permissions')
    localStorage.removeItem('auth._refresh_token.local')
    localStorage.removeItem('auth._token.local')
    localStorage.removeItem('auth.strategy')
  },

  SET_LOADING(state){
    state.isLoading = true;
  },

  DONE_LOADING(state){
    state.isLoading = false;
  },

}