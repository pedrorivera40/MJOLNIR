<template>
	<v-card>
		<v-toolbar
				color="green darken-1"
				dark
				flat
		>
			<v-spacer />
			<v-toolbar-title>{{sport}}</v-toolbar-title>
			<v-spacer />
		</v-toolbar>
		<v-container>
      <v-row align="center"
      justify="center">
        <h1>Tarzanes</h1>
      </v-row>
      <v-row align="center"
      justify="center">
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
        <v-col>
          <v-row align="center"
            justify="end">
            <v-col md=3 align="end">
              <v-btn class="mr-4" @click="goToEditTeam" color="green darken-1">Editar Equipo</v-btn>
            </v-col>
            <v-col md=3 align="end">
              <v-btn class="mr-4" @click="goToCreateTeam" color="green darken-1">Añadir Equipo +</v-btn>
            </v-col>
          </v-row>
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
							<v-container>
                <v-row>
                  <v-carousel
                  cycle
                  hide-delimiters
                  show-arrows-on-hover
                  >
                    <v-carousel-item
                      v-for="(team,i) in teams"
                      :key="i"
                      :src="team.team_image_link"
                    ></v-carousel-item>
                  </v-carousel>		
                </v-row>
								<v-row>
									<v-col>
										<h2> Sobre el Equipo: </h2>
										<p>
											{{current_team.about_team}}
										</p>
									</v-col>
								</v-row>
							</v-container>
						</v-card>
						
				</v-tab-item>

        <v-tab-item>
          <v-row align="center"
            justify="end">
            <v-col md=3 align="end">
              <v-btn class="mr-4" @click="goToAddMembers" color="green darken-1">Añadir Miembro +</v-btn>
            </v-col>
          </v-row>
          <v-row
          v-for="member in members.members" 
          :key='member.athlete_id'
          align="center" justify="center"> 
            <v-col >
              <v-hover
                v-slot:default="{ hover }"
                close-delay="200"
              >
                <athlete_simple
                  :first_name="member.first_name"
                  :middle_name="member.middle_name"
                  :last_names="member.last_names"
                  :short_bio="member.short_bio"
                  :height_feet="member.height_feet"
                  :height_inches="member.height_inches"
                  :study_program="member.study_program"
                  :date_of_birth="member.date_of_birth"
                  :school_of_precedence="member.school_of_precedence"
                  :athlete_positions="member.athlete_positions"
                  :athlete_categories="member.athlete_categories"   
                  :number="member.number"
                  :profile_image_link="member.profile_image_link"
                  :sport="member.sport"
                  :branch="member.branch"
                  :athlete_id="member.athlete_id"
                  :years_of_participation="member.years_of_participation"
                />
              </v-hover>
            </v-col>
            <v-col align="center" justify="center" sm=1>
              <v-hover
                v-slot:default="{ hover }"
                close-delay="200"
              >
                <v-icon x-large color="red darken-2" @click="removeMember(member.athlete_id)">mdi-trash-can-outline </v-icon>
              </v-hover>
            </v-col>
          </v-row>
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

            <v-tab-item>				
                <v-card flat>
                  <v-data-table 
                    dense 
                    :headers="headers" 
                    :items="statistics_per_season.season" 
                    item-key="season" 
                    class="elevation-1"								
                    loading-text="Recolectando Data...Por favor espere"
                    v-if="statistics_per_season != ''"
                  >			
                  </v-data-table>

                </v-card>
            
            </v-tab-item>
            <v-tab-item>
              <v-card flat>
                  <v-data-table 
                    dense 
                    :headers="headers" 
                    :items="statistics_per_season.season" 
                    item-key="season" 
                    class="elevation-1"								
                    loading-text="Recolectando Data...Por favor espere"
                    v-if="statistics_per_season != ''"
                  >			
                  </v-data-table>

                </v-card>
            </v-tab-item>
          </v-tabs>

        <v-tab-item>
        </v-tab-item>
      </v-tab-item>
			
			</v-tabs>
		</v-container>        
			
	</v-card>
</template>

