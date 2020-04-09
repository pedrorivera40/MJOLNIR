export default {
  user: state => state.user,
  isLoggedIn(state) {
    /* !! returns thruthyness of the statement. 
    Thus determines is there is a user logges in or not */
    return !!state.user
  }
}