const cookieparser = process.server ? require('cookieparser') : undefined

export default function ({ $auth, redirect, req }) {
  if (req.headers.cookie) {
    const parsed = cookieparser.parse(req.headers.cookie)
    console.log(parsed)

    if ($auth.loggedIn) {
      if (parsed.user)
      console.log('user cookie',parsed.user)
        return redirect('/dashboard')
    }
  } else return redirect('/login')
}