<script>
import Logo from '~/components/Logo.vue'
import athlete_simple from '~/components/athlete_simple.vue'
export default {
  components: {
    Logo,
    athlete_simple
  },


    data: () =>({
    
      //NOTE: Using pre-written data for athlete with id:8,
      //      will need to fetch this data below from the API.
    
      about_team:"Because he's the hero Gotham deserves, but not the one it needs right now, so we'll hunt him. Because he can take it, because he's not a hero. He's a silent guardian, a watchful protector, a Dark Knight.",

      sport:'Baloncesto',     
			branch:'Masculino', 

			season:'',
			seasonsseasons:['2020'],
			headers:[//Need to dynamically buid this after fetchin data.Might hardcode this depending on the sport.
				{
					text:'Event Date',
					align: 'start',
					sortable: true,
					value:"Event.event_date"
				},
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

      ],
      //IMPORTANT FOR METHODS:
      selected: '',
      statistics_per_season:'',
      members:'',
      yearList:[],  
      defaultSelected:[],

    //Get all teams from a given sport is necessary
    teams: [
          {
            team_id: 1,
            season_year: 2020,
            team_image_link: 'https://scontent-mia3-2.xx.fbcdn.net/v/t1.0-9/85226550_3003297953092352_1360046190787297280_o.jpg?_nc_cat=107&_nc_sid=cdbe9c&_nc_oc=AQmakM3rR18YLUFlI8ZRraQEU8mHM4f2V-1UI3Dv5eo-C3XwYGCO7mkelEfv3qWOem0&_nc_ht=scontent-mia3-2.xx&oh=1ef35fa1c82cd0fe716b8ccde133d9e7&oe=5EB4A8D7',
          },
          {
            team_id: 2,
            season_year: 2021,
            team_image_link: 'https://scontent-mia3-2.xx.fbcdn.net/v/t1.0-9/53308974_2150741998347956_5929499645469261824_o.jpg?_nc_cat=102&_nc_sid=cdbe9c&_nc_oc=AQkRydUsowo3pUMMVoN8KdZMqSWP60zWLGlFYgOQLJhN6eH2SAQB01cyGsigTmasvv0&_nc_ht=scontent-mia3-2.xx&oh=7fc8133a08a2c9e049dedbbc689d62a3&oe=5EB5C2E2',
          },
          {
            team_id: 3,
            season_year: 2022,
            team_image_link: 'https://scontent-mia3-2.xx.fbcdn.net/v/t1.0-9/89775037_3018436938245120_7244710629703942144_o.jpg?_nc_cat=103&_nc_sid=cdbe9c&_nc_oc=AQm3OioI29F5kvicCjSrascjVapegmU7TrqInUzAdUK_Odqr1yFkNqxgzUcondMhuuo&_nc_ht=scontent-mia3-2.xx&oh=eb53711a5de3d73ace11e40f4f663c11&oe=5EB4540F',
          },
          {
            team_id: 4,
            season_year: 2023,
            team_image_link: 'https://scontent-mia3-2.xx.fbcdn.net/v/t1.0-9/53255400_2150742488347907_5032536115572113408_o.jpg?_nc_cat=110&_nc_sid=cdbe9c&_nc_oc=AQlAZzUmMDbfLqJXSfAOlDAoP7_pyp58sPqPJ1MLE9-JgUtmldcr3NEq3OcNJMZEgt8&_nc_ht=scontent-mia3-2.xx&oh=9ca5fa4bb6ee0bdc1acb52841855cf6f&oe=5EB61445',
          },
        ],

      current_team:'',

      }),//end of data()
    
    created(){
      
      this.buildYearList()
      this.buildDefaultValues()
      this.getSeasonData()
      
    }, 

		methods: {
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
      },
      goToEditTeam(){
            this.$router.push('/equipo/edit/')
        },
      goToCreateTeam(){
            this.$router.push('/equipo/create/')
        },
      goToAddMembers(){
            this.$router.push('/equipo/members/add/')
        },
      removeMember(athlete_id){
            console.log("Will Remove Athlete("+athlete_id+") from Team("+this.current_team.team_id+")")
        },
			getSeasonData(){
        console.log(this.season)
				if(this.season!=''){
          //This line below will later be modified to fetch data from a file.
          if(this.season == 2020){
            this.current_team = {
              team_id: 1,
              season_year: 2020,
              team_image_link: 'https://scontent-mia3-2.xx.fbcdn.net/v/t1.0-9/85226550_3003297953092352_1360046190787297280_o.jpg?_nc_cat=107&_nc_sid=cdbe9c&_nc_oc=AQmakM3rR18YLUFlI8ZRraQEU8mHM4f2V-1UI3Dv5eo-C3XwYGCO7mkelEfv3qWOem0&_nc_ht=scontent-mia3-2.xx&oh=1ef35fa1c82cd0fe716b8ccde133d9e7&oe=5EB4A8D7',
            }
            this.members = {"members":[
              {
                "first_name": "Bruce",
                "middle_name": "Batman",
                "last_names":"Wayne",
                "short_bio":"I am vengeance, I am the night.",
                "height_feet":7,
                "height_inches":0,
              
                "study_program":"Forensics", 
                "date_of_birth":"1980-07-21",
                "school_of_precedence":"Gotham High",
                "athlete_positions":["Base","Escolta"],
                "athlete_categories":{},      
                "number":27,
                "profile_image_link":"https://scontent-mia3-2.xx.fbcdn.net/v/t1.0-9/18056978_1321492691261909_7453541174330533269_n.jpg?_nc_cat=102&_nc_sid=8024bb&_nc_oc=AQmWfwxDy-LTXcZv4K0hcL8VNdr4F0JDlBW90Hq3YG157GtEuXYnB-AKL6hNki0uuh4&_nc_ht=scontent-mia3-2.xx&oh=6dc80a0cb41e6c693897b317148b3753&oe=5EB4AFCF",
                "sport":"Baloncesto",     
                "branch":"Masculino", 

                "years_of_participation":4,
                "athlete_id": 1,
              },
              {
                "first_name": "Richard",
                "middle_name": "Nightwing",
                "last_names":"Grayson",
                "short_bio":"I am vengeance, I am the night.",
                "height_feet":7,
                "height_inches":0,
              
                "study_program":"Police", 
                "date_of_birth":"1980-07-21",
                "school_of_precedence":"Flying Graysons",
                "athlete_positions":["Base","Escolta"],
                "athlete_categories":{},      
                "number":77,
                "profile_image_link":"https://vignette.wikia.nocookie.net/marvel_dc/images/a/a2/Nightwing_0008.jpg/revision/latest?cb=20111009075845",
                "sport":"Baloncesto",     
                "branch":"Masculino",

                "years_of_participation":4,
                "athlete_id": 2,
              },
              {
                "first_name": "Clark",
                "middle_name": "Superman",
                "last_names":"Kent",
                "short_bio":"Up, Up, and Away",
                "height_feet":7,
                "height_inches":0,
              
                "study_program":"Reporter", 
                "date_of_birth":"1980-07-21",
                "school_of_precedence":"Smallville High",
                "athlete_positions":["Base","Escolta"],
                "athlete_categories":{},      
                "number":1,
                "profile_image_link":"https://pbs.twimg.com/media/DUOPKlWU0AEGY0S.jpg:large",
                "sport":"Baloncesto",     
                "branch":"Masculino",

                "years_of_participation":4,
                "athlete_id": 3,
              }
              ],
            }
          } 
          else if(this.season==2021){
            this.current_team = {
              team_id: 2,
              season_year: 2021,
              team_image_link: 'https://scontent-mia3-2.xx.fbcdn.net/v/t1.0-9/53308974_2150741998347956_5929499645469261824_o.jpg?_nc_cat=102&_nc_sid=cdbe9c&_nc_oc=AQkRydUsowo3pUMMVoN8KdZMqSWP60zWLGlFYgOQLJhN6eH2SAQB01cyGsigTmasvv0&_nc_ht=scontent-mia3-2.xx&oh=7fc8133a08a2c9e049dedbbc689d62a3&oe=5EB5C2E2',
            }
            this.members = {"members":[
              {
                "first_name": "Bruce",
                "middle_name": "Batman",
                "last_names":"Wayne",
                "short_bio":"I am vengeance, I am the night.",
                "height_feet":7,
                "height_inches":0,
              
                "study_program":"Forensics", 
                "date_of_birth":"1980-07-21",
                "school_of_precedence":"Gotham High",
                "athlete_positions":["Base","Escolta"],
                "athlete_categories":{},      
                "number":27,
                "profile_image_link":"https://scontent-mia3-2.xx.fbcdn.net/v/t1.0-9/18056978_1321492691261909_7453541174330533269_n.jpg?_nc_cat=102&_nc_sid=8024bb&_nc_oc=AQmWfwxDy-LTXcZv4K0hcL8VNdr4F0JDlBW90Hq3YG157GtEuXYnB-AKL6hNki0uuh4&_nc_ht=scontent-mia3-2.xx&oh=6dc80a0cb41e6c693897b317148b3753&oe=5EB4AFCF",
                "sport":"Baloncesto",     
                "branch":"Masculino", 

                "years_of_participation":4,
                "athlete_id": 1,
              },
              {
                "first_name": "Clark",
                "middle_name": "Superman",
                "last_names":"Kent",
                "short_bio":"Up, Up, and Away",
                "height_feet":7,
                "height_inches":0,
              
                "study_program":"Reporter", 
                "date_of_birth":"1980-07-21",
                "school_of_precedence":"Smallville High",
                "athlete_positions":["Base","Escolta"],
                "athlete_categories":{},      
                "number":1,
                "profile_image_link":"https://pbs.twimg.com/media/DUOPKlWU0AEGY0S.jpg:large",
                "sport":"Baloncesto",     
                "branch":"Masculino",

                "years_of_participation":4,
                "athlete_id": 3,
              }
              ],
            }
          } 
          else if(this.season==2022){
            this.current_team ={
                team_id: 3,
                season_year: 2022,
                team_image_link: 'https://scontent-mia3-2.xx.fbcdn.net/v/t1.0-9/89775037_3018436938245120_7244710629703942144_o.jpg?_nc_cat=103&_nc_sid=cdbe9c&_nc_oc=AQm3OioI29F5kvicCjSrascjVapegmU7TrqInUzAdUK_Odqr1yFkNqxgzUcondMhuuo&_nc_ht=scontent-mia3-2.xx&oh=eb53711a5de3d73ace11e40f4f663c11&oe=5EB4540F',
              }
            this.members = {"members":[
              {
                "first_name": "Bruce",
                "middle_name": "Batman",
                "last_names":"Wayne",
                "short_bio":"I am vengeance, I am the night.",
                "height_feet":7,
                "height_inches":0,
              
                "study_program":"Forensics", 
                "date_of_birth":"1980-07-21",
                "school_of_precedence":"Gotham High",
                "athlete_positions":["Base","Escolta"],
                "athlete_categories":{},      
                "number":27,
                "profile_image_link":"https://scontent-mia3-2.xx.fbcdn.net/v/t1.0-9/18056978_1321492691261909_7453541174330533269_n.jpg?_nc_cat=102&_nc_sid=8024bb&_nc_oc=AQmWfwxDy-LTXcZv4K0hcL8VNdr4F0JDlBW90Hq3YG157GtEuXYnB-AKL6hNki0uuh4&_nc_ht=scontent-mia3-2.xx&oh=6dc80a0cb41e6c693897b317148b3753&oe=5EB4AFCF",
                "sport":"Baloncesto",     
                "branch":"Masculino", 

                "years_of_participation":4,
                "athlete_id": 1,
              },
              {
                "first_name": "Richard",
                "middle_name": "Nightwing",
                "last_names":"Grayson",
                "short_bio":"I am vengeance, I am the night.",
                "height_feet":7,
                "height_inches":0,
              
                "study_program":"Police", 
                "date_of_birth":"1980-07-21",
                "school_of_precedence":"Flying Graysons",
                "athlete_positions":["Base","Escolta"],
                "athlete_categories":{},      
                "number":77,
                "profile_image_link":"https://vignette.wikia.nocookie.net/marvel_dc/images/a/a2/Nightwing_0008.jpg/revision/latest?cb=20111009075845",
                "sport":"Baloncesto",     
                "branch":"Masculino",

                "years_of_participation":4,
                "athlete_id": 2,
              },
              ],
            }
          } 
          else if(this.season==2023){
            this.current_team = {
              team_id: 4,
              season_year: 2023,
              team_image_link: 'https://scontent-mia3-2.xx.fbcdn.net/v/t1.0-9/53255400_2150742488347907_5032536115572113408_o.jpg?_nc_cat=110&_nc_sid=cdbe9c&_nc_oc=AQlAZzUmMDbfLqJXSfAOlDAoP7_pyp58sPqPJ1MLE9-JgUtmldcr3NEq3OcNJMZEgt8&_nc_ht=scontent-mia3-2.xx&oh=9ca5fa4bb6ee0bdc1acb52841855cf6f&oe=5EB61445',
            }
            this.members = {"members":[
              {
                "first_name": "Bruce",
                "middle_name": "Batman",
                "last_names":"Wayne",
                "short_bio":"I am vengeance, I am the night.",
                "height_feet":7,
                "height_inches":0,
              
                "study_program":"Forensics", 
                "date_of_birth":"1980-07-21",
                "school_of_precedence":"Gotham High",
                "athlete_positions":["Base","Escolta"],
                "athlete_categories":{},      
                "number":27,
                "profile_image_link":"https://scontent-mia3-2.xx.fbcdn.net/v/t1.0-9/18056978_1321492691261909_7453541174330533269_n.jpg?_nc_cat=102&_nc_sid=8024bb&_nc_oc=AQmWfwxDy-LTXcZv4K0hcL8VNdr4F0JDlBW90Hq3YG157GtEuXYnB-AKL6hNki0uuh4&_nc_ht=scontent-mia3-2.xx&oh=6dc80a0cb41e6c693897b317148b3753&oe=5EB4AFCF",
                "sport":"Baloncesto",     
                "branch":"Masculino", 

                "years_of_participation":4,
                "athlete_id": 1,
              },
              {
                "first_name": "Richard",
                "middle_name": "Nightwing",
                "last_names":"Grayson",
                "short_bio":"I am vengeance, I am the night.",
                "height_feet":7,
                "height_inches":0,
              
                "study_program":"Police", 
                "date_of_birth":"1980-07-21",
                "school_of_precedence":"Flying Graysons",
                "athlete_positions":["Base","Escolta"],
                "athlete_categories":{},      
                "number":77,
                "profile_image_link":"https://vignette.wikia.nocookie.net/marvel_dc/images/a/a2/Nightwing_0008.jpg/revision/latest?cb=20111009075845",
                "sport":"Baloncesto",     
                "branch":"Masculino",

                "years_of_participation":4,
                "athlete_id": 2,
              },
              {
                "first_name": "Clark",
                "middle_name": "Superman",
                "last_names":"Kent",
                "short_bio":"Up, Up, and Away",
                "height_feet":7,
                "height_inches":0,
              
                "study_program":"Reporter", 
                "date_of_birth":"1980-07-21",
                "school_of_precedence":"Smallville High",
                "athlete_positions":["Base","Escolta"],
                "athlete_categories":{},      
                "number":1,
                "profile_image_link":"https://pbs.twimg.com/media/DUOPKlWU0AEGY0S.jpg:large",
                "sport":"Baloncesto",     
                "branch":"Masculino",

                "years_of_participation":4,
                "athlete_id": 3,
              }
              ],
            }
          } 
          
          this.statistics_per_season = {"season":[
            {
            "Event": {
                "athlete_id": 8,
                "basketball_event_id": 2,
                "event_date": "Mon, 30 Mar 2020 00:00:00 GMT",
                "event_id": 3
            },
            "Event_Statistics": {
                "assists": 10,
                "blocks": 1,
                "field_goal_attempt": 120,
                "field_goal_percentage": 100,
                "free_throw_attempt": 0,
                "free_throw_percentage": 0.0,
                "points": 120,
                "rebounds": 0,
                "steals": 0,
                "successful_field_goal": 120,
                "successful_free_throw": 0,
                "successful_three_point": 40,
                "three_point_attempt": 40,
                "three_point_percentage": 100.0,
                "turnovers": 3
            }
            },
            {
            "Event": {
                "athlete_id": 8,
                "basketball_event_id": 6,
                "event_date": "Sat, 14 Mar 2020 00:00:00 GMT",
                "event_id": 4
            },
            "Event_Statistics": {
                "assists": 20,
                "blocks": 3,
                "field_goal_attempt": 12,
                "field_goal_percentage": 50,
                "free_throw_attempt": 36,
                "free_throw_percentage": 55.56,
                "points": 37,
                "rebounds": 21,
                "steals": 15,
                "successful_field_goal": 6,
                "successful_free_throw": 20,
                "successful_three_point": 5,
                "three_point_attempt": 10,
                "three_point_percentage": 50.0,
                "turnovers": 1
            }
            },
            {
            "Event": {
                "athlete_id": 8,
                "basketball_event_id": 17,
                "event_date": "Wed, 01 Apr 2020 00:00:00 GMT",
                "event_id": 5
            },
            "Event_Statistics": {
                "assists": 1,
                "blocks": 1,
                "field_goal_attempt": 1,
                "field_goal_percentage": 100,
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
            },
            {
            "Event": {
                "athlete_id": 8,
                "basketball_event_id": 19,
                "event_date": "Mon, 20 Apr 2020 00:00:00 GMT",
                "event_id": 6
            },
            "Event_Statistics": {
                "assists": 1,
                "blocks": 1,
                "field_goal_attempt": 1,
                "field_goal_percentage": 100,
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
        ]
          } 
				}
			}
		}
		
}
</script>