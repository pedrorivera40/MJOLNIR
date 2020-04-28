<template>
  <v-container>
    <v-row>
      <v-col>
        <v-row justify="center">
          <h1 class="text-lg-center">{{ uprm_team }}</h1>
        </v-row>
        <v-row justify="center">
          <v-card class="ma-3 pa-6" outlined tile>
            <h1 class="text-lg-center">{{ current_uprm_score }}</h1>
          </v-card>
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
          <v-card class="ma-3 pa-6" outlined tile>
            <h1 class="text-md-center">{{ current_set }}</h1>
          </v-card>
        </v-row>
      </v-col>
      <v-col>
        <v-row justify="center">
          <h1 class="text-lg-center">{{ opp_team }}</h1>
        </v-row>
        <v-row justify="center">
          <v-card class="ma-3 pa-6" outlined tile>
            <h1 class="text-lg-center">{{ current_opp_score }}</h1>
          </v-card>
        </v-row>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
export default {
  props: {
    uprm_team: String,
    opp_team: String,
    uprm_score: Number,
    opp_score: Number,
    current_set: Number,
    current_uprm_score: Number, // Score of the current set for UPRM team.
    current_opp_score: Number // Score of the current set for opponent team.
  }
};
</script>