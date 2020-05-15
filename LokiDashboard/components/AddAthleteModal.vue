<template>
  <v-row justify="center">
    <v-dialog v-model=dialog persistent max-width="600">
      <v-card >
        <v-toolbar color="primary_dark" flat>
          <v-spacer/>
          <v-toolbar-title class="headline white--text">Atleta</v-toolbar-title>
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
          
          <v-form v-model="valid" ref="form">
            <v-container v-if="formated()">
              <v-row justify="start">
              <v-col              
                  md="3"
              >

                <h2>Nombre:</h2>
                  
              </v-col>
              </v-row>
              <v-row justify="start">
                <v-col        
                  md="6"
                >             
                  <v-text-field
                    v-model.lazy="first_name"          
                    
                    :counter="20"
                    label="Primer Nombre*"              
                    :rules="[required('Primer Nombre'),nameFormat('Primer Nombre'),maxLength('Nombre',20)]"
                  ></v-text-field>              
                </v-col>
              </v-row>

              <v-row justify="start">
                <v-col              
                  md="6"
                >
                  <v-text-field
                    v-model="middle_name"                
                    :counter="20"
                    label="Segundo Nombre"                    
                    :rules="[nameFormat('Segundo Nombre'),maxSummaryLength('Segundo Nombre',20)]"
                  ></v-text-field>              
                </v-col>
              </v-row>

              <v-row justify="start">
                <v-col              
                  md="9"    
                >              
                  <v-text-field
                    v-model="last_names"
                    :counter="40"                
                    label="Apellidos*"
                    required
                    :rules="[required('Apellidos'),nameFormat('Apellidos'),maxLength('Apellidos',40)]"
                  ></v-text-field>              
                </v-col>
              </v-row>

              <v-row justify="start">
              <v-col>        

                <h2>Fecha de Nacimiento:</h2>
                  
              </v-col>
              </v-row>
              <v-row justify="center" >
                  <v-col sm="6"  md="4">
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
                        label="Fecha"                        
                        readonly
                        v-on="on"
                      ></v-text-field>
                    </template>
                    <v-date-picker v-model="date" color = "green darken-1" no-title scrollable locale="es-419">
                      <v-spacer></v-spacer>
                      <v-btn text color="primary" @click="menu = false">Cancelar</v-btn>
                      <v-btn text color="primary" @click="$refs.menu.save(date)">OK</v-btn>
                    </v-date-picker>
                  </v-menu>
                </v-col>  
              </v-row>

              <v-row justify="start">
              <v-col>        

                <h2>Biografía:</h2>
                  
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

              <v-row justify="start">
                <v-col md="3">

                <h2>Estatura:</h2>
                  
                </v-col>
              </v-row>
              <v-row justify="start">
                <v-col md="4">
                  <v-autocomplete
                    v-model="height_feet"
                    :items="feet"
                    label ="Pies"                   
                  ></v-autocomplete>
                </v-col>
              </v-row>
              <v-row justify="start">
                <v-col md="4">         
                    <v-autocomplete
                    v-model="height_inches"
                    :items="inches"
                    label ="Pulgadas"                   
                  ></v-autocomplete>
                </v-col>
              </v-row>

              <v-row justify="start">

                <v-col md="3">

                <h2>Educación:</h2>
                  
                </v-col>
              </v-row>

              <v-row justify="start">
                <v-col md="8">              
                  <v-text-field
                    v-model="study_program"                                   
                    label="Programa de Estudio"                   
                    :counter="30"
                    :rules="[alphaSpaces('Programa de Estudio'),maxSummaryLength('Programa de Estudio',30)]"
                  ></v-text-field>
                  
                </v-col>
              </v-row>
            
              <v-row justify="start"> 
                <v-col md="8">             
                  <v-text-field
                    v-model="school_of_precedence"                                  
                    label="Escuela de Precedencia"
                    :counter="30"                    
                    :rules="[alphaSpaces('Escuela de Precedencia'),maxSummaryLength('Escuela de Precedencia',30)]"
                  ></v-text-field>            
                </v-col>                
              </v-row> 

              <v-row justify="start">
                <v-col md="5">  
                  <v-autocomplete
                    v-model="year_of_study"
                    :items="yearsOfStudy"                                 
                    label ="Año de Estudio"                
                  ></v-autocomplete>
                </v-col> 
              </v-row> 

              <v-row justify="start"> 
                
                <v-col>
                <h2>Deporte:</h2>
                  
                </v-col>
              </v-row>

              <v-row justify="start">

                <v-col md="12">              
                  <v-autocomplete
                    v-model.lazy="sport"
                    :items="sportsList"               
                    label ="Deporte*"
                    item-text="sportName"
                    item-value="id"                    
                    v-on:change="setCategoriesAndPositions()"
                    :rules="[teamRequired('Deporte')]"
                  ></v-autocomplete>              
                </v-col>
              </v-row>
              <v-row justify="start">
                <v-col md="5">  
                  <v-autocomplete
                    v-model="years_of_participation"
                    :items="yearsOfParticipation"              
                    label ="Años de Participación"                                    
                  ></v-autocomplete>
                </v-col>              
              </v-row>

              <v-row justify="start" v-if="!isEmpty(sport_positions) || !isEmpty(sport_categories)">
                <v-col md="4">              
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
              </v-row>

              <v-row justify="start" v-if="!isEmpty(sport_positions) || !isEmpty(sport_categories)">
                <v-col md="4"> 
                
                  <div v-for="(value,key) in sport_positions" :key="key" >
                    <v-checkbox
                      v-model="sport_positions[key]"
                      :true-value=false
                      :false-value=true
                      :label="key" 
                      :key="key"                   
                      v-on:change="updatePositons(key,sport_positions[key])"
                      v-if="!isEmpty(sport_positions)"                                        
                    ></v-checkbox>
                  </div>
                
                  
                  <div v-for="(value,key) in sport_categories" :key="key">
                    <v-checkbox
                      v-model="sport_categories[key]"
                      :true-value=false
                      :false-value=true
                      :label="key"
                      :key="key"
                      v-on:change="updateCategories(key,sport_categories[key])"
                      v-if="!isEmpty(sport_categories)"                      
                    ></v-checkbox>
                  </div>

                </v-col>                   
              </v-row>  

              <v-row justify="start" v-if="sportHasNumber"> 

                <v-col md="12">              
                  <div>                  
                    <h2>
                      
                      Número del Atleta:

                    </h2>
                  </div> 
                </v-col>
              </v-row>

              <v-row justify="start" v-if="sportHasNumber">
                <v-col md="4">
                  <v-autocomplete
                    v-model="number"
                    :items="numbers"
                    label ="Número"             
                  ></v-autocomplete>

                </v-col>
              </v-row>            

              <v-row justify="start">

                <v-col md="12">

                <h2>Imagen de Perfil:</h2>
                  
                </v-col>
              </v-row>

              <v-row justify="start">

                <v-col md="12">             
                  <v-textarea
                    v-model="profile_image_link"                                
                    label="Enlace de Imagen de Perfil"                   
                    required
                    :counter="1000"
                    auto-grow
                    rows = "1"
                    outlined
                    :rules="[maxSummaryLength('Enlace de Imagen de Perfil',1000)]"
                  ></v-textarea>              
                </v-col>
              </v-row> 

              <v-row>
                <v-col>
                   <v-checkbox
                    v-model="terms"
                    label="Estoy de acuerdo con la información*."
                  >
                  </v-checkbox>
                </v-col>
              </v-row> 

            </v-container>
            <small>*indica un campo requirido.</small>
          </v-form>      
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
            <v-btn text color="grey darken-3" @click="close()">
             Cerrar
            </v-btn>
           <v-btn 
              color="primary darken-1" 
              text      
              :disabled="!(valid & terms)"
              @click="submit"
              :loading="adding"
            >
              Guardar
            </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-row>    
