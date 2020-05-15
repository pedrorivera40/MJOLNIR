<template>
  <v-app class="backgrnd">
    <v-app-bar app color="primary" dark clipped-left v-if="$auth.loggedIn">
      <v-app-bar-nav-icon @click.stop="drawer = !drawer" />

      <v-toolbar-title class="headline font-weight-medium"
        >Huella Deportiva Dashboard</v-toolbar-title
      >

      <v-spacer />

      <v-icon class="mr-2" >mdi-account-circle</v-icon>

      <span class="font-weight-medium" dark v-if="user !== null">{{
        user.username
      }}</span>
      <v-tooltip bottom>
        <template v-slot:activator="{ on }">
          <v-btn class="ml-2" @click="logout(user)" v-on="on" icon>
            <v-icon>mdi-logout</v-icon>
          </v-btn>
        </template>
        <span>Logout</span>
      </v-tooltip>
    </v-app-bar>

    <v-navigation-drawer
      class="nav-drawer"
      app
      v-model="drawer"
      bottom
      clipped
      v-if="$auth.loggedIn"
    >
      <v-list dense>
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
          <v-list-item
            v-if="
              $store.state.userAuth.userPermissions[9]['22'] ||
              $store.state.userAuth.userPermissions[10]['23'] ||
              $store.state.userAuth.userPermissions[11]['24']
            "
            to="/usuarios"
            nuxt
          >
            <v-list-item-icon>
              <v-icon>mdi-clipboard-account</v-icon>
            </v-list-item-icon>
            <v-list-item-title>Manejo de Usuarios</v-list-item-title>
          </v-list-item>
        </v-list-item-group>
      </v-list>
    </v-navigation-drawer>
    <v-content>
      <v-container class="main-container">
        <nuxt />
      </v-container>
    </v-content>
    <TheSnackBar />
    <v-footer color="grey lighten-3" :fixed="fixed" app>
      <v-spacer />
      <span>MJOLNIR &copy; {{ new Date().getFullYear() }}</span>
    </v-footer>
  </v-app>
</template>

<script>
import { mapActions, mapGetters } from "vuex";
import TheSnackBar from "@/components/notifications/TheSnackBar";
export default {
  components: {
    TheSnackBar
  },
  data() {
    return {
      displayUser: "",
      clipped: false,
      drawer: !this.$vuetify.breakpoint.smAndDown, //it breakpoint small and down, drawer hidden by default.
      fixed: false,
      items: [
        {
          icon: "mdi-view-dashboard",
          title: "Dashboard",
          to: "/dashboard"
        },
        {
          icon: "mdi-account-group",
          title: "Equipos",
          to: "/deportes"
        },
        {
          icon: "mdi-run",
          title: "Atletas",
          to: "/atletas"
        },
        {
          icon: "mdi-calendar-multiple",
          title: "Eventos",
          to: "/eventos"
        }
      ],
      miniVariant: false,
      right: true,
      rightDrawer: false,
      title: "Vuetify.js"
    };
  },
  methods: {
    ...mapActions({
      logout: "userAuth/logout",
      setUser: "userAuth/setUser"
    }),
  },
  computed: {
    ...mapGetters({
      user: "userAuth/user"
    })
  },
  mounted() {
    this.setUser();
  }
};
</script>

<style lang="scss" scoped>
@import "../assets/variables.scss";
.backgrnd {
  background-color: whitesmoke;
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
}
</style>
