export default {
  mode: 'universal',
  /*
  ** Headers of the page
  */
  head: {
    titleTemplate: '%s - Huella Deportiva Web',
    title: 'Huella Deportiva Web' || process.env.npm_package_name,
    meta: [
      { charset: 'utf-8' },
      { name: 'viewport', content: 'width=device-width, initial-scale=1' },
      { hid: 'description', name: 'description', content: process.env.npm_package_description || '' }
    ],
    link: [
      { rel: 'icon', type: 'image/x-icon', href: '/favicon.ico' }
    ]
  },
  /*
  ** Customize the progress-bar color
  */
  loading: { color: '#fff' },
  /*
  ** Global CSS
  */
  css: [
  ],
  /*
  ** Plugins to load before mounting the App
  */
  plugins: [
  ],
  /*
  ** Nuxt.js dev-modules
  */
  buildModules: [
    '@nuxtjs/vuetify',
  ],
  /*
  ** Nuxt.js modules
  */
  modules: [
    // Doc: https://axios.nuxtjs.org/usage
    '@nuxtjs/axios',
    // Doc: https://github.com/nuxt-community/dotenv-module
    '@nuxtjs/dotenv',
    //Doc: https://auth.nuxtjs.org 
    '@nuxtjs/auth',
  ],
  /*
  ** Axios module configuration
  ** See https://axios.nuxtjs.org/options
  */
  axios: {
    // baseURL: 'https://white-smile-272204.ue.r.appspot.com/' //Route for the Flask API Hosted
    baseURL: 'http://127.0.0.1:5000/' //Route for the Flask API Local
  },

  /*
  ** Auth module configuration
  ** See https://auth.nuxtjs.org/schemes/local.html#options
  */
  auth: {
    strategies: {
      redirect: {
        login: '/login',
        logout: '/',
        callback: false,
        home: '/dashboard'
      },
      local: {
        endpoints: {
          login: { url: 'auth/', method: 'post', propertyName: 'auth.token' },
          user: false,
          logout: false,
        },
        // tokenRequired: true,
        tokenType: '',
        autoFetchUser: false,
      }
    }
  },
  /**
   * Router module configuration
   */
  router: {
    middleware: [
      'auth' //sets global guard. All routes requires auth, unless explicitly stated otherwise.
    ]
  },
  /*
  ** vuetify module configuration
  ** https://github.com/nuxt-community/vuetify-module
  */
  vuetify: {
    customVariables: ['~/assets/variables.scss'],
    theme: {
      dark: false,
      light: true,
      themes: {
        dark: {
          primary: '#168F09',
          primary_dark: '#0B7300',
          primary_light: '#26B117',
          accent: '#45b439',
          error: '#FF5252',
          info: '#2196F3',
          success: '#4CAF50',
          warning: '#FFC107',
        },
        light: {
          primary: '#168F09',
          primary_dark: '#0B7300',
          primary_light: '#26B117',
          accent: '#999999',
          error: '#FF5252',
          info: '#2196F3',
          success: '#4CAF50',
          warning: '#FFC107',
        },
      }
    }
  },
  /**
   * Development server configuration
   */
  server: {
    // host: "0.0.0.0",
    host: "127.0.0.1",
    port: 7071
  },
  /*
  ** Build configuration
  */
  build: {
    /*
    ** You can extend webpack config here
    */
    transpile: [
      "vee-validate/dist/rules"
    ],
    extend(config, ctx) {
    }
  }
}
