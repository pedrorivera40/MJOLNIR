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
       
			<v-container v-if="formated()">  
				<v-row>
					<v-img
						
						width="300px"
						height="400px"
						:src="event.sport_img_url"
					></v-img>
				</v-row>

				<v-row class="text-wrap">            
					<v-col						
						md="12"
					>	
				
					<v-card-text>
							<h2 class="text-wrap">Fecha del Evento:<wbr> {{date}}</h2>
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
							<h2>Localización: {{getLocality()}}</h2>							
						</v-card-text>	
					</v-col>					
				</v-row>
				<v-row>			
					<v-col						
						md="12"
					>						
						<v-card-text >
							<h2>Lugar del Evento: {{event.venue}}</h2>							
						</v-card-text>								
					</v-col>
				</v-row>
		

				<v-row>
					<v-col						
						md="12"
					>	
						<v-card-text >
							<h2>Nombre de Oponente: {{event.opponent_name}}</h2>							
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
								{{event.event_summary}}
								</p>
							</v-card-text>
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
					
					this.team = this.event.sport_name + '-' + this.event.branch + '-'+ this.event.team_season_year
					
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

<style scoped>
h2{
	font-weight: normal;
	word-break: keep-all;	
}


</style>