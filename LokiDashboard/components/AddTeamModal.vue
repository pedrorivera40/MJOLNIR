<template>
    <v-row justify="center">
        <v-dialog v-model="dialog" persistent max-width="600px">
            <v-card width="800" class="elevation-12 mx-auto">
                <v-toolbar color="green darken-1" dark flat>
                    <v-toolbar-title>Crear Equipo {{sport_name}} - {{branch_name}}</v-toolbar-title>
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
                                            <!-- <v-select
                                                v-model="season"
                                                item-value="season_year" 
                                                item-text="season_year"
                                                :items="yearList" 
                                                label ="Temporada"
                                                prepend-icon="mdi-calendar-blank-multiple"
                                                :disabled = "loadingQuery"
                                                :loading = "loadingQuery"
                                                @input="getSeasonData"
                                            ></v-select> -->
                                            <v-select
                                                v-model="season_year"
                                                item-value="season_year" 
                                                item-text="season_year"
                                                :items="yearList"
                                                label ="Año de Temporada*"
                                                prepend-icon="mdi-calendar-blank-multiple"
                                                :rules="[seasonRequired('Temporada')]"
                                                
                                            ></v-select>
                                        </v-col>
                                    </v-row>    
                                </v-col>  
                            </v-row> 
                            <v-row>
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
                                            
                                            <v-textarea
                                                v-model="team_image_url"                  
                                                label="Enlace de Imagen de Equipo"
                                                auto-grow
                                                outlined
                                                rows = "1"
                                                :counter="1000"
                                                :rules="[maxSummaryLength('Enlace de Imagen de Equipo',1000)]"
                                            ></v-textarea>
                                            
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
                                            label="Breve Descripcion Del Equipo"
                                            auto-grow
                                            outlined
                                            rows = "3"
                                            :counter="1000"
                                            :rules="[generalPhrase('Breve Descripcion Del Equipo'),maxSummaryLength('Breve Descripcion Del Equipo',1000)]"
                                        ></v-textarea>
                                
                                </v-col>
                            </v-row>
                            <small>*indica un campo requirido.</small>
                            <v-row>
                                <v-spacer/>
                                <v-spacer/>
                                <v-col>
                                    <v-btn color="grey darken-3" text @click="close()" :disabled="loadingQuery">cancelar</v-btn>
                                </v-col>
                                <v-col>
                                    <v-btn color="grey darken-3" text @click="clear()" :disabled="loadingQuery">borrar</v-btn>
                                </v-col>
                                <v-col>
                                    <v-btn color="primary darken-1" text @click="submit" :loading="loadingQuery" :disabled="!valid">guardar</v-btn>
                                </v-col>
                            </v-row>   
                        </v-container>
                    </v-form>
                
                </v-card-text>
            </v-card>
        </v-dialog>
    </v-row>
</template>

<script>
    import rules from "@/utils/validations"  
    import {mapActions,mapGetters} from "vuex"
  
  

  export default {
      name:"AddTeamModal",
      props:{
        dialog: Boolean,
        sport_id: Number,
        season_year_prop: Number,
        sport_name: String,
        branch_name: String
        // season_year: Number
        // year_list: Array
      },
    data: () => ({
        //For Validation
        valid:false,

        sport_route:'',

        season:0,
        team_image_url:'',
        about_team:'',
        
        //PAYLOAD
        current_team:'',
        current_team_id:'',

        date: new Date().toISOString().substr(0,10),
        yearList:[],

        season_year:'',
        
    }),
           
      
      
    created(){
        this.buildYearList()
    }, 

    methods: {
        //TODO: will be removed
        buildYearList(){
            let yearToAdd = 2020
            let currentYear = new Date(2023,8).getFullYear()
            this.season = currentYear
            this.season_year = this.season_year_prop
            while(yearToAdd <= currentYear)
            {
                this.yearList.push(yearToAdd++)
            }
        },
        ...rules,

        ...mapActions({
            setQueryLoading:"teams/setQueryLoading",
            postTeam:"teams/postTeam",
            setNullTeam:"teams/setNullTeam",
            setNullTeamMembers:"teams/setNullTeamMembers",
            getTeamByYear:"teams/getTeamByYear",
        }),
      
        close() {
            this.$emit("update:dialog", false);
        },
        async submit () {
            this.setQueryLoading()
            let payload_edit = {
                "sport_id":Number(this.sport_id),
                "season_year":Number(this.season_year),
                "team_image_url":this.team_image_url,
                "about_team": this.about_team
            }
            // console.log("WHAT ARE THE CURRENT VALUES BEFORE QUERY???",payload_edit)
            await this.postTeam(payload_edit)
            await this.getSeasonDataPost()
    
            this.$emit("update:season_year_prop", this.season_year);
            this.close()

        },
        getSeasonDataPost(){
            this.setQueryLoading()
            this.setNullTeam()
            this.setNullTeamMembers()
            const team_params = {
                sport_id: String(this.sport_id),
                season_year: String(this.season_year)
            }
            //console.log("At the index level inside the getSeasonData, request params look like",team_params)
            this.getTeamByYear(team_params)   			
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
</script>