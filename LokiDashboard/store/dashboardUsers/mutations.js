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

  UPDATE_USER(state, user) {
    //TODO TESTING if this triggers a refresh.
    const index = state.users.findIndex(arruser => arruser.id === user.id )
    if(index!==-1){
      //Susbtitute the old user with the updated user.
      state.users.splice(index, 1,user)
    }
    
    

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