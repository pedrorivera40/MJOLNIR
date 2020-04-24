<template>
  <div v-if="formated_event_info()" class="wrapper">
    <h1>Resultados {{sport_name}}</h1>
    <!-- PURELY FOR TESTING PURPOSES, TODO: REMOVE SOON 4/24 -->
    <!-- <v-btn class="mr-4" @click="getAllEventStatistics(event_id)" color="green darken-1">GET AGAIN</v-btn>
    <v-btn class="mr-4" @click="formated_member_stats()" color="green darken-1">CHECK THE STATS</v-btn> -->
    <!-- TODO: HOW TO MAKE THIS SIMPLER FORMAT DATE? -->
    <!-- <h3>Evento de {{event_info.Event.event_date}}</h3> -->
    <div class="content-area pa-4 pt-12">
    <v-container v-if="formated_member_stats()">
        <v-row align="center"
        justify="center">
        <v-card width=400 class="mx-lg-auto" outlined>
            <v-card-title>
                <v-row justify="center">
                    <h3>Final Result</h3>
                </v-row>
                </v-card-title>
            <v-container>
                <v-row >  
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
                            <h3>{{opponent_name}}</h3>
                        </v-row>
                    </v-col>
                    
                </v-row>
            </v-container>
        </v-card>   
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
                        <!-- :headers="headers"
                        :items="users"
                        :search="search"
                        :loading="isLoadingU" -->
                        <!-- THE SPORTS STATS TABLE TABLE! -->
                        <v-data-table
                        dense 
                        :headers="headers" 
                        :items="payload_stats.athlete_statistic"
                        item-key="payload_stats.athlete_statistic" 
                        class="elevation-1"								
                        >
                        <template #item.full_name="{ item }">{{ item.athlete_info.first_name }} {{item.athlete_info.middle_name}} {{ item.athlete_info.last_names }}</template>
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
                        >
                        </v-data-table>
                    </v-card>
                </v-tab-item>
            </v-tabs>
        </v-container>
    </v-container>
    </div>
    </div>
</template>

