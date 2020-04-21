//Mutations are how you modify the state of the app.
export default {

  /**
   * Mutation that adds a snackbar object to the state list of snackbars.
   * @param {*} state vuex state
   * @param {*} snackbar snackbar object.
   */
  SET_SNACKBAR(state, snackbar) {
    //Set snackbars, if notificatoins come from the system they will be added to the list.
    state.snackbars = state.snackbars.concat(snackbar);
  },
}