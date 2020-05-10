<template>
  <v-row justify="center">
    <v-dialog  v-model="dialog" persistent max-width="600">
      <v-card>
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
          <v-spacer />
        </v-toolbar>
        <v-card-text>            
          
          <v-form v-model="valid" v-if="formated()">
            <v-container>

              <v-row justify="start">
                <v-col>
                  <h2> Escoge la fecha y hora del evento </h2>
                </v-col>
              </v-row>
                          
              <v-row>            
                <v-col             
                  md="12"
                >	

                <h2>Fecha del Evento:</h2>
                  
                </v-col>
              </v-row>

              <v-row>
                <v-col>
                <v-date-picker
                  v-model="date"
                  full-width
                  :landscape="$vuetify.breakpoint.smAndUp"
                  :show-current="true"
                  color="green darken-1"
                  class="mt-4"
                  locale="es-419"
                  :min ="min_date"
                  :max ="max_date" 
                ></v-date-picker>
                  
                </v-col>
              </v-row>

              <v-row>            
                <v-col>	

                <h2>Hora del Evento:</h2>
                  
                </v-col>
              </v-row>

              <v-row>
                <v-col>                  
                
                <v-time-picker 
                  v-model="time" 
                  :landscape="$vuetify.breakpoint.mdAndUp"
                  color="green darken-1"
                ></v-time-picker>
                  
                </v-col>
              </v-row>

              <v-row justify="start">
                <v-col>        

                  <h2>Localización:</h2>
                
                </v-col>
              </v-row>
              <v-row justify="center">
                <v-col              
                  md="6"
                >                
                  <v-select
                    v-model.lazy="locality"
                    :items="localities"                  
                    label ="Localización"
                    :rules="[required('Localización')]"
                  ></v-select>                
                </v-col>
              </v-row>

              <v-row justify="center">
                <v-col              
                  md="6"
                >          
                  <v-text-field
                    v-model="venue"                                     
                    label="Lugar del Evento"
                    required
                    counter="25"
                    :rules="[alphaSpaces('Lugar del Evento')]"
                  ></v-text-field>                
                </v-col>
              </v-row>

              <v-row justify="start">
                <v-col>	

                  <h2>Equipo de UPRM:</h2>
                  
                </v-col>
              </v-row>
              <v-row justify="center">
                <v-col             
                  md="9"                  
                >               
                <v-autocomplete
                      v-model="team"
                      :items="teamsList"                
                      name="Equipo"                    
                      label ="Equipo"
                      item-text="sportName"
                      item-value="id"                  
                      :rules="[teamRequired('Equipo')]"
                  ></v-autocomplete>               
                </v-col>


              </v-row>

              <v-row>
                <v-col md="12">	

                  <h2>Nombre de Oponente:</h2>
                  
                </v-col>
              </v-row>
              <v-row justify="center">
                <v-col md="6">              
                  <v-text-field
                    v-model="opponent_name"                                  
                    label="Nombre de Oponente"
                    required
                    counter="25"
                    :rules="[generalPhrase('Nombre de Oponente')]"
                  ></v-text-field>
                  
                </v-col>
              </v-row>
              <v-row>
                <v-col>	

                  <h2>Resumen de Evento:</h2>
                  
                </v-col>
              </v-row>
              <v-row justify="center">
                <v-col              
                  md="9"
                >                
                  <v-textarea
                    v-model="eventSummary"                      
                    :counter="250"                  
                    label="Resumen"
                    auto-grow
                    rows = "2"
                    outlined
                    :rules="[minLength('Resumen',1),maxSummaryLength('Resumen',250)]"
                  ></v-textarea>                
                </v-col>
              </v-row>

              <v-row justify="start">
                <v-col>
                   <v-checkbox
                    v-model="terms"
                    :label="`Estoy de acuerdo con la información.`"
                  >
                  </v-checkbox>
                </v-col>
              </v-row>      
              
            </v-container>
          </v-form>      
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
            <v-btn  @click="close()">
             Cerrar
            </v-btn>
           <v-btn 
              color="green darken-1" 
                        
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
    name:"AddEventModal",
    props:{
      dialog:Boolean,
      trigger:Boolean,
    },
    
    data: () => ({
      ready : false,
      valid:false,      
      terms:false,
      adding:false,
      //Here are the fields to be used by the edit form:
      date:'',
      time:'', 
			locality:'',
			localities:['Casa','Afuera'],
			venue:'',
			teamSport:'',		
      opponent_name:'',
      eventSummary:null,
      yearList:[],
      year:'',
      team:'',
      teamsList:[],
      min_date:'',
      max_date:'',   
         
      
    }),

   

    methods: {
      ...rules,

      ...mapActions({
        addEvent:"events/addEvent",
        getEventTeams:"events/getEventTeams"
      }),

      /**
       * Function to be called after the user 
       * has entered valid information in the required
       * field and has agreed to the terms.
       */
      async submit () {        
        this.adding = true
        const event_attributes = {}//Temp Object for the attributes of the event.

        event_attributes['event_date'] = this.date + ' ' + this.time

        if(this.locality.localeCompare('Casa') == 0)
          event_attributes['is_local'] = true
        else if(this.locality.localeCompare('Afuera') == 0)
          event_attributes['is_local'] = false        
        
        event_attributes['venue'] = this.venue
        event_attributes['opponent_name'] = this.opponent_name
        event_attributes['event_summary'] = this.eventSummary
        
        //Contruct Object for the vuex action to be called.        
        const eventJSON = {'team_id':this.team,'attributes':event_attributes}
        
        //Call vuex action and store response
        const response = await this.addEvent(eventJSON)
        this.adding = false
        if(response !== 'error'){
          this.$emit("update:trigger",false)
          this.close()          
        }    
        
      },

      /**
       * Closes the AddEventModal
       */
      close () {       
        this.ready = false
        this.terms = false
        this.$emit("update:dialog",false);
      
      },

      /**
       * Builds the team selection list to be used 
       * in the edit form.
       */
      buildTeamsList(){
        for(let i = 0; i < this.teams.length; i ++)
        {
          let sportObj = this.teams[i].team_info
          //console.log(sportObj)
          this.teamsList.push({'id':sportObj['team_id'],'sportName':'Deporte: ' + sportObj['sport_name']+'-'+sportObj['branch_name'] + ' Temporada: ' + sportObj['season_year']})

        }
      },

      /**
       * Indicates whether the event edit form is formated,
       * if it is not formated then it formats and prepares 
       * the form.
       */
      formated(){
        if(this.teams.length > 0){
          if(this.ready){
            return true
          }
          else{
            this.buildTeamsList()
            this.resetDate()
            this.team = ''
            this.venue = ''
            this.locality = ''
            this.opponent_name = ''
            this.eventSummary = null
            this.ready = true
          }
        }
        else{
          this.getEventTeams()//Get the teams from the database and store them in the state
          return false
        }
      },
      /**
       * Resets the date field in the form and formats it in 
       * a way that can be used by the date and time fields.
       */
      resetDate()
      {
        let time_zone_offset = new Date().getTimezoneOffset() * 60000
        const newDate =  new Date(Date.now() - time_zone_offset)
        this.date = newDate.toISOString().substring(0,10)
        this.time = newDate.getUTCHours()+':'+newDate.getUTCMinutes()
        
        const dateYear = newDate.getFullYear()
        //This fields restricts the dates that can be chosen.
        this.min_date = dateYear +'-01-01'
        this.max_date = dateYear+1 +'-12-31'
      }
      
    },

    computed: {
		...mapGetters({
			 teams:"events/event_teams"
		}),
		

	},
	
  }
</script>