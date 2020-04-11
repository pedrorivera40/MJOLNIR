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
import Logo from "~/components/Logo.vue";
import VuetifyLogo from "~/components/VuetifyLogo.vue";
import SportCard from "../../components/SportCard.vue";
import ErrorCard from "../../components/ErrorCard.vue";

export default {
  components: {
    Logo,
    VuetifyLogo,
    SportCard,
    ErrorCard
  },
  data() {
    return {
      error_string: "This is a damn error",
      dialog: false,
      error_icon: "mdi-alert-circle-outline",
      page_title: "Deportes Femenino",
      sports: [
        {
          branch_name: "femenina  ",
          sport_id: 18,
          sport_image_url:
            "https://scontent.fsig2-1.fna.fbcdn.net/v/t1.0-9/75481733_2645220682233416_2668964974918893568_o.jpg?_nc_cat=103&_nc_sid=e007fa&_nc_ohc=vYxbJQDLHnoAX_08xhx&_nc_ht=scontent.fsig2-1.fna&oh=ca3d1d73a7d36f88a65094568cd54710&oe=5EB500AA",
          sport_name: "Tenis de Campo"
        },
        {
          branch_name: "femenina  ",
          sport_id: 16,
          sport_image_url:
            "https://scontent.fsig2-1.fna.fbcdn.net/v/t1.0-9/57619118_2226257830796372_302697234753912832_o.jpg?_nc_cat=109&_nc_sid=e007fa&_nc_ohc=JOsXhrEM1tUAX8dDHSv&_nc_ht=scontent.fsig2-1.fna&oh=ca2da5e6e2342cfd795624cb292ee289&oe=5EB771E8",
          sport_name: "Softbol"
        },
        {
          branch_name: "femenina  ",
          sport_id: 15,
          sport_image_url:
            "https://scontent.fsig1-1.fna.fbcdn.net/v/t1.0-9/88102141_2995864247169056_8504767147161944064_o.jpg?_nc_cat=101&_nc_sid=e007fa&_nc_ohc=7iMRLrLUW7AAX_CZufe&_nc_ht=scontent.fsig1-1.fna&oh=a11b1b14f9b0bf3a58ad435bb29c0c9f&oe=5EAAA7AE",
          sport_name: "Tenis de Mesa"
        },
        {
          branch_name: "femenina  ",
          sport_id: 12,
          sport_image_url:
            "https://scontent.fsig1-1.fna.fbcdn.net/v/t1.0-9/70916818_2501810766574409_3176798918700695552_o.jpg?_nc_cat=102&_nc_sid=e007fa&_nc_ohc=Jokgru5MxFcAX-Iepr4&_nc_ht=scontent.fsig1-1.fna&oh=1e231a8b32569ced072a763ee0270c55&oe=5EA8EF86",
          sport_name: "Voleibol"
        },
        {
          branch_name: "femenina  ",
          sport_id: 10,
          sport_image_url:
            "https://scontent.fsig1-1.fna.fbcdn.net/v/t1.0-9/87275067_3003297419759072_5465629605404606464_o.jpg?_nc_cat=107&_nc_sid=e007fa&_nc_ohc=zHfnqen2khcAX-eoOmi&_nc_ht=scontent.fsig1-1.fna&oh=4c49785d0a8dbccdb59b3419f13d1ad1&oe=5EAC3C9E",
          sport_name: "Baloncesto"
        },
        {
          branch_name: "femenina  ",
          sport_id: 5,
          sport_image_url:
            "https://scontent.fsig1-1.fna.fbcdn.net/v/t1.0-9/58595547_2226257994129689_639596050000117760_o.jpg?_nc_cat=109&_nc_sid=e007fa&_nc_ohc=xXhLnzI_Ly8AX9TjEXX&_nc_ht=scontent.fsig1-1.fna&oh=61c5bc219d6741df74425df02b5b540f&oe=5EA8C2B7",
          sport_name: "Softball"
        },
        {
          branch_name: "femenina  ",
          sport_id: 11,
          sport_image_url:
            "https://scontent.fsig1-1.fna.fbcdn.net/v/t1.0-9/88983239_2989638081125006_5994073246109007872_n.jpg?_nc_cat=104&_nc_sid=e007fa&_nc_ohc=eCtVJEHWHjEAX-4zKxa&_nc_ht=scontent.fsig1-1.fna&oh=b6e46d5ef1e373fa84c065ee433e784a&oe=5EAAE8DB",
          sport_name: "Fútbol"
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
