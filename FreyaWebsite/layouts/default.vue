<template>
  <v-app class="app">
    <v-app-bar fixed app dark color="blue-grey darken-4">
      <client-only>
        <v-app-bar-nav-icon
          v-if="this.$vuetify.breakpoint.smAndDown"
          @click.stop="drawer = !drawer"
        ></v-app-bar-nav-icon>
        <h3 v-if="this.$vuetify.breakpoint.smAndDown" class="headline">
          Huella Deportiva Web
        </h3>
        <v-img
          v-else
          @click="home"
          src="/logo.png"
          max-width="100px"
          class="ml-4 logo"
        />

        <v-spacer />
        <nav v-if="this.$vuetify.breakpoint.mdAndUp">
          <nuxt-link
            v-for="item in items"
            :key="item.title"
            class="ma-2 nav text-uppercase"
            class-active="active"
            :to="item.to"
          >
            {{ item.title }}
          </nuxt-link>
        </nav>
      </client-only>
    </v-app-bar>
    <v-navigation-drawer
      class="nav-drawer"
      v-model="drawer"
      app
      bottom
      temporary
    >
      <v-list nav>
        <v-list-item-group class="nav-links">
          <v-list-item to="/" nuxt>
            <v-list-item-icon>
              <v-icon>mdi-home</v-icon>
            </v-list-item-icon>
            <v-list-item-title>Home</v-list-item-title>
          </v-list-item>
          <v-list-item
            v-for="(item, index) in items"
            :key="index"
            :to="item.to"
            nuxt
          >
            <v-list-item-icon>
              <v-icon>{{ item.icon }}</v-icon>
            </v-list-item-icon>
            <v-list-item-title>{{ item.title }}</v-list-item-title>
          </v-list-item>
        </v-list-item-group>
      </v-list>
    </v-navigation-drawer>
    <v-content>
      <v-container>
        <nuxt />
      </v-container>
    </v-content>
    <v-footer fixed app>
      <v-spacer></v-spacer>
      <span>MJOLNIR &copy; {{ new Date().getFullYear() }}</span>
    </v-footer>
  </v-app>
</template>

<script>
export default {
  methods: {
    home() {
      this.$router.push("/");
    }
  },
  data() {
    return {
      drawer: false,
      items: [
        {
          icon: "mdi-calendar-multiple",
          title: "Eventos",
          to: "/eventos"
        },
        {
          icon: "mdi-account-group",
          title: "Deportes: Masculino",
          to: "/deportes-masculino"
        },
        {
          icon: "mdi-account-group-outline",
          title: "Deportes: Femenino",
          to: "/deportes-femenino"
        },
        {
          icon: "mdi-account-multiple-outline",
          title: "Deportes de Exhibición",
          to: "/deportes-exhibicion"
        },
        {
          icon: "mdi-run-fast",
          title: "Atletas",
          to: "/atletas"
        },
        {
          icon: "mdi-paw",
          title: "Sobre Nosotros",
          to: "/inspire"
        }
      ]
    };
  }
};
</script>
<style lang="scss" scoped>
.app {
  background-color: whitesmoke;
}
.nav {
  text-decoration: none;
  color: whitesmoke;
  font-weight: 400;
  font-size: 1.3rem;
  &:hover {
    color: #168f09;
  }

  &:focus {
    outline: none;
  }
}
.logo {
  cursor: pointer;
}
.nuxt-link-active {
  color: #168f09;
}
.nav-drawer {
  .nav-links {
    a {
      color: #168f09;
    }
  }
}
</style>