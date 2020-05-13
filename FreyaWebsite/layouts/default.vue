<template>
  <v-app>
    <v-app-bar
      :clipped-left="clipped"
      fixed
      app
      dark
      color="blue-grey darken-4"
    >
      <v-img @click="home" src="/logo.png" max-width="100px" class="ml-4 logo" />

      <v-spacer />
      <nav>
        <nuxt-link
          v-for="item in items"
          :key="item.title"
          class="ma-1 nav text-uppercase"
          class-active="active"
          :to="item.to"
        >
          {{ item.title }}
        </nuxt-link>
      </nav>
    </v-app-bar>
    <v-content>
      <v-container>
        <nuxt />
      </v-container>
    </v-content>
    <v-footer :fixed="fixed" app>
      <v-spacer></v-spacer>
      <span>MJOLNIR &copy; {{ new Date().getFullYear() }}</span>
    </v-footer>
  </v-app>
</template>

<script>
export default {
  methods:{
    home(){
      this.$router.push('/')
    }
  },
  data() {
    return {
      clipped: false,
      drawer: false,
      fixed: false,
      items: [
        {
          icon: "mdi-apps",
          title: "Eventos",
          to: "/eventos"
        },
        {
          icon: "mdi-chart-bubble",
          title: "Deportes Masculino",
          to: "/deportes-masculino"
        },
        {
          icon: "mdi-chart-bubble",
          title: "Deportes Femenino",
          to: "/deportes-femenino"
        },
        {
          icon: "mdi-chart-bubble",
          title: "Deportes de Exhibición",
          to: "/deportes-exhibicion"
        },
        {
          icon: "mdi-chart-bubble",
          title: "Sobre Nosotros",
          to: "/inspire"
        }
      ],
      miniVariant: false,
      right: true,
      rightDrawer: false,
      title: "Vuetify.js"
    };
  }
};
</script>
<style lang="scss" scoped>
  .nav{
    text-decoration: none;
    color: whitesmoke;
    font-weight: 300;
    font-size: 1.3rem;
    &:hover {
      color: #168f09;
    }
    
  }
  .logo {
    cursor: pointer;
  }
  .nuxt-link-exact-active {
      color: #168f09;
      font-weight: 500;
    }
</style>