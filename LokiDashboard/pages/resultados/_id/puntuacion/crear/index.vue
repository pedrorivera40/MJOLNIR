<template>
  <v-card width="800" class="elevation-12 mx-auto">
    <v-toolbar color="green darken-1" dark flat>
        <v-toolbar-title>Crear Puntuacion Final {{sport}} - {{branch}}</v-toolbar-title>
        <v-spacer />
    </v-toolbar>
    <v-card-text>            
      <ValidationObserver ref="observer" v-slot="{ validate, reset }">
        <form>
            <v-container>  
                <v-row>
                    <v-col>
                        <v-row>      
                            <div>                  
                            <h2>
                                Puntuación de UPRM:
                            </h2>
                            </div> 
                        </v-row>
                        <v-row 
                        align ="center"
                        justify = "center"
                        >
                            <v-col                   
                            >
                                <ValidationProvider v-slot="{ errors }" name="UPRM Score" rules="numeric|required">
                                    <v-text-field
                                        v-model="payload_final_score.attributes.uprm_score"                      
                                        :error-messages="errors"
                                        label="Puntuación de UPRM"
                                        outlined
                                        required
                                    ></v-text-field>
                                </ValidationProvider>
                            </v-col>
                        </v-row>    
                    </v-col>  
                    <v-col>
                        <v-row>
                            <h2>Puntuación del Oponente:</h2>
                            </v-row>
                            <v-row 
                            align ="center"
                            justify = "center"
                            >
                            <v-col  
                            >
                                <ValidationProvider v-slot="{ errors }" name="Opponent Score" rules="numeric|required">
                                    <v-text-field
                                        v-model="payload_final_score.attributes.opponent_score"                      
                                        :error-messages="errors"
                                        label="Puntuación del Oponente"
                                        outlined
                                        required
                                    ></v-text-field>
                                </ValidationProvider>
                            </v-col>
                        </v-row>
                    </v-col>
                </v-row>      
                <v-row>
                    <v-spacer/>
                    <v-spacer/>
                    <v-col>
                        <v-btn class="mr-4" @click="submit">submit</v-btn>
                        <v-btn @click="clear">clear</v-btn>
                    </v-col>
                </v-row>   
            </v-container>
        </form>
      </ValidationObserver>
    </v-card-text>
  </v-card>
</template>

<script>
    import { required, email, max, alpha_spaces, alpha, alpha_dash, regex,required_if,numeric } from 'vee-validate/dist/rules'
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

  extend('email', {
    ...email,
    message: 'Email must be valid',
  })

  extend('alpha',{
    ...alpha,
    message: "{_field_} solamente debe tener caracteres",
  })

  extend('alpha_spaces',{
    ...alpha_spaces,
    message: "{_field_} solamente debe contener caracters,guiones y/o espacios",
  })
  extend('alpha_dash',{
    ...alpha_dash,
    message: "{_field_} puede contener un guiones",
  })
  extend('regex',{
    ...regex,
    message:"El campos es invalido",
  })
  extend('required_if',{
    ...required_if,
    message:"La posicion es requerida para este deporte",
  })
  extend('numeric',{
    ...numeric,
    message:"{_field_} solamente debe tener numeros",
  })
  

  export default {
    components: {
        ValidationProvider,
        ValidationObserver,
    },
    data: () => ({  
        date: new Date().toISOString().substr(0,10),
        about_team:'',
        team_image_url:'',
        sport_id:1,
        // TODO: (Herbert) Verificar como hacer que esto [sport and branch] sea dinamico, pasado por el sport previo
        sport:'Baloncesto',      
        branch:'Masculino',


        //NEEDED. 
        event_id:1, //get from route ?
    }),
           
      
      
    created(){
        this.initializeSportData()
    }, 

    methods: {
        initializeSportData(){
        //console.log(this.season)
        this.payload_final_score = {
        "event_id":this.event_id,
        "attributes":
            {
                "uprm_score":'',
                "opponent_score":''
            }
        }
        },


        async submit() {
            const isValid = await this.$refs.observer.validate()     
            if  (!isValid){
                //simply doesn't leave right now, think if want a box. 
            }
            else{
                if (this.payload_final_score.event_id != ''){
                    console.log(this.payload_final_score)
                    this.goToResults()
                }
                
            }
            
        },
        clear () {
            this.initializeSportData()
            // TODO: (Herbert) Check how this works
            this.$refs.observer.reset()
        },
        getSport(){
            return this.sport
        },
        goToResults(){
             this.$router.push('/resultados/')
        }
    },
  }
 
</script>