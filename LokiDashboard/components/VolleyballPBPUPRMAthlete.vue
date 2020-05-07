<template class="justify-center">
  <v-card outlined class="pa-md-4 mx-lg-auto">
    <v-row align="center" justify="space-around">
      <v-col :cols="1" class="mx-4">
        <v-checkbox v-model="in_game" color="primary" @change="inGameChanged()"></v-checkbox>
      </v-col>
      <v-col :cols="3">
        <v-row justify="center">
          <v-avatar size="100" class="mx-10">
            <v-icon x-large color="primary" v-if="!athlete_img" height="100px">mdi-account</v-icon>
            <v-img v-else :src="athlete_img" alt="ATHLETE" height="100px" />
            <v-progress-circular indeterminate color="grey lighten-5"></v-progress-circular>
          </v-avatar>
        </v-row>
      </v-col>
      <v-col justify="left">
        <v-card-title
          class="text-left"
          style="word-break: normal;"
        >#{{athlete_number}}. {{athlete_name}}</v-card-title>
      </v-col>
    </v-row>
  </v-card>
</template>

<script>
export default {
  props: {
    athlete_name: String,
    athlete_img: String,
    athlete_number: Number,
    athlete_id: Number,
    in_game: false
  },
  data: () => ({
    // in_game: false
  }),
  methods: {
    inGameChanged() {
      console.log(this.in_game);
    }
  }
};
</script>