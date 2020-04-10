<template>
  <v-card width="800" class="elevation-12 mx-auto">
    <v-toolbar color="green darken-1" dark flat>
      <v-spacer />
      <v-toolbar-title>Evento</v-toolbar-title>
      <v-spacer />
    </v-toolbar>
    <v-card-text>       
       
			<v-container>  
				<v-row>
					<v-img
						v-if="sportImg != ''"
					
						height="400px"
						:src="sportImg"
					></v-img>
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
							readonly
							required							
						></v-text-field>
					</v-col>             
				</v-row>

				<v-row>
					<v-col
						cols="1"
						md="3"
					>	

					<h2>Localizacion:</h2>
					
					</v-col>

					<v-col
						cols="12"
						md="3"
					>							
						<v-text-field
							v-model="locality"							
							label ="Localizacion"
							readonly
							required
						></v-text-field>						
					</v-col>

					<v-col
						cols="12"
						md="3"
					>						
						<v-text-field
							v-model="venue"									                    
							label="Lugar del Evento"
							readonly
							required
						></v-text-field>							
					</v-col>
				</v-row>

				<v-row>
					<v-col
						cols="1"
						md="3"
					>	

					<h2>Equipo de Tarzanes:</h2>
						
					</v-col>

					<v-col
						cols="1"
						md="3"
					>
						<v-text-field
								v-model="teamSport"
								label="Deporte"									
								readonly                
								prepend-icon=""
						></v-text-field>
					</v-col>

					<v-col
						cols="1"
						md="3"
					>
						<v-text-field
								v-model="year"                                                           
								label ="A~no del equipo"										
								readonly                                        
								prepend-icon=""
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
							v-model="opponent_name"									                  
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
						<v-btn color="green darken-1" dark class="mr-4">Ver Estadisticas</v-btn>						
					</v-col>
				</v-row>
				
			</v-container>
		
      
    </v-card-text>
  </v-card>
</template>

<script>

 

  export default {
    
    data: () => ({
			
			sportImg:'https://scontent.fsig1-1.fna.fbcdn.net/v/t1.0-9/74883001_2671827106239440_2718595271939325952_o.jpg?_nc_cat=111&_nc_sid=e007fa&_nc_ohc=lqrGrpZippsAX_BafZ8&_nc_ht=scontent.fsig1-1.fna&oh=da934963689fa5b8d79b31a40cd62835&oe=5EA9881E',
			date:'2020-04-18', 
			locality:'Casa',        
			venue:'Mangual',
			teamSport:'Baloncesto-masculino',		
			opponent_name:'Tornados',
			summary:'',
			year:'2020',		   
		
    }),

    created(){
      
      //will call fetch method here
      
    },   
  

    methods: {     

      //need a fecth function for api here
    },
  }
</script>