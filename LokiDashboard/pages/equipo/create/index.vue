<template>
  <v-card width="800" class="elevation-12 mx-auto">
    <v-toolbar color="green darken-1" dark flat>
        <v-toolbar-title>Crear Equipo {{sport}} - {{branch}}</v-toolbar-title>
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
                                Temporada:
                            </h2>
                            </div> 
                        </v-row>
                        <v-row 
                        align ="center"
                        justify = "center"
                        >
                            <v-col                   
                            >
                                <!-- TODO: (Herbert) Verify just how to validate this so it's REQUIRED / NOT NULL -->
                                <v-select
                                v-model="season_year"
                                :items="yearList"
                                label ="Año de Temporada"
                                prepend-icon="mdi-calendar-blank-multiple"
                                ></v-select>
                            </v-col>
                        </v-row>    
                    </v-col>  
                    <v-col>
                        <v-row>
                            <h2>Imagen de Equipo:</h2>
                            </v-row>
                            <v-row 
                            align ="center"
                            justify = "center"
                            >
                            <v-col  
                            >
                                <ValidationProvider v-slot="{ errors }" name="Enlace de Imagen de Equipo" rules="">
                                    <v-text-field
                                        v-model="team_image_url"
                                        :error-messages="errors"                    
                                        label="Enlace de Imagen de Equipo"
                                        prepend-icon="mdi-link"
                                        required
                                    ></v-text-field>
                                </ValidationProvider>
                            </v-col>
                        </v-row>
                    </v-col>
                </v-row>      
                <v-row>
                    <h2>Sobre el Equipo:</h2>
                </v-row>
                <v-row 
                align ="center"
                justify = "center"
                >
                    <v-col             
                    >
                        <ValidationProvider v-slot="{ errors }" name="SobreEquipo" rules="max:1000">
                            <v-textarea
                                v-model="about_team"                      
                                :counter="1000"
                                :error-messages="errors"
                                label="Breve Descripcion Del Equipo"
                                auto-grow
                                rows = "3"
                                outlined
                            ></v-textarea>
                        </ValidationProvider>
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
    import { required, email, max, alpha_spaces, alpha, alpha_dash, regex,required_if } from 'vee-validate/dist/rules'
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
        sports:['Voleibol','Baloncesto','Atletismo'],
        branch:'Masculino',
        branches:['Masculino','Femenino','Otro'],
      
        season_year:'',
        yearList:[],
    }),
           
      
      
    created(){
        this.buildYearList()
    }, 

    methods: {
        buildYearList(){
            let yearToAdd = 2020
            let currentYear = new Date(2023,8).getFullYear()
            this.season = currentYear
            
            while(yearToAdd <= currentYear)
            {
                this.yearList.push(yearToAdd++)
            }
        },
        submit () {
            this.$refs.observer.validate()
            this.goToTeam()
        },
        clear () {
            
            this.about_team='',
           
            this.season_year=0,
            this.team_image_url='',
            
            // TODO: (Herbert) Check how this works
            this.$refs.observer.reset()
        },
        updateCategories(key,value){
            console.log(key)
            console.log(!value)
            this.sport_category[key]=!value
            console.log(this.sport_category)
            
        },
        getVal(key)
        {
            return this.sport_category[key]
        },

        getSport(){
            return this.sport
        },
        goToTeam(){
             this.$router.push('/equipo/')
        }
    },
  }
    // The Only Arguments we need. 
    //{
    //"sport_id":1,   -->selected from existing
    //"season_year":"2020", --> selected from yearList
    //"team_image_url":"www.google.com" -->inserted
    //}
</script>