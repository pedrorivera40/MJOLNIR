<template>
  <v-container class="wrapper">
    <h1 class="primary_dark--text pl-3">Eventos</h1>
    <div class="content-area pa-4 pt-12">
      <v-card>
        <v-card-title>
          <v-row>
            <v-menu
              v-model="menu"
              bottom
              origin="center center"
              transition="slide-x-transition"
              :close-on-content-click="false"
            >
              <template v-slot:activator="{ on }">
                <v-col md="3">
                  <v-btn 
                  color="primary_light" 
                  class="white--text"
                  @click="activateEventCreationForm"
                  :disabled="!$store.state.userAuth.userPermissions[0]['13']"
                  >
                    <v-icon left>mdi-plus</v-icon>Añadir Evento
                  </v-btn>

                  <v-btn color="white" v-on="on">
                    <v-icon left>mdi-filter-variant</v-icon>Filtros
                  </v-btn>
                </v-col>
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
                      <v-text-field v-model="date" label="Fecha del Evento" readonly v-on="on"></v-text-field>
                    </template>
                    <v-date-picker
                      v-model="date"
                      color="green darken-1"
                      no-title
                      scrollable
                      locale="es-419"
                    >
                      <v-spacer></v-spacer>
                      <v-btn text color="primary" @click="dateMenu = false">Cancelar</v-btn>
                      <v-btn text color="primary" @click="$refs.menu.save(date)">OK</v-btn>
                    </v-date-picker>
                  </v-menu>
                </v-list-item>
                <v-list-item>
                  <v-autocomplete v-model="sport" :items="sports" label="Deporte"></v-autocomplete>
                </v-list-item>
                <v-list-item>
                  <v-select v-model="branch" :items="branches" label="Rama"></v-select>
                </v-list-item>
                <v-list-item>
                  <v-select v-model="locality" :items="localities" label="Localizacion"></v-select>
                </v-list-item>
                <v-list-item>
                  <v-checkbox v-model="eventHasPBP" label="Eventos con PBP"> </v-checkbox>
                </v-list-item>
                <v-list-item>
                  <v-card-actions>
                    <v-btn @click="clearFilters">Borrar</v-btn>

                    <v-btn @click="filterTheList">Filtrar</v-btn>
                  </v-card-actions>
                </v-list-item>
              </v-list>
            </v-menu>
          </v-row>
        </v-card-title>

        <v-data-table
          :headers="headers"
          :items="filteredEvents"
          :loading="loadingEvents()"
          no-data-text="No hay eventos."
          loading-text="Buscando eventos"
        >
          <template v-slot:item.hasPBP="{ item }">
            <v-tooltip bottom>
              <template v-slot:activator="{ on }">
                <v-btn
                  v-if="item.sport_name == 'Voleibol' & item.hasPBP"
                  color="primary"
                  outlined
                  small
                  v-on="on"
                  @click="goToPBPSequence(item)"
                >Ver PBP</v-btn>
              </template>
              <span>Ver Play-by-Play</span>
            </v-tooltip>
            <v-tooltip bottom>
              <template v-slot:activator="{ on }">
                <v-btn
                  v-if="item.sport_name == 'Voleibol' & !item.hasPBP"
                  color="primary"
                  outlined
                  small
                  v-on="on"
                  @click="createPBPSequence(item)"
                  :disabled="!$store.state.userAuth.userPermissions[3]['16']"
                >Crear PBP</v-btn>
              </template>
              <span>Crear Play-by-Play</span>
            </v-tooltip>
            <span class='text' v-if="item.sport_name !='Voleibol'">
              N/A
            </span>
          </template> 
          <template v-slot:item.actions="{ item }">
            <v-tooltip bottom>
              <template v-slot:activator="{ on }">
                <v-icon
                  med
                  class="mr-2 table-actions"
                  v-on="on"
                  @click="viewEvent(item.id)"
                >mdi-eye-plus</v-icon>
              </template>
              <span>Ver Evento</span>
            </v-tooltip>

            <v-tooltip bottom>
              <template v-slot:activator="{ on }">
                <v-icon
                  medium
                  class="mr-2 table-actions"
                  v-on="on"
                  @click="editEvent(item)"
                  :disabled="!$store.state.userAuth.userPermissions[2]['15']"
                >mdi-pencil</v-icon>
              </template>
              <span>Editar Evento</span>
            </v-tooltip>
            <v-tooltip bottom>
              <template v-slot:activator="{ on }">
                <v-icon
                  medium
                  class="mr-2 table-actions"
                  v-on="on"
                  @click="prepareEventToRemove(item.id)"
                  :disabled="!$store.state.userAuth.userPermissions[1]['14']"
                >mdi-delete</v-icon>
              </template>
              <span>Borrar Evento</span>
            </v-tooltip>
          </template>
        </v-data-table>

        <EditEventModal
          :dialog.sync="dialogEdit"
          :id="editedItem.id"
          :date="editedItem.event_date"
          :time="editedItem.time"
          :locality="editedItem.is_local"
          :venue="editedItem.venue"
          :sport_name="editedItem.sport_name"
          :branch="editedItem.branch"
          :team_season_year="editedItem.team_season_year"
          :opponent_name="editedItem.opponent_name"
          :event_summary="editedItem.event_summary"
          :trigger.sync="ready"
        />

        <AddEventModal :dialog.sync="dialogAdd" :trigger.sync="ready" />

        <DeleteEventModal :dialog.sync="dialogDelete" :id="eid" :trigger.sync="ready" />

        <v-dialog v-model="dialogPBP" persistent max-width="400">
          <v-card>
            <v-card-title class="headline">Falta el nombre del oponente</v-card-title>
            <v-card-text>Tienes que editar el evento y añadirle un nombre del oponente.</v-card-text>
            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn color="black" text @click="closePBPDialog()">Cerrar</v-btn>
            </v-card-actions>
          </v-card>
        </v-dialog>
      </v-card>
    </div>
  </v-container>
