<template>
  <v-card width="800" class="elevation-12 mx-auto">
    <v-toolbar color="green darken-1" dark flat>
      <v-spacer/>
      <v-toolbar-title>Atleta</v-toolbar-title>
      <v-progress-linear
				:active="!ready"
				indeterminate
				absolute
				bottom
				color = "white"
			></v-progress-linear>	
      <v-spacer />
    </v-toolbar>
    <v-card-text>           
      
      <v-form v-model="valid">
        <v-container v-if="formated()">
          <v-row>
            <v-col
              cols="12"
              md="2"
            >             
              <v-text-field
                v-model="first_name"          
                
                :counter="20"
                label="Nombre"
                required
                :rules="[required('Nombre'),nameFormat('Nombre'),maxLength('Nombre',20)]"
              ></v-text-field>              
            </v-col>

            <v-col
              cols="12"
              md="3"
            >
              <v-text-field
                v-model="middle_name"                
                :counter="20"
                label="Segundo Nombre"
                required
                :rules="[nameFormat('Segundo Nombre'),maxSummaryLength('Segundo Nombre',20)]"
              ></v-text-field>              
            </v-col>

            <v-col
              cols="12"
              md="4"
            >              
              <v-text-field
                v-model="last_names"
                :counter="40"                
                label="Apellidos"
                required
                :rules="[required('Apellidos'),nameFormat('Apellidos'),maxLength('Apellidos',40)]"
              ></v-text-field>              
            </v-col>
            
              <v-col cols="12" sm="6" md="3">
              <v-menu
                ref="menu"
                v-model="menu"
                :close-on-content-click="false"
                :return-value.sync="date_of_birth"
                transition="scale-transition"
                offset-y
                min-width="290px"
              >
              
                <template v-slot:activator="{ on }">
                  <v-text-field
                    v-model="date_of_birth"
                    label="Fecha de nacimiento"
                    prepend-icon="mdi-calendar"
                    readonly
                    v-on="on"
                  ></v-text-field>
                </template>
                <v-date-picker v-model="date_of_birth" color = "green darken-1" no-title scrollable locale="es-419">
                  <v-spacer></v-spacer>
                  <v-btn text color="primary" @click="menu = false">Cancel</v-btn>
                  <v-btn text color="primary" @click="$refs.menu.save(date_of_birth)">OK</v-btn>
                </v-date-picker>
              </v-menu>
            </v-col>  
          </v-row>
          
          <v-row>
            <v-col>
              <v-textarea
                v-model="short_bio"                      
                :counter="1000"                
                label="Biografía"
                auto-grow
                rows = "3"
                outlined
                :rules="[generalPhrase('Biografía'),maxSummaryLength('Biografía',1000)]"
              ></v-textarea>
            </v-col>
          </v-row>

          <v-row>
            <v-col
              cols="1"
              md="3"
            >

            <h2>Estatura:</h2>
              
            </v-col>

            <v-col
              cols="12"
              md="4"
            >
              <v-select
                v-model="height_feet"
                :items="feet"
                label ="Pies"
                prepend-icon="mdi-human-male-height"
              ></v-select>
                <v-select
                v-model="height_inches"
                :items="inches"
                label ="Pulgadas"
                prepend-icon="mdi-human-male-height"
              ></v-select>
            </v-col>
          </v-row>

          <v-row>

            <v-col
              cols="1"
              md="3"
            >

            <h2>Educación:</h2>
              
            </v-col>

            <v-col
            cols="12"
            md="4"
            >              
              <v-text-field
                v-model="study_program"                                   
                label="Programa de Estudio"
                prepend-icon="mdi-school"
                :rules="[alphaSpaces('Programa de Estudio')]"
              ></v-text-field>
              
            </v-col>
            
            <v-col
              cols="12" 
              md="4"               
            >  
              <v-select
                v-model="years_of_study"
                :items="yearsOfStudy"              
                label ="Año de Estudio"                
              ></v-select>
            </v-col>      
            
            <v-col
              cols="12"
              md="3"
            >
            </v-col>
            <v-col
            cols="12"
            md="4"
            >             
              <v-text-field
                v-model="school_of_precedence"                                  
                label="Escuela de Precedencia"
                prepend-icon="mdi-school-outline"
                :rules="[alphaSpaces('Programa de Estudio')]"
              ></v-text-field>            
            </v-col>
            
          </v-row>

          <v-row> 
            
            <v-col
              cols="1"
              md="3"
            >

            <h2>Deporte:</h2>
              
            </v-col>
          
            <v-col
              cols="12"
              md=5
            >
            <v-text-field
              v-model="sport"
              readonly
              disabled
            ></v-text-field>
            
            </v-col>

           

            <v-col
              cols="12" 
              md="4"               
            >  
              <v-select
                v-model="years_of_participation"
                :items="yearsOfParticipation"              
                label ="Años de Participación"                
              ></v-select>
            </v-col>              
          </v-row>

          <v-row>
            <v-col
              cols="12" 
              md="4"               
            >              
              <div>                  
                <h2 v-if="!isEmpty(athlete_positions)">
                  
                  Posiciones:

                </h2>
              </div>

              <div>                  
                <h2 v-if="!isEmpty(athlete_categories)">
                  
                  Categorías:

                </h2>
              </div>

            </v-col>

            <v-col
              cols="12" 
              md="4"               
            > 
            
              <div v-for="(value,key) in athlete_positions" :key="key" >
                <v-checkbox
                  :input-value="value"
                  :label="key"                    
                  v-on:change="updatePositons(key,value)"
                  v-if="!isEmpty(athlete_positions)"                                        
                ></v-checkbox>
              </div>
            
              
              <div v-for="(value,key) in athlete_categories" :key="key">
                
                <v-checkbox
                  :input-value="value"
                  :label="key"
                  v-on:change="updateCategories(key,value)"
                  v-if="!isEmpty(athlete_categories)"                      
                ></v-checkbox>
              </div>

            </v-col>                   
          </v-row>  

          <v-row> 

            <v-col
              cols="12" 
              md="4"               
            >              
              <div>                  
                <h2 v-if="sportHasNumber">
                  
                  Número del Atleta:

                </h2>
              </div> 
            </v-col>

            <v-col
              cols="12" 
              md="4"               
            >
              <v-select
                v-model="number"
                :items="numbers"
                label ="Número del Athleta"
                prepend-icon="mdi-numeric-0-box"
                v-if="sportHasNumber"
              ></v-select>

            </v-col>
          </v-row>            

          <v-row>

            <v-col
              cols="1"
              md="3"
            >

            <h2>Imagen de Perfil:</h2>
              
            </v-col>


            <v-col
            cols="12"
            md="5"
            >             
              <v-text-field
                v-model="profile_image_link"                                
                label="Enlace de Imagen de Perfil"
                prepend-icon="mdi-link"
                required
              ></v-text-field>              
            </v-col>

          </v-row>


          <v-row>
            <v-spacer/>
            <v-spacer/>
            <v-col>
              <v-btn :disabled="!valid" class="mr-4" color="green darken-1" @click="submit">Someter</v-btn>
              <v-btn @click="clear">Borrar</v-btn>
            </v-col>
          </v-row>
          
        </v-container>
      </v-form>      
    </v-card-text>
  </v-card>
