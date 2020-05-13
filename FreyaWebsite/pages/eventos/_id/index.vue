<template>
  <v-card width="800" class="elevation-12 mx-auto">
    <v-toolbar color="green darken-1" dark flat>
      <v-spacer />
      <v-toolbar-title>Evento</v-toolbar-title>
			<v-progress-linear
				:active="!ready"
				indeterminate
				absolute
				bottom
				color = "white"
			></v-progress-linear>	
      <v-spacer></v-spacer>
    </v-toolbar>
    <v-card-text>       
       
			<v-container v-if="formated() && ready && eventExists">  
				<v-row>
					<v-img
						
						width="300px"
						height="400px"
						:src="sport_img_url"
					></v-img>
				</v-row>

				<v-row>            
					<v-col						
						md="12"
					>	
				
					<v-card-text>
							<h2>Fecha del Evento:<wbr> {{date}}</h2>
					</v-card-text>						               
					</v-col>			      
				</v-row>

				<v-row>            
					<v-col						
						md="12"
					>	
				
					<v-card-text>
							<h2>Hora del Evento:<wbr> {{time}}</h2>
					</v-card-text>						               
					</v-col>			      
				</v-row>
				
				<v-row>
					<v-col						
						md="12"
					>	
					<v-card-text >
							<h2>Equipo de UPRM: {{team}}</h2>							
					</v-card-text>					
					</v-col>					
				</v-row>				

				<v-row>
					<v-col					
						md="12"
					>	
						<v-card-text >
							<h2>Localización: {{locality}}</h2>							
						</v-card-text>	
					</v-col>					
				</v-row>
				<v-row>			
					<v-col						
						md="12"
					>						
						<v-card-text >
							<h2>Lugar del Evento: {{venue}}</h2>							
						</v-card-text>								
					</v-col>
				</v-row>
		

				<v-row>
					<v-col						
						md="12"
					>	
						<v-card-text >
							<h2>Nombre de Oponente: {{opponent_name}}</h2>							
						</v-card-text>							
						
					</v-col>				
				</v-row>

				<v-row>
						<v-col						
							md="12"
						>	
							<v-card-text>
								<h2>Resumen de Evento:</h2>
								<p>
								{{event_summary}}
								</p>
							</v-card-text>
						</v-col>
				</v-row>
		

				<v-row>
					<v-spacer/>
					<v-spacer/>
					<v-col>
						<v-btn 
							color="green darken-1" 
							dark 
							class="mr-4" 
							@click="goToEventStatistics()"
						>	
							Ver Estadisticas
						</v-btn>						
					</v-col>
				</v-row>
				
			</v-container>

			<v-container v-if="!eventExists">
				<v-row justify="center">
					<v-col>
						<h1> No existe este evento </h1>
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
		time:'',
		date:'',
		eventExists:true,
		venue:'',
		opponent_name:'',
		sport_img_url:'',
		event_summary:'',		
		
	}),



	methods: {     
		...mapActions({
			getEventByID:"events/getEventByID"
		}),

		/**
		 * Returns a formated sport name used in the viewer card.
		 */
		getSportFullSportName()
		{
			return this.event.sport_name + " " + this.event.branch
		},

		/**
		 * Routes user to the statisticts page, using 
		 * the event id in the route.
		 */
		goToEventStatistics(){
			this.$router.push("/resultados/"+this.event.id)
		},	
		
		/**
		 * Returns a string denoting whether an event is local 
		 * or away.
		 */
		getLocality(){
			if(this.event.is_local){

				return 'Casa'
			}
			else
				return 'Afuera'

		},

		/**
		 * Verifies if the event data has been formated, if not then 
		 * it proceeds to format the event data so that it can be displayed
		 * properly in the card view.
		 */
		async formated(){
		
			if(this.ready){
				return true
			}
			else{
				const response = await this.getEventByID(this.$route.params.id)
				if(response == 'error')
				{
					this.eventExists = false
					this.ready = true
					return true
				}
				
				let eventDate = new Date(Date.parse(this.event.event_date))
				this.date = eventDate.toISOString().substr(0,10)
				let hours = eventDate.getUTCHours()
				let minutes = eventDate.getUTCMinutes()
				
				let amPM = null
				if(hours > 12){
					amPM = 'PM'
					hours -= 12
				}
				else if(hours < 12)
					amPM = 'AM'

				if(minutes < 10)
					this.time = hours + ":0"+minutes + amPM
				else if(minutes >=10)
					this.time = hours + ":" +minutes + amPM				 	
			
				if(this.event.is_local)
					this.locality = 'Casa'
			
				else
					this.locality = 'Afuera'
				
				this.team = this.event.sport_name + '-' + this.event.branch + '-'+ this.event.team_season_year
				this.venue = this.event.venue
				this.opponent_name = this.event.opponent_name
				this.sport_img_url = this.event.sport_img_url
				this.event_summary = this.event.event_summary						
				this.ready = true
				return true
			}
		

		}
		
		
	},

	computed: {
		...mapGetters({
			 event:"events/event"
		}),
		

	},
	
	
}
</script>

<style scoped>
h2{
	font-weight: normal;
	word-break: keep-all;	
}


</style>