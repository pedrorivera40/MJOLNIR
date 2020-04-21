<template>
  <v-container>
    <v-row>
      <v-col>
        <h1 class="display-1">{{page_title}}</h1>
      </v-col>
    </v-row>
    <v-row>
      <v-col>
        <div v-if="(sports.length === 0) && !dialog">
          <v-overlay opacity="0.3">
            <v-progress-circular indeterminate></v-progress-circular>
          </v-overlay>
        </div>
      </v-col>
    </v-row>

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

    <v-row>
      <v-col v-for="sport in sports" :key="sport.sport_id" cols="12" md="6" lg="3">
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

export default {
  components: {
    SportCard
  },
  data() {
    return {
      error_string: "This emulates an error comming from the database.",
      dialog: false,
      error_icon: "mdi-alert-circle-outline",
      page_title: "Deportes Exhibicion",
      sports: [
        {
          branch_name: "exhibicion",
          sport_id: 17,
          sport_image_url:
            "https://scontent.fsig2-1.fna.fbcdn.net/v/t1.0-9/59419203_2233385630083592_6226045808450469888_o.jpg?_nc_cat=107&_nc_sid=e007fa&_nc_ohc=T14DDBN8-58AX91oVOi&_nc_ht=scontent.fsig2-1.fna&oh=42fdaaa85dd7ddac366cdb58dbf39fc2&oe=5EB6F84F",
          sport_name: "Baile"
        }
      ]
    };
  },
  methods: {
    redirect(sport_id) {
      // This will throw 404. TODO -> Meet with Herbert for details about this page.
      this.$router.push("equipo/" + sport_id);
    }
  }
};
</script>
