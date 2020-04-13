<template>
  <v-container>
    <v-row>
      <v-col>
        <v-row justify="center">UPRM</v-row>
        <v-row justify="center">20</v-row>
      </v-col>
      <v-col>
        <v-row justify="center">CURRENT SET</v-row>
        <v-row justify="center">1</v-row>
        <v-row justify="center">SCORE</v-row>
        <v-row justify="center">2 - 1</v-row>
      </v-col>
      <v-col>
        <v-row justify="center">UPR-RP</v-row>
        <v-row justify="center">25</v-row>
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