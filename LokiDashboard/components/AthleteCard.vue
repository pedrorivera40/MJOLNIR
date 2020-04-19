<template>

<v-card  width="100%" height="100%" outlined>
    <v-container >
      <v-row >
        <v-col md=3>
          <v-avatar size="100">
            <v-icon v-if="img == null" height="100px"> mdi-account </v-icon>
            <v-img v-else :src="img" height="100px" />
          </v-avatar>
        </v-col>     
        <v-col md=9>
          <v-card-title> Nombre: {{firstName}} <br/> {{lastNames}}</v-card-title>
          <v-card-subtitle >
            Deporte: {{sportName}} 
          </v-card-subtitle>
          <v-card-actions>
            <v-btn  @click="goToAthlete">
              <v-icon> mdi-eye-plus-outline </v-icon>            
            </v-btn>

            <v-btn color="green darken-1" dark @click="editAthlete">
              <v-icon> mdi-pencil </v-icon>            
            </v-btn>
            <v-btn color="red darken-1" dark @click="removeAthlete">
              <v-icon> mdi-delete </v-icon>            
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
    removeAthlete() {
      console.log("Removing athlete with id:" + this.athleteID)
    },

    editAthlete() {
      this.$router.push("/atleta/" + this.athleteID + "/editar");
    },
    goToAthlete() {
      this.$router.push("/atleta/" + this.athleteID);
    }
  }
};
</script>

