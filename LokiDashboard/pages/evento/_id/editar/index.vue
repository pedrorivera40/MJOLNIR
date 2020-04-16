<template>
  <v-card width="800" class="elevation-12 mx-auto">
    <v-toolbar color="green darken-1" dark >
      <v-spacer />
      <v-toolbar-title>Editar Evento</v-toolbar-title>
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
                item-text="text"
                item-value="value"             
                label ="Localización"              
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
                :rules="[minLength('Lugar del Evento',5)]"
              ></v-text-field>              
            </v-col>
          </v-row>

          <v-row>
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
              <v-text-field
                v-model="team"
                label="Equipo"									
                readonly                 
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
                required
                :rules="[minLength('Nombre de Oponente',2)]"
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
                @click="submit"
              >
                Someter
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
import { mapActions, mapGetters} from "vuex";
import rules from "../../../../utils/validations"
export default {
  
  data: () => ({
    ready:false,
    valid:false,
    date:'', 
    locality:'',
    localities:[{'text':'Casa','value':true},{'text':'Afuera','value':false}],
    venue:'',
    team:'',		
    opponent_name:'',
    eventSummary:'',    
   
    
  }),
   


  methods: {

    ...mapActions({
			getEventByID:"events/getEventByID"
    }),
    
    ...rules,

    submit () { 

      let jsonForRequest = {

        'attributes':[this.date,this.locality,this.venue,this.opponent_name,this.eventSummary]

      }
      console.log(jsonForRequest)
           
     
    },
    clear () {

      this.date = new Date(Date.parse(this.event.event_date)).toISOString().substr(0,10)
      
      this.locality = this.event.is_local      
     
      
      if(this.event.venue)
        this.venue = this.event.venue      
      
      if(this.event.opponent_name)
        this.opponent_name = this.event.opponent_name

      if(this.event.event_summary)
        this.eventSummary = this.event.event_summary
      
            
    }, 
    formated(){
			if(this.event){
				if(this.ready){
					return true
				}
				else{
					this.date = new Date(Date.parse(this.event.event_date)).toISOString().substr(0,10)
            
          this.locality = this.event.is_local
				
					this.team = "Deporte: " + this.event.sport_name + '-' + this.event.branch + " Temporada: " + this.event.team_season_year		
					
          
          if(this.event.venue)
            this.venue = this.event.venue
          
         
          if(this.event.opponent_name)
            this.opponent_name = this.event.opponent_name
          if(this.event.event_summary)
            this.eventSummary = this.event.event_summary
          
          

					this.ready = true
				}
			}
			else
			{
				return false
			}

		}    
  }, 

  computed:{
    ...mapGetters({
			 event:"events/event"
		}),		
  },

  mounted() {
		this.getEventByID(this.$route.params.id);		
	}
}
</script>