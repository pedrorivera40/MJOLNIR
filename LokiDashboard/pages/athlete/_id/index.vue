<template>
	<v-card>
		<v-toolbar
				color="green darken-1"
				dark
				flat
		>
			<v-spacer />
			<v-toolbar-title> Perfil de Atleta </v-toolbar-title>
			<v-spacer />
		</v-toolbar>
		<v-container>
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
												<v-img src="https://i.pinimg.com/originals/27/f3/0e/27f30eb66f427ef0d6395f92576a0a7d.png"></v-img>
																												
										</v-avatar> 																					
									</v-col>

									<v-col md=5>
										<h3>{{first_name}} {{middle_name}} {{last_names}} </h3>
										<span class="text"><b>Estatura:</b> {{height_feet}}' {{height_inches}}" </span>
										<v-spacer/>	
										<span class="text"><b>Programa de Estudio:</b> {{study_program}} </span>	
										<v-spacer/>
										<span class="text"><b>Escuela de Precedencia:</b> {{school_of_precedence}} </span>							
										<v-spacer/>
										<span class="text"><b>Numero:</b> {{number}} </span>		 																					
									</v-col>

									<v-col md=4>
										<v-spacer/>
										<span class="text"><b>Deporte:</b> {{sport}}</span>
										<v-spacer/>	
										<span class="text"><b>Rama:</b> {{branch}}</span>
										<v-spacer/>
										<h4> Posiciones: </h4>
											
										<div v-for="position in athlete_positions" v-bind:key="position.id">
											<span class="text">{{position}}</span>
										

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
export default {

    data: () =>({
    
      //NOTE: Using pre-written data for athlete with id:8,
      //      will need to fetch this data below from the API.
      
      first_name: 'Bruce',
      middle_name: 'Batman',
      last_names:'Wayne',
      short_bio:'I am vengeance, I am the night.',
      height_feet:7,
			height_inches:0,
		
      study_program:'Forensics', 
      date_of_birth:'1980-07-21',
      school_of_precedence:'Gotham High',
      athlete_positions:["Base","Escolta"],
      athlete_categories:{},      
      number:27,
      profile_image_link:'https://i.pinimg.com/originals/27/f3/0e/27f30eb66f427ef0d6395f92576a0a7d.png',
      sport:'Baloncesto',     
			branch:'Masculino', 

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
		}
		
}
</script>