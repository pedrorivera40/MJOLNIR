export default {
  setSnackbar({commit}, snackbar) {
    snackbar.showing = true
    snackbar.color = snackbar.color || 'success'
    snackbar.multiline = (snackbar.text.length > 50) ? true: false
    commit('SET_SNACKBAR', snackbar)
  },
}