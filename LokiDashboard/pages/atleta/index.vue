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
                :return-value.sync="date"
                transition="scale-transition"
                offset-y
                min-width="290px"
              >
              
                <template v-slot:activator="{ on }">
                  <v-text-field
                    v-model="date"
                    label="Fecha de nacimiento"
                    prepend-icon="mdi-calendar"
                    readonly
                    v-on="on"
                  ></v-text-field>
                </template>
                <v-date-picker v-model="date" color = "green darken-1" no-title scrollable locale="es-419">
                  <v-spacer></v-spacer>
                  <v-btn text color="primary" @click="menu = false">Cancel</v-btn>
                  <v-btn text color="primary" @click="$refs.menu.save(date)">OK</v-btn>
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
                v-model="year_of_study"
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
              md="4"               
            >              
              <v-select
                v-model="sport"
                :items="sportsList"               
                label ="Deporte"
                item-text="sportName"
                item-value="id"
                prepend-icon="mdi-volleyball"
                v-on:change="setCategoriesAndPositions()"
                :rules="[teamRequired('Deporte')]"
              ></v-select>              
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
                <h2 v-if="!isEmpty(sport_positions)">
                  
                  Posiciones:

                </h2>
              </div>

              <div>                  
                <h2 v-if="!isEmpty(sport_categories)">
                  
                  Categorías:

                </h2>
              </div>

            </v-col>

            <v-col
              cols="12" 
              md="4"               
            > 
            
              <div v-for="(value,key) in sport_positions" :key="key" >
                <v-checkbox
                  :input-value="value"
                  :label="key"                    
                  v-on:change="updatePositons(key,value)"
                  v-if="!isEmpty(sport_positions)"                                        
                ></v-checkbox>
              </div>
            
              
              <div v-for="(value,key) in sport_categories" :key="key">
                <v-checkbox
                  :input-value="value"
                  :label="key"
                  v-on:change="updateCategories(key,value)"
                  v-if="!isEmpty(sport_categories)"                      
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
  import rules from "../../utils/validations"
  import sportsData from "../../data/athletePagesData/sports.json"


  export default {
    
    data: () => ({
      
      valid:false,
      ready:false,
      selected_categories:[],
      date:'',
      menu: false,
      first_name: '',
      middle_name: '',
      last_names:'',
      short_bio:'',
      height_feet:'',
      height_inches:'',
      study_program:'', 
      date_of_birth:'',
      school_of_precedence:'',
      athlete_position:'',
      year_of_study:'',
      years_of_participation:'',
      sport_positions:{},
      sport_categories:{},
      number:'',
      profile_image_link:'',
      sport_id:0,
      sport:'',      
      sportsList:[],
      sports:sportsData.Sports,
      sportHasNumber:false,
      branch:'',
      branches:['Masculino','Femenino','Otro'],
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

      submit () {

        console.log(this.sports)
        
      },
      clear () {
        
        this.first_name= '',
        this.middle_name= '',
        this.last_names='',
        this.short_bio='',
        this.height_feet='',
        this.height_inches='',
        this.study_program='', 
        this.date_of_birth='',
        this.school_of_precedence='',        
        this.number='',
        this.profile_image_link='',
        this.sportHasNumber=false         
        this.sport ='' 
        this.years_of_participation = ''
        this.sport_positions = {}
        this.sport_categories = {} 
        this.resetDate()
        
      },

      updatePositons(key,value){
        
        this.sport_positions[key]=!value       
      },
      updateCategories(key,value){
        
        this.sport_categories[key]=!value       
      },


      

      formated(){
        if(this.sports){
          if(this.ready){ return true }
          
          else{
            
            this.resetDate()
            
            for(let i = 0; i < this.sports.length; i++){
              let sportObj = this.sports[i]
              this.sportsList.push({'id':sportObj['sport_id'],'sportName':sportObj['sport_name']+'-'+sportObj['branch_name']})              
            }
            this.ready = true            
          }
        }
        else
          return false
      },

      setCategoriesAndPositions(){
        this.sport_positions = {}
        this.sport_categories = {}
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
        let sportsWithNumbers = [BALONCESTO_M]
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
  }
</script>