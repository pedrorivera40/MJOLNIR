<template>
  <v-app>
    <v-app-bar fixed app dark color="blue-grey darken-4">
      <v-app-bar-nav-icon @click.stop="drawer = !drawer"></v-app-bar-nav-icon>
      <v-img
        @click="home"
        src="/logo.png"
        :max-width="$vuetify.breakpoint.smAndDown ? '80px' : '100px'"
        class="ml-4 logo"
      />

      <v-spacer />
      <nav v-if="$vuetify.breakpoint.mdAndUp">
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
    <v-navigation-drawer
      class="nav-drawer"
      v-model="drawer"
      app
      bottom
      temporary
    >
      <v-list nav>
        <v-list-item-group class="nav-links">
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
      ]
    };
  }
};
</script>
<style lang="scss" scoped>
.nav {
  text-decoration: none;
  color: whitesmoke;
  font-weight: 300;
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
.nuxt-link-exact-active {
  color: #168f09;
  font-weight: 500;
}
.nav-drawer {
  .nav-links {
    a {
      color: #168f09;
    }
  }
}
</style>