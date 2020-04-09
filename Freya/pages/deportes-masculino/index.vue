<template>
  <v-container>
    <v-row>
      <v-col>
        <h1 class="display-1">Deportes</h1>
      </v-col>
    </v-row>
    <v-row>
      <v-col v-for="sport in sports" :key="sport.id" cols="12" md="6" lg="3">
        <SportCard :sport_name="sport.sport_name" :img="sport.img" />
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import Logo from "~/components/Logo.vue";
import VuetifyLogo from "~/components/VuetifyLogo.vue";
import SportCard from "../../components/SportCard.vue";

export default {
  components: {
    Logo,
    VuetifyLogo,
    SportCard
  },
  data() {
    return {
      sports: [
        {
          sport_name: "Baloncesto",
          img:
            "https://scontent.fsig1-1.fna.fbcdn.net/v/t1.0-9/88207403_3003298336425647_2084912734775803904_o.jpg?_nc_cat=109&_nc_sid=e007fa&_nc_ohc=WGEYwiYREnsAX8BP7zH&_nc_ht=scontent.fsig1-1.fna&oh=924e05d564c1f4f5fa5a1e70fad416fb&oe=5EB319D6"
        },
        {
          sport_name: "Voleibol",
          img:
            "https://scontent.fsig1-1.fna.fbcdn.net/v/t1.0-9/73139670_2620608184694666_909863064738725888_o.jpg?_nc_cat=108&_nc_sid=e007fa&_nc_ohc=z4LDJnx9nwoAX_fAoQa&_nc_ht=scontent.fsig1-1.fna&oh=a9a7e40ba8a03eb480e6f4553653f8aa&oe=5EB2B01F"
        },
        {
          sport_name: "Baloncesto",
          img:
            "https://scontent.fsig1-1.fna.fbcdn.net/v/t1.0-9/88207403_3003298336425647_2084912734775803904_o.jpg?_nc_cat=109&_nc_sid=e007fa&_nc_ohc=WGEYwiYREnsAX8BP7zH&_nc_ht=scontent.fsig1-1.fna&oh=924e05d564c1f4f5fa5a1e70fad416fb&oe=5EB319D6"
        },
        {
          sport_name: "Voleibol",
          img:
            "https://scontent.fsig1-1.fna.fbcdn.net/v/t1.0-9/73139670_2620608184694666_909863064738725888_o.jpg?_nc_cat=108&_nc_sid=e007fa&_nc_ohc=z4LDJnx9nwoAX_fAoQa&_nc_ht=scontent.fsig1-1.fna&oh=a9a7e40ba8a03eb480e6f4553653f8aa&oe=5EB2B01F"
        },
        {
          sport_name: "Baloncesto",
          img:
            "https://scontent.fsig1-1.fna.fbcdn.net/v/t1.0-9/88207403_3003298336425647_2084912734775803904_o.jpg?_nc_cat=109&_nc_sid=e007fa&_nc_ohc=WGEYwiYREnsAX8BP7zH&_nc_ht=scontent.fsig1-1.fna&oh=924e05d564c1f4f5fa5a1e70fad416fb&oe=5EB319D6"
        },
        {
          sport_name: "Voleibol",
          img:
            "https://scontent.fsig1-1.fna.fbcdn.net/v/t1.0-9/73139670_2620608184694666_909863064738725888_o.jpg?_nc_cat=108&_nc_sid=e007fa&_nc_ohc=z4LDJnx9nwoAX_fAoQa&_nc_ht=scontent.fsig1-1.fna&oh=a9a7e40ba8a03eb480e6f4553653f8aa&oe=5EB2B01F"
        },
        {
          sport_name: "Baloncesto",
          img:
            "https://scontent.fsig1-1.fna.fbcdn.net/v/t1.0-9/88207403_3003298336425647_2084912734775803904_o.jpg?_nc_cat=109&_nc_sid=e007fa&_nc_ohc=WGEYwiYREnsAX8BP7zH&_nc_ht=scontent.fsig1-1.fna&oh=924e05d564c1f4f5fa5a1e70fad416fb&oe=5EB319D6"
        },
        {
          sport_name: "Voleibol",
          img:
            "https://scontent.fsig1-1.fna.fbcdn.net/v/t1.0-9/73139670_2620608184694666_909863064738725888_o.jpg?_nc_cat=108&_nc_sid=e007fa&_nc_ohc=z4LDJnx9nwoAX_fAoQa&_nc_ht=scontent.fsig1-1.fna&oh=a9a7e40ba8a03eb480e6f4553653f8aa&oe=5EB2B01F"
        }
      ]
    };
  }
};
</script>
