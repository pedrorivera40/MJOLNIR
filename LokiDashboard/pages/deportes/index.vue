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
    <v-tabs background-color="#f5f5f5" align-with-title centered grow>
      <v-tabs-slider />
      <v-tab>Rama Masculina</v-tab>

      <v-tab>Rama Femenina</v-tab>

      <v-tab>Deportes de Exhibición</v-tab>

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

    <v-row></v-row>

    <v-row></v-row>
  </v-container>
</template>

<script>
import SportsView from "../../components/SportsView.vue";
export default {
  components: {
    SportsView
  },
  data() {
    return {
      error_string: "This is a damn error",
      dialog: false,
      error_icon: "mdi-alert-circle-outline",
      page_title: "Deportes",
      male_branch: "masculino",
      female_branch: "femenino",
      exibit_branch: "exhibicion",
      sports: [
        {
          branch_name: "femenino",
          sport_id: 18,
          sport_image_url:
            "https://scontent.fsig2-1.fna.fbcdn.net/v/t1.0-9/75481733_2645220682233416_2668964974918893568_o.jpg?_nc_cat=103&_nc_sid=e007fa&_nc_ohc=vYxbJQDLHnoAX_08xhx&_nc_ht=scontent.fsig2-1.fna&oh=ca3d1d73a7d36f88a65094568cd54710&oe=5EB500AA",
          sport_name: "Tenis de Campo"
        },
        {
          branch_name: "femenino",
          sport_id: 16,
          sport_image_url:
            "https://scontent.fsig2-1.fna.fbcdn.net/v/t1.0-9/57619118_2226257830796372_302697234753912832_o.jpg?_nc_cat=109&_nc_sid=e007fa&_nc_ohc=JOsXhrEM1tUAX8dDHSv&_nc_ht=scontent.fsig2-1.fna&oh=ca2da5e6e2342cfd795624cb292ee289&oe=5EB771E8",
          sport_name: "Softbol"
        },
        {
          branch_name: "exhibicion",
          sport_id: 17,
          sport_image_url:
            "https://scontent.fsig2-1.fna.fbcdn.net/v/t1.0-9/59419203_2233385630083592_6226045808450469888_o.jpg?_nc_cat=107&_nc_sid=e007fa&_nc_ohc=T14DDBN8-58AX91oVOi&_nc_ht=scontent.fsig2-1.fna&oh=42fdaaa85dd7ddac366cdb58dbf39fc2&oe=5EB6F84F",
          sport_name: "Baile"
        },
        {
          branch_name: "masculino",
          sport_id: 13,
          sport_image_url:
            "http://deportes.uprm.edu/wp-content/uploads/2015/10/Logo-Oficial.png",
          sport_name: "TestSportWithCategory"
        },
        {
          branch_name: "masculino",
          sport_id: 14,
          sport_image_url:
            "http://deportes.uprm.edu/wp-content/uploads/2015/10/Logo-Oficial.png",
          sport_name: "TestSportWithPosition"
        },
        {
          branch_name: "femenino",
          sport_id: 15,
          sport_image_url:
            "https://scontent.fsig1-1.fna.fbcdn.net/v/t1.0-9/88102141_2995864247169056_8504767147161944064_o.jpg?_nc_cat=101&_nc_sid=e007fa&_nc_ohc=7iMRLrLUW7AAX_CZufe&_nc_ht=scontent.fsig1-1.fna&oh=a11b1b14f9b0bf3a58ad435bb29c0c9f&oe=5EAAA7AE",
          sport_name: "Tenis de Mesa"
        },
        {
          branch_name: "masculino",
          sport_id: 7,
          sport_image_url:
            "https://scontent.fsig1-1.fna.fbcdn.net/v/t1.0-9/88079647_2995865743835573_4918146400446840832_o.jpg?_nc_cat=107&_nc_sid=e007fa&_nc_ohc=lVEHw0Gk00MAX_npfCs&_nc_ht=scontent.fsig1-1.fna&oh=f51f6c78278be3ede9e9adcc228e07f7&oe=5EAA80F3",
          sport_name: "Tenis de Mesa"
        },
        {
          branch_name: "masculino",
          sport_id: 1,
          sport_image_url:
            "https://scontent.fsig1-1.fna.fbcdn.net/v/t1.0-9/88207403_3003298336425647_2084912734775803904_o.jpg?_nc_cat=109&_nc_sid=e007fa&_nc_ohc=cPJHsQ73nbMAX988FmN&_nc_ht=scontent.fsig1-1.fna&oh=1ff606b6b98ae4bd4d211840ac373a2a&oe=5EAB30D6",
          sport_name: "Baloncesto"
        },
        {
          branch_name: "masculino",
          sport_id: 2,
          sport_image_url:
            "https://scontent.fsig1-1.fna.fbcdn.net/v/t1.0-9/70464070_2501810789907740_7951115497288761344_o.jpg?_nc_cat=111&_nc_sid=e007fa&_nc_ohc=jmq2DHPOaZkAX9edy-A&_nc_ht=scontent.fsig1-1.fna&oh=6ae24f48af684b58f7b7e884aab5adb1&oe=5EACA4BB",
          sport_name: "Voleibol"
        },
        {
          branch_name: "femenino",
          sport_id: 12,
          sport_image_url:
            "https://scontent.fsig1-1.fna.fbcdn.net/v/t1.0-9/70916818_2501810766574409_3176798918700695552_o.jpg?_nc_cat=102&_nc_sid=e007fa&_nc_ohc=Jokgru5MxFcAX-Iepr4&_nc_ht=scontent.fsig1-1.fna&oh=1e231a8b32569ced072a763ee0270c55&oe=5EA8EF86",
          sport_name: "Voleibol"
        },
        {
          branch_name: "femenino",
          sport_id: 10,
          sport_image_url:
            "https://scontent.fsig1-1.fna.fbcdn.net/v/t1.0-9/87275067_3003297419759072_5465629605404606464_o.jpg?_nc_cat=107&_nc_sid=e007fa&_nc_ohc=zHfnqen2khcAX-eoOmi&_nc_ht=scontent.fsig1-1.fna&oh=4c49785d0a8dbccdb59b3419f13d1ad1&oe=5EAC3C9E",
          sport_name: "Baloncesto"
        },
        {
          branch_name: "femenino",
          sport_id: 5,
          sport_image_url:
            "https://scontent.fsig1-1.fna.fbcdn.net/v/t1.0-9/58595547_2226257994129689_639596050000117760_o.jpg?_nc_cat=109&_nc_sid=e007fa&_nc_ohc=xXhLnzI_Ly8AX9TjEXX&_nc_ht=scontent.fsig1-1.fna&oh=61c5bc219d6741df74425df02b5b540f&oe=5EA8C2B7",
          sport_name: "Softball"
        },
        {
          branch_name: "masculino",
          sport_id: 3,
          sport_image_url:
            "https://scontent.fsig1-1.fna.fbcdn.net/v/t1.0-9/74883001_2671827106239440_2718595271939325952_o.jpg?_nc_cat=111&_nc_sid=e007fa&_nc_ohc=lqrGrpZippsAX_BafZ8&_nc_ht=scontent.fsig1-1.fna&oh=da934963689fa5b8d79b31a40cd62835&oe=5EA9881E",
          sport_name: "Fútbol"
        },
        {
          branch_name: "femenino",
          sport_id: 11,
          sport_image_url:
            "https://scontent.fsig1-1.fna.fbcdn.net/v/t1.0-9/88983239_2989638081125006_5994073246109007872_n.jpg?_nc_cat=104&_nc_sid=e007fa&_nc_ohc=eCtVJEHWHjEAX-4zKxa&_nc_ht=scontent.fsig1-1.fna&oh=b6e46d5ef1e373fa84c065ee433e784a&oe=5EAAE8DB",
          sport_name: "Fútbol"
        },
        {
          branch_name: "masculino",
          sport_id: 4,
          sport_image_url:
            "https://scontent.fsig1-1.fna.fbcdn.net/v/t1.0-9/78952608_2738351966253620_2123712129298071552_o.jpg?_nc_cat=107&_nc_sid=e007fa&_nc_ohc=2yi5Wd4tCSQAX9DgGWk&_nc_ht=scontent.fsig1-1.fna&oh=11cb03d308be92338f1323a7a85270b5&oe=5EAA370E",
          sport_name: "Beisbol"
        },
        {
          branch_name: "masculino",
          sport_id: 9,
          sport_image_url:
            "https://scontent.fsig2-1.fna.fbcdn.net/v/t1.0-9/74570444_2590444937710991_8977391808044597248_o.jpg?_nc_cat=100&_nc_sid=e007fa&_nc_ohc=anfmUDqPjbkAX9S9cDa&_nc_ht=scontent.fsig2-1.fna&oh=7fbc954a2ee8ea74e33c3a156223b9cf&oe=5EB57DC4",
          sport_name: "Tenis de Campo"
        },
        {
          branch_name: "masculino",
          sport_id: 8,
          sport_image_url:
            "https://scontent.fsig2-1.fna.fbcdn.net/v/t31.0-8/13131245_1023629247725909_6768642735138623573_o.jpg?_nc_cat=104&_nc_sid=e007fa&_nc_ohc=3qXAykZk65UAX-EQBop&_nc_ht=scontent.fsig2-1.fna&oh=37b19c7f1c891be7db0d578e5d0ae3dc&oe=5EB76E21",
          sport_name: "Atletismo"
        },
        {
          branch_name: "masculino",
          sport_id: 6,
          sport_image_url:
            "https://scontent.fsig2-1.fna.fbcdn.net/v/t1.0-9/58382011_2226304914124997_4136953121307885568_o.jpg?_nc_cat=110&_nc_sid=e007fa&_nc_ohc=k-uRMWrWrRsAX_OCT18&_nc_ht=scontent.fsig2-1.fna&oh=9f1fe435ae60997fc5567db872d62343&oe=5EB7E209",
          sport_name: "Judo"
        }
      ]
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
    }
  }
};
</script>