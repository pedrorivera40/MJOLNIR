<template>
	<v-card>
		<v-toolbar
				color="green darken-1"
				dark
				flat
		>
			<v-spacer />
			<v-toolbar-title>{{sport_name}}</v-toolbar-title>
			<v-spacer />
		</v-toolbar>
		<v-container>
      <v-col>
      </v-col>
      <v-row align="center">
        <v-col justify="center" align="center">
          <h1>Tarzanes</h1>
        </v-col>
      </v-row>
      <v-row align="center"
      justify="start">
        <v-col md=3>
          <v-select
            v-model="season"
            item-value="season_year" 
            item-text="season_year"
            :items="yearList" 
            label ="Temporada"
            prepend-icon="mdi-calendar-blank-multiple"
            @input="getSeasonData"
          ></v-select>
        </v-col>
      </v-row>
			<v-tabs 
					centered
			>
				<v-tabs-slider/>
				<v-tab>
						DESCRIPCIÓN
				</v-tab>

        <v-tab>
						ATLETAS
				</v-tab>

				<v-tab>
						ESTADÍSTICAS
				</v-tab>

        <v-tab>
						EVENTOS
				</v-tab>

				<v-tab-item>

						<v-card class="mx-auto" outlined>								
							<v-container v-if="formated()">
                <!-- <v-row>
                  <v-carousel
                  cycle
                  hide-delimiters
                  show-arrows-on-hover
                  >
                    <v-carousel-item
                      v-for="(team,i) in teams"
                      :key="i"
                      :src="team.team_image_url"
                    ></v-carousel-item>
                  </v-carousel>		
                </v-row> -->
                <v-row align = "center" justify = "center">
                  <v-col justify = "center" align = "center">
                    <v-icon v-if="current_team.team_image_url == null" height="100"> mdi-account-group  </v-icon>
                    <v-img v-else :src="current_team.team_image_url" aspect-ratio="2"> 
                    </v-img>
                  </v-col>
                </v-row>
								<v-row>
									<v-col v-if = "current_team.about_team">
										<h2> Sobre el Equipo: </h2>
										<p>
											{{current_team.about_team}}
										</p>
									</v-col>
								</v-row>
							</v-container>
              <v-container v-else>
                <v-row align = "center" justify = "center">
                  <v-col justify = "center" align = "center">
                    <h2>No Team Found</h2>
                  </v-col>
                </v-row>
              </v-container>
						</v-card>
						
				</v-tab-item>

        <v-tab-item>
          <v-container v-if="formated_members()">
            <v-row
            v-for="member in members" 
            :key='member.athlete_id'
            align="center" justify="center"> 
              <v-col >
                <v-hover
                  v-slot:default="{ hover }"
                  close-delay="200"
                >
                  <AthleteCardSimple
                    :first_name="member.first_name"
                    :middle_name="member.middle_name"
                    :last_names="member.last_names"
                    :height_inches="member.height_inches"
                    :study_program="member.study_program"
                    :school_of_precedence="member.school_of_precedence"
                    :athlete_positions="member.athlete_positions"
                    :athlete_categories="member.athlete_categories"   
                    :number="member.number"
                    :profile_image_link="member.profile_image_link"
                    :athlete_id="member.athlete_id"
                    :years_of_participation="member.years_of_participation"
                  />
                </v-hover>
              </v-col>
            </v-row>
          </v-container>
          <v-container v-else>
            <v-row align = "center" justify = "center">
              <v-col justify = "center" align = "center">
                <h2>No Team Members Found</h2>
              </v-col>
            </v-row>
          </v-container>
        </v-tab-item>
        
				<v-tab-item>
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

            <!-- TODO: need to make it so the table "by athlete" has the season statistics OF EACH ATHLETE. Show athlete name and maaaybe pic. -->
            <!-- TODO: need to make it so the table "by team" doesnt have date, just the general statistics of the team for the season. -->
            <v-tab-item>				
                <v-card flat>
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
                  <!-- Basketball Table -->
                  <v-data-table 
                    dense 
                    :headers="headers" 
                    :items="statistics_per_season.season_stats" 
                    :search="search_individual"
                    item-key="season_stats" 
                    class="elevation-1"								
                    loading-text="Recolectando Data...Por favor espere"
                    v-if="statistics_per_season != ''"
                  >		
                  <template #item.full_name="{ item }">{{ item.Athlete.first_name }} {{item.Athlete.middle_name}} {{ item.Athlete.last_names }}</template>	
                  </v-data-table>

                </v-card>
            
            </v-tab-item>
            <v-tab-item>
              <v-card flat>
                  <v-data-table 
                    dense 
                    :headers="team_headers" 
                    :items="team_statistics_per_season" 
                    item-key="team_statistics_per_season" 
                    class="elevation-1"								
                    loading-text="Recolectando Data...Por favor espere"
                    v-if="team_statistics_per_season != ''"
                  >			
                  </v-data-table>

                </v-card>
            </v-tab-item>
          </v-tabs>

        
        </v-tab-item>
        <v-tab-item>
          <v-row>
            <v-col v-for="(value,key) in events" :key=key md="3">
          
            <EventCardSimple      
              :eventID="value.id"     
              :eventDate="value.event_date"
              opponentName='UPRP'
              :localScore='value.local_score'
              :opponentScore='value.opponent_score' 
              eventSummary="El evento fue entretinido"
            />        
            </v-col>
          </v-row>
        </v-tab-item>
			</v-tabs>
		</v-container>        
			
	</v-card>
