<template>
  <v-card width="800" class="elevation-12 mx-auto">
    <v-toolbar color="green darken-1" dark flat>
      <v-spacer />
      <v-toolbar-title>Evento</v-toolbar-title>
			<v-progress-linear
				:active="!ready"
				inderterminate
				absolute
				bottom
				color = "blue-grey lighten-1"
			></v-progress-linear>			
      <v-spacer />

    </v-toolbar>
    <v-card-text>       
       
			<v-container v-if="formated()">  
				<v-row>
					<v-img
						
						width="300px"
						height="400px"
						:src="event.sport_img_url"
					></v-img>
				</v-row>
				<v-row>
						<v-col
							cols="1"
							md="3"
						>	

							<h2>Resumen de Evento:</h2>
							
						</v-col>

						<v-col
							cols="12"
							md="9"
						>
						
							<v-textarea
								v-model="event.event_summary"    
								
								label="Resumen"
								rows="2"
								readonly
								outlined
							></v-textarea>
							
						</v-col>
				</v-row>

				<v-row>            
					<v-col
						cols="12"
						md="3"
					>	

					<h2>Fecha del Evento:</h2>						               
					</v-col>

					<v-col
						cols=12
						md=2
					>
						<v-text-field
							v-model="date"
							label="Fecha"								
							readonly
												
						></v-text-field>
					</v-col>             
				</v-row>

				<v-row>
					<v-col
						cols="1"
						md="3"
					>	

					<h2>Localización:</h2>
					
					</v-col>

					<v-col
						cols="12"
						md="3"
					>							
						<v-text-field
							:value="getLocality()"							
							label ="Localización"
							readonly
							
						></v-text-field>						
					</v-col>

					<v-col
						cols="12"
						md="3"
					>						
						<v-text-field
							v-model="event.venue"									                    
							label="Lugar del Evento"
							readonly
							
						></v-text-field>							
					</v-col>
				</v-row>

				<v-row>
					<v-col
						cols="1"
						md="3"
					>	

					<h2>Equipo de UPRM:</h2>
						
					</v-col>

					<v-col
						cols="1"
						md="9"
					>
						<v-text-field
								v-model="team"
								label="Equipo"									
								readonly                
								
						></v-text-field>
					</v-col>
				</v-row>

				<v-row>
					<v-col
						cols="1"
						md="3"
					>	

						<h2>Nombre de Oponente:</h2>
						
					</v-col>

					<v-col
						cols="12"
						md="4"
					>
						<v-text-field
							v-if="event"
							v-model="event.opponent_name"									                  
							label="Oponente"
							readonly
							required
						></v-text-field>
					
					</v-col>
				</v-row>


				<v-row>
					<v-spacer/>
					<v-spacer/>
					<v-col>
						<v-btn color="green darken-1" dark class="mr-4" @click="log">Ver Estadisticas</v-btn>						
					</v-col>
				</v-row>
				
			</v-container>
		
      
    </v-card-text>
  </v-card>
</template>

<script>

import { mapActions, mapGetters } from "vuex"

export default {
	
	data: () => ({
		
		
		team:'',
		locality:'',		
		ready:false,		   
		
	}),



	methods: {     
		...mapActions({
			getEventByID:"events/getEventByID"
		}),

		getSportFullSportName()
		{
			return this.event.sport_name + " " + this.event.branch
		},

		
		log(){
			console.log(this.event)
		},
		getLocality(){
			if(this.event.is_local){

				return 'Casa'
			}
			else
				return 'Afuera'

		},
		formated(){
			if(this.event){
				if(this.ready){
					return true
				}
				else{
					this.date = new Date(Date.parse(this.event.event_date)).toISOString().substr(0,10)
					if(this.event.is_local)
						this.locality = 'Casa'
				
					else
						this.locality = 'Afuera'
					
					this.team = "Deporte: " + this.event.sport_name + '-' + this.event.branch + " Temporada: " + this.event.team_season_year
					
					this.ready = true
				}
			}
			else
			{
				return false
			}

		}
		
		
	},

	computed: {
		...mapGetters({
			 event:"events/event"
		}),
		

	},
	mounted() {
		this.getEventByID(this.$route.params.id);
		
	}
}
</script>