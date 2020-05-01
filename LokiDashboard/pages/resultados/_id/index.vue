<template>
  <v-container class="wrapper">
    <v-container v-if="formated_event_info()">
        <h1 class="primary_dark--text pl-3">Resultados {{sport_name}}</h1>
        <!-- TODO: HOW TO MAKE THIS SIMPLER FORMAT DATE? -->
        <h3>Evento de {{event_date}}</h3>
    </v-container>
    <div class="content-area pa-4 pt-12">
        <v-container>
            <v-container v-if="formated_member_stats()">
                <v-row align="center" justify="center">
                    <v-card width=400 class="mx-lg-auto" outlined>
                        <v-card-title>
                            <v-row justify="center">
                                <h3>Puntuación Final</h3>
                            </v-row>
                            </v-card-title>
                        <v-container>
                            <v-row v-if="formated_final_score()">
                                <v-col >
                                    <v-row justify="center">
                                        <h1>{{uprm_score}}</h1>
                                    </v-row>
                                    <v-row justify="center">
                                        <h3>UPRM</h3>
                                    </v-row>
                                </v-col>
                                
                                <v-col align="center">
                                    <v-row justify="center">
                                        <h2>-</h2>
                                    </v-row>
                                </v-col>
                                
                                <v-col>
                                    <v-row justify="center">
                                        <h1>{{opponent_score}}</h1>
                                    </v-row>
                                    <v-row justify="center">
                                        <h3 v-if="opponent_name">{{opponent_name}}</h3>
                                        <h3 v-else>Oponente</h3>
                                    </v-row>
                                </v-col>
                                
                            </v-row>
                            <v-row v-else justify="center">
                                <v-col align="center">
                                    <h3>No Hay Puntuación Final Disponible</h3>
                                </v-col>
                            </v-row>
                        </v-container>
                    </v-card>   
                </v-row>
                <v-row justify="center" align="center">
                    <v-spacer/>
                    <v-spacer/>
                    <v-col>
                        <v-btn
                            color="primary_light"
                            class="white--text"
                            @click="addFinalScore()"
                        >
                            <v-icon left>
                            mdi-plus
                            </v-icon>
                            Añadir Puntuación Final
                        </v-btn>
                    </v-col>
                    
                    <v-col>
                        <v-btn
                            color="primary_light"
                            class="white--text"
                            @click="editFinalScore()"
                        >
                            <v-icon left>
                            mdi-pencil
                            </v-icon>
                            Editar Puntuación Final
                        </v-btn>
                    </v-col>
                    <v-spacer/>
                    <v-spacer/>
                </v-row>
                <v-container>   
                    <v-tabs centered>
                        <v-tabs-slider/>
                        <v-tab>
                            POR ATLETA
                        </v-tab>

                        <v-tab>
                            POR EQUIPO
                        </v-tab>
                        <v-tab-item>
                            <v-card>
                                
                                <v-card-title>
                                <v-row>
                                    <v-col>
                                    <v-btn
                                        color="primary_light"
                                        class="white--text"
                                        @click="addAthleteStatistics()"
                                    >
                                        <v-icon left>
                                        mdi-plus
                                        </v-icon>
                                        Añadir Estadisticas de Atleta
                                    </v-btn>
                                    <v-spacer />
                                    </v-col>
                                    <v-col cols="4">
                                    <v-text-field
                                        append-icon="mdi-magnify"
                                        label="Búsqueda"
                                        rounded
                                        dense
                                        outlined
                                        single-line
                                        hide-details
                                    />
                                    </v-col>
                                </v-row>
                                </v-card-title>
                                <!-- :headers="headers"
                                :items="users"
                                :search="search"
                                :loading="isLoadingU" -->
                                <!-- THE SPORTS STATS TABLE -->
                                <v-data-table
                                dense 
                                :headers="headers" 
                                :items="payload_stats.athlete_statistic"
                                item-key="athlete_statistic" 
                                class="elevation-1"								 
                                >
                                <!-- v-if="isBasketballTable" -->
                                <template #item.full_name="{ item }">{{ item.athlete_info.first_name }} {{item.athlete_info.middle_name}} {{ item.athlete_info.last_names }}</template>
                                <template v-slot:item.actions="{ item }">
                                    <v-tooltip bottom>
                                    <template v-slot:activator="{ on }">
                                        <v-icon
                                        small
                                        class="mr-2 table-actions"
                                        v-on="on"
                                        @click.stop="editAthleteStatistics(item)"
                                        >
                                        mdi-pencil
                                        </v-icon>
                                    </template>
                                    <span>Editar Estadisticas de Atleta</span>
                                    </v-tooltip>
                                    <!-- <v-tooltip bottom>
                                    <template v-slot:activator="{ on }">
                                        <v-icon
                                        small
                                        class="mr-2 table-actions"
                                        v-on="on"
                                        @click="editPermissions(item)"
                                        >
                                        mdi-shield-lock
                                        </v-icon>
                                    </template>
                                    <span>Edit User Permissions</span>
                                    </v-tooltip> -->
                                    <v-tooltip bottom>
                                    <template v-slot:activator="{ on }">
                                        <v-icon
                                        small
                                        class="mr-2 table-actions"
                                        v-on="on"
                                        @click.stop="deleteAthleteStatistics(item)"
                                        >
                                        mdi-delete
                                        </v-icon>
                                    </template>
                                    <span>Eliminar Estadisticas De Atleta</span>
                                    </v-tooltip>
                                </template>
                                </v-data-table>
                                
                                
                                
                            </v-card>
                        </v-tab-item>
                        <v-tab-item>
                            <v-card>
                                <!-- :headers="headers"
                                :items="users"
                                :search="search"
                                :loading="isLoadingU" -->
                                <v-data-table
                                dense 
                                :headers="team_headers" 
                                :items="team_statistics"
                                item-key="team_statistics" 
                                class="elevation-1"								
                                v-if="payload_stats != ''"
                                >
                                </v-data-table>
                            </v-card>
                        </v-tab-item>
                    </v-tabs>
                </v-container>
            </v-container>
            <AddFinalScoreModal
                v-if ="dialogAddFinalScore"
                :dialog.sync="dialogAddFinalScore"
                :event_id="event_id"
                :sport_route="sport_route"
                :uprm_score.sync="uprm_score"
                :opponent_score.sync="opponent_score"
            />
            <UpdateFinalScoreModal
                v-if ="dialogEditFinalScore"
                :dialog.sync="dialogEditFinalScore"
                :event_id="event_id"
                :sport_route="sport_route"
                :uprm_score.sync="uprm_score"
                :opponent_score.sync="opponent_score"
            />
        </v-container>
    </div>
  </v-container>
