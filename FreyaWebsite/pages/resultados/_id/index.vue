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
      ready_for_stats:false,
    };
  },
  
created(){
    // this.clearEventInfo()
    // this.clearAllStats()
    this.event_id = this.$route.params.id
    console.log("[1] GOT EVENT ID",this.event_id)
    this.getEventInfo(this.event_id)
    console.log("[2] GOT EVENT INGO",this.event_info)

    
    this.getAllEventStatistics(this.event_id)
    console.log("[4] GOT EVENT STATS",this.results_payload)

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
            this.sport_id = 1
            // this.sport_id =  this.event_info.sport_id 
            this.sport_name = this.event_info.sport_name
            this.opponent_name = this.event_info.opponent_name
            this.buildTable()
            console.log("[3] BUILT TABLE",this.results_payload)
            return true
        }
        else{
            return false
        }
    },
    formated_member_stats(){
        if(this.results_payload){
            console.log("RESULTS PAYLOAD RECEIVED",this.results_payload)
            if(this.sport_id == this.BASKETBALL_IDM || this.sport_id == this.BASKETBALL_IDF){this.payload_stats = this.results_payload.Basketball_Event_Statistics}
            else if(this.sport_id == this.VOLLEYBALL_IDM || this.sport_id == this.VOLLEYBALL_IDF){this.payload_stats = this.results_payload.Volleyball_Event_Statistics}
            else if(this.sport_id == this.SOCCER_IDM || this.sport_id == this.SOCCER_IDF){this.payload_stats = this.results_payload.Soccer_Event_Statistics}
            else if(this.sport_id == this.BASEBALL_IDM || this.sport_id == this.SOFTBALL_IDF){this.payload_stats = this.results_payload.Softball_Event_Statistics}
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
        this.event_id = this.$route.params.id
        if (this.event_id == 1 || this.event_id == 32){
            //Getting Sport Information
            this.sport_id = this.BASKETBALL_IDM
            this.sport_name = "Baloncesto"
            //Getting Event Information
            this.event_info = {
                "Event": {
                    "branch": "masculino",
                    "event_date": "Sat, 19 Apr 2025 00:00:00 GMT",
                    "event_summary": "Test Event #1: Using to Add All Stats",
                    "id": 32,
                    "is_local": true,
                    "opponent_name": "Inter SG",
                    "sport_img_url": "https://scontent.fsig1-1.fna.fbcdn.net/v/t1.0-9/88207403_3003298336425647_2084912734775803904_o.jpg?_nc_cat=109&_nc_sid=e007fa&_nc_ohc=cPJHsQ73nbMAX988FmN&_nc_ht=scontent.fsig1-1.fna&oh=1ff606b6b98ae4bd4d211840ac373a2a&oe=5EAB30D6",
                    "sport_name": "Baloncesto",
                    "team_id": 25,
                    "team_season_year": 2025,
                    "venue": "Mangual"
                }
            }
        }
    },
    buildDefault(){
     
    },
    buildTable(){
        console.log(this.payload_stats)
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

    // editPermissions(user) {
    //   this.editedItem = Object.assign({}, user); //This hsit is to not mess with vuex state
    //   this.dialogPermissions = true;
    //   this.getPermissions(user.id);
    // }, resetPassword(user) {
    //   console.log('reset')
    // },
    // Herbert Functions
    getSeasonData(){
        //console.log(this.season)
        // TODO: CHANGE SO NOT HARDCODED IDS
		if(this.sport_id!=''){
            if(this.sport_id == this.BASKETBALL_IDM || this.sport_id == this.BASKETBALL_IDF){
                this.payload_stats = {// payload_stats.Basketball_Event_Statistics.athlete_statistic.statistics.
                    "Basketball_Event_Statistics": {
                        "athlete_statistic": [
                        {
                            "athlete_info": {
                                "athlete_id": 4,
                                "basketball_event_id": 16,
                                "first_name": "Larry",
                                "last_names": "Bird",
                                "middle_name": null,
                                "number": 33,
                                "profile_image_link": null
                            },
                            "statistics": {
                                "assists": 2,
                                "blocks": 2,
                                "field_goal_attempt": 2,
                                "field_goal_percentage": 100.0,
                                "free_throw_attempt": 2,
                                "free_throw_percentage": 100.0,
                                "points": 2,
                                "rebounds": 2,
                                "steals": 2,
                                "successful_field_goal": 2,
                                "successful_free_throw": 2,
                                "successful_three_point": 2,
                                "three_point_attempt": 2,
                                "three_point_percentage": 100.0,
                                "turnovers": 2
                            }
                        },
                        {
                            "athlete_info": {
                                "athlete_id": 8,
                                "basketball_event_id": 17,
                                "first_name": "Bruce",
                                "last_names": "Wayne",
                                "middle_name": "Batman",
                                "number": 27,
                                "profile_image_link": "dccomics.com"
                            },
                            "statistics": {
                                "assists": 1,
                                "blocks": 1,
                                "field_goal_attempt": 1,
                                "field_goal_percentage": 100.0,
                                "free_throw_attempt": 1,
                                "free_throw_percentage": 100.0,
                                "points": 1,
                                "rebounds": 1,
                                "steals": 1,
                                "successful_field_goal": 1,
                                "successful_free_throw": 1,
                                "successful_three_point": 1,
                                "three_point_attempt": 1,
                                "three_point_percentage": 100.0,
                                "turnovers": 1
                            }
                        }
                        ],
                        "event_info": {
                            "basketball_event_team_stats_id": 7,
                            "event_id": 5
                        },
                        "opponent_score": 1,
                        "team_statistics": {
                            "basketball_statistics": {
                                "assists": 500,
                                "blocks": 500,
                                "field_goal_attempt": 500,
                                "field_goal_percentage": 100.0,
                                "free_throw_attempt": 500,
                                "free_throw_percentage": 100.0,
                                "points": 500,
                                "rebounds": 500,
                                "steals": 500,
                                "successful_field_goal": 500,
                                "successful_free_throw": 500,
                                "successful_three_point": 500,
                                "three_point_attempt": 500,
                                "three_point_percentage": 100.0,
                                "turnovers": 500
                            }
                        },
                        "uprm_score": 5073
                    }   
                }
                this.team_statistics.push(this.payload_stats.Basketball_Event_Statistics.team_statistics)
                this.opponent_score = (this.payload_stats.Basketball_Event_Statistics.opponent_score)
                this.uprm_score = (this.payload_stats.Basketball_Event_Statistics.uprm_score)
                // this.opponent_name = (this.payload_stats.Basketball_Event_Statistics.opponent_name)
                
            }
        }
            
    }
  },
  computed: {
    // ...mapGetters({
    //   users: "dashboardUsers/users",
    //   isLoadingU: "dashboardUsers/isLoadingU"
    // })
    // a computed getter
    isBasketballTable: function () {
      // `this` points to the vm instance
      return (this.payload_stats != '' && (this.sport_id == this.BASKETBALL_IDM || this.sport_id == this.BASKETBALL_IDF))
    },
    isVolleyballTable: function () {
      // `this` points to the vm instance
      return (this.payload_stats != '' && (this.sport_id == this.VOLLEYBALL_IDM || this.sport_id == this.VOLLEYBALL_IDF))
    },
    isSoccerTable: function () {
      // `this` points to the vm instance
      return (this.payload_stats != '' && (this.sport_id == this.SOCCER_IDM || this.sport_id == this.SOCCER_IDF))
    },
    isBaseballTable: function () {
      // `this` points to the vm instance
      return (this.payload_stats != '' && (this.sport_id == this.BASEBALL_IDM || this.sport_id == this.SOFTBALL_IDF))
    },
    ...mapGetters({
        results_payload:"results/results_payload",
        event_info:"results/event_info"
	})
  },
//   mounted() {
//     this.getUsers();
//   }
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