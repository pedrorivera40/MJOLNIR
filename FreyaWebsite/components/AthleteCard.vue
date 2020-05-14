<template>
  <v-card height="100%" width="100%" outlined>
    <v-container>
      <v-list-item>
        <v-list-item-avatar color="accent" size="95">
          <v-icon v-if="img == null" color="blue-grey" size="50"> mdi-account </v-icon>
          <v-img v-else :src="img" height="100px" />
        </v-list-item-avatar>
        <v-list-item-content>
          <v-list-item-title class="title">
            Nombre: {{ firstName }} <br />
            {{ lastNames }}
          </v-list-item-title>
          <v-list-item-subtitle>Deporte: {{ sportName }}</v-list-item-subtitle>
        </v-list-item-content>
      </v-list-item>

    </v-container>
    <v-card-actions>
      <v-spacer></v-spacer>
      <v-btn text color="primary" @click="goToAthlete">
        ver perfil
      </v-btn>
    </v-card-actions>
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
    /**
     * Redirects to the athlete viewer page using
     * the id of the athlete already given as a prop.
     */
    goToAthlete() {
      this.$router.push("/atletas/" + this.athleteID);
    }
  }
};
</script>

