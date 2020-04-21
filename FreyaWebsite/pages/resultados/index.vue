<template>
  <div class="wrapper">
    <h1>Resultados {{sport_name}}</h1>
    <div class="content-area pa-4 pt-12">
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
    <v-tabs
              centered
          >
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
                        <v-col cols="4">
                        <v-text-field
                            v-model="search_individual"
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
                    <!-- THE BASKETBALL TABLE -->
                    <v-data-table
                    dense 
                    :headers="headers" 
                    :items="payload_stats.Basketball_Event_Statistics.athlete_statistic"
                    :search="search_individual"
                    item-key="athlete_statistic" 
                    class="elevation-1"								
                    v-if="isBasketballTable"
                    >
                    
                    </v-data-table>
                    <!-- VOLLEYBALL TABLE -->
                    <v-data-table
                    dense 
                    :headers="headers" 
                    :items="payload_stats.Volleyball_Event_Statistics.athlete_statistic"
                    :search="search_individual"
                    item-key="athlete_statistic" 
                    class="elevation-1"								
                    v-if="isVolleyballTable"
                    >
                    </v-data-table>
                    <!-- SOCCER TABLE -->
                    <v-data-table
                    dense 
                    :headers="headers" 
                    :items="payload_stats.Soccer_Event_Statistics.athlete_statistic"
                    :search="search_individual"
                    item-key="athlete_statistic" 
                    class="elevation-1"								
                    v-if="isSoccerTable"
                    >
                    </v-data-table>
                    <!-- BASEBALL TABLE -->
                    <v-data-table
                    dense 
                    :headers="headers" 
                    :items="payload_stats.Baseball_Event_Statistics.athlete_statistic"
                    :search="search_individual"
                    item-key="athlete_statistic" 
                    class="elevation-1"								
                    v-if="isBaseballTable"
                    >
                    
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
      search_individual: "",
      sport_id: 2,
      sport_name: "Soccer",
      opponent_score:'',
      opponent_name:"INTER SG", //TODO: MAKE THIS VALUE DYNAMIC
      uprm_score:'',
      payload_stats:'',
      BASKETBALL_IDM: 1,
      BASKETBALL_IDF: 10,
      VOLLEYBALL_IDM: 2,
      VOLLEYBALL_IDF: 12,
      BASEBALL_IDM: 4,
      SOFTBALL_IDF: 16, 
      SOCCER_IDM: 3,
      SOCCER_IDF: 11
      //season:''

    };
  },
  
