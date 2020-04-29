<template>
    <v-row justify="center">
        <v-dialog v-model="dialog" persistent max-width="600px">
            <v-card width="800" class="elevation-12 mx-auto">
                <v-toolbar color="green darken-1" dark flat>
                    <v-toolbar-title>Editar Equipo {{sport_name}} - {{branch}}</v-toolbar-title>
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
                                            <!-- <v-select
                                                v-model="season_year"
                                                :items="yearList"
                                                label ="Año de Temporada"
                                                prepend-icon="mdi-calendar-blank-multiple"
                                            ></v-select> -->
                                            <v-text-field
                                                v-model="season_year"
                                                disabled
                                                readonly
                                                solo
                                                prepend-icon="mdi-calendar-blank-multiple"
                                            ></v-text-field>
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
                                        <v-col>
                                            <v-text-field
                                                v-model="team_image_url"
                                                label="Enlace de Imagen de Equipo"
                                                prepend-icon="mdi-link"
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
                                        label="Breve Descripcion Del Equipo"
                                        auto-grow
                                        rows = "3"
                                        :rules="[generalPhrase('Breve Descripcion Del Equipo'),maxSummaryLength('Breve Descripcion Del Equipo',1000)]"
                                    ></v-textarea>
                                </v-col>
                            </v-row>

                            <v-row>
                                <v-spacer/>
                                <v-spacer/>
                                <v-col>
                                    <v-btn color="primary ligthen-1" text @click="close()">close</v-btn>
                                </v-col>
                                <v-col>
                                    <v-btn color="primary ligthen-1" text @click="submit" :loading="loadingQuery">submit</v-btn>
                                </v-col>
                                <v-col>
                                    <v-btn color="primary ligthen-1" text @click="clear">clear</v-btn>
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
      name:"UpdateTeamModal",
    props:{
        dialog: Boolean,
        sport_id: Number,
        season_year: Number,
        about_team: String,
        team_image_url: String,

    },
    data: () => ({
        //For Validation
        valid:false,


        sport_route:'',
        // TODO: (Herbert) Verificar como hacer que esto [sport and branch] sea dinamico, pasado por el sport previo
        //USED FOR TEAM SUBMISSION:
        // sport_id:'',
        sport_name:'',
        branch:'Masculino',
        // TODO: FIX ROUTE PARAMS. TEMPORARILY SELECTED LIKE THIS. NEED TO SOMEHOW GET IT FROM OTHER ROUTE.
        // season_year:2020,
        // team_image_url:'',
        // about_team:'',

        //PAYLOAD
        current_team:'',
        current_team_id:'',
        ready_for_edit:'',
    }),



    created(){
        if (this.about_team == null){
            this.about_team = ''
        }
        if (this.team_image_url == null){
            this.team_image_url = ''
        }
        // this.setNullTeam()
        // this.ready_for_edit = true
        // this.buildDefaultValues()
        // this.setQueryLoading()
        // const team_params = {
        //   sport_id: String(this.sport_id),
        //   season_year: String(this.season_year)
        // }
        // this.getTeamByYearSimple(team_params)
    },

    methods: {
        ...rules,

        ...mapActions({
            getTeamByYearSimple:"teams/getTeamByYearSimple",
            setQueryLoading:"teams/setQueryLoading",
            editTeam:"teams/editTeam",
            setNullTeam:"teams/setNullTeam",
            getTeamByYearSimple:"teams/getTeamByYearSimple"

        }),

        formated(){
            if(this.team){
                // console.log("im out here waddup the ready is",this.ready_for_edit)
                if(this.ready_for_edit){
                    // console.log("got in whats up")
                    this.current_team_id = this.team.team_info.team_id
                    this.about_team = this.team.team_info.about_team
                    this.team_image_url = this.team.team_info.team_image_url
                    this.ready_for_edit = false
                }
                return true
            }
            else{
                return false
            }
        },

        buildDefaultValues(){
            this.sport_id = this.$route.params.id
            if(this.sport_id == this.BASKETBALL_IDM || this.sport_id == this.BASKETBALL_IDF){this.sport_name = "Baloncesto", this.sport_route = "basketball"}
            else if(this.sport_id == this.VOLLEYBALL_IDM || this.sport_id == this.VOLLEYBALL_IDF){this.sport_name = "Voleibol",this.sport_route = "volleyball"}
            else if(this.sport_id == this.SOCCER_IDM || this.sport_id == this.SOCCER_IDF){this.sport_name = "Fútbol", this.sport_route = "soccer"}
            else if(this.sport_id == this.BASEBALL_IDM || this.sport_id == this.SOFTBALL_IDF){this.sport_name = "Beisbol", this.sport_route = "baseball"}
            else{this.sport_name = '', this.sport_route = ''}
        },
        close() {
            this.$emit("update:dialog", false);
        },
        async submit () {
            let payload_edit = {
                "sport_id":Number(this.sport_id),
                "season_year":Number(this.season_year),
                "team_image_url":this.team_image_url,
                "about_team":this.about_team
            }
            console.log(payload_edit)
            await this.setQueryLoading()
            await this.editTeam(payload_edit)
            await this.getSeasonDataUpdate()
            // while(this.loadingQuery){}
      
            this.close()
            // this.goToTeam()
            // }
        },
        clear () {
            this.about_team='',
            this.team_image_url=''
        },
        getSeasonDataUpdate(){
            this.setQueryLoading()
            this.setNullTeam()
            // this.setNullMembersStats()
            // this.setNullTeamStats()
        
            const team_params = {
                sport_id: String(this.sport_id),
                season_year: String(this.season_year)
            }
            //console.log("At the index level inside the getSeasonData, request params look like",team_params)
            this.getTeamByYearSimple(team_params)   			
        },
        goToTeam(){
             this.$router.push('/equipo/'+sport_id)
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