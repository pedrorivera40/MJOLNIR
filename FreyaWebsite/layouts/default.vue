<template>
  <v-app>
    <v-app-bar
      :clipped-left="clipped"
      fixed
      app
      dark
      color="blue-grey darken-4"
    >
      <v-img src="/logo.png" max-width="100px" class="ml-4" />

      <v-spacer />
      <v-btn
        v-for="item in items"
        :key="item.title"
        class="ma-1"
        text
        nuxt
        :to="item.to"
      >
        {{ item.title }}
      </v-btn>
    </v-app-bar>
    <v-content>
      <v-container>
        <nuxt />
      </v-container>
    </v-content>
    <v-navigation-drawer v-model="rightDrawer" :right="right" temporary fixed>
      <v-list>
        <v-list-item @click.native="right = !right">
          <v-list-item-action>
            <v-icon light>
              mdi-repeat
            </v-icon>
          </v-list-item-action>
          <v-list-item-title>Switch drawer (click me)</v-list-item-title>
        </v-list-item>
      </v-list>
    </v-navigation-drawer>
    <v-footer :fixed="fixed" app>
      <span>&copy; {{ new Date().getFullYear() }}</span>
    </v-footer>
  </v-app>
</template>

<script>
export default {
  data() {
    return {
      clipped: false,
      drawer: false,
      fixed: false,
      items: [
        {
          icon: "mdi-apps",
          title: "Eventos",
          to: "/"
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
