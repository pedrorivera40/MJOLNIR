//Mutations are how you modify the state of the app.
export default {

  /**
   * Mutation to set the state of the user bing managed.
   * @param {*} state vuex state object
   * @param {*} user Object with the information of the user being managed
   */
  SET_USER(state, user) {
    //Set user data
    state.user = user
  },

  /**
   * Mutation to set the state of the system users.
   * @param {*} state vuex state object
   * @param {*} users list of system users
   */
  SET_USERS(state, users) {
    //Set user data
    state.users = users

  },

  /**
   * 
   * @param {*} state vuex state object
   * @param {*} permissions permissions object for the user being managed.
   */
  SET_PERMISSIONS(state, permissions) {
    //Set user data
    state.permissions = permissions

  },

  /**
   * Mutation to filter the state's users effectively deleting them.
   * @param {*} state vuex state object
   * @param {*} id if of the user being deleted.
   */
  DELETE_USER(state, id){
    state.users = state.users.filter(users => users.id !== id)
  },


  /**
   * Mutation to add a new user to the state's users list.
   * @param {*} state vuex state object
   * @param {*} user Object with the information of the user being added
   */
  ADD_USER(state, user) {
    state.users.push(user)

  },

  /**
   * Mutation to set the information of the updated user in the state's users list.
   * @param {*} state vuex state object
   * @param {*} user Object with the information of the user being updated
   */
  UPDATE_USER(state, user) {
    const index = state.users.findIndex(arruser => arruser.id === user.id )
    if(index!==-1){
      //Susbtitute the old user with the updated user.
      state.users.splice(index, 1,user)
    }
  },

  /**
   * Mutation to commit to the state the change of active status of a user in the system.
   * @param {*} state vuex state object
   * @param {*} user Object with the information of the user being unlocked.
   */
  UNLOCK_USER(state, user) {
    user.is_active = !user.is_active
    const index = state.users.findIndex(arruser => arruser.id === user.id )
    if(index!==-1){
      //Susbtitute the old user with the updated user.
      state.users.splice(index, 1,user)
    }
  },
  
  /**
   * Mutation to trigger the loadin animation of the users table or the permissions dialog..
   * @param {*} state vuex state object
   * @param {*} selector Parameter to select between users or permissions
   */
  SET_LOADING(state, selector){
    if(selector==='users'){
      state.isLoadingU = true
    }
    else if (selector==='permission'){
      state.isLoadingP = true;
    } 
  },

  /**
   * Mutation to signal the end of the loading animation of the users table or the permissions dialog..
   * @param {*} state vuex state object
   * @param {*} selector Parameter to select between users or permissions
   */
  DONE_LOADING(state, selector){
    if(selector==='users'){
      state.isLoadingU = false;
    }else if (selector==='permission'){
      state.isLoadingP = false;
    }
  },

}