</template>

<script>
  import rules from "../../../../utils/validations"
  import { mapActions, mapGetters} from "vuex"
  


  export default {
    
    data: () => ({
      
      valid:false,
      ready:false,
      selected_categories:[],
      
      menu: false,
      first_name: '',
      middle_name: null,
			last_names:'',
			date_of_birth:'',
      short_bio:'',
      height_feet:Number,
			height_inches:Number,
      study_program:'', 
      date_of_birth:'',
			school_of_precedence:'',
			years_of_participation:'',
			years_of_study:'',
      athlete_positions:{},
      athlete_categories:{},      
      number:Number,
      profile_image_link:'',
      sport:'',     
			branch:'',
      sport_id:0,
      sport:'',            
      branch:'',
      sportHasNumber:false,
      feet: [4,5,6,7],      
      inches:[0.0,0.5,1.0,1.5,2.0,2.5,3.0,3.5,4.0,4.5,5.0,5.5,6.0,6.5,7.0,7.5,8.0,8.5,9.0,9.5,10.0,10.5,11.0,11.5,12.0],
      yearsOfStudy:[1,2,3,4,5,6,7,8,9,10],
      yearsOfParticipation:[1,2,3,4],
      numbers:[0,1,2,3,4,5,6,7,8,9,10,11,12,
              13,14,15,16,17,18,19,20,21,22,
              23,24,25,26,27,28,29,30,31,32,
              33,34,35,36,37,38,39,40,41,42,
              43,44,45,46,47,48,49,50,51,52,
              53,54,55,56,57,58,59,60,61,62,
              63,64,65,66,67,68,69,70,71,72,
              73,74,75,76,77,78,79,80,81,82,
              83,84,85,86,87,88,89,90,91,92,
              93,94,95,96,97,98,99],
         
      
      
    }),
           
      
      
    
  

    methods: {
      ...rules,

      ...mapActions({
				getAthleteByID:"athletes/getAthleteByID"
			}),

      submit () {

        let athlete_attributes = {}
        athlete_attributes['first_name'] = this.first_name
        athlete_attributes['middle_name']  = this.middle_name
        athlete_attributes['last_names'] = this.last_names
        athlete_attributes['short_bio'] = this.short_bio
        
        if(this.height_feet != NaN & this.height_inches != NaN)
          athlete_attributes['height'] = this.height_feet*12.0 + this.height_inches*1.0
        else
          athlete_attributes['height'] = null

        athlete_attributes['study_program'] = this.study_program
        athlete_attributes['date_of_birth'] = this.date
        athlete_attributes['school_of_precedence'] = this.school_of_precedence
        
        if(this.number != NaN) 
          athlete_attributes['number'] = this.number
        else
          athlete_attributes['number'] = null
        
        athlete_attributes['profile_image_link'] = this.profile_image_link

        athlete_attributes['sport_id'] = this.sport

        if(this.year_of_study != '')
          athlete_attributes['year_of_study'] = this.year_of_study
        else
          athlete_attributes['year_of_study'] = null
        
        if(this.years_of_participation != '') 
          athlete_attributes['years_of_participation'] = this.years_of_participation

        athlete_attributes['positions'] = this.sport_positions

        athlete_attributes['categories'] = this.sport_categories

        console.log("Editing the athlete with id:" + this.athlete.id + " with the following information:")
        console.log(athlete_attributes)

        this.$router.push('/atletas/')

        
        
      },
      clear () {
        
        	this.first_name = this.athlete.fName
							this.last_names = this.athlete.lName	
							if(this.athlete.mName)
								this.middle_name = this.athlete.mName

							this.sport = this.athlete.sportName + '-' + this.athlete.sportBranch.charAt(0).toUpperCase() + this.athlete.sportBranch.slice(1)
							
							
							if(this.athlete.bio)
								this.short_bio = this.athlete.bio

							if(this.athlete.number){
                this.number = this.athlete.number
                this.sportHasNumber = true
              }

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
								this.athlete_positions={}
								const entries = Object.entries(this.athlete.athlete_positions)
								for(const [name, value] of entries){
									
										this.athlete_positions[name] = value
									
								}
							}
							if(this.athlete.athlete_categories)
							{
                this.athlete_categories={}
                
								const entries = Object.entries(this.athlete.athlete_categories)
								for(const [name, value] of entries){
									
										this.athlete_categories[name]=value
									
                }
                
							}					
        
       console.log(this.athlete_positions)
       console.log(this.athlete_categories)
      },

      updatePositons(key,value){
        
        this.athlete_positions[key]=!value       
      },
      updateCategories(key,value){
        
        this.athlete_categories[key]=!value       
      },


      

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

							this.sport = this.athlete.sportName + '-' + this.athlete.sportBranch.charAt(0).toUpperCase() + this.athlete.sportBranch.slice(1)
							
							
							if(this.athlete.bio)
								this.short_bio = this.athlete.bio

							if(this.athlete.number){
                this.number = this.athlete.number
                this.sportHasNumber = true
              }

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
								
								const entries = Object.entries(this.athlete.athlete_positions)
								for(const [name, value] of entries){
									
										this.athlete_positions[name] = value
									
								}
							}
							if(this.athlete.athlete_categories)
							{
                
               
								const entries = Object.entries(this.athlete.athlete_categories)
								for(const [name, value] of entries){
									
										this.athlete_categories[name]=value
									
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

      setCategoriesAndPositions(){
        
        for(let i = 0; i < this.sports.length; i++){
            let sportObj = this.sports[i]
            if(this.sport == sportObj['sport_id']){
              let positions = sportObj['positions']
              if(positions.length > 0){
                for(let j = 0; j < positions.length; j++){
                  this.sport_positions[positions[j]]=false;                   
                }
              }
              let categories = sportObj['categories']
              if(categories.length > 0){
                for(let k = 0; k < categories.length; k++){
                  this.sport_categories[categories[k]]=false;                   
                }
              }
            }
        }
        this.sportNumber()
        console.log(this.sport)
        
      },

      isEmpty(obj){
        for(let key in obj){
          if(obj.hasOwnProperty(key))
            return false
        }
        return true
      },

      sportNumber(){
        const BALONCESTO_M = 1 
        const BALONCESTO_F = 10
        const SOFTBOL = 16        
        const BEISBOL = 4
        const VOLEIBOL_M = 2
        const VOLEIBOL_F = 12
        const FUTBOL_M = 3
        const FUTBOL_F = 11
        let sportsWithNumbers = [BALONCESTO_M,BALONCESTO_F,SOFTBOL,BEISBOL,VOLEIBOL_M,VOLEIBOL_F,
                                 FUTBOL_M,FUTBOL_F]
        if(this.sport != '')
        {
          for(let i = 0; i < sportsWithNumbers.length; i++){
            if(this.sport == sportsWithNumbers[i]){
              this.sportHasNumber = true
              return;
            }
          }
          this.sportHasNumber = false
        }

      },

      resetDate(){
        let time_zone_offset = new Date().getTimezoneOffset() * 60000      
        this.date = new Date(Date.now() - time_zone_offset).toISOString().substring(0,10)
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