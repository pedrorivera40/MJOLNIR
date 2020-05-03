<template>
  <v-row justify="center">
    <v-dialog v-model="dialog" persistent max-width="600">
      <v-card>
        <v-toolbar color="green darken-1" dark >
          <v-spacer />
          <v-toolbar-title> {{setForm}}</v-toolbar-title>
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

              <v-row>
                <v-col> 	

                  <h2>Equipo de UPRM: {{team_}}</h2>
                  
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
                  v-model="date_"
                  full-width
                  :landscape="$vuetify.breakpoint.smAndUp"
                  :show-current="true"
                  color="green darken-1"
                  class="mt-4"
                  locale="es-419"
                  :min="min_date"
                  :max="max_date"
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
                  v-model="time_" 
                  :landscape="$vuetify.breakpoint.mdAndUp"
                  color="green darken-1"
                  ></v-time-picker>
                  
                </v-col>
              </v-row>          

              <v-row>
                <v-col              
                  md="12"
                >	

                <h2>Localización:</h2>
                
                </v-col>
              </v-row>
              <v-row justify="center">
                <v-col              
                  md="6"
                > 
                        
                  <v-select
                    v-model="locality_"
                    :items="localities"
                    item-text="text"
                    item-value="value"             
                    label ="Localización"              
                  ></v-select>            
                </v-col>
              </v-row>

              <v-row justify="center">
                <v-col              
                  md="6"
                >              
                  <v-text-field
                    v-model="venue_"                                    
                    label="Lugar del Evento"
                    required
                    counter="25"
                    :rules="[alphaSpaces('Lugar del Evento')]"
                  ></v-text-field>              
                </v-col>
              </v-row>

              <v-row>
                <v-col             
                  md="12"
                >	

                  <h2>Nombre de Oponente:</h2>
                  
                </v-col>
              </v-row>
              <v-row justify="center">
                <v-col              
                  md="6"
                >              
                  <v-text-field
                    v-model="opponent_name_"                                    
                    label="Oponente"
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

                <v-col              
                  md="9"
                >                
                  <v-textarea
                    v-model="eventSummary_"                      
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
                <v-col>
                   <v-checkbox
                    v-model="terms"
                    :label="`Yo quiero editar el evento con id:${id}`"
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
              :loading="editing"
            >
              Editar
            </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-row>
</template>

<script>
import { mapActions, mapGetters} from "vuex";
import rules from "@/utils/validations"
export default {

  name: "EditEventModal",
  props:{
    dialog:Boolean,
    date:String,
    time:String,    
    locality:Boolean,
    venue:String,
    sport_name:String,
    branch:String,
    team_season_year:Number,
    opponent_name:String,
    event_summary:String,
    id:Number,
    trigger:Boolean,

  },
  
  data: () => ({
    ready:false,
    valid:false,
    date_:'',     
    time_:'',
    locality_:Boolean,
    localities:[{'text':'Casa','value':true},{'text':'Afuera','value':false}],
    venue_:'',
    team_:'',	
    terms:false,	
    opponent_name_:'',
    eventSummary_:'',
    loading:true, 
    editing:false,
    min_date:'',
    max_date:'',  
   
    
  }),
   


  methods: {

    ...mapActions({      
      editEvent:"events/editEvent"
    }),
    
    ...rules,

    async submit () { 

      this.editing = true
      const event_attributes = {}

      event_attributes['event_date'] = this.date_ + ' ' + this.time_
      event_attributes['is_local'] = this.locality_      
      event_attributes['venue'] = this.venue_
      event_attributes['opponent_name'] = this.opponent_name_
      event_attributes['event_summary'] = this.eventSummary_
      
      const eventJSON = {'event_id':this.id,'attributes':event_attributes}
      
      const response = await this.editEvent(eventJSON)

      this.editing = false
      if(response !== 'error'){
        this.$emit("update:trigger",false)
        this.close()        
      }          
     
    },
     
    format(){
			
      if(this.dialog && !this.ready){       
        
        this.date_ = this.date

        const dateYear = this.team_season_year
        this.min_date = dateYear +'-01-01'
        this.max_date = dateYear+1 +'-12-31'
        

        
        this.time_ = this.time        

        this.locality_ = this.locality
      
        this.team_ = this.sport_name + '-' + this.branch + '-' + this.team_season_year		        
        
        if(this.venue)
          this.venue_ = this.venue   
        
        if(this.opponent_name)
          this.opponent_name_ = this.opponent_name

        if(this.event_summary)
          this.eventSummary_ = this.event_summary
        
        

        this.ready = true
        this.loading = false    
      }

    },
    close(){
      this.ready = false
      this.terms = false
      this.venue_ = ''
      this.opponent_name_ = ''
      this.eventSummary_ = ''
      this.$emit("update:dialog",false);       
    }
       
  }, 

  computed:{
    setForm(){     
      this.format()
      return "Editar Evento"

    }	
  },

 
}
</script>