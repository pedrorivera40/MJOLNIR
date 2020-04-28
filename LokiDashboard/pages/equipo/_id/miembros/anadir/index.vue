<template>
<!-- TODO: Verify how to pass the team ID, if by route or some other way -->
<!-- TODO: Check/Confirm that query exists in order to get all athletes of one sport, at least the name fields + ID -->
<!-- TODO: Check how to make field dynamic in order to add multiple, and be able to remove some from addlist before adding/submitting. -->
<!-- TODO: instead of a list of all athletes in sport, it could be a search...no idea how to do that though. -->
  <v-card width="800" class="elevation-12 mx-auto">
    <v-toolbar color="green darken-1" dark flat>
        <v-toolbar-title>Añadir Atleta a Equipo {{sport_name}} - {{branch}}</v-toolbar-title>
        <v-spacer />
    </v-toolbar>
    <v-card-text>            
      
        <form>
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
                <v-row justify="end">
                    <v-btn class="mr-4" @click="submit">submit</v-btn>
                </v-row>   
            </v-container>
        </form>
     
    </v-card-text>
  </v-card>
</template>

<script>
    import rules from "../../../../../utils/validations"  
    import {mapActions,mapGetters} from "vuex"

  export default {
    components: {

    },
    data: () => ({
        valid:false,
        sport_id:'',
        sport_route:'',
        team_id:28,
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
        this.buildDefaultValues()
        this.setQueryLoading()
        this.getSportAthletes(this.sport_id)
    },       
    methods: {
        ...rules,

        ...mapActions({
            setQueryLoading:"teams/setQueryLoading",
            addMembers:"teams/addMembers",
            getSportAthletes:"teams/getSportAthletes",
            setSportAthletesNull:"teams/setSportAthletesNull"
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
    
        submit () {
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
            this.addMembers(athlete_params)
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