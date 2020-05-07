const cookieparser = process.server ? require('cookieparser') : undefined


// TO fix issue with notifications  changing state error
export const strict = false


//Rehydrates permission from cookies on reloads
export const actions = {
  async nuxtServerInit({ commit }, { $auth, req }) {
    let permissions = null
    let user = null
    if (req.headers.cookie) {
      const parsed = cookieparser.parse(req.headers.cookie)
      if (parsed.permissions && parsed.user) {
        try {
          permissions = JSON.parse(parsed.permissions)
          user = JSON.parse(parsed.user)
          await $auth.setUser(user)
        } catch (err) {
          console.log(err)
        }
      }
      // commit("userAuth/SET_USER_DATA_ON_RELOAD", { root: true })
      commit("userAuth/SET_USER_PERMISSIONS", permissions, { root: true })
    }
  }
}
