<template>
  <v-card width="800" class="elevation-12 mx-auto">
    <v-toolbar color="green darken-1" dark flat>
      <v-spacer />
      <v-toolbar-title>Evento</v-toolbar-title>
      <v-spacer />
    </v-toolbar>
    <v-card-text>            
      <ValidationObserver ref="observer" v-slot="{ validate, reset }">
        <form>
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

              <h2>Localizacion:</h2>
              
              </v-col>

              <v-col
                cols="12"
                md="3"
              >
                <ValidationProvider v-slot="{ errors }" name="Localizacion" rules="required">
                  <v-select
                    v-model="locality"
                    :items="localities"
                    :error-messages="errors"
                    label ="Localizacion"
                    prepend-icon=""
                  ></v-select>
                </ValidationProvider>
              </v-col>

              <v-col
                cols="12"
                md="4"
              >
                <ValidationProvider v-slot="{ errors }" name="Lugar del Evento" rules="alpha_spaces">
                  <v-text-field
                    v-model="venue"
                    :error-messages="errors"                    
                    label="Lugar del Evento"
                    required
                  ></v-text-field>
                </ValidationProvider>
              </v-col>
						</v-row>

            <v-row>
              <v-col
                cols="1"
                md="3"
            	>	

              <h2>Equipo de Tarzanes:</h2>
               
            	</v-col>

              <v-col
                cols="1"
                md="3"
            	>
               <v-text-field
                    v-model="teamSport"
                    label="Deporte"									
										readonly                
                    prepend-icon=""
                ></v-text-field>
              </v-col>

              <v-col
                cols="1"
                md="3"
            	>
               <v-text-field
                    v-model="year"                                                           
                    label ="A~no del equipo"										
										readonly                                        
                    prepend-icon=""
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
                <ValidationProvider v-slot="{ errors }" name="Nombre de Oponente" rules="alpha_spaces">
                  <v-text-field
                    v-model="opponent_name"
                    :error-messages="errors"                    
                    label="Oponente"
                    required
                  ></v-text-field>
                </ValidationProvider>
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
                <ValidationProvider v-slot="{ errors }" name="Resumen" rules="max:250">
                  <v-textarea
                    v-model="eventSummary"                      
                    :counter="250"
                    :error-messages="errors"
                    label="Resumen"
                    auto-grow
                    rows = "2"
                    outlined
                  ></v-textarea>
                </ValidationProvider>
              </v-col>
            </v-row>


            <v-row>
              <v-spacer/>
              <v-spacer/>
              <v-col>
                <v-btn color="green darken-1" dark class="mr-4" @click="submit">Someter</v-btn>
                <v-btn @click="clear">Borrar</v-btn>
              </v-col>
            </v-row>
            
          </v-container>
        </form>
      </ValidationObserver>
    </v-card-text>
  </v-card>
</template>

<script>
  import { required, email, max, alpha_spaces, alpha, alpha_dash, regex,required_if, is_not } from 'vee-validate/dist/rules'
  import { extend, ValidationObserver, ValidationProvider, setInteractionMode } from 'vee-validate'

  setInteractionMode('eager')

  extend('required', {
    ...required,
    message: '{_field_} no puede estar vacio',
  })

  extend('max', {
    ...max,
    message: '{_field_} no puede contener mas de {length} caracteres',
  })
 

  extend('alpha',{
    ...alpha,
    message: "{_field_} solamente debe tener caracteres",
  })

  extend('alpha_spaces',{
    ...alpha_spaces,
    message: "{_field_} solamente debe contener caracters,guiones y/o espacios",
  })
  
  extend('regex',{
    ...regex,
    message:"El campos es invalido",
  })
 

  export default {
    components: {
      ValidationProvider,
      ValidationObserver,
    },
    data: () => ({
      
			date:'2020-04-18', 
			locality:'Casa',
			localities:['Casa','Afuera'],
			venue:'Mangual',
			teamSport:'Baloncesto-masculino',		
      opponent_name:'Tornados',
      eventSummary:'El juego fue entretenido!',
      
			year:'2020',
			yearList:[],    
      
    }),

    created(){
      
      this.buildYearList()
      
    },   
  

    methods: {
      submit () {
        console.log(this.date) 
        console.log(this.teamSport)      
        this.$refs.observer.validate()
      },
      clear () {
				this.locality =''
				this.date = new Date().toISOString().substr(0,10)
				

        this.$refs.observer.reset()
      },
     
      buildYearList(){
        let yearToAdd = 2020
        let currentYear = new Date(2024,8).getFullYear()
        
        
        while(yearToAdd <= currentYear)
        {
            this.yearList.push(yearToAdd++)
        }
      },
      

      
    },
  }
</script>