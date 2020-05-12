export default {
  /**
   * Action to create a snackbar that serves as system wide notification delivery for system actions.
   * @param {*} param0 destructuring of vuex context object
   * @param {*} snackbar options for the snackbar component
   */
  setSnackbar({commit}, snackbar) {
    snackbar.showing = true
    snackbar.color = snackbar.color || 'success'
    snackbar.multiline = (snackbar.text.length > 100) ? true: false
    commit('SET_SNACKBAR', snackbar)
  },
}