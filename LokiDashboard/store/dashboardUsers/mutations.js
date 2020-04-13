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
  SET_PERMISSIONS(state, permissions) {
    //Set user data
    state.permissions = permissions

  },

  DELETE_USER(state, id){
    state.users = state.users.filter(users => users.id !== id)
  },

  ADD_USER(state, user) {
    state.users.push(user)

  },
  
  SET_LOADING(state, selector){
    if(selector==='users'){
      state.isLoadingU = true
    }
    else if (selector==='permission'){
      state.isLoadingP = true;
    } 
  },

  DONE_LOADING(state, selector){
    if(selector==='users'){
      state.isLoadingU = false;
    }else if (selector==='permission'){
      state.isLoadingP = false;
    }
  },

}