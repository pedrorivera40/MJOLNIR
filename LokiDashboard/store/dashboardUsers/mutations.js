//Mutations are how you modify the state of the app.
export default {
  SET_USER(state, user) {
    //Set user data
    state.user = user
  },
  SET_USERS(state, users) {
    //Set user data
    state.users = users

  },

  SET_LOADING(state){
    state.isLoading = true;
  },

  DONE_LOADING(state){
    state.isLoading = false;
  },

}