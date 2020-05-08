<template class="justify-center">
  <v-card outlined class="pa-md-4 mx-lg-auto">
    <v-row align="center" justify="space-around">
      <v-col :cols="1" class="mx-4">
        <v-checkbox v-model="in_game" color="primary" @change="inGameChanged()"></v-checkbox>
      </v-col>
      <v-col :cols="3">
        <v-row justify="center">
          <v-avatar size="75" class="mx-10">
            <v-icon x-large color="primary" v-if="!athlete_img" height="100px">mdi-account</v-icon>
            <v-img v-else :src="athlete_img" alt="ATHLETE" height="75px" />
            <v-progress-circular indeterminate color="grey lighten-5"></v-progress-circular>
          </v-avatar>
        </v-row>
      </v-col>
      <v-col justify="left">
        <v-card-title
          v-if="athlete_middle_name === ''"
          class="text-left"
          style="word-break: normal;"
        >#{{athlete_number}}. {{athlete_first_name}} {{athlete_last_names}}</v-card-title>
        <v-card-title
          v-else
          class="text-left"
          style="word-break: normal;"
        >#{{athlete_number}}. {{athlete_first_name}} {{athlete_middle_name}} {{athlete_last_names}}</v-card-title>
      </v-col>
    </v-row>
  </v-card>
</template>

<script>
import { mapActions, mapGetters } from "vuex";

export default {
  props: {
    athlete_first_name: String,
    athlete_middle_name: String,
    athlete_last_names: String,
    athlete_img: String,
    athlete_number: Number,
    athlete_id: Number,
    event_id: Number,
    roster: null
  },
  data: () => ({
    in_game: false
  }),

  mounted() {
    for (let i = 0; i < this.roster.length; i++) {
      if (this.roster[i].athlete_id == this.athlete_id) {
        this.in_game = true;
      }
    }
  },

  methods: {
    ...mapActions({
      addUPRMAthlete: "volleyballPBP/addUPRMAthlete",
      removeUPRMAthlete: "volleyballPBP/removeUPRMAthlete"
    }),

    async inGameChanged() {
      if (this.in_game) {
        // Payload for athlete to be
        const payload = {
          event_id: this.event_id,
          data: this.athlete_id,
          team: "uprm"
        };
        await this.addUPRMAthlete(payload);
      } else {
        const params = `event_id=${this.event_id}&athlete_id=${this.athlete_id}&team=uprm`;
        await this.removeUPRMAthlete(params);
      }
    }
  },
  computed: {
    // Functions for getting values in the data models.
    ...mapGetters({
      uprmRoster: "volleyballPBP/uprmRoster"
    })
  },
  watch: {
    // Manage checkbox based on uprmRoster latest state.
    uprmRoster: function() {
      for (let athlete in this.uprmRoster) {
        if (this.uprmRoster[athlete].athlete_id == this.athlete_id) {
          this.in_game = true;
          return;
        }
      }
      this.in_game = false;
    }
  }
};
</script>