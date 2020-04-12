<template>
  <v-card width="100%" height="100%">
    <v-container>
      <v-card-title>Nombre: {{firstName}} {{lastNames}}</v-card-title>

      <v-card-text class="text--primary">
        <div>Deporte: {{sportName}}</div>
      </v-card-text>

      <v-spacer />

      <v-btn @click="goToAthlete">Detalles</v-btn>
      <v-btn color="green darken-1" dark @click="editAthlete">Editar</v-btn>
      <v-btn color="red darken-1" dark @click="removeAthlete">Remover</v-btn>
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
      //Connect to api for remove
    },

    editAthlete() {
      this.$router.push("/athlete/" + this.athleteID + "/edit");
    },
    goToAthlete() {
      this.$router.push("/athlete/" + this.athleteID);
    }
  }
};
</script>