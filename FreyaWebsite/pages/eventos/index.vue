<template>
  <v-container grid-list-sm>
    <v-row>
      <h1>Eventos:</h1>
    </v-row>

    <v-row class="text-right">
      <v-col align="end">
        <v-menu
          v-model="menu"
          bottom
          origin="center center"
          transition="slide-x-transition"
          :close-on-content-click="false"
        >
          <template v-slot:activator="{ on }">
            <v-btn color="green darken-1" dark v-on="on">
              <v-icon left>mdi-filter-variant</v-icon>Filtros
            </v-btn>
          </template>

          <v-list>
            <v-list-item>
              <v-menu
                ref="menu"
                v-model="dateMenu"
                :close-on-content-click="false"
                :return-value.sync="date"
                transition="scale-transition"
                offset-y
                min-width="290px"
              >
                <template v-slot:activator="{ on }">
                  <v-text-field
                    v-model="date"
                    label="Fecha del Evento"
                    readonly
                    v-on="on"
                  ></v-text-field>
                </template>
                <v-date-picker
                  v-model="date"
                  color="green darken-1"
                  no-title
                  scrollable
                  locale="es-419"
                >
                  <v-spacer></v-spacer>
                  <v-btn text color="primary" @click="dateMenu = false"
                    >Cancelar</v-btn
                  >
                  <v-btn text color="primary" @click="$refs.menu.save(date)"
                    >OK</v-btn
                  >
                </v-date-picker>
              </v-menu>
            </v-list-item>
            <v-list-item>
              <v-autocomplete
                v-model="sport"
                :items="sports"
                label="Deporte"
              ></v-autocomplete>
            </v-list-item>
            <v-list-item>
              <v-select
                v-model="branch"
                :items="branches"
                label="Rama"
              ></v-select>
            </v-list-item>
            <v-list-item>
              <v-select
                v-model="locality"
                :items="localities"
                label="Localizacion"
              ></v-select>
            </v-list-item>
            <v-list-item>
              <v-checkbox v-model="eventHasPBP" label="Eventos con PBP">
              </v-checkbox>
            </v-list-item>

            <v-list-item>
              <v-btn @click="clearFilters">Borrar</v-btn>
              <v-spacer />
              <v-btn @click="createFilteredList">Filtrar</v-btn>
            </v-list-item>
          </v-list>
        </v-menu>
      </v-col>
    </v-row>

    <v-row v-if="filteredEvents != ''">
      <v-col v-for="(value, key) in filteredEvents" :key="key" cols="12"
        sm="6"
        lg="4">
        <EventCard
          :eventID="value.id"
          :sportName="value.sport_name"
          :eventDate="value.event_date"
          :opponentName="value.opponent_name"
          :img="value.sport_img_url"
          :localScore="value.local_score"
          :opponentScore="value.opponent_score"
          :eventSummary="value.event_summary"
          :hasPBP="value.hasPBP"
        />
      </v-col>
    </v-row>

    <v-row v-else>
      <v-col v-for="(value, key) in events" :key="key" cols="12"
        sm="6"
        lg="4">
        <EventCard
          :eventID="value.id"
          :sportName="value.sport_name"
          :eventDate="value.event_date"
          :opponentName="value.opponent_name"
          :img="value.sport_img_url"
          :localScore="value.local_score"
          :opponentScore="value.opponent_score"
          :eventSummary="value.event_summary"
          :hasPBP="value.hasPBP"
        />
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import { mapActions, mapGetters } from "vuex";
import EventCard from "../../components/EventCard";

export default {
  components: {
    EventCard
  },

  data: () => ({
    menu: false,
    dateMenu: false,
    date: "",
    sport: "",
    branch: "",
    locality: "",
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
    branches: ["Masculino", "Femenino", "Exhibición"],
    localities: ["Casa", "Afuera"],
    filteredEvents: "", //This list is the one presented in the events viewer when filtered.
    eventHasPBP: false
  }),

  methods: {
    ...mapActions({
      getEvents: "events/getEvents"
    }),

    /**
     * Clears the filter fields
     * and resets the filtered list
     * if filters have been applied.
     */
    clearFilters() {
      this.date = "";
      this.sport = "";
      this.branch = "";
      this.locality = "";
      this.eventHasPBP = false;
      this.menu = false;

      if (this.filteredEvents.length != this.events.length) {
        this.filteredEvents = [];
        for (let i = 0; i < this.events.length; i++) {
          this.filteredEvents.push(this.events[i]);
        }
      }
    },

    /**
     * Creates a the filtered list, after
     * the user has clicked to filte button,
     * using the the filters selected.
     */
    createFilteredList() {
      this.filteredEvents = [];

      for (let i = 0; i < this.events.length; i++) {
        this.filteredEvents.push(this.events[i]);
      }
      for (let i = this.filteredEvents.length - 1; i >= 0; i--) {
        event = this.filteredEvents[i];
        if (this.sport != "") {
          if (this.sport.localeCompare(event["sport_name"]) != 0) {
            this.filteredEvents.splice(i, 1);
            continue;
          }
        }
        if (this.branch != "") {
          if (this.branch.localeCompare(event["branch"]) != 0) {
            this.filteredEvents.splice(i, 1);
            continue;
          }
        }
        if (this.locality != "") {
          if (this.locality.localeCompare("Casa") == 0) {
            if (event["is_local"] != true) {
              this.filteredEvents.splice(i, 1);
              continue;
            }
          } else {
            if (event["is_local"] != false) {
              this.filteredEvents.splice(i, 1);
              continue;
            }
          }
        }
        if (this.date != "") {
          if (Date.parse(this.date) != Date.parse(event["event_date"])) {
            this.filteredEvents.splice(i, 1);
            continue;
          }
        }
        if (this.eventHasPBP == true) {
          if (!event.hasPBP) {
            this.filteredEvents.splice(i, 1);
            continue;
          }
        }
      }
      this.menu = false;
    }
  },

  computed: {
    ...mapGetters({
      events: "events/events"
    })
  },

  mounted() {
    this.getEvents();
  }
};
</script>