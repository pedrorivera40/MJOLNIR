<template>
  <v-app class="backgrnd">
    <v-content>
      <v-container class="main-container">
        <nuxt />
      </v-container>
    </v-content>
    <TheSnackBar />
  </v-app>
</template>

<script>
import TheSnackBar from "@/components/notifications/TheSnackBar";
export default {
  components: {
    TheSnackBar,
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
}
</style>
