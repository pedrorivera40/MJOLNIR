<template>
  <v-container class="mx-auto" max-width="400">
    <v-row justify="center">
      <v-icon size="100">{{icon}}</v-icon>
    </v-row>
    <v-row justify="center">
      <h1 font-size="10">{{error_text}}</h1>
    </v-row>
  </v-container>
</template>

<script>
export default {
  props: {
    error_text: String,
    icon: String
  }
};
</script>

<style>
</style>