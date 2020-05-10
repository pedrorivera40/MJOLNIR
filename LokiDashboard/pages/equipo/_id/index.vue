<template>
<v-container class="wrapper">
  <h1 class="primary_dark--text pl-3">Manejo de Equipos</h1>
    <div class="content-area pa-4 pt-12">
    <v-card>
      <v-toolbar
          color="green darken-1"
          dark
          flat
      >
        <v-spacer />
        <v-toolbar-title>{{sport_name}}</v-toolbar-title>
        <v-progress-linear
				:active="loadingQuery"
				indeterminate
				absolute
				bottom
				color = "white"
			></v-progress-linear>
        <v-spacer />
      </v-toolbar>
      <v-container>
        <v-col>
        </v-col>
        <v-row align="center">
          <v-col justify="center" align="center">
            <h1>Tarzanes</h1>
          </v-col>
        </v-row>
        <v-row align="center"
        justify="center">
          <v-col md=3>
            <v-select
              v-model="season"
              item-value="season_year" 
              item-text="season_year"
              :items="yearList" 
              label ="Temporada"
              prepend-icon="mdi-calendar-blank-multiple"
              :disabled = "loadingQuery"
              :loading = "loadingQuery"
              @input="getSeasonData"
            ></v-select>
          </v-col>
          <v-col>
            <v-row align="center"
              justify="end">
              <v-spacer />
              <v-col md=3 align="end">
                <v-btn color="primary_light" :disabled = "(loadingQuery ||(current_team == null)||(current_team == '')) || !$store.state.userAuth.userPermissions[14]['27']"
                  class="white--text" @click="goToEditTeam">Editar Equipo</v-btn>
              </v-col>
              <v-spacer />
              <v-col md=3 align="end">
                <v-btn color="primary_light" :disabled = "(loadingQuery ||(current_team == null)||(current_team == '')) || !$store.state.userAuth.userPermissions[12]['25']"
                  class="white--text" @click="removeTeamLocal">Remover Equipo</v-btn>
              </v-col>
              <v-spacer />
              <v-col md=3 align="end">
                <v-btn color="primary_light" :disabled = "loadingQuery || !$store.state.userAuth.userPermissions[13]['26']"
                  class="white--text" @click="goToCreateTeam">Añadir Equipo +</v-btn>
              </v-col>
              <v-spacer />
            </v-row>
          </v-col>
        </v-row>
        <v-tabs
            centered
        >
          <v-tabs-slider/>
          <v-tab>
              DESCRIPCIÓN
          </v-tab>

          <v-tab>
              ATLETAS
          </v-tab>

          <v-tab-item>
          
              <v-card class="mx-auto" outlined>								
                <v-container v-if="formated()">
                  <v-row align = "center" justify = "center">
                    <v-col justify = "center" align = "center">
                      <v-icon v-if="(current_team.team_image_url == null)||(current_team.team_image_url == '')" height="100"> mdi-account-group  </v-icon>
                      <v-img v-else :src="current_team.team_image_url" aspect-ratio="2"> 
                      </v-img>
                    </v-col>
                  </v-row>
                  <v-row>
                    <v-col v-if ="(current_team.about_team != null)&&(current_team.about_team != '')">
                      <h2> Sobre el Equipo: </h2>
                      <p>
                        {{current_team.about_team}}
                      </p>
                    </v-col>
                  </v-row>
                </v-container>
                <v-container v-else>
                  <v-row align = "center" justify = "center">
                    <v-col justify = "center" align = "center">
                      <h2>No Se Encontro Equipo</h2>
                    </v-col>
                  </v-row>
                </v-container>
              </v-card>
              
          </v-tab-item>

          <v-tab-item>
            <v-container v-if="formated_members()">
              <v-row align="center"
                justify="end">
                <v-col md=3 align="end">
                  <v-btn color="primary_light" :disabled = "(loadingQuery ||(current_team == null)||(current_team == '')) || !$store.state.userAuth.userPermissions[14]['27']"
                  class="white--text" @click="goToAddMembers">Añadir Miembro +</v-btn>
                </v-col>
              </v-row>
              <v-row
              v-for="member in members" 
              :key='member.athlete_id'
              align="center" justify="center"> 
                <v-col >
                  <v-hover
                    v-slot:default="{ hover }"
                    close-delay="200"
                  >
                    <AthleteCardSimple
                      :first_name="member.first_name"
                      :middle_name="member.middle_name"
                      :last_names="member.last_names"
                      :height_inches="member.height_inches"
                      :study_program="member.study_program"
                      :school_of_precedence="member.school_of_precedence"
                      :athlete_positions="member.athlete_positions"
                      :athlete_categories="member.athlete_categories"   
                      :number="member.number"
                      :profile_image_link="member.profile_image_link"
                      :athlete_id="member.athlete_id"
                      :years_of_participation="member.years_of_participation"
                    />
                  </v-hover>
                </v-col>
                <v-col align="center" justify="center" sm=1>
                  <v-hover
                    v-slot:default="{ hover }"
                    close-delay="200"
                  >
                    <v-icon x-large color="red darken-2" @click="removeTeamMemberLocal(member.athlete_id)">mdi-trash-can-outline </v-icon>
                  </v-hover>
                </v-col>
              </v-row>
            </v-container>
            <v-container v-else>
              <v-row align="center"
              justify="end">
              <v-col md=3 align="end">
                <v-btn color="primary_light" :disabled = "(loadingQuery ||(current_team == null)||(current_team == ''))"
                  class="white--text" @click="goToAddMembers">Añadir Miembro +</v-btn>
              </v-col>
            </v-row>
              <v-row align = "center" justify = "center">
                <v-col justify = "center" align = "center">
                  <h2>No Se Encontraron Miembros de Equipo</h2>
                </v-col>
              </v-row>
            </v-container>
          </v-tab-item>
        
        </v-tabs>
      </v-container>    
      <AddTeamModal
        v-if="dialogAddTeam"
        :dialog.sync="dialogAddTeam"
        :sport_id="sport_id"
        :season_year_prop.sync="season"
      />
      <UpdateTeamModal
        v-if="dialogEditTeam"
        :dialog.sync="dialogEditTeam"
        :sport_id="sport_id"
        :season_year="season"
        :about_team="current_team.about_team"
        :team_image_url="current_team.team_image_url"
      />
      <AddTeamMembersModal
        v-if="dialogAddTeamMember"
        :dialog.sync="dialogAddTeamMember"
        :sport_id="sport_id"
        :team_id="current_team_id"
        :season_year="season"
      />
      <DeleteTeamMemberModal
        v-if="dialogDeleteTeamMember"
        :dialog.sync="dialogDeleteTeamMember"
        :athlete_id="athlete_id_deletion"
        :team_id="current_team_id"
        :sport_id="sport_id"
        :season_year="season"
      />
      <DeleteTeamModal
        v-if="dialogDeleteTeam"
        :dialog.sync="dialogDeleteTeam"
        :sport_id="sport_id"
        :season_year="season"
      />
    </v-card>
    </div>
