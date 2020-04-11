<template>
  <v-app>
    <v-content>
    <v-container class="main-container">
      <nuxt />
    </v-container>
  </v-content>
  </v-app>
</template>

<script>
export default {};
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