</template>

<script>
import { mapActions, mapGetters } from "vuex";
import EditEventModal from "@/components/EditEventModal";
import AddEventModal from "@/components/AddEventModal";
import DeleteEventModal from "@/components/DeleteEventModal";
export default {
  components: {
    EditEventModal,
    AddEventModal,
    DeleteEventModal
  },

  data: () => ({
    ready: false,
    menu: false,
    dialogDelete: false,
    dialogEdit: false,
    dialogAdd: false,
    dialogPBP: false,
    terms: false,
    dateMenu: false,
    loading: true,
    eventHasPBP: false,
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
      "Porrismo",

    ],
    branches: ["Masculino", "Femenino", "Exhibición"],
    localities: ["Casa", "Afuera"],
    filteredEvents:[],//This list is the one presented to the users
    eid: 0,//This is the id of the event to be deleted.
    headers: [
      {
        text: "ID",
        align: "start",
        value: "id"
      },
      { text: "Fecha del Evento", value: "event_date" },
      { text: "Deporte", value: "sport_name" },
      { text: "Rama", value: "branch" },
      { text: "Lugar del Evento", value: "venue" },
      { text: "Play-by-Play", align: "center", value: "hasPBP" },
      { text: "Acciones", value: "actions", sortable: false }
    ],

    //This will be used by the EditEventModal
    editedItem:{
      event_date: "",
      time: "",
      is_local: "",
      venue: "",
      event_summary: "",
      opponent_name: "",
      sport_name: "",
      branch: "",
      team_season_year: 0,
      id: 0
    }

  }),

  methods: {
    ...mapActions({
      getEvents: "events/getEvents",
      removeEvent: "events/removeEvent",
      startPBPSequence: "events/startPBPSequence"
    }),

    /**
     * Activates the AddEventModal dialog component.
     */
    activateEventCreationForm(){
      this.dialogAdd = true
    },

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
     * Returns false if events have been loaded and formated,
     * else it returns true after it formats the data of the events
     * list that have been loaded from the database.
     * 
     */
    loadingEvents(){      
      if(this.events.length > 0){
        if(this.ready){
          return false
        }
        else{         
          
          this.filteredEvents = []
          for (let i = 0; i < this.events.length; i++) {
            this.filteredEvents.push(this.events[i]);
            const parsedDate = new Date(Date.parse(this.events[i].event_date));
            const eDate = parsedDate.toISOString().substring(0, 10);
            const time = parsedDate.getUTCHours() + ":" + parsedDate.getMinutes();
            
            this.filteredEvents[i].event_date = eDate;
            this.filteredEvents[i].time = time;
          }
          this.ready = true;
        }
      }
      else{
        return true
      }
    },    
    
    /**
     * Applies the filters selected 
     * by the user on the  viewable
     * events table.
     */
    filterTheList() {
      this.filteredEvents = [];

      for (let i = 0; i < this.events.length; i++) {
        this.filteredEvents.push(this.events[i]);
        this.filteredEvents[i].event_date = new Date(this.events[i].event_date)
          .toISOString()
          .substring(0, 10);
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
      this.menu = false
    },

    
    /**
     * Routes the user to the event viewer page
     * of the event with the id given as parameter 
     * @param eventID The id of the event
     */
    viewEvent(eventID){
      this.$router.push('/evento/'+eventID)
    },

    /**
     * Activates the EditEventModal using the event information
     * given as parameter.
     * @param event The event Object containg the information of the event to be edited.
     */
    editEvent(event){ 
      console.log(event)    
      this.editedItem = Object.assign({},event)
      this.dialogEdit = true      
    },
    

    /**
     * Activates the DeleteEventModal using
     * the id of the event given as a parameter.
     * @param eventID The id of event to be removed
     */
    prepareEventToRemove(eventID){
      this.eid = eventID
      this.dialogDelete = true
    },    

    /**
     * Routes user to pbp sequence page.
     */
    goToPBPSequence(event)
    {
      this.$router.push('/jugadas-'+event.sport_name.toLowerCase()+'/'+event.id)
    },

    /**
     * Calls the start pbp sequence action
     */
    createPBPSequence(event)
    {
      
      if(event.opponent_name == null || event.opponent_name == '')
        this.dialogPBP = true

      else{
        const eventJSON = {"sport_name":event.sport_name,"event_id":event.id}
        this.startPBPSequence(eventJSON)
      }
    },

    /**
     * Closes the pbp warning dialog 
     */
    closePBPDialog(){
      this.dialogPBP = false
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

<style lang="scss" scoped>
@import "@/assets/tableStyle.scss";
</style>