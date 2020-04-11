export default {
  setSnackbar({commit}, snackbar) {
    snackbar.showing = true;
    snackbar.color = snackbar.color || 'success';
    commit('SET_SNACKBAR', snackbar);
  },
  closeSnackbar({commit}, snackbar) {
    snackbar.showing = false;
    // commit('CLOSE_SNACKBAR', snackbar);
  },
}