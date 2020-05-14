<template>
  <v-card>
    <v-toolbar :color="in_color" dark flat>
      <v-row justify="center" align="center">
        <v-card-title class="title text-center" style="word-break: normal;">{{ error_header }}</v-card-title>
      </v-row>
    </v-toolbar>
    <v-row>
      <v-card-text class="subtitle-1 text-center" style="word-break: normal;">{{ error_message }}</v-card-text>
    </v-row>
  </v-card>
</template>

<script>
export default {
  props: {
    error_header: String,
    error_message: String,
    in_color: String
  }
};
</script>

