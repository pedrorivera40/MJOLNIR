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
      <v-spacer />
    </v-toolbar>
    <v-card-text>            
      
      <v-form v-model="valid" v-if="formated()">
        <v-container>            
          <v-row>            
            <v-col
              cols="1"
              md="3"
            >	

            <h2>Fecha del Evento:</h2>
              
            </v-col>

            <v-col
              cols="12"
              
            >
            <v-date-picker
              v-model="date"
              full-width
              :landscape="$vuetify.breakpoint.smAndUp"
              :show-current="true"
              color="green darken-1"
              class="mt-4"
              locale="es-419"
            ></v-date-picker>
              
            </v-col>
          </v-row>

          <v-row>
            <v-col
              cols="1"
              md="3"
            >	

            <h2>Localización:</h2>
            
            </v-col>

            <v-col
              cols="12"
              md="3"
            >                
              <v-select
                v-model="locality"
                :items="localities"                  
                label ="Localización"
                :rules="[required('Localización')]"
              ></v-select>                
            </v-col>

            <v-col
              cols="12"
              md="4"
            >          
              <v-text-field
                v-model="venue"                                     
                label="Lugar del Evento"
                required
                :rules="[alphaSpaces('Lugar del Evento')]"
              ></v-text-field>                
            </v-col>
          </v-row>

          <v-row >
            <v-col
              cols="1"
              md="3"
            >	

            <h2>Equipo de UPRM:</h2>
              
            </v-col>

            <v-col 
              cols="1"
              md="9"
              
            >               
            <v-select
                  v-model="team"
                  :items="teamsList"                
                  name="Equipo"                    
                  label ="Equipo"
                  item-text="sportName"
                  item-value="id"                  
                  :rules="[teamRequired('Equipo')]"
              ></v-select>               
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
                label="Nombre de Oponente"
                required
                :rules="[generalPhrase('Nombre de Oponente')]"
              ></v-text-field>
              
            </v-col>
          </v-row>
          <v-row>
            <v-col
              cols="1"
              md="3"
            >	

              <h2>Resumen de Evento:</h2>
              
            </v-col>

            <v-col
              cols="12"
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


          <v-row>
            <v-spacer/>
            <v-spacer/>
            <v-col>
              <v-btn 
                color="green darken-1" 
                class="mr-4" 
                :disabled="!valid" 
                @click="submit">Someter
              </v-btn>
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
  import teamsData from "../../data/eventsPagesData/teams.json"

  export default {
    
    data: () => ({
      ready : false,
      valid:false,
			date:'', 
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
      teams:teamsData,      
      
    }),

   

    methods: {
      ...rules,

      submit () {

        let event_attributes = {}

        event_attributes['event_date'] = this.date

        if(this.locality.localeCompare('Casa') == 0)
          event_attributes['is_local'] = true
        else if(this.locality.localeCompare('Afuera') == 0)
          event_attributes['is_local'] = false
        
        event_attributes['team_id'] = this.team
        event_attributes['opponent_name'] = this.opponent_name
        event_attributes['event_summary'] = this.eventSummary

        console.log("Creating a new event with the following information:")
        console.log(event_attributes)

        this.$router.push('/eventos/')
        
      },
      clear () {
        this.locality =''
        this.team = ''
        this.eventSummary = null
        this.opponent_name = ''
        this.resetDate()  
      },
      buildTeamsList(){
        for(let i = 0; i < this.teams.length; i ++)
        {
          let sportObj = this.teams[i].team_info
          //console.log(sportObj)
          this.teamsList.push({'id':sportObj['team_id'],'sportName':'Deporte: ' + sportObj['sport_name']+'-'+sportObj['branch_name'] + ' Temporada: ' + sportObj['season_year']})

        }
      },

      formated(){
        if(this.teams){
          if(this.ready){
            return true
          }
          else{
            this.buildTeamsList()
            this.resetDate()
            this.ready = true
          }

        }
        else{
          return false
        }
      },
      
      resetDate()
      {
        let time_zone_offset = new Date().getTimezoneOffset() * 60000
      
        this.date = new Date(Date.now() - time_zone_offset).toISOString().substring(0,10)
        
      }

      
    },
  }
</script>