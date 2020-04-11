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
      page_title: "Deportes Masculino",
      sports: [
        {
          branch_name: "masculino ",
          sport_id: 7,
          sport_image_url:
            "https://scontent.fsig1-1.fna.fbcdn.net/v/t1.0-9/88079647_2995865743835573_4918146400446840832_o.jpg?_nc_cat=107&_nc_sid=e007fa&_nc_ohc=lVEHw0Gk00MAX_npfCs&_nc_ht=scontent.fsig1-1.fna&oh=f51f6c78278be3ede9e9adcc228e07f7&oe=5EAA80F3",
          sport_name: "Tenis de Mesa"
        },
        {
          branch_name: "masculino ",
          sport_id: 1,
          sport_image_url:
            "https://scontent.fsig1-1.fna.fbcdn.net/v/t1.0-9/88207403_3003298336425647_2084912734775803904_o.jpg?_nc_cat=109&_nc_sid=e007fa&_nc_ohc=cPJHsQ73nbMAX988FmN&_nc_ht=scontent.fsig1-1.fna&oh=1ff606b6b98ae4bd4d211840ac373a2a&oe=5EAB30D6",
          sport_name: "Baloncesto"
        },
        {
          branch_name: "masculino ",
          sport_id: 2,
          sport_image_url:
            "https://scontent.fsig1-1.fna.fbcdn.net/v/t1.0-9/70464070_2501810789907740_7951115497288761344_o.jpg?_nc_cat=111&_nc_sid=e007fa&_nc_ohc=jmq2DHPOaZkAX9edy-A&_nc_ht=scontent.fsig1-1.fna&oh=6ae24f48af684b58f7b7e884aab5adb1&oe=5EACA4BB",
          sport_name: "Voleibol"
        },
        {
          branch_name: "masculino ",
          sport_id: 3,
          sport_image_url:
            "https://scontent.fsig1-1.fna.fbcdn.net/v/t1.0-9/74883001_2671827106239440_2718595271939325952_o.jpg?_nc_cat=111&_nc_sid=e007fa&_nc_ohc=lqrGrpZippsAX_BafZ8&_nc_ht=scontent.fsig1-1.fna&oh=da934963689fa5b8d79b31a40cd62835&oe=5EA9881E",
          sport_name: "Fútbol"
        },
        {
          branch_name: "masculino ",
          sport_id: 4,
          sport_image_url:
            "https://scontent.fsig1-1.fna.fbcdn.net/v/t1.0-9/78952608_2738351966253620_2123712129298071552_o.jpg?_nc_cat=107&_nc_sid=e007fa&_nc_ohc=2yi5Wd4tCSQAX9DgGWk&_nc_ht=scontent.fsig1-1.fna&oh=11cb03d308be92338f1323a7a85270b5&oe=5EAA370E",
          sport_name: "Beisbol"
        },
        {
          branch_name: "masculino ",
          sport_id: 9,
          sport_image_url:
            "https://scontent.fsig2-1.fna.fbcdn.net/v/t1.0-9/74570444_2590444937710991_8977391808044597248_o.jpg?_nc_cat=100&_nc_sid=e007fa&_nc_ohc=anfmUDqPjbkAX9S9cDa&_nc_ht=scontent.fsig2-1.fna&oh=7fbc954a2ee8ea74e33c3a156223b9cf&oe=5EB57DC4",
          sport_name: "Tenis de Campo"
        },
        {
          branch_name: "masculino ",
          sport_id: 8,
          sport_image_url:
            "https://scontent.fsig2-1.fna.fbcdn.net/v/t31.0-8/13131245_1023629247725909_6768642735138623573_o.jpg?_nc_cat=104&_nc_sid=e007fa&_nc_ohc=3qXAykZk65UAX-EQBop&_nc_ht=scontent.fsig2-1.fna&oh=37b19c7f1c891be7db0d578e5d0ae3dc&oe=5EB76E21",
          sport_name: "Atletismo"
        },
        {
          branch_name: "masculino ",
          sport_id: 6,
          sport_image_url:
            "https://scontent.fsig2-1.fna.fbcdn.net/v/t1.0-9/58382011_2226304914124997_4136953121307885568_o.jpg?_nc_cat=110&_nc_sid=e007fa&_nc_ohc=k-uRMWrWrRsAX_OCT18&_nc_ht=scontent.fsig2-1.fna&oh=9f1fe435ae60997fc5567db872d62343&oe=5EB7E209",
          sport_name: "Judo"
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