created(){
      this.buildTable()
      this.getSeasonData()
      //this.buildDefault()
    }, 
  methods: {
    buildDefault(){
        if (this.sport_id!=''){
            if (this.sport_id == this.BASKETBALL_IDM || this.sport_id == this.BASKETBALL_IDF){
                this.editedItem = {
                            "athlete_info": {
                                "athlete_id": '',
                                "basketball_event_id": '',
                                "first_name": '',
                                "last_names": '',
                                "middle_name": '',
                                "number": '',
                                "profile_image_link":''
                            },
                            "statistics": {
                                "assists":'',
                                "blocks":'',
                                "field_goal_attempt": '',
                                "field_goal_percentage": '',
                                "free_throw_attempt": '',
                                "free_throw_percentage": '',
                                "points":'',
                                "rebounds": '',
                                "steals": '',
                                "successful_field_goal": '',
                                "successful_free_throw": '',
                                "successful_three_point": '',
                                "three_point_attempt": '',
                                "three_point_percentage": '',
                                "turnovers": ''
                            }
                        }
                }
                else if (this.sport_id == this.VOLLEYBALL_IDM || this.sport_id == this.VOLLEYBALL_IDF){
                    this.editedItem = {
                            "athlete_info": {
                                "athlete_id": '',
                                "first_name": '',
                                "last_names": '',
                                "middle_name": '',
                                "number": '',
                                "profile_image_link": '',
                                "volleyball_event_id": ''
                            },
                            "statistics": {
                                "aces": '',
                                "assists":'',
                                "attack_errors": '',
                                "blocking_errors": '',
                                "blocks": '',
                                "digs": '',
                                "kill_points": '',
                                "reception_errors": '',
                                "service_errors":''
                            }
                        }
                }
                else if (this.sport_id == this.SOCCER_IDM || this.sport_id == this.SOCCER_IDF){
                    this.editedItem = {
                            "athlete_info": {
                                "athlete_id": '',
                                "first_name": '',
                                "last_names": '',
                                "middle_name": '',
                                "number": '',
                                "profile_image_link": '',
                                "soccer_event_id": ''
                            },
                            "statistics": {
                                "assists": '',
                                "cards": '',
                                "fouls": '',
                                "goal_attempts": '',
                                "successful_goals": '',
                                "tackles": ''
                            }
                        }
                }
                else if (this.sport_id == this.BASEBALL_IDM || this.sport_id == this.SOFTBALL_IDF){
                    this.editedItem = {
                            "athlete_info": {
                            "athlete_id": '',
                            "baseball_event_id": '',
                            "first_name": '',
                            "last_names": '',
                            "middle_name": '',
                            "number": '',
                            "profile_image_link": ''
                            },
                            "statistics": {
                            "at_bats": '',
                            "base_on_balls": '',
                            "hits": '',
                            "left_on_base": '',
                            "runs": '',
                            "runs_batted_in": '',
                            "strikeouts":''
                            }
                        }
                }
            }
    },
    buildTable(){
        // basketball
        if (this.sport_id!=''){
            if (this.sport_id == this.BASKETBALL_IDM || this.sport_id == this.BASKETBALL_IDF){
                this.headers = 
                [
                {
                    text:'Athlete',
                    align: 'start',
                    sortable: true,
                    value: 'athlete_info.first_name'
                },
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
                {
                    text:'Athlete',
                    align: 'start',
                    sortable: true,
                    value: 'athlete_info.first_name'
                },
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
                {
                    text:'Athlete',
                    align: 'start',
                    sortable: true,
                    value: 'athlete_info.first_name'
                },
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
                {
                    text:'Athlete',
                    align: 'start',
                    sortable: true,
                    value: 'athlete_info.first_name'
                },
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


    // ...mapActions({
    //   getUsers: "dashboardUsers/getUsers",
    //   getPermissions: "dashboardUsers/getPermissions"
    // }),
    // setStatus(status) {
    //   return status ? "Active" : "Inactive";
    // },
    deleteAthleteStatistics(user) {
       if(this.sport_id == this.BASKETBALL_IDM || this.sport_id == this.BASKETBALL_IDF){
            this.editedItemIndex = this.payload_stats.Basketball_Event_Statistics.athlete_statistic.indexOf(user)
            this.editedItem = this.payload_stats.Basketball_Event_Statistics.athlete_statistic[this.editedItemIndex]
        }
        else if(this.sport_id == this.VOLLEYBALL_IDM || this.sport_id == this.VOLLEYBALL_IDF){
            this.editedItemIndex = this.payload_stats.Volleyball_Event_Statistics.athlete_statistic.indexOf(user)
            this.editedItem = this.payload_stats.Volleyball_Event_Statistics.athlete_statistic[this.editedItemIndex]
        }
        else if (this.sport_id == this.SOCCER_IDM || this.sport_id == this.SOCCER_IDF){
            this.editedItemIndex = this.payload_stats.Soccer_Event_Statistics.athlete_statistic.indexOf(user)
            this.editedItem = this.payload_stats.Soccer_Event_Statistics.athlete_statistic[this.editedItemIndex]
        }
        else if (this.sport_id == this.BASEBALL_IDM || this.sport_id == this.SOFTBALL_IDF){
            this.editedItemIndex = this.payload_stats.Baseball_Event_Statistics.athlete_statistic.indexOf(user)
            this.editedItem = this.payload_stats.Baseball_Event_Statistics.athlete_statistic[this.editedItemIndex]
        }
        //this.editedItem = Object.assign({}, user); //This hsit is to not mess with vuex state
        //console.log("Will Remove Athlete Statistics for("+this.editedItem+")")
        console.log(this.editedItem)
        console.log("Will Remove Athlete Statistics for "+(this.editedItem.athlete_info.first_name)+" of Athlete ID ("+(this.editedItem.athlete_info.athlete_id)+").")
    },
    deleteTeamStatistics(user) {
       if(this.sport_id == this.BASKETBALL_IDM || this.sport_id == this.BASKETBALL_IDF){
            this.editedItem = this.payload_stats.Basketball_Event_Statistics.event_info
        }
        else if(this.sport_id == this.VOLLEYBALL_IDM || this.sport_id == this.VOLLEYBALL_IDF){
           this.editedItem = this.payload_stats.Volleyball_Event_Statistics.event_info
        }
        else if (this.sport_id == this.SOCCER_IDM || this.sport_id == this.SOCCER_IDF){
            this.editedItem = this.payload_stats.Soccer_Event_Statistics.event_info
        }
        else if (this.sport_id == this.BASEBALL_IDM || this.sport_id == this.SOFTBALL_IDF){
           this.editedItem = this.payload_stats.Baseball_Event_Statistics.event_info
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
        this.$router.push('/resultados/individual/editar')
    },
    editTeamStatistics(user) {
    //   this.editedItemIndex = this.users.indexOf(user)
    //   this.editedItem = Object.assign({}, user); //This hsit is to not mess with vuex state
    //   this.dialogEdit = true;
        return
    },
    addAthleteStatistics(user) {
    //   this.editedItemIndex = this.users.indexOf(user)
    //   this.editedItem = Object.assign({}, user); //This hsit is to not mess with vuex state
    //   this.dialogEdit = true;
        this.$router.push('/resultados/individual/crear')
    },
    addTeamStatistics(user) {
    //   this.editedItemIndex = this.users.indexOf(user)
    //   this.editedItem = Object.assign({}, user); //This hsit is to not mess with vuex state
    //   this.dialogEdit = true;
        return
    },
    addFinalScore() {
        this.$router.push('/resultados/puntuacion/crear')
    },
    editFinalScore() {
        this.$router.push('/resultados/puntuacion/editar')
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
            else if(this.sport_id == this.VOLLEYBALL_IDM || this.sport_id == this.VOLLEYBALL_IDF){
                this.payload_stats = {
                    "Volleyball_Event_Statistics": {
                        "athlete_statistic": [
                        {
                            "athlete_info": {
                                "athlete_id": 70,
                                "first_name": "Jill",
                                "last_names": "Valentine",
                                "middle_name": null,
                                "number": null,
                                "profile_image_link": null,
                                "volleyball_event_id": 3
                            },
                            "statistics": {
                                "aces": 1,
                                "assists": 1,
                                "attack_errors": 1,
                                "blocking_errors": 1,
                                "blocks": 1,
                                "digs": 1,
                                "kill_points": 1,
                                "reception_errors": 1,
                                "service_errors": 1
                            }
                        },
                        {
                            "athlete_info": {
                                "athlete_id": 71,
                                "first_name": "Claire",
                                "last_names": "Redfield",
                                "middle_name": null,
                                "number": null,
                                "profile_image_link": null,
                                "volleyball_event_id": 4
                            },
                            "statistics": {
                                "aces": 3,
                                "assists": 3,
                                "attack_errors": 3,
                                "blocking_errors": 3,
                                "blocks": 3,
                                "digs": 3,
                                "kill_points": 3,
                                "reception_errors": 3,
                                "service_errors": 3
                            }
                        }
                        ],
                        "event_info": {
                            "event_id": 7,
                            "volleyball_event_team_stats_id": 1
                        },
                        "opponent_score": 500,
                        "team_statistics": {
                        "volleyball_statistics": {
                            "aces": 1,
                            "assists": 1,
                            "attack_errors": 1,
                            "blocking_errors": 1,
                            "blocks": 1,
                            "digs": 1,
                            "kill_points": 1,
                            "reception_errors": 1,
                            "service_errors": 1
                            }
                        },
                        "uprm_score": 200
                    }
                }
                this.team_statistics.push(this.payload_stats.Volleyball_Event_Statistics.team_statistics)
                this.opponent_score = (this.payload_stats.Volleyball_Event_Statistics.opponent_score)
                this.uprm_score = (this.payload_stats.Volleyball_Event_Statistics.uprm_score)
                // this.opponent_name = (this.payload_stats.Volleyball_Event_Statistics.opponent_name)
            }
            else if (this.sport_id == this.SOCCER_IDM || this.sport_id == this.SOCCER_IDF){
                this.payload_stats = {
                    "Soccer_Event_Statistics": {
                        "athlete_statistic": [
                        {
                            "athlete_info": {
                                "athlete_id": 73,
                                "first_name": "Sheva",
                                "last_names": "Alomar",
                                "middle_name": null,
                                "number": null,
                                "profile_image_link": null,
                                "soccer_event_id": 9
                            },
                            "statistics": {
                                "assists": 1,
                                "cards": 1,
                                "fouls": 1,
                                "goal_attempts": 1,
                                "successful_goals": 1,
                                "tackles": 1
                            }
                        },
                        {
                            "athlete_info": {
                                "athlete_id": 74,
                                "first_name": "Ada",
                                "last_names": "Wong",
                                "middle_name": null,
                                "number": null,
                                "profile_image_link": null,
                                "soccer_event_id": 10
                            },
                            "statistics": {
                                "assists": 2,
                                "cards": 2,
                                "fouls": 2,
                                "goal_attempts": 2,
                                "successful_goals": 2,
                                "tackles": 2
                            }
                        }
                        ],
                        "event_info": {
                            "event_id": 10,
                            "soccer_event_team_stats_id": 5
                        },
                        "opponent_score": 50,
                        "team_statistics": {
                        "soccer_statistics": {
                            "assists": 10,
                            "cards": 10,
                            "fouls": 20,
                            "goal_attempts": 50,
                            "successful_goals": 30,
                            "tackles": 20
                        }
                        },
                        "uprm_score": 100
                    }
                }
                this.team_statistics.push(this.payload_stats.Soccer_Event_Statistics.team_statistics)
                this.opponent_score = (this.payload_stats.Soccer_Event_Statistics.opponent_score)
                this.uprm_score = (this.payload_stats.Soccer_Event_Statistics.uprm_score)
                // this.opponent_name = (this.payload_stats.Soccer_Event_Statistics.opponent_name)
            }
            else if (this.sport_id == this.BASEBALL_IDM || this.sport_id == this.SOFTBALL_IDF){
                this.payload_stats = {
                    "Baseball_Event_Statistics": {
                        "athlete_statistic": [
                        {
                            "athlete_info": {
                            "athlete_id": 104,
                            "baseball_event_id": 11,
                            "first_name": "Leon ",
                            "last_names": "Kennedy",
                            "middle_name": null,
                            "number": 2,
                            "profile_image_link": null
                            },
                            "statistics": {
                            "at_bats": 1,
                            "base_on_balls": 1,
                            "hits": 1,
                            "left_on_base": 1,
                            "runs": 1,
                            "runs_batted_in": 1,
                            "strikeouts": 1
                            }
                        },
                        {
                            "athlete_info": {
                            "athlete_id": 105,
                            "baseball_event_id": 12,
                            "first_name": "Nemesis",
                            "last_names": "Tyrant",
                            "middle_name": null,
                            "number": 3,
                            "profile_image_link": null
                            },
                            "statistics": {
                            "at_bats": 1,
                            "base_on_balls": 1,
                            "hits": 1,
                            "left_on_base": 1,
                            "runs": 1,
                            "runs_batted_in": 1,
                            "strikeouts": 1
                            }
                        }
                        ],
                        "event_info": {
                        "baseball_event_team_stats_id": 3,
                        "event_id": 24
                        },
                        "opponent_score": 100,
                        "team_statistics": {
                        "baseball_statistics": {
                            "at_bats": 1,
                            "base_on_balls": 1,
                            "hits": 1,
                            "left_on_base": 1,
                            "runs": 1,
                            "runs_batted_in": 1,
                            "strikeouts": 1
                        }
                        },
                        "uprm_score": 100
                    }
                }
                this.team_statistics.push(this.payload_stats.Baseball_Event_Statistics.team_statistics)
                this.opponent_score = (this.payload_stats.Baseball_Event_Statistics.opponent_score)
                this.uprm_score = (this.payload_stats.Baseball_Event_Statistics.uprm_score)
                // this.opponent_name = (this.payload_stats.Baseball_Event_Statistics.opponent_name)
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
    }
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