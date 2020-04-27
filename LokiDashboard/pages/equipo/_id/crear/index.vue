<template>
  <v-card width="800" class="elevation-12 mx-auto">
    <v-toolbar color="green darken-1" dark flat>
        <v-toolbar-title>Crear Equipo {{sport_name}} - {{branch}}</v-toolbar-title>
        <v-spacer />
    </v-toolbar>
    <v-card-text>            
      
        <v-form v-model="valid">
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
                                
                                    <v-text-field
                                        v-model="team_image_url"
                                        :error-messages="errors"                    
                                        label="Enlace de Imagen de Equipo"
                                        prepend-icon="mdi-link"
                                        required
                                    ></v-text-field>
                                
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
                        
                            <v-textarea
                                v-model="about_team"                      
                                :counter="1000"
                                :error-messages="errors"
                                label="Breve Descripcion Del Equipo"
                                auto-grow
                                rows = "3"
                                outlined
                                :rules="[generalPhrase('Breve Descripcion Del Equipo'),maxSummaryLength('Breve Descripcion Del Equipo',1000)]"
                            ></v-textarea>
                       
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
        </v-form>
      
    </v-card-text>
  </v-card>
</template>

<script>
    import rules from "../../../../utils/validations"  
    import {mapActions,mapGetters} from "vuex"
  
  

  export default {
    components: {
       
    },
    data: () => ({
        //For Validation
        valid:false,

        sport_route:'',
        // TODO: (Herbert) Verificar como hacer que esto [sport and branch] sea dinamico, pasado por el sport previo
        //USED FOR TEAM SUBMISSION:
        sport_id:'',
        sport_name:'',
        branch:'Masculino',
        // TODO: FIX ROUTE PARAMS. TEMPORARILY SELECTED LIKE THIS. NEED TO SOMEHOW GET IT FROM OTHER ROUTE.
        season_year:0,
        team_image_url:'',
        about_team:'',
        
        //PAYLOAD
        current_team:'',
        current_team_id:'',

        date: new Date().toISOString().substr(0,10),
        yearList:[],
        
    }),
           
      
      
    created(){
        this.setNullTeam()
        this.buildYearList()
        this.buildDefaultValues()
        this.setQueryLoading()
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
        ...rules,

        ...mapActions({
            setQueryLoading:"teams/setQueryLoading",
            postTeam:"teams/postTeam",
            setNullTeam:"teams/setNullTeam"
        }),

        buildDefaultValues(){
            this.sport_id = this.$route.params.id
            if(this.sport_id == this.BASKETBALL_IDM || this.sport_id == this.BASKETBALL_IDF){this.sport_name = "Baloncesto", this.sport_route = "basketball"}
            else if(this.sport_id == this.VOLLEYBALL_IDM || this.sport_id == this.VOLLEYBALL_IDF){this.sport_name = "Voleibol",this.sport_route = "volleyball"}
            else if(this.sport_id == this.SOCCER_IDM || this.sport_id == this.SOCCER_IDF){this.sport_name = "Fútbol", this.sport_route = "soccer"}
            else if(this.sport_id == this.BASEBALL_IDM || this.sport_id == this.SOFTBALL_IDF){this.sport_name = "Beisbol", this.sport_route = "baseball"}
            else{this.sport_name = '', this.sport_route = ''}
        },
        async submit () {
            let payload_edit = {
                "sport_id":Number(this.sport_id),
                "season_year":Number(this.season_year),
                "team_image_url":this.team_image_url,
                "about_team": this.about_team
            }
            console.log(Number(this.sport_id))
            console.log(parseInt(this.sport_id))
            console.log(this.sport_id)
            console.log("WHAT ARE THE CURRENT VALUES BEFORE QUERY???",payload_edit)
            this.postTeam(payload_edit)
            // this.goToTeam()
            // }
        },
        clear () {
            this.about_team='',
            this.season_year=0,
            this.team_image_url=''
        },
        
        
        goToTeam(){
            this.$router.push('/equipo/'+this.sport_id)
        }
    },
    computed: {
	    ...mapGetters({
            team:"teams/team",
            loadingQuery:"teams/loadingQuery"
        })
    }
  }
    // The Only Arguments we need. 
    //{
    //"sport_id":1,   -->selected from existing
    //"season_year":"2020", --> selected from yearList
    //"team_image_url":"www.google.com" -->inserted
    //}
</script>