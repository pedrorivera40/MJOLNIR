const cookieparser = process.server ? require('cookieparser') : undefined


// TO fix issue with notifications  changing state error
export const strict = false


//Rehydrates permission from cookies on reloads
export const actions = {
  nuxtServerInit ({ commit }, { req }) {
    let permissions = null
    if (req.headers.cookie) {
      const parsed = cookieparser.parse(req.headers.cookie)
      try {
        permissions = JSON.parse(parsed.permissions)
      } catch (err) {
        console.log(error)
      }
    }
    commit("userAuth/SET_USER_PERMISSIONS", permissions, {root:true})
  }
}