</v-container>
</template>

<script>
import EventCard from '@/components/EventCard'
import AthleteCardSimple from '@/components/AthleteCardSimple.vue'
import AddTeamModal from '@/components/AddTeamModal'
import AddTeamMembersModal from '@/components/AddTeamMembersModal'
import UpdateTeamModal from '@/components/UpdateTeamModal'
import DeleteTeamMemberModal from '@/components/DeleteTeamMemberModal'
import DeleteTeamModal from '@/components/DeleteTeamModal'
import {mapActions,mapGetters} from "vuex"

export default {
  components: {
    AthleteCardSimple,
    EventCard:EventCard,
    AddTeamModal,
    AddTeamMembersModal,
    UpdateTeamModal,
    DeleteTeamMemberModal,
    DeleteTeamModal
  },


    data: () =>({
      //Dialog support for component change
      dialogAddTeam:false,
      dialogEditTeam:false,
      dialogAddTeamMember:false,
      dialogDeleteTeam:false,
      dialogDeleteTeamMember:false,

      //NOTE: Using pre-written data for athlete with id:8,
      //      will need to fetch this data below from the API.
    
      // about_team:"Because he's the hero Gotham deserves, but not the one it needs right now, so we'll hunt him. Because he can take it, because he's not a hero. He's a silent guardian, a watchful protector, a Dark Knight.",

      sport_name:'',    
      //TODO: Check remove/change branch to dynamic (if necessary) 
			branch:'Masculino', 
      sport_id:'',
      sport_route:'',
			season:'',
      //For table
      headers:[],
      team_headers:[],
      //IMPORTANT FOR METHODS:
      selected: '',
      statistics_per_season:'',
      team_statistics_per_season:[],
      members:'',
      yearList:[],  
      defaultSelected:[],
      athlete_id_deletion:'',

      //SPORT DETERMINATION VARIABLES 
      BASKETBALL_IDM: 1,
      BASKETBALL_IDF: 10,
      VOLLEYBALL_IDM: 2,
      VOLLEYBALL_IDF: 12,
      BASEBALL_IDM: 4,
      SOFTBALL_IDF: 16, 
      SOCCER_IDM: 3,
      SOCCER_IDF: 11,

      current_team:'',
      current_team_id:'',
      events:[],
      ready_for_members: false,
      }),//end of data()
    
    created(){
      this.setNullTeam()
      this.setNullTeamMembers()
      // this.setNullMembersStats()
      // this.setNullTeamStats()
      this.current_team = null
      this.members = null
      // this.statistics_per_season = null
      // this.team_statistics_per_season = null
      
      
      
      this.buildYearList()
      this.buildDefaultValues()
      this.getSeasonData()
      // this.buildTable()
      
      
    }, 

		methods: {
      ...mapActions({
        getTeamByYear:"teams/getTeamByYear",
        getTeamMembers:"teams/getTeamMembers",
        stopGetMembers:"teams/stopGetMembers",
        stopGetMemberStats:"teams/stopGetMemberStats",
        stopGetTeamStats:"teams/stopGetTeamStats",
        setQueryLoading:"teams/setQueryLoading",
        getMemberStatistics:"teams/getMemberStatistics",
        getTeamStatistics:"teams/getTeamStatistics",
        setNullTeam:"teams/setNullTeam",
        setNullTeamMembers:"teams/setNullTeamMembers",
        setNullMembersStats:"teams/setNullMemberStats",
        setNullTeamStats:"teams/setNullTeamStats",
        removeTeam:"teams/removeTeam",
        removeTeamMember:"teams/removeTeamMember"
      }),
      
      formated(){
        if(this.team){
          this.current_team_id = this.team.team_info.team_id
          this.current_team = this.team.team_info
          
          if(this.readyForMembers){
            console.log("INDEX LEVEL LOCAL TEAM",this.current_team)
            console.log("INDEX LEVEL QUERY TEAM",this.team)
            this.getTeamMembers(this.current_team_id)
            this.stopGetMembers()
            // this.ready_for_members = false
          }
          // this.readyForMembers = false
          
          return true
        }
        else{
          this.team_members = null
          return false
        }
      },
      formated_members(){
        if(this.team_members){
          this.members = this.team_members.team_members
          return true
        }
        else{
          return false
        }
      },
      
      buildYearList(){
        let yearToAdd = 2020
        let currentYear = new Date(2023,8).getFullYear()
        this.season = currentYear
        
        while(yearToAdd <= currentYear)
        {
            this.yearList.push({'season_year':yearToAdd++})
        }
      },
      buildDefaultValues(){
        let currentYear = new Date(2023,8).getFullYear()
        this.defaultSelected.push({'season_year':currentYear})
        this.sport_id = this.$route.params.id
        if(this.sport_id == this.BASKETBALL_IDM || this.sport_id == this.BASKETBALL_IDF){this.sport_name = "Baloncesto", this.sport_route = "basketball"}
        else if(this.sport_id == this.VOLLEYBALL_IDM || this.sport_id == this.VOLLEYBALL_IDF){this.sport_name = "Voleibol",this.sport_route = "volleyball"}
        else if(this.sport_id == this.SOCCER_IDM || this.sport_id == this.SOCCER_IDF){this.sport_name = "Fútbol", this.sport_route = "soccer"}
        else if(this.sport_id == this.BASEBALL_IDM || this.sport_id == this.SOFTBALL_IDF){this.sport_name = "Beisbol", this.sport_route = "baseball"}
        else{this.sport_name = '', this.sport_route = ''}
        
      },
      goToEditTeam(){
        this.dialogEditTeam = true;
            // this.$router.push('/equipo/'+this.sport_id+'/editar/')
        },
      goToCreateTeam(){
        this.dialogAddTeam = true;
            // this.$router.push('/equipo/'+this.sport_id+'/crear/')
        },
      goToAddMembers(){
        this.dialogAddTeamMember = true;
            // this.$router.push('/equipo/'+this.sport_id+'/miembros/anadir/')
        },
      // TODO: Implement the removes so they probly create a pop up for confirmation?
      removeTeamMemberLocal(athlete_id){
        this.athlete_id_deletion = athlete_id;
        // console.log("Will Remove Athlete("+this.athlete_id_deletion+") from Team("+this.current_team.team_id+")")
        this.dialogDeleteTeamMember = true;
        },
      removeTeamLocal(){
            // console.log("Will Remove Team("+this.current_team.team_id+")")
            this.dialogDeleteTeam = true;
        },
     
			getSeasonData(){
        this.setQueryLoading()
        this.setNullTeam()
        this.setNullTeamMembers()
        // this.setNullMembersStats()
        // this.setNullTeamStats()
        this.current_team = null
        this.statistics_per_season = null
        this.team_statistics_per_season = null
        this.members = null
    
        const team_params = {
          sport_id: String(this.sport_id),
          season_year: String(this.season)
        }
        //console.log("At the index level inside the getSeasonData, request params look like",team_params)
        this.getTeamByYear(team_params)   			
			}
    },
    computed: {
			...mapGetters({
        team:"teams/team",
        team_members:"teams/team_members",
        readyForMembers:"teams/readyForMembers",
        readyForMemberStats:"teams/readyForMemberStats",
        loadingQuery: "teams/loadingQuery"
        // readyForTeamStats:"teams/readyForTeamStats",
        // member_statistics:"teams/member_statistics",
        // team_statistics:"teams/team_statistics"

			})
		}

}
</script>


<style lang="scss" scoped>
@import "@/assets/variables.scss";
.wrapper {
  height: 100%;

  .content-area {
    height: 100%;
    width: 100%;

    .table-actions {
      &:hover {
        color: $primary-color;
      }
    }
  }
}
</style>