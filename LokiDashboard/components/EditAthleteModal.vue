<template>
  <v-row justify="center">
    <v-dialog v-model="dialog" persistent max-width="600">
      <v-card>
        <v-toolbar color="primary_dark" flat>
          <v-spacer/>
          <v-toolbar-title class="headline white--text">{{setForm}}</v-toolbar-title>
          <v-progress-linear
            :active="loading"
            indeterminate
            absolute
            bottom
            color = "white"
          ></v-progress-linear>	
          <v-spacer />
        </v-toolbar>
        <v-card-text>           
          
          <v-form v-model="valid">
            <v-container>
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
                    v-model="first_name_"          
                    
                    :counter="20"
                    label="Primer Nombre*"
                    required
                    :rules="[required('Primer Nombre'),nameFormat('Primer Nombre'),maxLength('Nombre',20)]"
                  ></v-text-field>              
                </v-col>
              </v-row>

              <v-row justify="start">
                <v-col              
                  md="6"
                >
                  <v-text-field
                    v-model="middle_name_"                
                    :counter="20"
                    label="Segundo Nombre"
                    required
                    :rules="[nameFormat('Segundo Nombre'),maxSummaryLength('Segundo Nombre',20)]"
                  ></v-text-field>              
                </v-col>
              </v-row>

              <v-row justify="start">
                <v-col              
                  md="9"
                >              
                  <v-text-field
                    v-model="last_names_"
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
                    :return-value.sync="date_of_birth_"
                    transition="scale-transition"
                    offset-y
                    min-width="290px"
                  >
                  
                    <template v-slot:activator="{ on }">
                      <v-text-field
                        v-model="date_of_birth_"
                        label="Fecha"                       
                        readonly
                        v-on="on"
                      ></v-text-field>
                    </template>
                    <v-date-picker v-model="date_of_birth_" color = "green darken-1" no-title scrollable locale="es-419">
                      <v-spacer></v-spacer>
                      <v-btn text color="primary" @click="menu = false">Cancelar</v-btn>
                      <v-btn text color="primary" @click="$refs.menu.save(date_of_birth_)">OK</v-btn>
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
                    v-model="short_bio_"                      
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
                <v-col              
                  md="3"
                >

                <h2>Estatura:</h2>
                  
                </v-col>
              </v-row>
              <v-row justify="start">
                <v-col              
                  md="4"
                >
                  <v-autocomplete
                    v-model="height_feet_"
                    :items="feet"
                    label ="Pies"                    
                  ></v-autocomplete>
                </v-col>
              </v-row>
              <v-row justify="start">
                <v-col md="4">         
                    <v-autocomplete
                    v-model="height_inches_"
                    :items="inches"
                    label ="Pulgadas"                    
                  ></v-autocomplete>
                </v-col>
              </v-row>

              <v-row justify="start">

                <v-col              
                  md="3"
                >

                <h2>Educación:</h2>
                  
                </v-col>
              </v-row>

              <v-row justify="start">
                <v-col            
                  md="8"
                >              
                  <v-text-field
                    v-model="study_program_"                                   
                    label="Programa de Estudio"                    
                    :counter="30"
                    :rules="[alphaSpaces('Programa de Estudio'),maxSummaryLength('Programa de Estudio',30)]"
                  ></v-text-field>
                  
                </v-col>
              </v-row>

              <v-row justify="start"> 
                <v-col            
                  md="8"
                >             
                  <v-text-field
                    v-model="school_of_precedence_"                                  
                    label="Escuela de Precedencia"                   
                    :counter="30"
                    :rules="[alphaSpaces('Escuela de Precedencia'),maxSummaryLength('Escuela de Precedencia',30)]"
                  ></v-text-field>            
                </v-col>
                
              </v-row>

              <v-row justify="start">
                <v-col              
                  md="4"               
                >  
                  <v-autocomplete
                    v-model="year_of_study_"
                    :items="yearsOfStudy"                                 
                    label ="Año de Estudio"                
                  ></v-autocomplete>
                </v-col>                  
              </v-row>

              <v-row justify="start"> 
                
                <v-col              
                  md="12"
                >

                <h2>Deporte:{{sport}}</h2>
                  
                </v-col>
              </v-row>

              <v-row justify="start">
                <v-col               
                  md="5"               
                >  
                  <v-autocomplete
                    v-model="years_of_participation_"
                    :items="yearsOfParticipation"              
                    label ="Años de Participación"                                    
                  ></v-autocomplete>
                </v-col>              
              </v-row>

              <v-row justify="start">
                <v-col               
                  md="4"               
                >              
                  <div>                  
                    <h2 v-if="!isEmpty(athlete_positions_)">
                      
                      Posiciones:

                    </h2>
                  </div>

                  <div>                  
                    <h2 v-if="!isEmpty(athlete_categories_)">
                      
                      Categorías:

                    </h2>
                  </div>

                </v-col>
              </v-row>

              <v-row justify="start">
                <v-col              
                  md="4"               
                > 
                
                  <div v-for="(value,key) in athlete_positions_" :key="key" >
                    
                    <v-checkbox         
                     
                      v-model="athlete_positions_[key]"
                      :true-value=false
                      :false-value=true
                      :label="key"
                      :key ="key"                                          
                      v-on:change="updatePositons(key,athlete_positions_[key])"
                      v-if="!isEmpty(athlete_positions_)"                                        
                    ></v-checkbox>
                  </div>               
                
                  
                  <div v-for="(value,key) in athlete_categories_" :key="key">
                    <v-checkbox
                      v-model="athlete_categories_[key]"
                      :true-value=false
                      :false-value=true
                      :label="key"
                      :key ="key"
                      v-on:change="updateCategories(key,athlete_categories_[key])"
                      v-if="!isEmpty(athlete_categories_)"                      
                    ></v-checkbox>
                  </div>

                </v-col>                   
              </v-row>  

              <v-row justify="start"> 

                <v-col
                  md="12"
                >           
                  <div>                  
                    <h2 v-if="sportHasNumber">
                      
                      Número del Atleta:

                    </h2>
                  </div> 
                </v-col>
              </v-row>

              <v-row justify="start">
                <v-col               
                  md="4"               
                >
                  <v-autocomplete
                    v-model="number_"
                    :items="numbers"
                    label ="Número"                    
                    v-if="sportHasNumber"
                  ></v-autocomplete>

                </v-col>
              </v-row>            

              <v-row justify="start">

                <v-col             
                  md="12"
                >

                <h2>Imagen de Perfil:</h2>
                  
                </v-col>
              </v-row>

              <v-row justify="start">

                <v-col            
                  md="12"
                >             
                  <v-textarea
                    v-model="profile_image_link_"                                
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
                        label="He revisado mis cambios*."
                      >
                      </v-checkbox>
                    </v-col>
              </v-row>
              
            </v-container>
            <small>*indica un campo requerido.</small>
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
                :disabled="!(valid && terms)"
                @click="submit"
                :loading="editing"
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
import { mapActions, mapGetters} from "vuex"