</template>

<script>
import EventCardSimple from '~/components/EventCardSimple'
import AthleteCardSimple from '~/components/AthleteCardSimple.vue'

import {mapActions,mapGetters} from "vuex"

export default {
  components: {
    AthleteCardSimple,
    EventCardSimple:EventCardSimple
  },


    data: () =>({
    
      //NOTE: Using pre-written data for athlete with id:8,
      //      will need to fetch this data below from the API.
    
      about_team:"Because he's the hero Gotham deserves, but not the one it needs right now, so we'll hunt him. Because he can take it, because he's not a hero. He's a silent guardian, a watchful protector, a Dark Knight.",
      ready:false,
      sport_name:'',     
			branch:'Masculino', 
      sport_id:'',
			season:'',
			// seasonsseasons:['2020'],
      headers:[],
      team_headers:[],
      // [//Need to dynamically buid this after fetchin data.Might hardcode this depending on the sport.
			// 	{
			// 		text:'Event Date',
			// 		align: 'start',
			// 		sortable: true,
			// 		value:"Event.event_date"
			// 	},
			// 	{text: 'Assists', value: 'Event_Statistics.assists'},
			// 	{text: 'Blocks', value: 'Event_Statistics.blocks'},
			// 	{text: 'Field Goal Attempt', value: 'Event_Statistics.field_goal_attempt'},
			// 	{text: 'Field Goal Percentage(%)', value: 'Event_Statistics.field_goal_percentage'},
			// 	{text: 'Free Throw Attempt', value: 'Event_Statistics.free_throw_attempt'},
			// 	{text: 'Free Throw Percentage(%)', value: 'Event_Statistics.free_throw_percentage'},
			// 	{text: 'Points', value: 'Event_Statistics.points'},
			// 	{text: 'Rebounds', value: 'Event_Statistics.rebounds'},
			// 	{text: 'Steals', value: 'Event_Statistics.steals'},
			// 	{text: 'Successful Field Goal', value: 'Event_Statistics.successful_field_goal'},
			// 	{text: 'Successful Free Throw', value: 'Event_Statistics.successful_free_throw'},
			// 	{text: 'Successful Three Point', value: 'Event_Statistics.successful_three_point'},
			// 	{text: 'Three Point Attempt', value: 'Event_Statistics.three_point_attempt'},
			// 	{text: 'Three Point Percentage(%)', value: 'Event_Statistics.three_point_percentage'},
			// 	{text: 'Turnovers', value: 'Event_Statistics.turnovers'},

      // ],
      //IMPORTANT FOR METHODS:
      selected: '',
      statistics_per_season:'',
      team_statistics_per_season:[],
      members:'',
      yearList:[],  
      defaultSelected:[],

      BASKETBALL_IDM: 1,
      BASKETBALL_IDF: 10,
      VOLLEYBALL_IDM: 2,
      VOLLEYBALL_IDF: 12,
      BASEBALL_IDM: 4,
      SOFTBALL_IDF: 16, 
      SOCCER_IDM: 3,
      SOCCER_IDF: 11,

      search_individual: '',

      

    //Get all teams from a given sport is necessary
    teams: [
          {
            team_id: 1,
            season_year: 2020,
            team_image_url: 'https://scontent-mia3-2.xx.fbcdn.net/v/t1.0-9/85226550_3003297953092352_1360046190787297280_o.jpg?_nc_cat=107&_nc_sid=cdbe9c&_nc_oc=AQmakM3rR18YLUFlI8ZRraQEU8mHM4f2V-1UI3Dv5eo-C3XwYGCO7mkelEfv3qWOem0&_nc_ht=scontent-mia3-2.xx&oh=1ef35fa1c82cd0fe716b8ccde133d9e7&oe=5EB4A8D7',
          },
          {
            team_id: 2,
            season_year: 2021,
            team_image_url: 'https://scontent-mia3-2.xx.fbcdn.net/v/t1.0-9/53308974_2150741998347956_5929499645469261824_o.jpg?_nc_cat=102&_nc_sid=cdbe9c&_nc_oc=AQkRydUsowo3pUMMVoN8KdZMqSWP60zWLGlFYgOQLJhN6eH2SAQB01cyGsigTmasvv0&_nc_ht=scontent-mia3-2.xx&oh=7fc8133a08a2c9e049dedbbc689d62a3&oe=5EB5C2E2',
          },
          {
            team_id: 3,
            season_year: 2022,
            team_image_url: 'https://scontent-mia3-2.xx.fbcdn.net/v/t1.0-9/89775037_3018436938245120_7244710629703942144_o.jpg?_nc_cat=103&_nc_sid=cdbe9c&_nc_oc=AQm3OioI29F5kvicCjSrascjVapegmU7TrqInUzAdUK_Odqr1yFkNqxgzUcondMhuuo&_nc_ht=scontent-mia3-2.xx&oh=eb53711a5de3d73ace11e40f4f663c11&oe=5EB4540F',
          },
          {
            team_id: 4,
            season_year: 2023,
            team_image_url: 'https://scontent-mia3-2.xx.fbcdn.net/v/t1.0-9/53255400_2150742488347907_5032536115572113408_o.jpg?_nc_cat=110&_nc_sid=cdbe9c&_nc_oc=AQlAZzUmMDbfLqJXSfAOlDAoP7_pyp58sPqPJ1MLE9-JgUtmldcr3NEq3OcNJMZEgt8&_nc_ht=scontent-mia3-2.xx&oh=9ca5fa4bb6ee0bdc1acb52841855cf6f&oe=5EB61445',
          },
        ],

      current_team:'',
      current_team_id:'',
      events:[],
      ready_for_members: false,

      }),//end of data()
    
    created(){
      this.current_team = null
      this.team_members = null
      this.buildYearList()
      this.buildDefaultValues()
      this.getSeasonData()
      this.buildTable()
      
      
    }, 

		methods: {
      ...mapActions({
        getTeamByYear:"teams/getTeamByYear",
        getTeamMembers:"teams/getTeamMembers",
        stopGetMembers:"teams/stopGetMembers"
      }),
      
      formated(){
        if(this.team){
          this.current_team_id = this.team.team_info.team_id
          this.current_team = this.team.team_info
          
          if(this.readyForMembers){
            console.log("HEYO CURR TEAM",this.current_team)
            console.log("HEYO TEAM",this.team)
            this.getTeamMembers(this.current_team_id)
            // this.ready_for_members = false
          }
          // this.readyForMembers = false
          this.stopGetMembers()
          return true
        }
        else{
          this.team_members = null
          return false
        }
      },
      formated_members(){
        if(this.team_members){
          this.members = this.team_members.team_members
          return true
        }
        else{
          return false
        }
      },

      // // ORIGINAL LUIS ATHLETE VERSION
      // formated(){
			// 	if(this.athlete){
			// 		if(this.ready){
			// 			return true
			// 		}
			// 		else{

			// 			if(!this.ready){

			// 				this.ready = true
			// 			}
			// 		}
			// 	}
			// 	else
			// 	{
			// 		return false
			// 	}

			// },


      buildTable(){
        // basketball
        if (this.sport_id == this.BASKETBALL_IDM || this.sport_id == this.BASKETBALL_IDF) {
          this.headers = [
            // {
            //   text:'Athlete',
            //   align: 'start',
            //   sortable: true,
            //   value: 'Athlete.first_name'
            // },
            {text: "Athlete", align:'start', sortable: true, value: "full_name" },
            {text: 'Assists', value: 'Event_Statistics.assists'},
            {text: 'Blocks', value: 'Event_Statistics.blocks'},
            {text: 'Field Goal Attempt', value: 'Event_Statistics.field_goal_attempt'},
            {text: 'Field Goal Percentage(%)', value: 'Event_Statistics.field_goal_percentage'},
            {text: 'Free Throw Attempt', value: 'Event_Statistics.free_throw_attempt'},
            {text: 'Free Throw Percentage(%)', value: 'Event_Statistics.free_throw_percentage'},
            {text: 'Points', value: 'Event_Statistics.points'},
            {text: 'Rebounds', value: 'Event_Statistics.rebounds'},
            {text: 'Steals', value: 'Event_Statistics.steals'},
            {text: 'Successful Field Goal', value: 'Event_Statistics.successful_field_goal'},
            {text: 'Successful Free Throw', value: 'Event_Statistics.successful_free_throw'},
            {text: 'Successful Three Point', value: 'Event_Statistics.successful_three_point'},
            {text: 'Three Point Attempt', value: 'Event_Statistics.three_point_attempt'},
            {text: 'Three Point Percentage(%)', value: 'Event_Statistics.three_point_percentage'},
            {text: 'Turnovers', value: 'Event_Statistics.turnovers'},
          ]
          this.team_headers = [
            {text: 'Assists', value: 'Event_Statistics.assists'},
            {text: 'Blocks', value: 'Event_Statistics.blocks'},
            {text: 'Field Goal Attempt', value: 'Event_Statistics.field_goal_attempt'},
            {text: 'Field Goal Percentage(%)', value: 'Event_Statistics.field_goal_percentage'},
            {text: 'Free Throw Attempt', value: 'Event_Statistics.free_throw_attempt'},
            {text: 'Free Throw Percentage(%)', value: 'Event_Statistics.free_throw_percentage'},
            {text: 'Points', value: 'Event_Statistics.points'},
            {text: 'Rebounds', value: 'Event_Statistics.rebounds'},
            {text: 'Steals', value: 'Event_Statistics.steals'},
            {text: 'Successful Field Goal', value: 'Event_Statistics.successful_field_goal'},
            {text: 'Successful Free Throw', value: 'Event_Statistics.successful_free_throw'},
            {text: 'Successful Three Point', value: 'Event_Statistics.successful_three_point'},
            {text: 'Three Point Attempt', value: 'Event_Statistics.three_point_attempt'},
            {text: 'Three Point Percentage(%)', value: 'Event_Statistics.three_point_percentage'},
            {text: 'Turnovers', value: 'Event_Statistics.turnovers'},
          ]
        }
        else if (this.sport_id == this.VOLLEYBALL_IDM || this.sport_id == this.VOLLEYBALL_IDF){
          this.headers = 
          [
          // {
          //     text:'Athlete',
          //     align: 'start',
          //     sortable: true,
          //     value: 'Athlete.first_name'
          // },
          {text: "Athlete", align:'start', sortable: true, value: "full_name" },
          {text: 'Kill Points', value: 'Event_Statistics.kill_points'},
          {text: 'Attack Errors', value: 'Event_Statistics.attack_errors'},
          {text: 'Assists', value: 'Event_Statistics.assists'},
          {text: 'Aces', value: 'Event_Statistics.aces'},
          {text: 'Service Errors', value: 'Event_Statistics.service_errors'},
          {text: 'Digs', value: 'Event_Statistics.digs'},
          {text: 'Blocks', value: 'Event_Statistics.blocks'},
          {text: 'Blocking Errors', value: 'Event_Statistics.blocking_errors'},
          {text: 'Reception Errors', value: 'Event_Statistics.reception_errors'},


          ]
          this.team_headers = 
          [
          {text: 'Kill Points', value: 'Event_Statistics.kill_points'},
          {text: 'Attack Errors', value: 'Event_Statistics.attack_errors'},
          {text: 'Assists', value: 'Event_Statistics.assists'},
          {text: 'Aces', value: 'Event_Statistics.aces'},
          {text: 'Service Errors', value: 'Event_Statistics.service_errors'},
          {text: 'Digs', value: 'Event_Statistics.digs'},
          {text: 'Blocks', value: 'Event_Statistics.blocks'},
          {text: 'Blocking Errors', value: 'Event_Statistics.blocking_errors'},
          {text: 'Reception Errors', value: 'Event_Statistics.reception_errors'},
    
          ]
        }
        else if (this.sport_id == this.SOCCER_IDM || this.sport_id == this.SOCCER_IDF){
            this.headers = 
            [
            // {
            //     text:'Athlete',
            //     align: 'start',
            //     sortable: true,
            //     value: 'Athlete.first_name'
            // },
            {text: "Athlete", align:'start', sortable: true, value: "full_name" },
            {text: 'Goal Attempts', value: 'Event_Statistics.goal_attempts'},
            {text: 'Assists', value: 'Event_Statistics.assists'},
            {text: 'Fouls', value: 'Event_Statistics.fouls'},
            {text: 'Cards', value: 'Event_Statistics.cards'},
            {text: 'Successful Goals', value: 'Event_Statistics.successful_goals'},
            {text: 'Tackles', value: 'Event_Statistics.tackles'},


            ]
            this.team_headers = 
            [
            {text: 'Goal Attempts', value: 'Event_Statistics.goal_attempts'},
            {text: 'Assists', value: 'Event_Statistics.assists'},
            {text: 'Fouls', value: 'Event_Statistics.fouls'},
            {text: 'Cards', value: 'Event_Statistics.cards'},
            {text: 'Successful Goals', value: 'Event_Statistics.successful_goals'},
            {text: 'Tackles', value: 'Event_Statistics.tackles'},
            
            ]
        }
        else if (this.sport_id == this.BASEBALL_IDM || this.sport_id == this.SOFTBALL_IDF){
            this.headers = 
            [
            // {
            //     text:'Athlete',
            //     align: 'start',
            //     sortable: true,
            //     value: 'Athlete.first_name'
            // },
            {text: "Athlete", align:'start', sortable: true, value: "full_name" },
            {text: 'At Bats', value: 'Event_Statistics.at_bats'},
            {text: 'Runs', value: 'Event_Statistics.runs'},
            {text: 'Hits', value: 'Event_Statistics.hits'},
            {text: 'Runs Batted In', value: 'Event_Statistics.runs_batted_in'},
            {text: 'Base On Balls', value: 'Event_Statistics.base_on_balls'},
            {text: 'Strikeouts', value: 'Event_Statistics.strikeouts'},
            {text: 'Left On Base', value: 'Event_Statistics.left_on_base'},
          
            ]
            this.team_headers = 
            [
            {text: 'At Bats', value: 'Event_Statistics.at_bats'},
            {text: 'Runs', value: 'Event_Statistics.runs'},
            {text: 'Hits', value: 'Event_Statistics.hits'},
            {text: 'Runs Batted In', value: 'Event_Statistics.runs_batted_in'},
            {text: 'Base On Balls', value: 'Event_Statistics.base_on_balls'},
            {text: 'Strikeouts', value: 'Event_Statistics.strikeouts'},
            {text: 'Left On Base', value: 'Event_Statistics.left_on_base'},
            
            ]
          }
        },

      buildYearList(){
        let yearToAdd = 2020
        let currentYear = new Date(2023,8).getFullYear()
        this.season = currentYear
        
        while(yearToAdd <= currentYear)
        {
            this.yearList.push({'season_year':yearToAdd++})
        }
      },
      buildDefaultValues(){
        let currentYear = new Date(2023,8).getFullYear()
        this.defaultSelected.push({'season_year':currentYear})
        this.sport_id = this.$route.params.id
        if(this.sport_id == this.BASKETBALL_IDM || this.sport_id == this.BASKETBALL_IDF){this.sport_name = "Baloncesto"}
        else if(this.sport_id == this.VOLLEYBALL_IDM || this.sport_id == this.VOLLEYBALL_IDF){this.sport_name = "Voleibol"}
        else if(this.sport_id == this.SOCCER_IDM || this.sport_id == this.SOCCER_IDF){this.sport_name = "Futbol"}
        else if(this.sport_id == this.BASEBALL_IDM || this.sport_id == this.SOFTBALL_IDF){this.sport_name = "Beisbol"}
        
      },
      getMembersData(){
      
        if(this.sport_id == this.BASKETBALL_IDM || this.sport_id == this.BASKETBALL_IDF){

          let current_stats = {
            "Basketball_Event_Season_Athlete_Statistics": [
              {
                "Athlete": {
                  "athlete_id": 1,
                  "first_name": "Kobe",
                  "last_names": "Bryant",
                  "middle_name": null,
                  "number": 24,
                  "profile_image_link": null
                },
                "Event_Statistics": {
                  "assists": 8,
                  "blocks": 8,
                  "field_goal_attempt": 8,
                  "field_goal_percentage": 100.0,
                  "free_throw_attempt": 8,
                  "free_throw_percentage": 100.0,
                  "points": 8,
                  "rebounds": 8,
                  "steals": 8,
                  "successful_field_goal": 8,
                  "successful_free_throw": 8,
                  "successful_three_point": 8,
                  "three_point_attempt": 8,
                  "three_point_percentage": 100.0,
                  "turnovers": 8
                }
              },
              {
                "Athlete": {
                  "athlete_id": 3,
                  "first_name": "Lebron",
                  "last_names": "James",
                  "middle_name": null,
                  "number": 23,
                  "profile_image_link": null
                },
                "Event_Statistics": {
                  "assists": 23,
                  "blocks": 5,
                  "field_goal_attempt": 2,
                  "field_goal_percentage": 50.0,
                  "free_throw_attempt": 7,
                  "free_throw_percentage": 100.0,
                  "points": 78,
                  "rebounds": 0,
                  "steals": 2,
                  "successful_field_goal": 1,
                  "successful_free_throw": 7,
                  "successful_three_point": 3,
                  "three_point_attempt": 10,
                  "three_point_percentage": 30.0,
                  "turnovers": 43
                }
              },
              {
                "Athlete": {
                  "athlete_id": 4,
                  "first_name": "Larry",
                  "last_names": "Bird",
                  "middle_name": null,
                  "number": 33,
                  "profile_image_link": null
                },
                "Event_Statistics": {
                  "assists": 10,
                  "blocks": 10,
                  "field_goal_attempt": 10,
                  "field_goal_percentage": 100.0,
                  "free_throw_attempt": 10,
                  "free_throw_percentage": 100.0,
                  "points": 10,
                  "rebounds": 10,
                  "steals": 10,
                  "successful_field_goal": 10,
                  "successful_free_throw": 10,
                  "successful_three_point": 10,
                  "three_point_attempt": 10,
                  "three_point_percentage": 100.0,
                  "turnovers": 10
                }
              },
              {
                "Athlete": {
                  "athlete_id": 8,
                  "first_name": "Bruce",
                  "last_names": "Wayne",
                  "middle_name": "Batman",
                  "number": 27,
                  "profile_image_link": null
                },
                "Event_Statistics": {
                  "assists": 35,
                  "blocks": 9,
                  "field_goal_attempt": 137,
                  "field_goal_percentage": 95.62043795620438,
                  "free_throw_attempt": 41,
                  "free_throw_percentage": 60.97560975609756,
                  "points": 162,
                  "rebounds": 26,
                  "steals": 20,
                  "successful_field_goal": 131,
                  "successful_free_throw": 25,
                  "successful_three_point": 50,
                  "three_point_attempt": 55,
                  "three_point_percentage": 90.9090909090909,
                  "turnovers": 9
                }
              }
            ]
          }
          this.statistics_per_season = {"season_stats":current_stats.Basketball_Event_Season_Athlete_Statistics}
          
        
          let current_team_stats = {
            "Basketball_Event_Season_Team_Statistics": {
              "Event_Statistics": {
                "assists": 2064,
                "blocks": 2020,
                "field_goal_attempt": 2145,
                "field_goal_percentage": 99.67365967365967,
                "free_throw_attempt": 2054,
                "free_throw_percentage": 99.22103213242454,
                "points": 2246,
                "rebounds": 2032,
                "steals": 2028,
                "successful_field_goal": 2138,
                "successful_free_throw": 2038,
                "successful_three_point": 2059,
                "three_point_attempt": 2071,
                "three_point_percentage": 99.4205697730565,
                "turnovers": 2058
              },
              "team_id": 1
            }
          }
          this.team_statistics_per_season.push(current_team_stats.Basketball_Event_Season_Team_Statistics)
        
        }
        if(this.sport_id == this.VOLLEYBALL_IDM || this.sport_id == this.VOLLEYBALL_IDF){
          let current_stats = {
            "Volleyball_Event_Season_Athlete_Statistics": [
              {
                "Athlete": {
                  "athlete_id": 71,
                  "first_name": "Claire",
                  "last_names": "Redfield",
                  "middle_name": null,
                  "number": null,
                  "profile_image_link": null
                },
                "Event_Statistics": {
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
              },
              {
                "Athlete": {
                  "athlete_id": 70,
                  "first_name": "Jill",
                  "last_names": "Valentine",
                  "middle_name": null,
                  "number": null,
                  "profile_image_link": null
                },
                "Event_Statistics": {
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
              }
            ]
          }
          this.statistics_per_season = {"season_stats":current_stats.Volleyball_Event_Season_Athlete_Statistics}
          
        
          let current_team_stats = {
            "Volleyball_Event_Season_Team_Statistics": {
              "Event_Statistics": {
                "aces": 1,
                "assists": 1,
                "attack_errors": 1,
                "blocking_errors": 1,
                "blocks": 1,
                "digs": 1,
                "kill_points": 1,
                "reception_errors": 1,
                "service_errors": 1
              },
              "team_id": 4
            }
          }
          this.team_statistics_per_season.push(current_team_stats.Volleyball_Event_Season_Team_Statistics)
        }
        if(this.sport_id == this.SOCCER_IDM || this.sport_id == this.SOCCER_IDF){
          let current_stats = {
            "Soccer_Event_Season_Athlete_Statistics": [
              {
                "Athlete": {
                  "athlete_id": 73,
                  "first_name": "Sheva",
                  "last_names": "Alomar",
                  "middle_name": null,
                  "number": null,
                  "profile_image_link": null
                },
                "Event_Statistics": {
                  "assists": 1,
                  "cards": 1,
                  "fouls": 1,
                  "goal_attempts": 1,
                  "successful_goals": 1,
                  "tackles": 1
                }
              },
              {
                "Athlete": {
                  "athlete_id": 74,
                  "first_name": "Ada",
                  "last_names": "Wong",
                  "middle_name": null,
                  "number": null,
                  "profile_image_link": null
                },
                "Event_Statistics": {
                  "assists": 2,
                  "cards": 2,
                  "fouls": 2,
                  "goal_attempts": 2,
                  "successful_goals": 2,
                  "tackles": 2
                }
              }
            ]
          }
          this.statistics_per_season = {"season_stats":current_stats.Soccer_Event_Season_Athlete_Statistics}
          
        
          let current_team_stats = {
            "Soccer_Event_Season_Team_Statistics": {
              "Event_Statistics": {
                "assists": 10,
                "cards": 10,
                "fouls": 20,
                "goal_attempts": 50,
                "successful_goals": 30,
                "tackles": 20
              },
              "team_id": 7
            }
          }
          this.team_statistics_per_season.push(current_team_stats.Soccer_Event_Season_Team_Statistics)
        }
        if(this.sport_id == this.BASEBALL_IDM || this.sport_id == this.SOFTBALL_IDF){
          let current_stats = {
            "Baseball_Event_Season_Athlete_Statistics": [
              {
                "Athlete": {
                  "athlete_id": 104,
                  "first_name": "Leon ",
                  "last_names": "Kennedy",
                  "middle_name": null,
                  "number": 2,
                  "profile_image_link": null
                },
                "Event_Statistics": {
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
                "Athlete": {
                  "athlete_id": 105,
                  "first_name": "Nemesis",
                  "last_names": "Tyrant",
                  "middle_name": null,
                  "number": 3,
                  "profile_image_link": null
                },
                "Event_Statistics": {
                  "at_bats": 1,
                  "base_on_balls": 1,
                  "hits": 1,
                  "left_on_base": 1,
                  "runs": 1,
                  "runs_batted_in": 1,
                  "strikeouts": 1
                }
              }
            ]
          }
          this.statistics_per_season = {"season_stats":current_stats.Baseball_Event_Season_Athlete_Statistics}
          
        
          let current_team_stats = {
            "Baseball_Event_Season_Team_Statistics": {
              "Event_Statistics": {
                "at_bats": 1,
                "base_on_balls": 1,
                "hits": 1,
                "left_on_base": 1,
                "runs": 1,
                "runs_batted_in": 1,
                "strikeouts": 1
              },
              "team_id": 14
            }
          }
          this.team_statistics_per_season.push(current_team_stats.Baseball_Event_Season_Team_Statistics)
        }
      },
      getEvents(){
        this.events =  [
        {
          "branch": "masculino",
          "event_date": "Wed, 01 Apr 2020 00:00:00 GMT",
          "id": 5,
          "is_local": true,
          "local_score": 5073,
          "opponent_color": null,
          "opponent_name": null,
          "opponent_score": 1,
          "sport_name": "Baloncesto",
          "team_id": 1,
          "venue": "Mangual"
        },
        {
          "branch": "masculino",
          "event_date": "Mon, 20 Apr 2020 00:00:00 GMT",
          "id": 6,
          "is_local": true,
          "local_score": 0,
          "opponent_color": null,
          "opponent_name": null,
          "opponent_score": 0,
          "sport_name": "Baloncesto",
          "team_id": 1,
          "venue": "Espada"
        },
        {
          "branch": "masculino",
          "event_date": "Mon, 23 Mar 2020 00:00:00 GMT",
          "id": 3,
          "is_local": false,
          "local_score": 200,
          "opponent_color": "red",
          "opponent_name": null,
          "opponent_score": 500,
          "sport_name": "Baloncesto",
          "team_id": 1,
          "venue": "Mangual"
        },
        {
          "branch": "masculino",
          "event_date": "Mon, 16 Mar 2020 00:00:00 GMT",
          "id": 17,
          "is_local": false,
          "local_score": null,
          "opponent_color": "black",
          "opponent_name": null,
          "opponent_score": null,
          "sport_name": "Baloncesto",
          "team_id": 1,
          "venue": "Choliseo"
        },
        {
          "branch": "masculino",
          "event_date": "Sat, 14 Mar 2020 00:00:00 GMT",
          "id": 4,
          "is_local": true,
          "local_score": null,
          "opponent_color": null,
          "opponent_name": null,
          "opponent_score": null,
          "sport_name": "Baloncesto",
          "team_id": 1,
          "venue": "Espada"
        }
      ]
      },
			getSeasonData(){
          this.team = null
          this.team_members = null
          this.current_team = null
          this.members = null
          // this.team = false
          // this.ready = false
          this.getMembersData()
          this.getEvents()
          const team_params = {
            sport_id: String(this.sport_id),
            season_year: String(this.season)
          }
          console.log("At the index level inside the getSeasonData, request params look like",team_params)
          // this.ready = false
          // this.team = false
          // this.ready_for_members = true
          this.getTeamByYear(team_params)
          
          // this.formated()
          // while(!this.team){
          //   this.ready = false
          // }
          // if (this.team){
          //       this.current_team = this.team.team_info
          //       this.team = ''
          //       this.ready = true
          // }

          
            
				
			}
    },

    computed: {
      // current_team: {
      //   // getter
      //   get: function () {
      //     return this.team
      //   },
      //   // setter
      //   set: function (newValue) {
      //     var names = newValue.split(' ')
      //     this.firstName = names[0]
      //     this.lastName = names[names.length - 1]
      //   }
      // },
			...mapGetters({
        team:"teams/team",
        team_members:"teams/team_members",
        readyForMembers:"teams/readyForMembers"
			})
		},

		mounted(){
      
      console.log("YOOOOOOOOOO WTF WE HEEEEEEEEEEEERE",this.sport_id,this.season)
      console.log("The request will have:",this.sport_id,this.season)
      const team_params = {
        sport_id: String(this.sport_id),
        season_year: String(this.season)
      }
      console.log("At the index level, request params look like",team_params)
      this.getTeamByYear(team_params)
      console.log("WE GOT THE TEAM BOI (from index):",this.team)
		}
}
</script>