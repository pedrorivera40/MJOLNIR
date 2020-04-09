<template>
  <v-app>
    <v-app-bar app color="primary" dark clipped-left v-if="$auth.isLoggedin">
      <v-app-bar-nav-icon @click.stop="drawer = !drawer" />

      <v-toolbar-title>Huella Deportiva Dashboard</v-toolbar-title>

      <v-spacer />

      <v-btn icon>
        <v-icon>mdi-account-circle</v-icon>
      </v-btn>

      <v-menu left bottom>
        <template v-slot:activator="{ on }">
          <v-btn icon v-on="on">
            <v-icon>mdi-menu-down</v-icon>
          </v-btn>
        </template>

        <v-list>
          <v-list-item v-for="n in 5" :key="n" @click="() => {}">
            <v-list-item-title>Option {{ n }}</v-list-item-title>
          </v-list-item>
        </v-list>
      </v-menu>
    </v-app-bar>

    <v-navigation-drawer
      class="nav-drawer"
      app
      v-model="drawer"
      bottom
      clipped
      v-if="$auth.isLoggedin"
    >
      >
      <v-list dense>
        <v-list-item-group class="nav-links">
          <v-list-item v-for="(item,index) in items" :key="index" :to="item.to" nuxt>
            <v-list-item-icon>
              <v-icon>{{ item.icon }}</v-icon>
            </v-list-item-icon>
            <v-list-item-title>{{item.title}}</v-list-item-title>
          </v-list-item>
        </v-list-item-group>
      </v-list>
    </v-navigation-drawer>
    <v-content>
      <v-container class="main-container">
        <nuxt />
      </v-container>
    </v-content>
    <v-footer :fixed="fixed" app>
      <v-spacer />
      <span>MJOLNIR &copy; {{ new Date().getFullYear() }}</span>
    </v-footer>
  </v-app>
</template>

<script>
export default {
  data() {
    return {
      clipped: false,
      drawer: true,
      fixed: false,
      items: [
        {
          icon: "mdi-view-dashboard",
          title: "Dashboard",
          to: "/dashboard"
        },
        {
          icon: "mdi-clipboard-account",
          title: "User Management",
          to: "/users"
        },
        {
          icon: "mdi-account-group",
          title: "Sports Teams",
          to: "/teams"
        },
        {
          icon: "mdi-run",
          title: "Athletes",
          to: "/athletes"
        },
        {
          icon: "mdi-calendar-multiple",
          title: "Events",
          to: "/events"
        },
        {
          icon: "mdi-strategy",
          title: "Play By Play",
          to: "/play-by-play"
        },
        {
          icon: "mdi-chart-bubble",
          title: "Inspire",
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
@import "../assets/variables.scss";
.main-container {
  height: 100%;
}
.nav-drawer {
  .nav-links {
    a {
      color: $highlight-color;
    }
  }
}
</style>
