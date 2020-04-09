<template>
  <v-container>
    <v-row>
      <v-col>
        <h1 class="display-1">Deportes</h1>
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
        <v-dialog v-model="dialog" max-width="425" max-height="100" persistent>
          <ErrorCard class="white" :error_text="error_string" :icon="error_icon" />
        </v-dialog>
      </v-col>
    </v-row>

    <v-row>
      <v-col v-for="sport in sports" :key="sport.id" cols="12" md="6" lg="3">
        <SportCard
          :sport_name="sport.sport_name"
          :img="sport.img"
          @click.native="redirect(sport.id)"
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
      sports: [
        {
          sport_name: "Baloncesto",
          id: 23,
          img:
            "https://scontent.fsig1-1.fna.fbcdn.net/v/t1.0-9/88207403_3003298336425647_2084912734775803904_o.jpg?_nc_cat=109&_nc_sid=e007fa&_nc_ohc=WGEYwiYREnsAX8BP7zH&_nc_ht=scontent.fsig1-1.fna&oh=924e05d564c1f4f5fa5a1e70fad416fb&oe=5EB319D6"
        }
        // {
        //   sport_name: "Voleibol",
        //   img:
        //     "https://scontent.fsig1-1.fna.fbcdn.net/v/t1.0-9/73139670_2620608184694666_909863064738725888_o.jpg?_nc_cat=108&_nc_sid=e007fa&_nc_ohc=z4LDJnx9nwoAX_fAoQa&_nc_ht=scontent.fsig1-1.fna&oh=a9a7e40ba8a03eb480e6f4553653f8aa&oe=5EB2B01F"
        // },
        // {
        //   sport_name: "Baloncesto",
        //   img:
        //     "https://scontent.fsig1-1.fna.fbcdn.net/v/t1.0-9/88207403_3003298336425647_2084912734775803904_o.jpg?_nc_cat=109&_nc_sid=e007fa&_nc_ohc=WGEYwiYREnsAX8BP7zH&_nc_ht=scontent.fsig1-1.fna&oh=924e05d564c1f4f5fa5a1e70fad416fb&oe=5EB319D6"
        // },
        // {
        //   sport_name: "Voleibol",
        //   img:
        //     "https://scontent.fsig1-1.fna.fbcdn.net/v/t1.0-9/73139670_2620608184694666_909863064738725888_o.jpg?_nc_cat=108&_nc_sid=e007fa&_nc_ohc=z4LDJnx9nwoAX_fAoQa&_nc_ht=scontent.fsig1-1.fna&oh=a9a7e40ba8a03eb480e6f4553653f8aa&oe=5EB2B01F"
        // },
        // {
        //   sport_name: "Baloncesto",
        //   img:
        //     "https://scontent.fsig1-1.fna.fbcdn.net/v/t1.0-9/88207403_3003298336425647_2084912734775803904_o.jpg?_nc_cat=109&_nc_sid=e007fa&_nc_ohc=WGEYwiYREnsAX8BP7zH&_nc_ht=scontent.fsig1-1.fna&oh=924e05d564c1f4f5fa5a1e70fad416fb&oe=5EB319D6"
        // },
        // {
        //   sport_name: "Voleibol",
        //   img:
        //     "https://scontent.fsig1-1.fna.fbcdn.net/v/t1.0-9/73139670_2620608184694666_909863064738725888_o.jpg?_nc_cat=108&_nc_sid=e007fa&_nc_ohc=z4LDJnx9nwoAX_fAoQa&_nc_ht=scontent.fsig1-1.fna&oh=a9a7e40ba8a03eb480e6f4553653f8aa&oe=5EB2B01F"
        // },
        // {
        //   sport_name: "Baloncesto",
        //   img:
        //     "https://scontent.fsig1-1.fna.fbcdn.net/v/t1.0-9/88207403_3003298336425647_2084912734775803904_o.jpg?_nc_cat=109&_nc_sid=e007fa&_nc_ohc=WGEYwiYREnsAX8BP7zH&_nc_ht=scontent.fsig1-1.fna&oh=924e05d564c1f4f5fa5a1e70fad416fb&oe=5EB319D6"
        // },
        // {
        //   sport_name: "Voleibol",
        //   img:
        //     "https://scontent.fsig1-1.fna.fbcdn.net/v/t1.0-9/73139670_2620608184694666_909863064738725888_o.jpg?_nc_cat=108&_nc_sid=e007fa&_nc_ohc=z4LDJnx9nwoAX_fAoQa&_nc_ht=scontent.fsig1-1.fna&oh=a9a7e40ba8a03eb480e6f4553653f8aa&oe=5EB2B01F"
        // }
      ]
    };
  },
  methods: {
    redirect(sport_id) {
      // This will throw 404. TODO -> Meet with Herbert for details about this page.
      this.$router.push("teams/" + sport_id);
    }
  }
};
</script>