<script>
import { mapActions, mapGetters } from "vuex";
export default {
  data() {
    return {
      
      dialogEdit: false,
      dialogDelete: false,
      dialogPermissions: false,
     
    //   headers: [
    //     {
    //       text: "ID",
    //       align: "start",
    //       sortable: false,
    //       value: "id"
    //     },
    //     { text: "Full Name", value: "full_name" },
    //     { text: "Username", value: "username" },
    //     { text: "Email", value: "email" },
    //     { text: "Account Status", value: "is_active" },
    //     { text: "Password", value: "password" },
    //     { text: "Actions", value: "actions", sortable: false }
    //   ],
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
      team_statistics:'',
      search_individual: "",
      sport_id:'',
      sport_route:'',
      sport_name: '',
      event_id:'',
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
      //INTEGRATION QUERY VARS
      ready_for_event:false,
      ready_for_stats:true,
    };
  },
  
created(){
    this.ready_for_stats=true
    this.clearEventInfo()
    this.clearAllStats()
    this.event_id = this.$route.params.id
    console.log("[1] GOT EVENT ID",this.event_id)
    this.getEventInfo(this.event_id)
    console.log("[2] GOT EVENT INFO",this.event_info)

    // const stat_params = {
    //     event_id: String(this.event_id),
    //     sport_route: String(this.sport_route)
    // }
    // this.getAllEventStatistics(this.stat_params)
    // console.log("[4] GOT EVENT STATS",this.results_payload)

    // this.buildTable()
    // console.log("[3] BUILT TABLE",this.results_payload)
 
}, 
  methods: {
    ...mapActions({
        getAllEventStatistics:"results/getAllEventStatistics",
        getEventInfo:"results/getEventInfo",
        clearEventInfo:"results/clearEventInfo",
        clearAllStats:"results/clearAllStats",
    }),
    formated_event_info(){
        console.log("the event info...(before)",this.results_payload)
        if(this.event_info){
            console.log("GETTING EVENT INFO (from formated method)",this.event_info)
            this.sport_id =  this.event_info.sport_id 
            this.sport_name = this.event_info.sport_name
            this.opponent_name = this.event_info.opponent_name

            if (this.ready_for_stats){
                this.buildTable()
                console.log("[3] BUILT TABLE",this.results_payload)
                this.buildDefaultValues()
                const stat_params = {
                    event_id: String(this.event_id),
                    sport_route: String(this.sport_route)
                }
                console.log("[4.(-1)] STAT PARAMS ARE (INDEX LEVEL)",stat_params)
                this.getAllEventStatistics(stat_params)
                console.log("[4] GOT EVENT STATS",this.results_payload)
                this.ready_for_stats = false
            }
            return true
        }
        else{
            return false
        }
    },
    formated_member_stats(){
        if(this.results_payload){
            console.log(" [5.(-1)] RESULTS PAYLOAD RECEIVED",this.results_payload)
            if(this.sport_id == this.BASKETBALL_IDM || this.sport_id == this.BASKETBALL_IDF){this.payload_stats = this.results_payload.Basketball_Event_Statistics}
            else if(this.sport_id == this.VOLLEYBALL_IDM || this.sport_id == this.VOLLEYBALL_IDF){this.payload_stats = this.results_payload.Volleyball_Event_Statistics}
            else if(this.sport_id == this.SOCCER_IDM || this.sport_id == this.SOCCER_IDF){this.payload_stats = this.results_payload.Soccer_Event_Statistics}
            else if(this.sport_id == this.BASEBALL_IDM || this.sport_id == this.SOFTBALL_IDF){this.payload_stats = this.results_payload.Baseball_Event_Statistics}
            else{
                this.payload_stats = null
                return false  
            }
            console.log("[5] WE SHOULD HAVE IT HERE!!!",this.payload_stats)
            this.team_statistics = [this.payload_stats.team_statistics]
            this.opponent_score = (this.payload_stats.opponent_score)
            this.uprm_score = (this.payload_stats.uprm_score)
            return true
        }
        else{
          return false
        }
    },
    buildDefaultValues(){
        if(this.sport_id == this.BASKETBALL_IDM || this.sport_id == this.BASKETBALL_IDF){this.sport_route = "basketball"}
        else if(this.sport_id == this.VOLLEYBALL_IDM || this.sport_id == this.VOLLEYBALL_IDF){this.sport_route = "volleyball"}
        else if(this.sport_id == this.SOCCER_IDM || this.sport_id == this.SOCCER_IDF){this.sport_route = "soccer"}
        else if(this.sport_id == this.BASEBALL_IDM || this.sport_id == this.SOFTBALL_IDF){this.sport_route = "baseball"}
        else{this.sport_route = ''}
    },

    buildTable(){
        console.log(this.payload_stats)
        
        if (this.sport_id!=''){
            //Basketball
            if (this.sport_id == this.BASKETBALL_IDM || this.sport_id == this.BASKETBALL_IDF){
                this.headers = 
                [
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

                ]
            }
            //Volleyball
            else if (this.sport_id == this.VOLLEYBALL_IDM || this.sport_id == this.VOLLEYBALL_IDF){
                this.headers = 
                [
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

                ]
            }
            //Soccer
            else if (this.sport_id == this.SOCCER_IDM || this.sport_id == this.SOCCER_IDF){
                this.headers = 
                [
                {text: "Athlete", align:'start', sortable: true, value: "full_name" },
                {text: 'Goal Attempts', value: 'statistics.goal_attempts'},
                {text: 'Assists', value: 'statistics.assists'},
                {text: 'Fouls', value: 'statistics.fouls'},
                {text: 'Cards', value: 'statistics.cards'},
                {text: 'Successful Goals', value: 'statistics.successful_goals'},
                {text: 'Tackles', value: 'statistics.tackles'},

                ]
                this.team_headers = 
                [
                {text: 'Goal Attempts', value: 'soccer_statistics.goal_attempts'},
                {text: 'Assists', value: 'soccer_statistics.assists'},
                {text: 'Fouls', value: 'soccer_statistics.fouls'},
                {text: 'Cards', value: 'soccer_statistics.cards'},
                {text: 'Successful Goals', value: 'soccer_statistics.successful_goals'},
                {text: 'Tackles', value: 'soccer_statistics.tackles'},

                ]
            }
            //Baseball
            else if (this.sport_id == this.BASEBALL_IDM || this.sport_id == this.SOFTBALL_IDF){
                this.headers = 
                [
                {text: "Athlete", align:'start', sortable: true, value: "full_name" },
                {text: 'At Bats', value: 'statistics.at_bats'},
                {text: 'Runs', value: 'statistics.runs'},
                {text: 'Hits', value: 'statistics.hits'},
                {text: 'Runs Batted In', value: 'statistics.runs_batted_in'},
                {text: 'Base On Balls', value: 'statistics.base_on_balls'},
                {text: 'Strikeouts', value: 'statistics.strikeouts'},
                {text: 'Left On Base', value: 'statistics.left_on_base'},

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

                ]
            }
        } 
    },
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
  }
}
</style>