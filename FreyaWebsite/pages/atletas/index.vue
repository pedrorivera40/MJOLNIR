<template>
  <v-container grid-list-sm v-if="isReady()">
    <v-row>
      <h1>Atletas:</h1>
    </v-row>

    <div v-if="athletes.length > 0">
      <v-row class="text-right">
        <v-col>
          <v-menu
            v-model="menu"
            bottom
            origin="center center"
            transition="slide-x-transition"
            :close-on-content-click="false"
          >
            <template v-slot:activator="{ on }">
              <v-btn color="green darken-1" dark v-on="on">
                <v-icon left>mdi-filter-variant</v-icon>
                Filtros
              </v-btn>
            </template>

            <v-list>
              <v-list-item>
                <v-select
                  v-model="sport"
                  :items="sports"
                  label="Deporte"
                ></v-select>
              </v-list-item>
              <v-list-item>
                <v-text-field v-model="name" label="Nombre"></v-text-field>
              </v-list-item>
              <v-list-item>
                <v-spacer />
                <v-btn text color="accent" @click="clearFilters">Borrar</v-btn>
                <v-btn text color="green darken-1" @click="applyFilters"
                  >Filtrar</v-btn
                >
              </v-list-item>
            </v-list>
          </v-menu>
        </v-col>
      </v-row>

      <v-row v-if="!!filteredAthletes">
        <v-col v-for="(value, key) in filteredAthletes" :key="key" cols="12" md="6" lg="3" >
          <AthleteCard
            :athleteID="value.id"
            :firstName="value.fName"
            :lastNames="value.lName"
            :sportName="value.sportName"
            :img="value.profilePicLink"
          />
        </v-col>
      </v-row>

      <v-row v-else>
        <v-col v-for="(value, key) in athletes" :key="key" cols="12"  md="6" lg="3">
          <AthleteCard
            :athleteID="value.id"
            :firstName="value.fName"
            :lastNames="value.lName"
            :sportName="value.sportName"
            :img="value.profilePicLink"
          />
        </v-col>
      </v-row>
    </div>
    <LoadingScreen v-else name-of-data="Atletas" />
  </v-container>
</template>

<script>
import AthleteCard from "../../components/AthleteCard";
import LoadingScreen from "../../components/general/LoadingScreen";
import { mapActions, mapGetters } from "vuex";

export default {
  components: {
    AthleteCard,
    LoadingScreen
  },

  data: () => ({
    menu: false,
    name: "",
    sport: "",
    sports: [
      "Voleibol",
      "Baloncesto",
      "Atletismo",
      "Fútbol",
      "Softbol",
      "Beisbol",
      "Tenis de Mesa",
      "Tenis de Campo",
      "Judo",
      "Natación",
      "Baile",
      "Campo Traviesa",
      "Halterofilia",
      "Taekwondo",
      "Porrismo"
    ],
    filteredAthletes: ""
  }),

  methods: {
    ...mapActions({
      getAthletes: "athletes/getAthletes"
    }),

    /**
     * Clears the filter fields
     * and resets the filtered list
     * if filters have been applied.
     */
    clearFilters() {
      this.name = "";
      this.sport = "";
      this.menu = false;

      if (this.filteredAthletes.length != this.athletes.length) {
        this.filteredAthletes = [];
        for (let i = 0; i < this.athletes.length; i++) {
          this.filteredAthletes.push(this.athletes[i]);
        }
      }
    },

    /**
     * Applies the filters to the viewed athletes
     * list.
     */
    applyFilters() {
      this.filteredAthletes = [];
      for (let i = 0; i < this.athletes.length; i++) {
        this.filteredAthletes.push(this.athletes[i]);
      }
      
      for(let i = this.filteredAthletes.length-1; i >=0; i--){
        let athlete=this.filteredAthletes[i]
        if(this.sport!=''){          
          if(this.sport.localeCompare(athlete['sportName'])!=0){
            this.filteredAthletes.splice(i,1)
            continue
          }
        }
        if (this.name != "") {
          let fullName = athlete["fName"] + " " + athlete["lName"];
          if (!fullName.toLowerCase().includes(this.name.toLowerCase())) {
            this.filteredAthletes.splice(i, 1);
            continue;
          }
        }
      }
    },

    /**
     * Returns true if athletes have been loaded, false otherwise.
     */
    isReady() {
      if (this.athletes) {
        return true;
      } else {
        return false;
      }
    }
  },

  computed: {
    ...mapGetters({
      athletes: "athletes/athletes"
    })
  },

  mounted() {
    this.getAthletes();
  }
};
</script>