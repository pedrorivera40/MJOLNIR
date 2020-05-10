<template>
    <v-card class="mx-auto" outlined @click="goToAthlete">								
        <v-container>
            <v-row>
                <v-col md=3 align="center" justify="center">
                
                    <v-avatar
                            class="profile"
                            color="grey"
                            size="150"                                                                                                                                                                                    
                    >       
                            <v-icon v-if="((profile_image_link == null)||(profile_image_link == ''))" height="100"> mdi-account </v-icon>
                            <v-img v-else :src="profile_image_link"/>
                                                                                            
                    </v-avatar> 																					
                </v-col>
                <v-col md =9>
                    <h2>{{first_name}} {{middle_name}} {{last_names}} </h2>
                    <v-row>
                        <v-col md=5>
                            <span class="text"><b>Estatura:</b>{{height_inches}}" </span>
                            <v-spacer/>	
                            <span class="text"><b>Programa de Estudio:</b> {{study_program}} </span>	
                            <v-spacer/>
                            <span class="text"><b>Escuela de Precedencia:</b> {{school_of_precedence}} </span>							
                            <v-spacer/>
                            <span class="text"><b>Año de Elegibilidad (LAI):</b> {{years_of_participation}} </span>		 																					
                        </v-col>

                        <v-col md=4>
                            <v-spacer/>
                            <span class="text"><b>Numero:</b> {{number}}</span>
                            <v-spacer/>
                            <h4> Posiciones: </h4>
                                
                            <div v-for="position in athlete_positions" v-bind:key="position.id">
                                <span class="text">{{position}}</span>
                            

                            </div>

                        </v-col>
                    </v-row>
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
      athlete_id: Number,
      first_name: String,
      middle_name: String,
      last_names:String,
	  height_inches:Number,
      study_program:String,
      school_of_precedence:String,
      athlete_positions:[String],
      athlete_categories:[String],      
      number:Number,
      profile_image_link:String,
      years_of_participation:String,
    },//end of data()
    methods:{
        goToAthlete(){
            this.$router.push('/atletas/'+this.athlete_id)
        }
    }
}
</script>