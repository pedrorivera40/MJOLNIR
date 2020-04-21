<template>
  <v-container>
    <v-card>
      <v-card width="600px" outlined class="pa-md-4 mx-lg-auto">
        <v-row align="center" justify="space-around">
          <v-col :cols="3">
            <v-avatar size="100" class="mx-10">
              <v-icon x-large :color="in_color" v-if="!athlete_img" height="100px">mdi-account</v-icon>
              <v-img v-else :src="athlete_img" alt="ATHLETE" height="100px" />
              <v-progress-circular indeterminate color="grey lighten-5"></v-progress-circular>
            </v-avatar>
          </v-col>
          <v-col allign="center">
            <v-row class="mx-10" justify="center">
              <v-card-title>#{{athlete_number}}. {{athlete_name}}</v-card-title>
            </v-row>
          </v-col>
        </v-row>
      </v-card>
    </v-card>
    <VolleyballStatistics :volleyball_stats="athlete_statistics" />
  </v-container>
</template>

<script>
import VolleyballStatistics from "../components/VolleyballStatistics";

export default {
  components: {
    VolleyballStatistics
  },
  props: {
    athlete_statistics: {},
    athlete_name: String,
    athlete_img: String,
    athlete_number: Number,
    in_color: String
  }
};
</script>