<template>

<v-card  height="100%" width="100%" outlined>
    <v-container >
      <v-row >
        <v-col  md=3>
          <v-avatar size="100">
            <v-icon v-if="img == null" height="100px"> mdi-account </v-icon>
            <v-img v-else :src="img" height="100px" />
          </v-avatar>
        </v-col>
         <v-col md=9>
          <v-card-title >  Nombre: {{firstName}} <br/> {{lastNames}}</v-card-title>
          <v-card-subtitle >
            Deporte: {{sportName}} 
          </v-card-subtitle>
          <v-card-actions >
            <v-btn  @click="goToAthlete">
              <v-icon> mdi-eye-plus-outline </v-icon>            
            </v-btn>       
          </v-card-actions>
        </v-col>
      </v-row>      
      
      
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

