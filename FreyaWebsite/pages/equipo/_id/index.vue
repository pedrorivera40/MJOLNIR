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
                    <h2>No Se Encontro Equipo</h2>
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
                <h2>No Se Encontraron Miembros de Equipo</h2>
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
              <v-container v-if="formated_member_stats()">		
                <v-card flat>
                  <!-- Basketball Table -->
                  <v-data-table 
                    dense 
                    :headers="headers" 
                    :items="statistics_per_season" 
                    item-key="statistics_per_season" 
                    class="elevation-1"								
                    loading-text="Recolectando Data...Por favor espere"
                    v-if="statistics_per_season != ''"
                  >		
                  <template #item.full_name="{ item }">{{ item.Athlete.first_name }} {{item.Athlete.middle_name}} {{ item.Athlete.last_names }}</template>	
                  </v-data-table>
                </v-card>
              </v-container>
              <v-container v-else>
                <v-row align = "center" justify = "center">
                  <v-col justify = "center" align = "center">
                    <h2>No Se Encontraron Estadisticas Individuales</h2>
                  </v-col>
                </v-row>
              </v-container>
            
            </v-tab-item>
            <v-tab-item>
              <v-container v-if="formated_team_stats()">
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
              </v-container>
              <v-container v-else>
                <v-row align = "center" justify = "center">
                  <v-col justify = "center" align = "center">
                    <h2>No Se Encontraron Estadisticas de Equipo</h2>
                  </v-col>
                </v-row>
              </v-container>
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
      sport_route:'',
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
      team_statistics_per_season:'',
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

      current_team:'',
      current_team_id:'',
      events:[],
      ready_for_members: false,

      }),//end of data()
    
    created(){
      this.setNullTeam()
      this.setNullTeamMembers()
      this.setNullMembersStats()
      this.setNullTeamStats()
      this.current_team = null
      this.members = null
      this.statistics_per_season = null
      this.team_statistics_per_season = null
      
      
      
      this.buildYearList()
      this.buildDefaultValues()
      this.getSeasonData()
      this.buildTable()
      
      
    }, 

		methods: {
      ...mapActions({
        getTeamByYear:"teams/getTeamByYear",
        getTeamMembers:"teams/getTeamMembers",
        stopGetMembers:"teams/stopGetMembers",
        stopGetMemberStats:"teams/stopGetMemberStats",
        stopGetTeamStats:"teams/stopGetTeamStats",
        getMemberStatistics:"teams/getMemberStatistics",
        getTeamStatistics:"teams/getTeamStatistics",
        setNullTeam:"teams/setNullTeam",
        setNullTeamMembers:"teams/setNullTeamMembers",
        setNullMembersStats:"teams/setNullMemberStats",
        setNullTeamStats:"teams/setNullTeamStats",
      }),
      
      formated(){
        if(this.team){
          this.current_team_id = this.team.team_info.team_id
          this.current_team = this.team.team_info
          
          if(this.readyForMembers){
            console.log("INDEX LEVEL LOCAL TEAM",this.current_team)
            console.log("INDEX LEVEL QUERY TEAM",this.team)
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
          if(this.readyForMemberStats){
            console.log("INDEX LEVEL QUERY MEMBERS:",this.team.members)
            const team_params = {
              sport_id: String(this.sport_id),
              season_year: String(this.season),
              sport_route: String(this.sport_route)
            }
            console.log("INDEX LEVEL STAT PARAMS:",this.team_params)
            this.getMemberStatistics(team_params)
          }
          this.stopGetMemberStats()
          return true
        }
        else{
          return false
        }
      },
      formated_member_stats(){
        if(this.member_statistics){
          if(this.sport_id == this.BASKETBALL_IDM || this.sport_id == this.BASKETBALL_IDF){this.statistics_per_season = this.member_statistics.Basketball_Event_Season_Athlete_Statistics}
          else if(this.sport_id == this.VOLLEYBALL_IDM || this.sport_id == this.VOLLEYBALL_IDF){this.statistics_per_season = this.member_statistics.Volleyball_Event_Season_Athlete_Statistics}
          else if(this.sport_id == this.SOCCER_IDM || this.sport_id == this.SOCCER_IDF){this.statistics_per_season = this.member_statistics.Soccer_Event_Season_Athlete_Statistics}
          else if(this.sport_id == this.BASEBALL_IDM || this.sport_id == this.SOFTBALL_IDF){this.statistics_per_season = this.member_statistics.Baseball_Event_Season_Athlete_Statistics}
          else{
            this.statistics_per_season = null
            return false  
          }
          if(this.readyForTeamStats){
            console.log("INDEX LEVEL QUERY MEMBER STATS:",this.statistics_per_season)
            const team_params = {
              sport_id: String(this.sport_id),
              season_year: String(this.season),
              sport_route: String(this.sport_route)
            }
            console.log("STRAIGHT FROM MEMBERS= STATS, PARAMS ARE:",this.team.members)
            this.getTeamStatistics(team_params)
          }
          this.stopGetTeamStats()
          return true
        }
        else{
          return false
        }
      },

      formated_team_stats(){
        if(this.team_statistics){
          console.log("//////=====THIS IS A FUCKING TEST YO=======////",this.team_statistics)
          if(this.sport_id == this.BASKETBALL_IDM || this.sport_id == this.BASKETBALL_IDF){this.team_statistics_per_season = [this.team_statistics.Basketball_Event_Season_Team_Statistics]}
          else if(this.sport_id == this.VOLLEYBALL_IDM || this.sport_id == this.VOLLEYBALL_IDF){this.team_statistics_per_season = [this.team_statistics.Volleyball_Event_Season_Team_Statistics]}
          else if(this.sport_id == this.SOCCER_IDM || this.sport_id == this.SOCCER_IDF){this.team_statistics_per_season = [this.team_statistics.Soccer_Event_Season_Team_Statistics]}
          else if(this.sport_id == this.BASEBALL_IDM || this.sport_id == this.SOFTBALL_IDF){this.team_statistics_per_season = [this.team_statistics.Baseball_Event_Season_Team_Statistics]}
          else{
            this.team_statistics_per_season = null
            return false
          }
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
        if(this.sport_id == this.BASKETBALL_IDM || this.sport_id == this.BASKETBALL_IDF){this.sport_name = "Baloncesto", this.sport_route = "basketball"}
        else if(this.sport_id == this.VOLLEYBALL_IDM || this.sport_id == this.VOLLEYBALL_IDF){this.sport_name = "Voleibol",this.sport_route = "volleyball"}
        else if(this.sport_id == this.SOCCER_IDM || this.sport_id == this.SOCCER_IDF){this.sport_name = "Fútbol", this.sport_route = "soccer"}
        else if(this.sport_id == this.BASEBALL_IDM || this.sport_id == this.SOFTBALL_IDF){this.sport_name = "Beisbol", this.sport_route = "baseball"}
        else{this.sport_name = '', this.sport_route = ''}
        
      },
      // getMembersData(){
      //   // if(this.sport_id == this.BASKETBALL_IDM || this.sport_id == this.BASKETBALL_IDF){
      //   //   this.team_statistics_per_season.push(current_team_stats.Baseball_Event_Season_Team_Statistics)
      //   // }
      // },
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
          this.setNullTeam()
          this.setNullTeamMembers()
          this.setNullMembersStats()
          this.setNullTeamStats()
          this.current_team = null
          this.statistics_per_season = null
          this.team_statistics_per_season = null
          this.members = null
          
          // this.team = false
          // this.ready = false
          // this.getMembersData()
          this.getEvents()
          const team_params = {
            sport_id: String(this.sport_id),
            season_year: String(this.season)
          }
          //console.log("At the index level inside the getSeasonData, request params look like",team_params)
          this.getTeamByYear(team_params)   
          // this.getMemberStatistics(team_params)    
          // this.getTeamStatistics(team_params)   


          
            
				
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
        readyForMembers:"teams/readyForMembers",
        readyForMemberStats:"teams/readyForMemberStats",
        readyForTeamStats:"teams/readyForTeamStats",
        member_statistics:"teams/member_statistics",
        team_statistics:"teams/team_statistics"

			})
		}

		// mounted(){
      
    
    //   // // console.log("The request will have:",this.sport_id,this.season)
    //   // const team_params = {
    //   //   sport_id: String(this.sport_id),
    //   //   season_year: String(this.season)
    //   // }
    //   // // console.log("At the index level, request params look like",team_params)
    //   // this.getTeamByYear(team_params)
      
    //   // // console.log("WE GOT THE TEAM BOI (from index):",this.team)
		// }
}
</script>