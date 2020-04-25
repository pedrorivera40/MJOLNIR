<template>
	<v-card>
		<v-toolbar
				color="green darken-1"
				dark
				flat
		>
			<v-spacer />
			<v-toolbar-title> Perfil de Atleta </v-toolbar-title>
			<v-progress-linear
				:active="!ready"
				indeterminate
				absolute
				bottom
				color = "white"
			></v-progress-linear>
			<v-spacer />
		</v-toolbar>
		<v-container v-if="formated()">
			<v-tabs
					centered
			>
				<v-tabs-slider/>
				<v-tab>
						Informacion				
				</v-tab>

				<v-tab>
						Estadisticas por Temporada						
				</v-tab>

				<v-tab-item>
				
						<v-card class="mx-auto" outlined>								
							<v-container>
								<v-row>
									<v-col md=3>
									
										<v-avatar
												class="profile"
												color="grey"
												size="200"																																														
										>
											<v-icon v-if="profile_image_link == ''">mdi-account </v-icon>
											<v-img v-else :src="profile_image_link"></v-img>																											
										</v-avatar> 																					
									</v-col>

									<v-col md=5>
										<h3>{{first_name}} {{middle_name}} {{last_names}} </h3>
										<span class="text"><b>Fecha de Nacimiento:</b> {{date_of_birth}} </span>
										<v-spacer/>	
										<span class="text"><b>Estatura:</b> {{height_feet}}' {{height_inches}}" </span>
										<v-spacer/>	
										<span class="text"><b>Programa de Estudio:</b> {{study_program}} </span>	
										<v-spacer/>
										<span class="text"><b>Año de Estudio:</b> {{years_of_study}}</span>
										<v-spacer/>
										<span class="text"><b>Escuela de Precedencia:</b> {{school_of_precedence}} </span>							
									</v-col>

									<v-col md=4>
										<v-spacer/>
										<span class="text"><b>Deporte:</b> {{sport}}</span>
										<v-spacer/>	
										<span class="text"><b>Rama:</b> {{branch}}</span>
										<v-spacer/>									
										<span class="text"><b>Años de Participación:</b> {{years_of_participation}}</span>
										<v-spacer/>	
										<span class="text"><b>Número:</b> {{number}} </span>										
									</v-col>

									<v-col v-if="athlete_positions !=''" md=3>
											<h4> Posiciones: </h4>										
											<div v-for="position in athlete_positions" v-bind:key="position.id">
												<span class="text">{{position}}</span>
											</div>
									</v-col>

									<v-col v-if="athlete_categories !=''" md=3>
											<h4> 	Categorías: </h4>										
											<div v-for="category in athlete_categories" v-bind:key="category.id">
												<span class="text">{{category}}</span>
											</div>
									</v-col>
								
								</v-row>
								
								<v-row>
									<v-col>
										<h3> Biografia: </h3>
										<p>
											{{short_bio}}
										</p>
									</v-col>
								</v-row>

						
							</v-container>
						</v-card>
						
				</v-tab-item>
				<v-tab-item>
						
						<v-card flat>
							<v-row>
								<v-col md=3>
									<v-select
										v-model="season"
										:items="seasons"
										label ="Temporada"
										prepend-icon="mdi-calendar-blank-multiple"
									
									></v-select>
								</v-col>

								<v-col md=3>
									<v-btn class="mr-4" @click="getSeasonData" color="green darken-1">Confirmar Temporada</v-btn>
								</v-col>
							</v-row>
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
		</v-container>        
			
	</v-card>
</template>

<script>
import { mapActions, mapGetters} from "vuex"


export default {

    data: () =>({    
     
      ready: false,
      first_name: '',
      middle_name: '',
			last_names:'',
			date_of_birth:'',
      short_bio:'',
      height_feet:'',
			height_inches:'',

      study_program:'', 
      date_of_birth:'',
			school_of_precedence:'',
			years_of_participation:'',
			years_of_study:'',
      athlete_positions:'',
      athlete_categories:'',      
      number:'',
      profile_image_link:'',
      sport:'',     
			branch:'', 

			season:'',
			seasons:['2020'],
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
      statistics_per_season:''   
    }),//end of data()
		
		methods: {
			...mapActions({
				getAthleteByID:"athletes/getAthleteByID"
			}),

			formated(){
				if(this.athlete){
					if(this.ready){
						return true
					}
					else{

						if(!this.ready){

							this.first_name = this.athlete.fName
							this.last_names = this.athlete.lName	
							if(this.athlete.mName)
								this.middle_name = this.athlete.mName

							this.sport = this.athlete.sportName
							this.branch = this.athlete.sportBranch.charAt(0).toUpperCase() + this.athlete.sportBranch.slice(1)
							
							if(this.athlete.bio)
								this.short_bio = this.athlete.bio

							if(this.athlete.number)
								this.number = this.athlete.number

							if(this.athlete.height)
							{
								this.height_feet = Math.floor(this.athlete.height/12)
								this.height_inches = this.athlete.height%12
							}

							if(this.athlete.profilePicLink)
								this.profile_image_link = this.athlete.profilePicLink
							

							if(this.athlete.school)
								this.school_of_precedence = this.athlete.school

							if(this.athlete.sProgram)
								this.study_program = this.athlete.sProgram
							
							if(this.athlete.yearOfStudy)
								this.years_of_study = this.athlete.yearOfStudy
							
							if(this.athlete.yearsOfParticipation)
								this.years_of_participation = this.athlete.yearsOfParticipation						
							
							if(this.athlete.dBirth)
								this.date_of_birth= new Date(Date.parse(this.athlete.dBirth)).toISOString().substr(0,10)
							
							if(this.athlete.athlete_positions)
							{
								this.athlete_positions = []
								const entries = Object.entries(this.athlete.athlete_positions)
								for(const [name, value] of entries){
									if(value){
										this.athlete_positions.push(name)
									}
								}
							}
							if(this.athlete.athlete_categories)
							{
								this.athlete_categories = []
								const entries = Object.entries(this.athlete.athlete_categories)
								for(const [name, value] of entries){
									if(value){
										this.athlete_categories.push(name)
									}
								}
							}					
							

							
							this.ready = true
						}
					}
				}
				else
				{
					return false
				}

			},
			

			getSeasonData(){
				if(this.season!=''){
					//This line below will later be modified to fetch data from a file.
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
		},

		computed: {
			...mapGetters({
				athlete:"athletes/athlete"
			})
		},

		mounted(){
			this.getAthleteByID(this.$route.params.id)
		}

		
}
</script>