<template>
  <v-layout
    column
  >
    <v-flex
      xs12
      sm8
      md6
    >
      <div class="text-center">
        <h1 class="header my-12">Welcome to Huella Deportiva Dashboard!</h1>
        <logo />
        <h2 class="my-6">Please, login to continue.</h2>
        <v-btn color="primary_dark" dark link to="/login">
          Login
        </v-btn>
      </div>
    </v-flex>
  </v-layout>
</template>

<script>
import Logo from '~/components/Logo.vue'

export default {
  components: {
    Logo,
  }
}
</script>

<style lang="scss" scoped>
  .header {
    font-size: 3rem;
  }
</style>