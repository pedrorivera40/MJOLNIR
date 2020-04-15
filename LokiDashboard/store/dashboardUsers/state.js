export default ()=>({
  /**
   * State of user to be managed.
   */
  user: null,

  /**
   * State of system users.
   */
  users: [],
  
  /**
   * State of the permissions of the user to be managed.
   */
  permissions: [],

  /**
   * Loading indicator for user update dialog.
   */
  isLoadingU: false,

  /**
   * User indicator for user permissions dialog.
   */
  isLoadingP: false,
})