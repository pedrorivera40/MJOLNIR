export default {
  /**
   * Getter for user to be managed.
   */
  user: state => state.user,

  /**
   * Getter for the system users.
   */
  users: state => state.users,

  /**
   * Getter for the permissions of the user being managed.
   */
  permissions: state => state.permissions,

  /**
   * Getter for the loading state of the user update operations.
   */
  isLoadingU: state => state.isLoadingU,

  /**
   * Getter fot the loading state of the permissions of the user being managed.
   */
  isLoadingP: state => state.isLoadingP
}