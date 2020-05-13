<template>
  <v-app>
    <v-app-bar
      :clipped-left="clipped"
      fixed
      app
      dark
      color="blue-grey darken-4"
    >
      <v-app-bar-nav-icon
        v-if="this.$vuetify.breakpoint.smAndDown"
        @click.stop="drawer = !drawer"
      ></v-app-bar-nav-icon>
      <div class="logo">
        <v-img
          v-if="this.$vuetify.breakpoint.smAndDown"
          @click="home"
          src="/logo.png"
          max-width="80px"
          class="ml-4 logo"
        />
        <v-img
          v-else
          @click="home"
          src="/logo.png"
          max-width="100px"
          class="ml-4 logo"
        />
      </div>

      <v-spacer />
      <nav v-if="this.$vuetify.breakpoint.mdAndUp">
        <nuxt-link
          v-for="item in items"
          :key="item.title"
          class="ma-4 nav text-uppercase"
          class-active="active"
          :to="item.to"
        >
          {{ item.title }}
        </nuxt-link>
      </nav>
    </v-app-bar>
    <v-navigation-drawer
      app
      v-model="drawer"
      v-if="this.$vuetify.breakpoint.smAndDown"
      class="nav-drawer"
      bottom
    >
      <v-list nav>
        <v-list-item-group
          class="nav-links"
        >
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
    <v-footer :fixed="fixed" app>
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
      clipped: false,
      drawer: false,
      fixed: false,
      items: [
        {
          icon: "mdi-calendar-multiple",
          title: "Eventos",
          to: "/eventos"
        },
        {
          icon: "mdi-account-group",
          title: "Deportes Masculino",
          to: "/deportes-masculino"
        },
        {
          icon: "mdi-account-group",
          title: "Deportes Femenino",
          to: "/deportes-femenino"
        },
        {
          icon: "mdi-account-group",
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
.nav {
  text-decoration: none;
  color: whitesmoke;
  font-weight: 300;
  font-size: 1.3rem;
  margin: 0 10px;
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
        color: #45b439;
      }
    }
  }
</style>