</template>

<script>
import { mapActions, mapGetters } from "vuex";
import AddFinalScoreModal from "@/components/AddFinalScoreModal";
import UpdateFinalScoreModal from "@/components/UpdateFinalScoreModal";
export default {
  data() {
    return {
      
      dialogAddFinalScore: false,
      dialogEditFinalScore:false,
    
      editedItemIndex: -1,
      editedItem: '',
      defaultItem: {
        full_name: "",
        username: "",
        email: "",
        is_active: "",
        id: 0
      },
      //====NEW/MODIFIED STUFF==========
      headers:[],
      team_headers:[],
      statistics_per_season:"",
      team_statistics:[],
    //   search_individual: "",
      sport_id: '',
      sport_route:'',
      sport_name: '',
      event_id:'',
      event_date:'',
    //   event_info:'',
      opponent_score:'',
      opponent_name:'', //TODO: MAKE THIS VALUE DYNAMIC
      uprm_score:'',
      payload_stats:'',
      BASKETBALL_IDM: 1,
      BASKETBALL_IDF: 10,
      VOLLEYBALL_IDM: 2,
      VOLLEYBALL_IDF: 12,
      BASEBALL_IDM: 4,
      SOFTBALL_IDF: 16, 
      SOCCER_IDM: 3,
      SOCCER_IDF: 11,
      //season:''

      //OTHE QUERY RELATED VALUES
      team_id:'',
      ready_for_stats:''

    };
  },
// created(){
  async mounted(){
    this.event_id = this.$route.params.id
    this.clearEventInfo()
    this.clearAllStats()
    this.ready_for_stats = true
    console.log("[1] GOT EVENT ID",this.event_id)
    await this.getEventInfo(this.event_id)
    console.log("[2] GOT EVENT INFO",this.event_info)
    // this.buildDefaultValues()
    // this.buildTable()
    // this.getSeasonData()
    //this.buildDefault()
    console.log("the event info...(before)",this.event_info)
        if(this.event_info){
            console.log("GETTING EVENT INFO (from formated method)",this.event_info)
            this.sport_id =  this.event_info.sport_id
            this.sport_name = this.event_info.sport_name
            this.opponent_name = this.event_info.opponent_name
            this.event_date = this.event_info.event_date
            this.team_id = this.event_info.team_id
            // if (this.ready_for_stats){
            console.log("are we ever getting in there????",this.readyForStats)
            if (this.ready_for_stats){
                this.clearAllStats()
                this.buildTable()
                console.log("[3] BUILT TABLE",this.event_info)
                this.buildDefaultValues()
                const stat_params = {
                    event_id: String(this.event_id),
                    sport_route: String(this.sport_route)
                }
                console.log("[4.(-1)] STAT PARAMS ARE (INDEX LEVEL)",stat_params)
                await this.getAllEventStatistics(stat_params)
                this.ready_for_stats = false
                if(this.results_payload){
                    console.log("[4] GOT EVENT STATS",this.results_payload)
                    // console.log(" [5.(-1)] RESULTS PAYLOAD RECEIVED",this.results_payload)
                    if(this.sport_id == this.BASKETBALL_IDM || this.sport_id == this.BASKETBALL_IDF){this.payload_stats = this.results_payload.Basketball_Event_Statistics}
                    else if(this.sport_id == this.VOLLEYBALL_IDM || this.sport_id == this.VOLLEYBALL_IDF){this.payload_stats = this.results_payload.Volleyball_Event_Statistics}
                    else if(this.sport_id == this.SOCCER_IDM || this.sport_id == this.SOCCER_IDF){this.payload_stats = this.results_payload.Soccer_Event_Statistics}
                    else if(this.sport_id == this.BASEBALL_IDM || this.sport_id == this.SOFTBALL_IDF){this.payload_stats = this.results_payload.Baseball_Event_Statistics}
                    else{
                        return false
                    }
                    console.log("[5] WE SHOULD HAVE IT HERE!!!",this.payload_stats)
                    this.team_statistics = [this.payload_stats.team_statistics]
                    this.opponent_score = (this.payload_stats.opponent_score)
                    this.uprm_score = (this.payload_stats.uprm_score)
                    return true
                }
                // console.log("[4] GOT EVENT STATS",this.results_payload)
                // this.ready_for_stats = false
                
            }
        }
    }, 
  components:{
      AddFinalScoreModal,
      UpdateFinalScoreModal
  },
  methods: {
    wtf(){
        return true
    },
    ...mapActions({
        getAllEventStatistics:"results/getAllEventStatistics",
        getEventInfo:"results/getEventInfo",
        clearEventInfo:"results/clearEventInfo",
        clearAllStats:"results/clearAllStats",
        //newish
        stopGetStats:"results/stopGetStats",
    }),
    
    //confirm why this method was deprecated
    formated_event_info(){
        if (this.sport_id != ''){
            return true
        }
        else return false
    },
    formated_member_stats(){
       if (this.payload_stats != ''){
           return true
       }
       else return false
    },
    formated_final_score(){
        console.log("[FS] Do we have a final score?",this.uprm_score,this.opponent_score)
        if(Number.isFinite(this.uprm_score)&&Number.isFinite(this.opponent_score)){
            return true
        }
        else return false
    },
    buildDefaultValues(){
        if(this.sport_id == this.BASKETBALL_IDM || this.sport_id == this.BASKETBALL_IDF){this.sport_route = "basketball"}
        else if(this.sport_id == this.VOLLEYBALL_IDM || this.sport_id == this.VOLLEYBALL_IDF){this.sport_route = "volleyball"}
        else if(this.sport_id == this.SOCCER_IDM || this.sport_id == this.SOCCER_IDF){this.sport_route = "soccer"}
        else if(this.sport_id == this.BASEBALL_IDM || this.sport_id == this.SOFTBALL_IDF){this.sport_route = "baseball"}
        else{this.sport_route = ''}
    },
    buildTable(){
        // basketball
        if (this.sport_id!=''){
            if (this.sport_id == this.BASKETBALL_IDM || this.sport_id == this.BASKETBALL_IDF){
                this.headers = 
                [
                // {
                //     text:'Athlete',
                //     align: 'start',
                //     sortable: true,
                //     value: 'athlete_info.first_name'
                // },
                {text: "Athlete", align:'start', sortable: true, value: "full_name" },
                {text: 'Asistencias', value: 'statistics.assists'},
                {text: 'Blocks', value: 'statistics.blocks'},
                {text: 'Field Goal Attempt', value: 'statistics.field_goal_attempt'},
                {text: 'Field Goal Percentage(%)', value: 'statistics.field_goal_percentage'},
                {text: 'Free Throw Attempt', value: 'statistics.free_throw_attempt'},
                {text: 'Free Throw Percentage(%)', value: 'statistics.free_throw_percentage'},
                {text: 'Points', value: 'statistics.points'},
                {text: 'Rebounds', value: 'statistics.rebounds'},
                {text: 'Steals', value: 'statistics.steals'},
                {text: 'Successful Field Goal', value: 'statistics.successful_field_goal'},
                {text: 'Successful Free Throw', value: 'statistics.successful_free_throw'},
                {text: 'Successful Three Point', value: 'statistics.successful_three_point'},
                {text: 'Three Point Attempt', value: 'statistics.three_point_attempt'},
                {text: 'Three Point Percentage(%)', value: 'statistics.three_point_percentage'},
                {text: 'Turnovers', value: 'statistics.turnovers'},
                { text: "Actions", value: "actions", sortable: false },

                ]
                this.team_headers = 
                [
                {text: 'Assists', value: 'basketball_statistics.assists'},
                {text: 'Blocks', value: 'basketball_statistics.blocks'},
                {text: 'Field Goal Attempt', value: 'basketball_statistics.field_goal_attempt'},
                {text: 'Field Goal Percentage(%)', value: 'basketball_statistics.field_goal_percentage'},
                {text: 'Free Throw Attempt', value: 'basketball_statistics.free_throw_attempt'},
                {text: 'Free Throw Percentage(%)', value: 'basketball_statistics.free_throw_percentage'},
                {text: 'Points', value: 'basketball_statistics.points'},
                {text: 'Rebounds', value: 'basketball_statistics.rebounds'},
                {text: 'Steals', value: 'basketball_statistics.steals'},
                {text: 'Successful Field Goal', value: 'basketball_statistics.successful_field_goal'},
                {text: 'Successful Free Throw', value: 'basketball_statistics.successful_free_throw'},
                {text: 'Successful Three Point', value: 'basketball_statistics.successful_three_point'},
                {text: 'Three Point Attempt', value: 'basketball_statistics.three_point_attempt'},
                {text: 'Three Point Percentage(%)', value: 'basketball_statistics.three_point_percentage'},
                {text: 'Turnovers', value: 'basketball_statistics.turnovers'},
                { text: "Actions", value: "actions", sortable: false },

                ]
            }
            else if (this.sport_id == this.VOLLEYBALL_IDM || this.sport_id == this.VOLLEYBALL_IDF){
                this.headers = 
                [
                // {
                //     text:'Athlete',
                //     align: 'start',
                //     sortable: true,
                //     value: 'athlete_info.first_name'
                // },
                {text: "Athlete", align:'start', sortable: true, value: "full_name" },
                {text: 'Kill Points', value: 'statistics.kill_points'},
                {text: 'Attack Errors', value: 'statistics.attack_errors'},
                {text: 'Assists', value: 'statistics.assists'},
                {text: 'Aces', value: 'statistics.aces'},
                {text: 'Service Errors', value: 'statistics.service_errors'},
                {text: 'Digs', value: 'statistics.digs'},
                {text: 'Blocks', value: 'statistics.blocks'},
                {text: 'Blocking Errors', value: 'statistics.blocking_errors'},
                {text: 'Reception Errors', value: 'statistics.reception_errors'},
                { text: "Actions", value: "actions", sortable: false },

                ]
                this.team_headers = 
                [
                {text: 'Kill Points', value: 'volleyball_statistics.kill_points'},
                {text: 'Attack Errors', value: 'volleyball_statistics.attack_errors'},
                {text: 'Assists', value: 'volleyball_statistics.assists'},
                {text: 'Aces', value: 'volleyball_statistics.aces'},
                {text: 'Service Errors', value: 'volleyball_statistics.service_errors'},
                {text: 'Digs', value: 'volleyball_statistics.digs'},
                {text: 'Blocks', value: 'volleyball_statistics.blocks'},
                {text: 'Blocking Errors', value: 'volleyball_statistics.blocking_errors'},
                {text: 'Reception Errors', value: 'volleyball_statistics.reception_errors'},
                { text: "Actions", value: "actions", sortable: false },

                ]
            }
            else if (this.sport_id == this.SOCCER_IDM || this.sport_id == this.SOCCER_IDF){
                this.headers = 
                [
                // {
                //     text:'Athlete',
                //     align: 'start',
                //     sortable: true,
                //     value: 'athlete_info.first_name'
                // },
                {text: "Athlete", align:'start', sortable: true, value: "full_name" },
                {text: 'Goal Attempts', value: 'statistics.goal_attempts'},
                {text: 'Assists', value: 'statistics.assists'},
                {text: 'Fouls', value: 'statistics.fouls'},
                {text: 'Cards', value: 'statistics.cards'},
                {text: 'Successful Goals', value: 'statistics.successful_goals'},
                {text: 'Tackles', value: 'statistics.tackles'},
                { text: "Actions", value: "actions", sortable: false },

                ]
                this.team_headers = 
                [
                {text: 'Goal Attempts', value: 'soccer_statistics.goal_attempts'},
                {text: 'Assists', value: 'soccer_statistics.assists'},
                {text: 'Fouls', value: 'soccer_statistics.fouls'},
                {text: 'Cards', value: 'soccer_statistics.cards'},
                {text: 'Successful Goals', value: 'soccer_statistics.successful_goals'},
                {text: 'Tackles', value: 'soccer_statistics.tackles'},
                { text: "Actions", value: "actions", sortable: false },

                ]
            }
            else if (this.sport_id == this.BASEBALL_IDM || this.sport_id == this.SOFTBALL_IDF){
                this.headers = 
                [
                // {
                //     text:'Athlete',
                //     align: 'start',
                //     sortable: true,
                //     value: 'athlete_info.first_name'
                // },
                {text: "Athlete", align:'start', sortable: true, value: "full_name" },
                {text: 'At Bats', value: 'statistics.at_bats'},
                {text: 'Runs', value: 'statistics.runs'},
                {text: 'Hits', value: 'statistics.hits'},
                {text: 'Runs Batted In', value: 'statistics.runs_batted_in'},
                {text: 'Base On Balls', value: 'statistics.base_on_balls'},
                {text: 'Strikeouts', value: 'statistics.strikeouts'},
                {text: 'Left On Base', value: 'statistics.left_on_base'},
                { text: "Actions", value: "actions", sortable: false },

                ]
                this.team_headers = 
                [
                {text: 'At Bats', value: 'baseball_statistics.at_bats'},
                {text: 'Runs', value: 'baseball_statistics.runs'},
                {text: 'Hits', value: 'baseball_statistics.hits'},
                {text: 'Runs Batted In', value: 'baseball_statistics.runs_batted_in'},
                {text: 'Base On Balls', value: 'baseball_statistics.base_on_balls'},
                {text: 'Strikeouts', value: 'baseball_statistics.strikeouts'},
                {text: 'Left On Base', value: 'baseball_statistics.left_on_base'},
                { text: "Actions", value: "actions", sortable: false },

                ]
            }
        }
          
        
    },


    // ...mapActions({
    //   getUsers: "dashboardUsers/getUsers",
    //   getPermissions: "dashboardUsers/getPermissions"
    // }),
    // setStatus(status) {
    //   return status ? "Active" : "Inactive";
    // },
    deleteAthleteStatistics(user) {
       if(this.sport_id == this.BASKETBALL_IDM || this.sport_id == this.BASKETBALL_IDF){
            this.editedItemIndex = this.payload_stats.athlete_statistic.indexOf(user)
            this.editedItem = this.payload_stats.athlete_statistic[this.editedItemIndex]
        }
        else if(this.sport_id == this.VOLLEYBALL_IDM || this.sport_id == this.VOLLEYBALL_IDF){
            this.editedItemIndex = this.payload_stats.athlete_statistic.indexOf(user)
            this.editedItem = this.payload_stats.athlete_statistic[this.editedItemIndex]
        }
        else if (this.sport_id == this.SOCCER_IDM || this.sport_id == this.SOCCER_IDF){
            this.editedItemIndex = this.payload_stats.athlete_statistic.indexOf(user)
            this.editedItem = this.payload_stats.athlete_statistic[this.editedItemIndex]
        }
        else if (this.sport_id == this.BASEBALL_IDM || this.sport_id == this.SOFTBALL_IDF){
            this.editedItemIndex = this.payload_stats.athlete_statistic.indexOf(user)
            this.editedItem = this.payload_stats.athlete_statistic[this.editedItemIndex]
        }
        //this.editedItem = Object.assign({}, user); //This hsit is to not mess with vuex state
        //console.log("Will Remove Athlete Statistics for("+this.editedItem+")")
        console.log(this.editedItem)
        console.log("Will Remove Athlete Statistics for "+(this.editedItem.athlete_info.first_name)+" of Athlete ID ("+(this.editedItem.athlete_info.athlete_id)+").")
    },
    deleteTeamStatistics(user) {
       if(this.sport_id == this.BASKETBALL_IDM || this.sport_id == this.BASKETBALL_IDF){
            this.editedItem = this.payload_stats.event_info
        }
        else if(this.sport_id == this.VOLLEYBALL_IDM || this.sport_id == this.VOLLEYBALL_IDF){
           this.editedItem = this.payload_stats.event_info
        }
        else if (this.sport_id == this.SOCCER_IDM || this.sport_id == this.SOCCER_IDF){
            this.editedItem = this.payload_stats.event_info
        }
        else if (this.sport_id == this.BASEBALL_IDM || this.sport_id == this.SOFTBALL_IDF){
           this.editedItem = this.payload_stats.event_info
        }
        //this.editedItem = Object.assign({}, user); //This hsit is to not mess with vuex state
        //console.log("Will Remove Athlete Statistics for("+this.editedItem+")")
        console.log(this.editedItem)
        console.log("Will Remove Team Statistics for Event ID("+(this.editedItem.event_id)+").")
    },
    editAthleteStatistics(user) {
    //   this.editedItemIndex = this.users.indexOf(user)
    //   this.editedItem = Object.assign({}, user); //This hsit is to not mess with vuex state
    //   this.dialogEdit = true;
        this.$router.push("/resultados/"+this.event_id+"/individual/editar")
    },
    editTeamStatistics(user) {
    //   this.editedItemIndex = this.users.indexOf(user)
    //   this.editedItem = Object.assign({}, user); //This hsit is to not mess with vuex state
    //   this.dialogEdit = true;
        return
    },
    addAthleteStatistics() {
    //   this.editedItemIndex = this.users.indexOf(user)
    //   this.editedItem = Object.assign({}, user); //This hsit is to not mess with vuex state
    //   this.dialogEdit = true;
        this.$router.push("/resultados/"+this.event_id+"/individual/crear")
    },
    addTeamStatistics(user) {
    //   this.editedItemIndex = this.users.indexOf(user)
    //   this.editedItem = Object.assign({}, user); //This hsit is to not mess with vuex state
    //   this.dialogEdit = true;
        return
    },
    addFinalScore() {
        // this.$router.push("/resultados/"+this.event_id+"/puntuacion/crear")
        this.dialogAddFinalScore = true;
    },
    editFinalScore() {
        this.dialogEditFinalScore = true;
        // this.$router.push("/resultados/"+this.event_id+"/puntuacion/editar")
    },
    // editPermissions(user) {
    //   this.editedItem = Object.assign({}, user); //This hsit is to not mess with vuex state
    //   this.dialogPermissions = true;
    //   this.getPermissions(user.id);
    // }, resetPassword(user) {
    //   console.log('reset')
    // },
    // Herbert Functions
   
  },
  computed: {
    ...mapGetters({
        results_payload:"results/results_payload",
        event_info:"results/event_info"
    })
    
    
  },
};
</script>

<style lang="scss" scoped>
@import "@/assets/variables.scss";
.wrapper {
  height: 100%;

  .content-area {
    height: 100%;
    width: 100%;

    .table-actions {
      &:hover {
        color: $primary-color;
      }
    }
  }
}
</style>