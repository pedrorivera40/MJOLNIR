<template>
<!-- TODO: Verify how to pass the team ID, if by route or some other way -->
<!-- TODO: Check/Confirm that query exists in order to get all athletes of one sport, at least the name fields + ID -->
<!-- TODO: Check how to make field dynamic in order to add multiple, and be able to remove some from addlist before adding/submitting. -->
<!-- TODO: instead of a list of all athletes in sport, it could be a search...no idea how to do that though. -->
  <v-card width="800" class="elevation-12 mx-auto">
    <v-toolbar color="green darken-1" dark flat>
        <v-toolbar-title>Añadir Atleta a Equipo {{sport}} - {{branch}}</v-toolbar-title>
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
                                Atleta:
                            </h2>
                            </div> 
                        </v-row>
                        <v-row 
                        align ="center"
                        justify = "center"
                        >
                            <v-col                   
                            >
                                <v-select
                                v-model="athlete"
                                :items="sport_athletes"
                                item-value="athlete_id" 
                                item-text="athlete_name"
                                label ="Atleta a Añadir"
                                prepend-icon="mdi-account-plus"
                                ></v-select>
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
        sport_id:1,
        team_id:1,
        // TODO: (Herbert) Verificar como hacer que esto [sport and branch] sea dinamico, pasado por el sport previo
        sport:'Baloncesto',      
        sports:['Voleibol','Baloncesto','Atletismo'],
        branch:'Masculino',
        branches:['Masculino','Femenino','Otro'],
        athlete: '',
        sport_athletes:[
            {
                athlete_name: "Bruce Wayne",
                athlete_id: "1"
            },
            {
                athlete_name: "Richard Grayson",
                athlete_id: "2"
            },
            {
                athlete_name: "Clark Kent",
                athlete_id: "3"
            },
            {
                athlete_name: "Hal Jordan",
                athlete_id: "4"
            },
            {
                athlete_name: "John Stewart",
                athlete_id: "5"
            },
            {
                athlete_name: "Wallace West",
                athlete_id: "6"
            },
            {
                athlete_name: "Arthur Curry",
                athlete_id: "7"
            },
            {
                athlete_name: "Jason Todd",
                athlete_id: "8"
            },
            {
                athlete_name: "Timothy Drake",
                athlete_id: "9"
            },
            {
                athlete_name: "Victor Stone",
                athlete_id: "10"
            },
            {
                athlete_name: "John Constantine",
                athlete_id: "11"
            },
            {
                athlete_name: "Simon Baz",
                athlete_id: "12"
            }
        ],
       
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
            console.log("Going to add athlete with id "+this.athlete+" to team with id "+this.team_id+".")
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
    //"team_image_url":"www.google.com" -->inserted, optional
    //"about_team": "some text" --> inserted, optional
    //}
</script>