export default {
  name:"EditAthleteModal",

  props:{
    dialog:Boolean,
    first_name:String,
    middle_name:String,
    last_names:String,
    date_of_birth:String,
    short_bio:String,
    height:Number,
    study_program:String,
    school_of_precedence:String,
    years_of_participation:Number,
    year_of_study:Number,
    athlete_positions:Object,
    athlete_categories:Object,
    number:Number,
    profile_image_link:String,
    sport_name:String,
    branch:String,
    sport_id:Number,
    id:Number,

  },
  
  data: () => ({
    editing:false,
    valid:false,
    ready:false,
    loading: true,
    terms:false,
    menu: false,
    first_name_: '',
    middle_name_: null,
    last_names_:'',
    date_of_birth_:'',
    short_bio_:'',
    height_feet_:'',
    height_inches_:'',
    study_program_:'',       
    school_of_precedence_:'',
    years_of_participation_:'',
    year_of_study_:'',
    athlete_positions_:null,
    athlete_categories_:null,      
    number_:'',
    profile_image_link_:'',
    sport:'',
    sport_id_:0,               
   
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
      editAthlete:"athletes/editAthlete"
    }),


    /**
     * Function to be called when an athlete is edited
     * with valid information and the user presses 
     * the edit button.
     */
    async submit () {
      
      this.editing = true

      const athlete_attributes = {}
      athlete_attributes['first_name'] = this.first_name_
      athlete_attributes['middle_name']  = this.middle_name_
      athlete_attributes['last_names'] = this.last_names_
      athlete_attributes['short_bio'] = this.short_bio_
      
      
      if(this.height_feet_ != '' & this.height_inches_ != '')
        athlete_attributes['height'] = this.height_feet_*12.0 + this.height_inches_*1.0
      else
        athlete_attributes['height'] = this.height      

      athlete_attributes['study_program'] = this.study_program_
      athlete_attributes['date_of_birth'] = this.date_of_birth_
      athlete_attributes['school_of_precedence'] = this.school_of_precedence_
      
      if(this.number_ != '') 
        athlete_attributes['number'] = this.number_
      else
        athlete_attributes['number'] = this.number
      
      athlete_attributes['profile_picture_link'] = this.profile_image_link_      

      if(this.year_of_study_ != '')
        athlete_attributes['year_of_study'] = this.year_of_study_
      else
        athlete_attributes['year_of_study'] = this.year_of_study
      
      if(this.years_of_participation_ != '') 
        athlete_attributes['years_of_participation'] = this.years_of_participation_
      else
        athlete_attributes['years_of_participation'] = this.years_of_participation

      let athlete_positions = {}
      const p_entries = Object.entries(this.athlete_positions_)
      for(const [name, value] of p_entries){
        
        if(!value)
          athlete_positions[name] = value
        else if(value && name in this.athlete_positions)
          athlete_positions[name] = value
        
      }
      athlete_attributes['positions'] = athlete_positions        

      let athlete_categories = {}
      const c_entries = Object.entries(this.athlete_categories_)
      for(const [name, value] of c_entries){
        
        if(!value)
          athlete_categories[name] = value
        else if(value && name in this.athlete_categories)
          athlete_categories[name] = value
        
      }
      athlete_attributes['categories'] = athlete_categories

      const athleteJSON = {'athlete_id': this.id,'attributes':athlete_attributes}   

      const resonse = await this.editAthlete(athleteJSON)

      this.editing = false     
      
      if(resonse != 'error')
      {
        this.close()        
      } 
      
    },    

    /**
     * Updates the positions of the 
     * athlete_positions_ object
     * @param key key of the athlete_positions_ Object
     * @param value value to be assigned to the position
     */
    updatePositons(key,value){
      
      this.athlete_positions_[key]=value  
        
    },

    /**
     * Updates the categories of the 
     * athlete_categories_ object
     * @param key key of the athlete_categories_ Object
     * @param value value to be assigned to the category
     */
    updateCategories(key,value){
      
      this.athlete_categories_[key]=value       
    },


    
    /**
     * Formats the content in the edit athlete form
     * fields.
     */
    format(){
      if(this.dialog && !this.ready){        

        this.first_name_ = this.first_name
        this.last_names_ = this.last_names
        if(this.middle_name)
          this.middle_name_ = this.middle_name

        this.sport = this.sport_name+ '-' + this.branch
        
        this.sport_id_ = this.sport_id
        
        if(this.short_bio)
          this.short_bio_ = this.short_bio

        if(this.number){
          this.number_ = this.number
          this.sportHasNumber = true
        }
        else{
          this.sportNumber()
        }

        if(this.height)
        {
          this.height_feet_ = Math.floor(this.height/12)
          this.height_inches_ = this.height%12
        }

        if(this.profile_image_link)
          this.profile_image_link_ = this.profile_image_link
        

        if(this.school_of_precedence)
          this.school_of_precedence_ = this.school_of_precedence

        if(this.study_program)
          this.study_program_ = this.study_program
        
        if(this.year_of_study)
          this.year_of_study_ = this.year_of_study
        
        if(this.years_of_participation)
          this.years_of_participation_ = this.years_of_participation
        
        if(this.date_of_birth)
          this.date_of_birth_ = new Date(Date.parse(this.date_of_birth)).toISOString().substr(0,10)
        else
          this.resetDate()
        
        
        this.athlete_positions_ = {}
        this.athlete_categories_ = {}
        for(let i = 0; i < this.sports.length; i++){
            let sportObj = this.sports[i]
            if(this.sport_id_ == sportObj['sport_id']){
              let positions = sportObj['positions']
              if(positions.length > 0){
                for(let j = 0; j < positions.length; j++){

                  if(positions[j] in this.athlete_positions)
                    this.athlete_positions_[positions[j]] = this.athlete_positions[positions[j]]
                  else
                    this.athlete_positions_[positions[j]]=true;                   
                }
              }
              let categories = sportObj['categories']
              if(categories.length > 0){
                for(let k = 0; k < categories.length; k++){
                  if(categories[k] in this.athlete_categories)
                    this.athlete_categories_[categories[k]] = this.athlete_categories[categories[k]]
                  else
                    this.athlete_categories_[categories[k]]=true;                    
                }
              }
              break
            }
        }
        
        
        this.ready = true
        this.loading = false
      }      
           
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
      if(this.sport_id_ != 0)
      {
        for(let i = 0; i < sportsWithNumbers.length; i++){
          if(this.sport_id_ == sportsWithNumbers[i]){
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
      this.date_of_birth_ = new Date(Date.now() - time_zone_offset).toISOString().substring(0,10)
    },

    /**
     * Closes the EditAthleteModal and resets optional 
     * fields.
     */
    close(){
      this.ready = false
      this.terms = false
      this.loading = true
      this.middle_name_ = null
      this.short_bio_ = ''
      this.years_of_participation_ = ''
      this.number_ = ''
      this.year_of_study_ = ''
      this.height_feet_ = ''
      this.height_inches_ = ''
      this.school_of_precedence_ = ''
      Object.keys(this.athlete_positions_).forEach(key => this.athlete_positions_[key] = null)
      Object.keys(this.athlete_categories_).forEach(key => this.athlete_categories_[key] = null)
      
      this.profile_image_link_ = ''
      
      this.resetDate()
      
      this.$emit("update:dialog",false);
    }

    
  },

  
  computed: {
    ...mapGetters({
      sports:"athletes/athlete_sports"
    }),
    setForm(){     
      this.format()
      return "Editar Atleta"

    }	
  },

  
}
</script>