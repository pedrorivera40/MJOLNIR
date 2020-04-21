<template class="justify-center">
  <v-hover v-slot:default="{ hover }" open-delay="25">
    <v-card width="600px" outlined class="pa-md-4 mx-lg-auto" :elevation="hover ? 16 : 2">
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
          <v-row justify="center">
            <v-btn color="green" dark @click="dialog = true">VER ESTADÍSTICAS</v-btn>
            <v-dialog v-model="dialog" max-width="600px">
              <VolleyballPBPAthleteStatistics
                :athlete_name="athlete_name"
                :athlete_img="athlete_img"
                :athlete_number="athlete_number"
                :athlete_statistics="athlete_statistics"
                :in_color="in_color"
              />
            </v-dialog>
          </v-row>
        </v-col>
      </v-row>
    </v-card>
  </v-hover>
</template>

<script>
import VolleyballPBPAthleteStatistics from "../components/VolleyballPBPAthleteStatistics";

export default {
  components: {
    VolleyballPBPAthleteStatistics
  },
  props: {
    athlete_name: String,
    athlete_img: String,
    athlete_number: Number,
    athlete_statistics: {},
    in_color: String
  },
  data: () => ({
    dialog: false
  })
};
</script>