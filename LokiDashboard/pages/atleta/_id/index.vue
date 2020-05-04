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
									<v-autocomplete
										v-model="season"
										:items="seasons"
										label ="Temporada"								
									></v-autocomplete>
								</v-col>

								<v-col md=3>
									<v-btn class="mr-4" @click="getSeasonData" color="green darken-1">Confirmar Temporada</v-btn>
								</v-col>
							</v-row>

					
							<v-row>
								<v-col>
									<v-data-table 
										dense 
										:headers="headers_" 
										:items="aggregate_statistics_per_season" 										
										class="elevation-1"
										loading="fetchinAthleteStats"
										:disable-pagination=true		
										:hide-default-footer=true													
										loading-text="Recolectando Data...Por favor espere"
										v-if="aggregate_statistics_per_season != '' & aggregate_statistics_per_season != ''"
									>		
									</v-data-table>
								</v-col>
							</v-row>


							<v-row>
								<v-col>
									<v-data-table 
										dense 
										:headers="headers" 
										:items="statistics_per_season"										 
										class="elevation-1"
										loading="fetchinAthleteStats"																
										loading-text="Recolectando Data...Por favor espere"
										v-if="statistics_per_season != ''"
									>		
									</v-data-table>
								</v-col>
							</v-row>

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
			fetchingAthleteStats:false,

			season:'',
			seasons:[],
			headers:'',
			headers_:'',
			statistics_per_season:'',
			aggregate_statistics_per_season:''
    }),//end of data()
		
		methods: {
			...mapActions({
				getAthleteByID:"athletes/getAthleteByID",
				getAthleteSeasonStats:"athletes/getAthleteSeasonStats",
				getAthleteAggregateSeasonStats:"athletes/getAthleteAggregateSeasonStats"
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
									if(!value){
										this.athlete_positions.push(name)
									}
								}
							}
							if(this.athlete.athlete_categories)
							{
								this.athlete_categories = []
								const entries = Object.entries(this.athlete.athlete_categories)
								for(const [name, value] of entries){
									if(!value){
										this.athlete_categories.push(name)
									}
								}
							}	
							
							this.buildSeasonList()
							this.ready = true
						}
					}
				}
				else
				{
					return false
				}

			},

			
			buildSeasonList(){
        let yearToAdd = 2020
        let currentYear = new Date(2025,8).getFullYear()
        
        
        while(yearToAdd <= currentYear)
        {
            this.seasons.push(yearToAdd++)
        }
      },
		

			formatedDate(event_date){
				
				const date = new Date(event_date).toISOString().substring(0,10)

				return date

			},
			

			async getSeasonData(){
				
				if(this.season !='')
				{
					this.fetchingAthleteStats = true
					let sport_name = ''
					
					if(this.sport.localeCompare("Baloncesto") == 0){
						sport_name = "basketball"
					}
					else if(this.sport.localeCompare("Voleibol") == 0){
						sport_name = "volleyball"
					}
					else if(this.sport.localeCompare("Beisbol") == 0 || this.sport.localeCompare("Softbol") == 0){
						sport_name = "baseball"
					}
					else if(this.sport.localeCompare("Fútbol") == 0){
						sport_name = "soccer"
					}
					

					const stats_params = {'sport_name':sport_name,'athlete_id':this.athlete.id,'season_year':this.season}
					
					const response_1 = await this.getAthleteSeasonStats(stats_params)
					const response_2 = await this.getAthleteAggregateSeasonStats(stats_params)

 					if(response_1 !== 'error' && response_2 !== 'error'){	
						this.statistics_per_season = []
						this.aggregate_statistics_per_season = []
						if(sport_name.localeCompare("basketball") == 0){
							for(let i = 0; i < this.athlete_stats_per_season.Basketball_Event_Season_Athlete_Statistics.length; i++){
								const statsObj =  this.athlete_stats_per_season.Basketball_Event_Season_Athlete_Statistics[i]
								this.statistics_per_season.push(statsObj)
								this.statistics_per_season[i].Event['event_date'] = this.formatedDate(statsObj.Event["event_date"])

							}
							this.aggregate_statistics_per_season.push(this.athlete_aggregate_stats_per_season.Basketball_Event_Season_Athlete_Statistics)
							this.buildHeadersList(sport_name)
						}

						else if(sport_name.localeCompare("baseball") == 0){
							for(let i = 0; i < this.athlete_stats_per_season.Baseball_Event_Season_Athlete_Statistics.length; i++){
								const statsObj =  this.athlete_stats_per_season.Baseball_Event_Season_Athlete_Statistics[i]
								this.statistics_per_season.push(statsObj)
								this.statistics_per_season[i].Event['event_date'] = this.formatedDate(statsObj.Event["event_date"])

							}
							this.aggregate_statistics_per_season.push(this.athlete_aggregate_stats_per_season.Baseball_Event_Season_Athlete_Statistics)
							this.buildHeadersList(sport_name)
						}
						else if(sport_name.localeCompare("volleyball") == 0){
							for(let i = 0; i < this.athlete_stats_per_season.Volleyball_Event_Season_Athlete_Statistics.length; i++){
								const statsObj =  this.athlete_stats_per_season.Volleyball_Event_Season_Athlete_Statistics[i]
								this.statistics_per_season.push(statsObj)
								this.statistics_per_season[i].Event['event_date'] = this.formatedDate(statsObj.Event["event_date"])

							}
							this.aggregate_statistics_per_season.push(this.athlete_aggregate_stats_per_season.Volleyball_Event_Season_Athlete_Statistics)
							this.buildHeadersList(sport_name)
						}
						else if(sport_name.localeCompare("soccer") == 0){
							for(let i = 0; i < this.athlete_stats_per_season.Soccer_Event_Season_Athlete_Statistics.length; i++){
								const statsObj =  this.athlete_stats_per_season.Soccer_Event_Season_Athlete_Statistics[i]
								this.statistics_per_season.push(statsObj)
								this.statistics_per_season[i].Event['event_date'] = this.formatedDate(statsObj.Event["event_date"])

							}
							this.aggregate_statistics_per_season.push(this.athlete_aggregate_stats_per_season.Soccer_Event_Season_Athlete_Statistics)
							this.buildHeadersList(sport_name)
						}

						this.fetchingAthleteStats = false
					}

				}
				
			},

			buildHeadersList(sport_name){
				if(sport_name.localeCompare("basketball") == 0){
					this.headers =	[
							{
								text:'Event Date',
								align: 'start',
								sortable: true,
								value:'Event.event_date'
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

					]
					this.headers_ = [
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
				else if(sport_name.localeCompare("volleyball") == 0){
					this.headers =	[
						{
							text:'Event Date',
							align: 'start',
							sortable: true,
							value:'Event.event_date'
						},
						{text: 'Kill Points', value: 'Event_Statistics.kill_points'},
						{text: 'Attack Errors', value: 'Event_Statistics.attack_errors'},
						{text: 'Assists', value: 'Event_Statistics.assists'},
						{text: 'Aces', value: 'Event_Statistics.aces'},
						{text: 'Service Errors', value: 'Event_Statistics.service_errors'},
						{text: 'Digs', value: 'Event_Statistics.digs'},
						{text: 'Blocks', value: 'Event_Statistics.blocks'},
						{text: 'Blocking Errors', value: 'Event_Statistics.blocking_errors'},
						{text: 'Reception Errors', value: 'Event_Statistics.reception_errors'}
							

					]
					this.headers_ = [
						{text: 'Kill Points', value: 'Event_Statistics.kill_points'},
						{text: 'Attack Errors', value: 'Event_Statistics.attack_errors'},
						{text: 'Assists', value: 'Event_Statistics.assists'},
						{text: 'Aces', value: 'Event_Statistics.aces'},
						{text: 'Service Errors', value: 'Event_Statistics.service_errors'},
						{text: 'Digs', value: 'Event_Statistics.digs'},
						{text: 'Blocks', value: 'Event_Statistics.blocks'},
						{text: 'Blocking Errors', value: 'Event_Statistics.blocking_errors'},
						{text: 'Reception Errors', value: 'Event_Statistics.reception_errors'}
						
					]
				}
				else if(sport_name.localeCompare("soccer") == 0){
					this.headers =	[
						{
							text:'Event Date',
							align: 'start',
							sortable: true,
							value:'Event.event_date'
						},
						{text: 'Goal Attempts', value: 'Event_Statistics.goal_attempts'},
						{text: 'Assists', value: 'Event_Statistics.assists'},
						{text: 'Fouls', value: 'Event_Statistics.fouls'},
						{text: 'Cards', value: 'Event_Statistics.cards'},
						{text: 'Successful Goals', value: 'Event_Statistics.successful_goals'},
						{text: 'Tackles', value: 'Event_Statistics.tackles'}
							

					]
					this.headers_ = [
						{text: 'Goal Attempts', value: 'Event_Statistics.goal_attempts'},
						{text: 'Assists', value: 'Event_Statistics.assists'},
						{text: 'Fouls', value: 'Event_Statistics.fouls'},
						{text: 'Cards', value: 'Event_Statistics.cards'},
						{text: 'Successful Goals', value: 'Event_Statistics.successful_goals'},
						{text: 'Tackles', value: 'Event_Statistics.tackles'}
						
					]
				}
				else if(sport_name.localeCompare("baseball") == 0){
					this.headers =	[
						{
							text:'Event Date',
							align: 'start',
							sortable: true,
							value:'Event.event_date'
						},
						{text: 'At Bats', value: 'Event_Statistics.at_bats'},
						{text: 'Runs', value: 'Event_Statistics.runs'},
						{text: 'Hits', value: 'Event_Statistics.hits'},
						{text: 'Runs Batted In', value: 'Event_Statistics.runs_batted_in'},
						{text: 'Base On Balls', value: 'Event_Statistics.base_on_balls'},
						{text: 'Strikeouts', value: 'Event_Statistics.strikeouts'},
						{text: 'Left On Base', value: 'Event_Statistics.left_on_base'}
							

					]
					this.headers_ = [
						{text: 'At Bats', value: 'Event_Statistics.at_bats'},
						{text: 'Runs', value: 'Event_Statistics.runs'},
						{text: 'Hits', value: 'Event_Statistics.hits'},
						{text: 'Runs Batted In', value: 'Event_Statistics.runs_batted_in'},
						{text: 'Base On Balls', value: 'Event_Statistics.base_on_balls'},
						{text: 'Strikeouts', value: 'Event_Statistics.strikeouts'},
						{text: 'Left On Base', value: 'Event_Statistics.left_on_base'}					
					]
				}
				
			}
		},

		computed: {
			...mapGetters({
				athlete:"athletes/athlete",
				athlete_stats_per_season:"athletes/athlete_stats_per_season",
				athlete_aggregate_stats_per_season:"athletes/athlete_aggregate_stats_per_season"
			})
		},

		mounted(){
			this.getAthleteByID(this.$route.params.id)
		}

		
}
</script>