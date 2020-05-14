<template>
  <v-app class="backgrnd">
    <v-content>
      <v-container class="main-container text-center">
        <h1 v-if="error.statusCode === 404">
          {{ pageNotFound }}
        </h1>
        <h1 v-else>
          {{ otherError }}
        </h1>
        <NuxtLink to="/">
          Home page
        </NuxtLink>
      </v-container>
    </v-content>
    <TheSnackBar />
  </v-app>
</template>

<script>
import TheSnackBar from "@/components/notifications/TheSnackBar";

export default {
  layout: "empty",
  components: {
    TheSnackBar
  },
  props: {
    error: {
      type: Object,
      default: null
    }
  },
  data() {
    return {
      pageNotFound: "404 Not Found",
      otherError: "An error occurred"
    };
  },
  head() {
    const title =
      this.error.statusCode === 404 ? this.pageNotFound : this.otherError;
    return {
      title
    };
  }
};
</script>

<style lang="scss" scoped>
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
