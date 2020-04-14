<template>
  <v-row>
    <v-col v-for="sport in sports" :key="sport.sport_id" cols="12" md="6" lg="3">
      <SportCard
        :sport_name="sport.sport_name"
        :img="sport.sport_image_url"
        @click.native="redirect(sport.sport_id)"
      />
    </v-col>
  </v-row>
</template>

<script>
import SportCard from "../components/SportCard.vue";

export default {
  components: {
    SportCard
  },
  props: {
    sports: []
  },
  methods: {
    redirect(sport_id) {
      // This part integrates with Herbert's Team Page.
      this.$router.push("equipo/" + sport_id);
    }
  }
};
</script>