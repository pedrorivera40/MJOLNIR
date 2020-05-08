<template>
    <v-row justify="center">
        <v-dialog v-model="dialog" persistent max-width="600px">
            <v-card width="800" class="elevation-12 mx-auto">
                <v-toolbar color="green darken-1" dark flat>
                    <v-toolbar-title>Añadir Atleta a Equipo {{sport_name}} - {{branch}}</v-toolbar-title>
                    <v-spacer />
                </v-toolbar>
                <v-card-text>            
                
                    <v-form v-model="valid">
                        <v-container v-if="formated()">  
                            <v-row>
                                <v-col>
                                    <v-row>
                                        <template v-slot:progress>
                                        <v-progress-linear
                                            absolute
                                            color="green lighten-3"
                                            height="4"
                                            indeterminate
                                        ></v-progress-linear>
                                        </template>
                                        
                                        <v-form>
                                        </v-form>
                                        <v-divider></v-divider>
                                    </v-row>
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
                                        <v-autocomplete
                                                v-model="members_to_add"
                                                :items="sport_athletes_local"
                                                filled
                                                chips
                                                color="blue-grey lighten-2"
                                                label="Select"
                                                item-text="fName"
                                                item-value="id"
                                                multiple
                                                >
                                                <template v-slot:selection="data">
                                                    <v-chip
                                                    v-bind="data.attrs"
                                                    :input-value="data.selected"
                                                    close
                                                    @click="data.select"
                                                    @click:close="remove_from_select(data.item)"
                                                    >
                                                    <v-avatar left>
                                                        <v-icon v-if="data.item.profilePicLink == null" height="100"> mdi-account  </v-icon>
                                                        <v-img v-else :src="data.item.profilePicLink"></v-img>
                                                    </v-avatar>
                                                    {{ data.item.fName }}
                                                    </v-chip>
                                                </template>
                                                <template v-slot:item="data">
                                                    <template v-if="typeof data.item !== 'object'">
                                                    <v-list-item-content v-text="data.item"></v-list-item-content>
                                                    </template>
                                                    <template v-else>
                                                    <v-list-item-avatar>
                                                        <v-icon v-if="data.item.profilePicLink == null" height="100"> mdi-account  </v-icon>
                                                        <v-img v-else :src="data.item.profilePicLink"></v-img>
                                                    </v-list-item-avatar>
                                                    <v-list-item-content>
                                                        <v-list-item-title v-html="data.item.fName"></v-list-item-title>
                                                    </v-list-item-content>
                                                    </template>
                                                </template>
                                                </v-autocomplete>
                                        </v-col>
                                    </v-row>    
                                </v-col>  
                            </v-row>      
                            <!-- <v-row justify="end">
                                <v-spacer/>
                                <v-spacer/>
                                <v-col>
                                    <v-btn color="primary ligthen-1" text @click="close()">close</v-btn>
                                </v-col>
                                <v-col>
                                    <v-btn color="primary ligthen-1" text @click="submit" :loading="loadingQuery">submit</v-btn>
                                </v-col>
                            </v-row>    -->
                        </v-container>
                        <v-container v-else>
                            <v-row align = "center" justify = "center">
                                <v-col justify = "center" align = "center">
                                <h2>No Se Encontraron Atletas Para Añadir</h2>
                                </v-col>
                            </v-row>
                        </v-container>
                        <v-container>
                            <v-row justify="end">
                                <v-spacer/>
                                <v-spacer/>
                                <v-col>
                                    <v-btn color="primary ligthen-1" text @click="close()">close</v-btn>
                                </v-col>
                                <v-col>                                                         
                                    <v-btn color="primary ligthen-1" text @click="submit" :loading="(loadingQuery&&formated())" >submit</v-btn>
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
        props:{
            dialog:Boolean,
            sport_id:Number,
            team_id:Number,
            season_year: Number
        },
        data: () => ({
            valid:false,
            // sport_id:'',
            sport_route:'',
            // team_id:28,
            // TODO: (Herbert) Verificar como hacer que esto [sport and branch] sea dinamico, pasado por el sport previo
            sport_name:'',  
            branch:'',    
            sport_athletes_local:'',
            members_to_add:'',
            members_to_add_formatted:'',
            yearList:[],
            ready_for_members:'',
        }),
        created(){
            this.members_to_add = []
            this.members_to_add_formatted = []
            this.setSportAthletesNull()
            this.ready_for_members = true
            // this.buildDefaultValues()
            
            const athlete_params = {
                sport_id:Number(this.sport_id),
                team_id:Number(this.team_id)
            }
            this.setQueryLoading()
            console.log("THE DAMN PARAMS",athlete_params)
            this.getSportAthletes(athlete_params)
        },       
        methods: {
            ...rules,

        ...mapActions({
            setQueryLoading:"teams/setQueryLoading",
            addMembers:"teams/addMembers",
            getSportAthletes:"teams/getSportAthletes",
            setSportAthletesNull:"teams/setSportAthletesNull",
            setNullTeam:"teams/setNullTeam",
            setNullTeamMembers:"teams/setNullTeamMembers",
            getTeamByYear:"teams/getTeamByYear"
        }),
        buildDefaultValues(){
            this.sport_id = this.$route.params.id
            if(this.sport_id == this.BASKETBALL_IDM || this.sport_id == this.BASKETBALL_IDF){this.sport_name = "Baloncesto", this.sport_route = "basketball"}
            else if(this.sport_id == this.VOLLEYBALL_IDM || this.sport_id == this.VOLLEYBALL_IDF){this.sport_name = "Voleibol",this.sport_route = "volleyball"}
            else if(this.sport_id == this.SOCCER_IDM || this.sport_id == this.SOCCER_IDF){this.sport_name = "Fútbol", this.sport_route = "soccer"}
            else if(this.sport_id == this.BASEBALL_IDM || this.sport_id == this.SOFTBALL_IDF){this.sport_name = "Beisbol", this.sport_route = "baseball"}
            else{this.sport_name = '', this.sport_route = ''}
        },
        formated(){
            if(this.sport_athletes){
                console.log("im out here waddup the ready is",this.ready_for_members)
                if(this.ready_for_members){
                    console.log("got in whats up",this.sport_athletes)
                    this.sport_athletes_local = this.sport_athletes
                    this.ready_for_members = false
                }
                return true
            }
            else{
                return false
            }
        },
        remove_from_select (item) {
            const index = this.members_to_add.indexOf(item.athlete_id)
            if (index >= 0) this.members_to_add.splice(index, 1)
        },
        close() {
            this.$emit("update:dialog", false);
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
        async submit () {
            var i;
            console.log("Going to add the members here!",this.members_to_add)
            this.members_to_add_formatted = []
            for (i = 0; i < this.members_to_add.length; i++) {
                const array_parameter = {
                    athlete_id: Number(this.members_to_add[i])
                }
                this.members_to_add_formatted.push(array_parameter);
            }

            const athlete_params = {
                team_id: Number(this.team_id),
                team_members: this.members_to_add_formatted
            }
            console.log("Going to add athletes to team with id "+this.team_id+".")
            console.log("Yeah yeah params 1",this.members_to_add_formatted)
            console.log("Yeah yeah params 2",athlete_params)
            await this.setQueryLoading()
            await this.addMembers(athlete_params)
            await this.getSeasonDataPost()
            this.close()
        },

        goToTeam(){
             this.$router.push('/equipo/')
        }
    },
    computed: {
	    ...mapGetters({
            sport_athletes:"teams/sport_athletes",
            loadingQuery:"teams/loadingQuery"
        })
    }
  }
    // The Only Arguments we need. 
    //{
    //"sport_id":1,   -->selected from existing
    //"season_year":"2020", --> selected from yearList
    //"team_image_url":"www.google.com" -->inserted, optional
    //"about_team": "some text" --> inserted, optional
    //}
</script>