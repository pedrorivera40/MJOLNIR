<template>
  <v-container>
    <v-row>
      <v-col>
        <h1 class="primary_dark--text pl-3">{{page_title}}</h1>
      </v-col>
    </v-row>
    <ErrorCard
      v-if="!loading && sports.length === 0"
      in_color="primary"
      error_header="Error de conexión"
      error_message="Hubo un error de conexión al buscar el listado de deportes."
    />
    <v-row v-if="loading" justify="center">
      <v-progress-circular :active="loading" indeterminate :size="50" color="primary"></v-progress-circular>
    </v-row>
    <v-tabs v-if="!loading && sports.length > 0" align-with-title centered grow>
      <v-tabs-slider />
      <v-tab>Rama Masculina</v-tab>

      <v-tab>Rama Femenina</v-tab>

      <v-tab>Deportes de Exhibición</v-tab>

      <v-divider></v-divider>

      <v-tab-item>
        <SportsView :sports="filter_by_branch(male_branch)" />
      </v-tab-item>
      <v-tab-item>
        <SportsView :sports="filter_by_branch(female_branch)" />
      </v-tab-item>
      <v-tab-item>
        <SportsView :sports="filter_by_branch(exibit_branch)" />
      </v-tab-item>
    </v-tabs>
    <v-row>
      <v-col>
        <v-snackbar
          color="white"
          v-model="dialog"
          max-width="425"
          max-height="100"
          class="text-center ma-2 black--text"
        >
          {{error_string}}
          <v-btn color="rgb(67, 160, 71)" text @click="dialog = false">Cerrar</v-btn>
        </v-snackbar>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import SportsView from "../../components/SportsView.vue";
import ErrorCard from "../../components/PBP/ErrorCard.vue";

import { mapGetters, mapActions } from "vuex";

export default {
  components: {
    SportsView,
    ErrorCard
  },
  data() {
    return {
      loading: true,
      error_string: "This emulates an error comming from the database",
      dialog: false,
      error_icon: "mdi-alert-circle-outline",
      page_title: "Deportes",
      male_branch: "Masculino",
      female_branch: "Femenino",
      exibit_branch: "Exhibición"
    };
  },
  methods: {
    filter_by_branch(branch) {
      // Returns the list of sports filtered by branch.
      // This is done to avoid querying the database on any tab switch.
      let result = [];
      for (let index in this.sports) {
        console.log(this.sports[index]);
        if (this.sports[index].branch_name == branch) {
          result.push(this.sports[index]);
        }
      }
      return result;
    },
    ...mapActions({
      getAllSports: "sports/getAllSports"
    }),
    redirect(sport_id) {
      this.$router.push("equipo/" + sport_id);
    }
  },
  computed: {
    ...mapGetters({
      sports: "sports/sports"
    })
  },
  async beforeMount() {
    if (this.sports.length === 0) {
      this.loading = true;
      await this.getAllSports();
      this.loading = false;
    }
  }
};
</script>