</template>

<script>
  import rules from "@/utils/validations"  
  import {mapActions,mapGetters} from "vuex"

  export default {
    name:"AddAthleteModal",
    props:{
      dialog:Boolean
    },
    data: () => ({

      terms: false,
      valid:false,
      ready:false,
      adding: false,
      selected_categories:[],
      date:'',
      menu: false,
      first_name: '',
      middle_name: null,
      last_names:'',
      short_bio:null,
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
      number:0,
      profile_image_link:'',
      sport_id:0,
      sport:'',      
      sportsList:[],     
      sportHasNumber:false,     
      feet: [3,4,5,6,7],      
      inches:[0.0,0.5,1.0,1.5,2.0,2.5,3.0,3.5,4.0,4.5,5.0,5.5,6.0,6.5,7.0,7.5,8.0,8.5,9.0,9.5,10.0,10.5,11.0,11.5],
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
        getAthleteSports:"athletes/getAthleteSports",
        addAthlete:"athletes/addAthlete"
      }),

      /**
       * Function to be called after the user 
       * has entered valid information in the required
       * field and has agreed to the terms.
       */
      async submit () {

        this.adding = true
        const athlete_attributes = {}
        athlete_attributes['first_name'] = this.first_name
        athlete_attributes['middle_name']  = this.middle_name
        athlete_attributes['last_names'] = this.last_names
        athlete_attributes['short_bio'] = this.short_bio

        if(!isNaN(this.height_feet) && this.height_feet !== '' && !isNaN(this.height_inches) && this.height_inches !== ''){          
          athlete_attributes['height'] = this.height_feet*12.0 + this.height_inches
        }
        else
          athlete_attributes['height'] = null

        athlete_attributes['study_program'] = this.study_program
        athlete_attributes['date_of_birth'] = this.date
        athlete_attributes['school_of_precedence'] = this.school_of_precedence
        
        if(!isNaN(this.number) && this.number !== '') 
          athlete_attributes['number'] = this.number
        else
          athlete_attributes['number'] = null
        
        athlete_attributes['profile_picture_link'] = this.profile_image_link

        

        if(this.year_of_study !== '')
          athlete_attributes['year_of_study'] = this.year_of_study
        else
          athlete_attributes['year_of_study'] = null
        
        if(this.years_of_participation !== '') 
          athlete_attributes['years_of_participation'] = this.years_of_participation
        else
          athlete_attributes['years_of_participation'] = null

        

        let athlete_positions = {}
        const p_entries = Object.entries(this.sport_positions)
        for(const [name, value] of p_entries){
          
          if(!value)
            athlete_positions[name] = value
          
        }
        athlete_attributes['positions'] = athlete_positions

        

        let athlete_categories = {}
        const c_entries = Object.entries(this.sport_categories)
        for(const [name, value] of c_entries){
          
          if(!value)
            athlete_categories[name] = value
          
        }
        athlete_attributes['categories'] = athlete_categories

        const athleteJSON ={'sID':this.sport,'attributes':athlete_attributes}
        
        const response =  await this.addAthlete(athleteJSON)
        
        this.adding = false        
       
        if(response !== 'error'){
          this.close()          
        }    
      },

      /**
       * Closes the AddEventModal
       */
      close() {
        this.ready = false
        this.terms = false
        this.clear()
        this.$emit("update:dialog", false)
      },
      /**
       * Clears and resets all optional fields in the form.
       */
      clear () {
        this.$refs.form.resetValidation()
        this.first_name= '',
        this.middle_name= null,
        this.last_names='',
        this.short_bio=null,
        this.height_feet='',
        this.height_inches='',
        this.study_program='', 
        this.date_of_birth='',
        this.school_of_precedence='',        
        this.number=0,
        this.profile_image_link='',
        this.sportHasNumber=false         
        this.sport ='' 
        this.years_of_participation = ''
        this.year_of_study = ''
        this.setCategoriesAndPositions() 
        this.resetDate()
        
      },

      /**
       * Updates the positions of the 
       * sport_positions object
       * @param key key of the sport_positions Object
       * @param value value to be assigned to the position
       */
      updatePositons(key,value){
        
        this.sport_positions[key]=value 
        console.log(this.sport_positions)      
      },

      /**
       * Updates the categories of the 
       * categories_categories object
       * @param key key of the sport_categories Object
       * @param value value to be assigned to the category
       */
      updateCategories(key,value){
        
        this.sport_categories[key]=value       
        console.log(this.sport_categories)
      },


      
      /**
       * Formats the content in the athlete creation form
       * sports list and date of birth fields and returns true
       * if it has been completed.
      */
      formated(){
        if(this.sports.length > 0){
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
        else{
          this.getAthleteSports()
          return false
        }
      },
      
      /**
       * Assign the sport's categories and positions
       * to the sport_positions and sport_categories Objects       * 
       */
      setCategoriesAndPositions(){
        this.sport_positions = {}
        this.sport_categories = {}
        Object.keys(this.sport_positions).forEach(key => this.sport_positions[key] = null)
        Object.keys(this.sport_categories).forEach(key => this.sport_categories[key] = null)
        for(let i = 0; i < this.sports.length; i++){
            let sportObj = this.sports[i]
            if(this.sport == sportObj['sport_id']){
              let positions = sportObj['positions']
              if(positions.length > 0){
                for(let j = 0; j < positions.length; j++){
                  this.sport_positions[positions[j]]=true;                   
                }
              }
              let categories = sportObj['categories']
              if(categories.length > 0){
                for(let k = 0; k < categories.length; k++){
                  this.sport_categories[categories[k]]=true;                   
                }
              }
              break
            }
        }
        this.sportNumber()        
        
      },

      /**
       * Returns true if object is empty, false otherwise
       * @param obj Javascript Object
       */
      isEmpty(obj){
        for(let key in obj){
          if(obj.hasOwnProperty(key))
            return false
        }
        return true
      },

    /**
     * Determines if the sport of the athlete
     * has numbers for the athlete and assigns
     * the value of true or false to th sportHasNumber
     * flag.
     */
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
      /**
       * Resets the date of the date_of_birth_ data variable
       * to the current date.
       */
      resetDate(){
        let time_zone_offset = new Date().getTimezoneOffset() * 60000      
        this.date = new Date(Date.now() - time_zone_offset).toISOString().substring(0,10)
      }

      
      
    },

    computed:{
      ...mapGetters({
        sports:"athletes/athlete_sports"
      }),
    },
   
    
  }
</script>