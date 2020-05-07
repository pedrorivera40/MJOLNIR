
export default function ({ store, redirect }) {
  if (
    !(store.state.userAuth.userPermissions[9]['22'] ||
      store.state.userAuth.userPermissions[10]['23'] ||
      store.state.userAuth.userPermissions[11]['24'])
  ) {
    return redirect('/dashboard')
  }
}