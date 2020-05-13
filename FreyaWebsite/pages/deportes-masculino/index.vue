<template>
  <v-container>
    <v-row>
      <v-col>
        <h1 class="display-1">{{ page_title }}</h1>
      </v-col>
    </v-row>
    <LoadingScreen v-if="sports.length === 0" nameOfData="Deportes" />
    <v-row>
      <v-col>
        <v-snackbar
          color="white"
          v-model="dialog"
          max-width="425"
          max-height="100"
          class="text-center ma-2 black--text"
        >
          {{ error_string }}
          <v-btn color="rgb(67, 160, 71)" text @click="dialog = false"
            >Cerrar</v-btn
          >
        </v-snackbar>
      </v-col>
    </v-row>

    <v-row>
      <v-col
        v-for="sport in sports"
        :key="sport.sport_id"
        cols="12"
        md="6"
        lg="3"
      >
        <SportCard
          :sport_name="sport.sport_name"
          :img="sport.sport_image_url"
          @click.native="redirect(sport.sport_id)"
        />
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import SportCard from "../../components/SportCard.vue";
import LoadingScreen from "../../components/general/LoadingScreen";
import { mapGetters, mapActions } from "vuex";

export default {
  components: {
    SportCard,
    LoadingScreen
  },
  data() {
    return {
      error_string: "This emulates an error comming from the database",
      dialog: false,
      error_icon: "mdi-alert-circle-outline",
      page_title: "Deportes Masculino"
    };
  },
  methods: {
    ...mapActions({
      getAllSports: "sports/getAllSports"
    }),
    redirect(sport_id) {
      this.$router.push("equipo/" + sport_id);
    }
  },
  computed: {
    ...mapGetters({
      sports: "sports/sportsMasculino"
    })
  },
  beforeMount() {
    if (this.sports.length === 0) {
      this.getAllSports();
    }
  }
};
</script>
