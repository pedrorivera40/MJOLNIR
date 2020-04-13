<template class="justify-center">
  <v-card width="600px" outlined class="pa-md-4 mx-lg-auto">
    <v-row align="center" justify="space-around">
      <v-col :cols="3">
        <v-avatar size="100" class="mx-10">
          <v-img :src="athlete_img" alt="ATHLETE" height="100px" />
          <v-progress-circular indeterminate color="grey lighten-5"></v-progress-circular>
        </v-avatar>
      </v-col>
      <v-col allign="center">
        <v-row class="mx-10" justify="center">
          <v-card-title>#{{athlete_number}}. {{athlete_name}}</v-card-title>
        </v-row>
        <v-row justify="center">
          <v-btn color="green" dark v-on="on">VER ESTADÍSTICAS</v-btn>
        </v-row>
      </v-col>
    </v-row>
  </v-card>
</template>

<script>
export default {
  props: {
    athlete_name: String,
    athlete_img: String,
    athlete_number: Number
  }
};
</script>