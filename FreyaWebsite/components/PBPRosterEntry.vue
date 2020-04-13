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
          <v-btn color="green" dark @click="dialog = true">VER ESTADÍSTICAS</v-btn>
          <v-dialog v-model="dialog" max-width="600px">
            <VolleyballStatistics :volleyball_stats="athlete_statistics" />
          </v-dialog>
        </v-row>
      </v-col>
    </v-row>
  </v-card>
</template>

<script>
import VolleyballStatistics from "../components/VolleyballStatistics";

export default {
  components: {
    VolleyballStatistics
  },
  props: {
    athlete_name: String,
    athlete_img: String,
    athlete_number: Number,
    athlete_statistics: {}
  },
  data: () => ({
    dialog: false
  })
};
</script>