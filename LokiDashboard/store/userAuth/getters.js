export default {
  /**
   * Getter or logged in user state.
   */
  user: state => state.user,

  /**
   * Getter for logged in user's permissions.
   */
  userPermissions: state => state.userPermissions,

  /**
   * Getter auth pages loading state.
   */
  isLoading: state => state.isLoading
}