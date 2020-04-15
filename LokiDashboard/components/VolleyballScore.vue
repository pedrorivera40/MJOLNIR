<template>
  <v-container>
    <v-row>
      <v-col>
        <v-row justify="center">
          <h1 class="text-lg-center">UPRM</h1>
        </v-row>
        <v-row justify="center">
          <v-layout row wrap align-center>
            <v-col class="text-right">
              <v-btn @click.native="on_uprm_score(-1)" class="ma-2" color="red" fab small dark>
                <v-icon>mdi-minus</v-icon>
              </v-btn>
            </v-col>
          </v-layout>
          <v-col>
            <v-card class="ma-3 pa-6" outlined tile>
              <h1 class="text-lg-center">{{ current_uprm_score }}</h1>
            </v-card>
          </v-col>
          <v-layout row wrap align-center>
            <v-col class="text-left">
              <v-btn @click.native="on_uprm_score(1)" class="ma-2" color="green" fab small dark>
                <v-icon>mdi-plus</v-icon>
              </v-btn>
            </v-col>
          </v-layout>
        </v-row>
      </v-col>
      <v-col>
        <v-row justify="center">
          <h2 class="text-md-center">MARCADOR</h2>
        </v-row>
        <v-row justify="center">
          <v-card class="ma-3 pa-6" outlined tile>
            <h1 class="text-md-center">{{ uprm_score }} - {{ opp_score }}</h1>
          </v-card>
        </v-row>
        <v-row justify="center">
          <h2 class="text-md-center">SET</h2>
        </v-row>
        <v-row justify="center">
          <v-layout row wrap align-center>
            <v-col class="text-right">
              <v-btn @click.native="on_set_change(-1)" class="ma-2" color="red" fab small dark>
                <v-icon>mdi-minus</v-icon>
              </v-btn>
            </v-col>
          </v-layout>
          <v-card class="ma-3 pa-6" outlined tile>
            <h1 class="text-md-center">{{ current_set }}</h1>
          </v-card>
          <v-layout row wrap align-center>
            <v-col class="text-left">
              <v-btn @click.native="on_set_change(1)" class="ma-2" color="green" fab small dark>
                <v-icon>mdi-plus</v-icon>
              </v-btn>
            </v-col>
          </v-layout>
        </v-row>
      </v-col>
      <v-col>
        <v-row justify="center">
          <h1 class="text-lg-center">UPR-RP</h1>
        </v-row>
        <v-row justify="center">
          <v-layout row wrap align-center>
            <v-col class="text-right">
              <v-btn @click.native="on_opp_score(-1)" class="ma-2" color="red" fab small dark>
                <v-icon>mdi-minus</v-icon>
              </v-btn>
            </v-col>
          </v-layout>
          <v-col>
            <v-card class="ma-3 pa-6" outlined tile>
              <h1 class="text-lg-center">{{ current_opp_score }}</h1>
            </v-card>
          </v-col>
          <v-layout row wrap align-center>
            <v-col class="text-left">
              <v-btn @click.native="on_opp_score(1)" class="ma-2" color="green" fab small dark>
                <v-icon>mdi-plus</v-icon>
              </v-btn>
            </v-col>
          </v-layout>
        </v-row>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
export default {
  data: () => ({
    uprm_team: "UPRM",
    opp_team: "UPR-RP",
    uprm_score: 0,
    opp_score: 0,
    current_set: 1,
    current_uprm_score: 0, // Score of the current set for UPRM team.
    current_opp_score: 0 // Score of the current set for opponent team.
  }),
  methods: {
    on_uprm_score(change) {
      this.current_uprm_score += change;
    },
    on_opp_score(change) {
      this.current_opp_score += change;
    },
    on_set_change(change) {
      this.current_set += change;
    }
  }
};
</script>