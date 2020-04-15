<template>

<v-card  max-height="400" width="100%" height="100%" outlined>
    <v-container class="text-center">
      <v-row justify="center">
        <v-col align="center">
          <v-avatar size="100">
            <v-icon v-if="img == null" height="100"> mdi-account </v-icon>
            <v-img v-else :src="img" height="100px" />
          </v-avatar>
        </v-col>
      </v-row>
      <v-row align="center">
        <v-col align-self="center">
          <v-card-title class="justify-center"> Nombre: {{firstName}} {{lastNames}}</v-card-title>
        </v-col>
      </v-row>
      <v-row justify="center">    
        <v-col align="center">
          <v-card-text >
            <h3> Deporte: {{sportName}} </h3>
          </v-card-text>
        </v-col>
      </v-row>
      
      <v-card-actions class="justify-center">
        <v-btn  @click="goToAthlete">
          <v-icon> mdi-eye-plus-outline </v-icon>            
        </v-btn>       
      </v-card-actions>
    </v-container>

  </v-card>
</template>

<script>
export default {
  props: {
    athleteID: Number,
    firstName: String,
    lastNames: String,
    sportName: String,
    img: String
  },
  methods: {
    
    goToAthlete() {
      this.$router.push("/atletas/" + this.athleteID);
    }
  }
};
</script>

