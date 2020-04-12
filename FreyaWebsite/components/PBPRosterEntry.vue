<template>
  <v-card>
    <v-row>
      <v-col>
        <v-avatar :src="athlete_img" class="grey lighten-2" max-width="200" max-height="200">
          <template v-slot:placeholder>
            <v-row class="fill-height ma-0" align="center" justify="center">
              <v-progress-circular indeterminate color="grey lighten-5"></v-progress-circular>
            </v-row>
          </template>
        </v-avatar>
      </v-col>
      <v-col>
        <v-card-title>#{{athlete_number}}. {{athlete_name}}</v-card-title>
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