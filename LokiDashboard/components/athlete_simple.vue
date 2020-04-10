<template>
    <v-card class="mx-auto" outlined @click="goToAthlete">								
        <v-container>
            <v-row>
                <v-col md=3>
                
                    <v-avatar
                            class="profile"
                            color="grey"
                            size="200"
                                                                        
                                                                                                                                                                        
                    >       
                            <v-img :src="profile_image_link"></v-img>
                                                                                            
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
</template>
<script>
export default {

   props:{
    
      //NOTE: Using pre-written data for athlete with id:8,
      //      will need to fetch this data below from the API.
      athlete_id: String,
      first_name: String,
      middle_name: String,
      last_names:String,
      short_bio:String,
      height_feet:String,
	  height_inches:String,
      study_program:String,
      date_of_birth:String,
      school_of_precedence:String,
      athlete_positions:[String],
      athlete_categories:[String],      
      number:String,
      profile_image_link:String,
      sport:String,    
	  branch:String, 
    },//end of data()
    methods:{
        goToAthlete(){
            this.$router.push('/athlete/'+this.athlete_id)
        }
    }
}
</script>