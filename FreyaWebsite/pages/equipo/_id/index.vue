<template>
	<v-card>
		<v-toolbar
				color="green darken-1"
				dark
				flat
		>
			<v-spacer />
			<v-toolbar-title>{{sport_name}} - {{branch}}</v-toolbar-title>
      <v-progress-linear
				:active="loadingQuery||loadingEventQuery"
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
          <h1>{{branch_mascot}}</h1>
        </v-col>
      </v-row>
      <v-row align="center"
      justify="end">
        <v-col md=3>
          <v-select
            v-model="season"
            item-value="season_year" 
            item-text="season_year"
            :items="yearList" 
            label ="Temporada"
            prepend-icon="mdi-calendar-blank-multiple"
            :disabled ="loadingQuery||loadingEventQuery"
            :loading="loadingQuery||loadingEventQuery"
            @input="getSeasonData"
          ></v-select>
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

				<v-tab>
						ESTADÍSTICAS
				</v-tab>

        <v-tab>
						EVENTOS
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
									<v-col v-if = "current_team.about_team">
										<h2> Sobre el Equipo: </h2>
										<p>
											{{current_team.about_team}}
										</p>
									</v-col>
								</v-row>
							</v-container>
              <v-container v-else-if="!loadingQuery&&!loadingEventQuery">
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
            </v-row>
          </v-container>
          <v-container v-else-if="!loadingQuery&&!loadingEventQuery">
            <v-row align = "center" justify = "center">
              <v-col justify = "center" align = "center">
                <h2>No Se Encontraron Miembros de Equipo</h2>
              </v-col>
            </v-row>
          </v-container>
        </v-tab-item>
        
				<v-tab-item>
          <v-tabs
              centered
          >
            <v-tabs-slider/>
            <v-tab>
                POR ATLETA
            </v-tab>

            <v-tab>
                POR EQUIPO
            </v-tab>

            <!-- TODO: need to make it so the table "by athlete" has the season statistics OF EACH ATHLETE. Show athlete name and maaaybe pic. -->
            <!-- TODO: need to make it so the table "by team" doesnt have date, just the general statistics of the team for the season. -->
            <v-tab-item>		
              <v-container v-if="formated_member_stats()">		
                <v-card flat>
                  <!-- Basketball Table -->
                  <v-data-table 
                    dense 
                    :headers="headers" 
                    :items="statistics_per_season" 
                    item-key="statistics_per_season" 
                    class="elevation-1"								
                    loading-text="Recolectando Data...Por favor espere"
                    v-if="statistics_per_season != ''"
                  >		
                  <template #item.full_name="{ item }">{{ item.Athlete.first_name }} {{item.Athlete.middle_name}} {{ item.Athlete.last_names }}</template>	
                  </v-data-table>
                </v-card>
              </v-container>
              <v-container v-else-if="!loadingQuery&&!loadingEventQuery">
                <v-row align = "center" justify = "center">
                  <v-col justify = "center" align = "center">
                    <h2>No Se Encontraron Estadisticas Individuales</h2>
                  </v-col>
                </v-row>
              </v-container>
            
            </v-tab-item>
            <v-tab-item>
              <v-container v-if="formated_team_stats()">
                <v-card flat>
                  <v-data-table 
                    dense 
                    :headers="team_headers" 
                    :items="team_statistics_per_season" 
                    item-key="team_statistics_per_season" 
                    class="elevation-1"								
                    loading-text="Recolectando Data...Por favor espere"
                    v-if="team_statistics_per_season != ''"
                  >			
                  </v-data-table>
                </v-card>
              </v-container>
              <v-container v-else-if="!loadingQuery&&!loadingEventQuery">
                <v-row align = "center" justify = "center">
                  <v-col justify = "center" align = "center">
                    <h2>No Se Encontraron Estadisticas de Equipo</h2>
                  </v-col>
                </v-row>
              </v-container>
            </v-tab-item>
          </v-tabs>

        
        </v-tab-item>
        <v-tab-item>
          <v-container v-if="formated_events()">
          <!-- <v-container> -->
            <v-row>
              <v-col v-for="(value,key) in events" :key=key md="3">
            <!-- TODO: Hardcoded Details Need to Be eliminated -->
              <EventCardSimple      
                :eventID="value.id"     
                :eventDate="value.event_date"
                :opponentName='value.opponent_name'
                :localScore='value.local_score'
                :opponentScore='value.opponent_score' 
                :eventSummary='value.event_summary'
                v-if="events != ''"
              />        
              </v-col>
            </v-row>
          </v-container>
          <v-container v-else-if="!loadingQuery&&!loadingEventQuery">
            <v-row align = "center" justify = "center">
              <v-col justify = "center" align = "center">
                <h2>No Se Encontraron Eventos Para El Equipo</h2>
              </v-col>
            </v-row>
          </v-container>
        </v-tab-item>
			</v-tabs>
		</v-container>        
			
	</v-card>
</template>

<script>
import EventCardSimple from '~/components/EventCardSimple'
import AthleteCardSimple from '~/components/AthleteCardSimple.vue'

import {mapActions,mapGetters} from "vuex"

export default {
  components: {
    AthleteCardSimple,
    EventCardSimple:EventCardSimple
  },


    data: () =>({
    
      //NOTE: Using pre-written data for athlete with id:8,
      //      will need to fetch this data below from the API.
    
      about_team:"Because he's the hero Gotham deserves, but not the one it needs right now, so we'll hunt him. Because he can take it, because he's not a hero. He's a silent guardian, a watchful protector, a Dark Knight.",
      ready:false,
      sport_name:'',     
      //TODO: Check remove/change branch to dynamic (if necessary)
			branch:'', 
      sport_id:'',
      sport_route:'',
			season:'',
      //For table
      headers:[],
      team_headers:[],
      //IMPORTANT FOR METHODS:
      selected: '',
      statistics_per_season:'',
      team_statistics_per_season:'',
      members:'',
      yearList:[],  
      defaultSelected:[],

      BASKETBALL_IDM: 1,
      BASKETBALL_IDF: 10,
      VOLLEYBALL_IDM: 2,
      VOLLEYBALL_IDF: 12,
      BASEBALL_IDM: 4,
      SOFTBALL_IDF: 16, 
      SOCCER_IDM: 3,
      SOCCER_IDF: 11,
      // OTHER SPORTS (MEDAL BASED)
      ATHLETICS_IDM: 8,
      ATHLETICS_IDF: 19,
      //OTHER SPORTS (MATCH BASED)
      FIELD_TENNIS_IDM: 9,
      FIELD_TENNIS_IDF: 18,
      TABLE_TENNIS_IDM:7,
      TABLE_TENNIS_IDF:15,
    

      current_team:'',
      current_team_id:'',
      events:'',
      ready_for_members: false,

      branch_mascot:'',

      }),//end of data()
    
    created(){
      this.setNullTeam()
      this.setNullTeamMembers()
      this.setNullMembersStats()
      this.setNullTeamStats()
      this.setNullEvents()
      this.current_team = null
      this.members = null
      this.statistics_per_season = null
      this.team_statistics_per_season = null
      this.events = null
      
      
      
      this.buildYearList()
      this.buildDefaultValues()
      this.getSeasonData()
      this.buildTable()
      
      
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
        setNullEvents:"teams/setNullEvents",
        getTeamEvents:"teams/getTeamEvents",
        setEventQueryLoading:"teams/setEventQueryLoading",
      }),
      
      formated(){
        if(this.team){
          this.current_team_id = this.team.team_info.team_id
          this.sport_name = this.team.team_info.sport_name
          this.branch = this.team.team_info.branch_name
          if (this.branch == "Masculino"){this.branch_mascot = "Tarzanes"}
          else if(this.branch == "Femenino"){this.branch_mascot = "Juanas"}
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
          if(this.readyForMemberStats){
            console.log("INDEX LEVEL QUERY MEMBERS:",this.team.members)
            const team_params = {
              sport_id: String(this.sport_id),
              season_year: String(this.season),
              sport_route: String(this.sport_route)
            }
            console.log("INDEX LEVEL STAT PARAMS:",this.team_params)
            this.getMemberStatistics(team_params)
          }
          this.stopGetMemberStats()
          return true
        }
        else{
          return false
        }
      },
      formated_member_stats(){
        if(this.member_statistics){
          if(this.sport_id == this.BASKETBALL_IDM || this.sport_id == this.BASKETBALL_IDF){this.statistics_per_season = this.member_statistics.Basketball_Event_Season_Athlete_Statistics}
          else if(this.sport_id == this.VOLLEYBALL_IDM || this.sport_id == this.VOLLEYBALL_IDF){this.statistics_per_season = this.member_statistics.Volleyball_Event_Season_Athlete_Statistics}
          else if(this.sport_id == this.SOCCER_IDM || this.sport_id == this.SOCCER_IDF){this.statistics_per_season = this.member_statistics.Soccer_Event_Season_Athlete_Statistics}
          else if(this.sport_id == this.BASEBALL_IDM || this.sport_id == this.SOFTBALL_IDF){this.statistics_per_season = this.member_statistics.Baseball_Event_Season_Athlete_Statistics}
          else if (this.sport_id == this.ATHLETICS_IDM || this.sport_id == this.ATHLETICS_IDF){this.statistics_per_season = this.member_statistics.Medal_Based_Event_Season_Athlete_Statistics}
          else if (this.sport_id == this.FIELD_TENNIS_IDM || this.sport_id == this.FIELD_TENNIS_IDF
                || this.sport_id == this.TABLE_TENNIS_IDM || this.sport_id == this.TABLE_TENNIS_IDF){
                  this.statistics_per_season = this.member_statistics.Match_Based_Event_Season_Athlete_Statistics
                }
          else{
            this.statistics_per_season = null
            return false  
          }
          if(this.readyForTeamStats){
            console.log("INDEX LEVEL QUERY MEMBER STATS:",this.statistics_per_season)
            const team_params = {
              sport_id: String(this.sport_id),
              season_year: String(this.season),
              sport_route: String(this.sport_route)
            }
            console.log("STRAIGHT FROM MEMBERS= STATS, PARAMS ARE:",this.team.members)
            this.getTeamStatistics(team_params)
          }
          this.stopGetTeamStats()
          return true
        }
        else{
          return false
        }
      },

      formated_team_stats(){
        if(this.team_statistics){
          console.log("Team Statistics:",this.team_statistics)
          if(this.sport_id == this.BASKETBALL_IDM || this.sport_id == this.BASKETBALL_IDF){this.team_statistics_per_season = [this.team_statistics.Basketball_Event_Season_Team_Statistics]}
          else if(this.sport_id == this.VOLLEYBALL_IDM || this.sport_id == this.VOLLEYBALL_IDF){this.team_statistics_per_season = [this.team_statistics.Volleyball_Event_Season_Team_Statistics]}
          else if(this.sport_id == this.SOCCER_IDM || this.sport_id == this.SOCCER_IDF){this.team_statistics_per_season = [this.team_statistics.Soccer_Event_Season_Team_Statistics]}
          else if(this.sport_id == this.BASEBALL_IDM || this.sport_id == this.SOFTBALL_IDF){this.team_statistics_per_season = [this.team_statistics.Baseball_Event_Season_Team_Statistics]}
          else if (this.sport_id == this.ATHLETICS_IDM || this.sport_id == this.ATHLETICS_IDF){this.team_statistics_per_season = this.team_statistics.Medal_Based_Event_Season_Team_Statistics}
          else if (this.sport_id == this.FIELD_TENNIS_IDM || this.sport_id == this.FIELD_TENNIS_IDF
                || this.sport_id == this.TABLE_TENNIS_IDM || this.sport_id == this.TABLE_TENNIS_IDF){
                  this.team_statistics_per_season = this.team_statistics.Match_Based_Event_Season_Team_Statistics
                }
          else{
            this.team_statistics_per_season = null
            return false
          }
          // if(this.readyForEvents){
            console.log("INDEX LEVEL QUERY TEAM STATS:",this.team_statistics_per_season)
          //   // this.getTeamEvents(this.current_team_id)
          // }
          // this.stopGetEvents()
          return true
        }
        else{
          return false
        }
      },

      formated_events(){
        if (this.events != '' && this.events != null){
          return true
        }
        else{
          return false
        } 
      },

      buildTable(){
        // basketball
        if (this.sport_id == this.BASKETBALL_IDM || this.sport_id == this.BASKETBALL_IDF) {
          this.headers = [
            // {
            //   text:'Athlete',
            //   align: 'start',
            //   sortable: true,
            //   value: 'Athlete.first_name'
            // },
            {text: "Atleta", align:'start', sortable: true, value: "full_name" },
            {text: 'Asistencias', value: 'Event_Statistics.assists'},
            {text: 'Bloqueos', value: 'Event_Statistics.blocks'},
            {text: 'Intentos de Tiro de Campo', value: 'Event_Statistics.field_goal_attempt'},
            {text: 'Porcentaje de Tiro de Campo (%)', value: 'Event_Statistics.field_goal_percentage'},
            {text: 'Intentos de Tiro Libre', value: 'Event_Statistics.free_throw_attempt'},
            {text: 'Porcentaje de Tiro Libre (%)', value: 'Event_Statistics.free_throw_percentage'},
            {text: 'Puntos', value: 'Event_Statistics.points'},
            {text: 'Rebotes', value: 'Event_Statistics.rebounds'},
            {text: 'Robos', value: 'Event_Statistics.steals'},
            {text: 'Tiros de Campo Exitosos', value: 'Event_Statistics.successful_field_goal'},
            {text: 'Tiros Libres Exitosos', value: 'Event_Statistics.successful_free_throw'},
            {text: 'Tiros de Tres Puntos Exitosos', value: 'Event_Statistics.successful_three_point'},
            {text: 'Intentos de Tiro de Tres', value: 'Event_Statistics.three_point_attempt'},
            {text: 'Porcentaje de Tiro de Tres (%)', value: 'Event_Statistics.three_point_percentage'},
            {text: 'Perdidas de Balón', value: 'Event_Statistics.turnovers'},

            ]
            this.team_headers =
            [
            {text: 'Asistencias', value: 'Event_Statistics.assists'},
            {text: 'Bloqueos', value: 'Event_Statistics.blocks'},
            {text: 'Intentos de Tiro de Campo', value: 'Event_Statistics.field_goal_attempt'},
            {text: 'Porcentaje de Tiro de Campo (%)', value: 'Event_Statistics.field_goal_percentage'},
            {text: 'Intentos de Tiro Libre', value: 'Event_Statistics.free_throw_attempt'},
            {text: 'Porcentaje de Tiro Libre (%)', value: 'Event_Statistics.free_throw_percentage'},
            {text: 'Puntos', value: 'Event_Statistics.points'},
            {text: 'Rebotes', value: 'Event_Statistics.rebounds'},
            {text: 'Robos', value: 'Event_Statistics.steals'},
            {text: 'Tiros de Campo Exitosos', value: 'Event_Statistics.successful_field_goal'},
            {text: 'Tiros Libres Exitosos', value: 'Event_Statistics.successful_free_throw'},
            {text: 'Tiros de Tres Puntos Exitosos', value: 'Event_Statistics.successful_three_point'},
            {text: 'Intentos de Tiro de Tres', value: 'Event_Statistics.three_point_attempt'},
            {text: 'Porcentaje de Tiro de Tres (%)', value: 'Event_Statistics.three_point_percentage'},
            {text: 'Perdidas de Balón', value: 'Event_Statistics.turnovers'},
          ]
        }
        else if (this.sport_id == this.VOLLEYBALL_IDM || this.sport_id == this.VOLLEYBALL_IDF){
          this.headers = 
          [
          // {
          //     text:'Athlete',
          //     align: 'start',
          //     sortable: true,
          //     value: 'Athlete.first_name'
          // },
          {text: "Atleta", align:'start', sortable: true, value: "full_name" },
          {text: 'Puntos de Ataque', value: 'Event_Statistics.kill_points'},
          {text: 'Errores de Ataque', value: 'Event_Statistics.attack_errors'},
          {text: 'Asistencias', value: 'Event_Statistics.assists'},
          {text: 'Servicio Directo', value: 'Event_Statistics.aces'},
          {text: 'Errores de Servicios', value: 'Event_Statistics.service_errors'},
          {text: 'Recepciones', value: 'Event_Statistics.digs'},
          {text: 'Bloqueo', value: 'Event_Statistics.blocks'},
          {text: 'Errores De Bloqueo', value: 'Event_Statistics.blocking_errors'},
          {text: 'Errores de Recepcion', value: 'Event_Statistics.reception_errors'},

          ]
          this.team_headers =
          [
          {text: 'Puntos de Ataque', value: 'Event_Statistics..kill_points'},
          {text: 'Errores de Ataque', value: 'Event_Statistics..attack_errors'},
          {text: 'Asistencias', value: 'Event_Statistics..assists'},
          {text: 'Servicio Directo', value: 'Event_Statistics..aces'},
          {text: 'Errores de Servicio', value: 'Event_Statistics..service_errors'},
          {text: 'Recepciones', value: 'Event_Statistics..digs'},
          {text: 'Bloqueos', value: 'Event_Statistics..blocks'},
          {text: 'Errores de Bloqueo', value: 'Event_Statistics..blocking_errors'},
          {text: 'Errores de Recepcion', value: 'Event_Statistics..reception_errors'},
    
          ]
        }
        else if (this.sport_id == this.SOCCER_IDM || this.sport_id == this.SOCCER_IDF){
            this.headers = 
            [
            // {
            //     text:'Athlete',
            //     align: 'start',
            //     sortable: true,
            //     value: 'Athlete.first_name'
            // },
            {text: "Atleta", align:'start', sortable: true, value: "full_name" },
            {text: 'Intentos de Gol', value: 'Event_Statistics.goal_attempts'},
            {text: 'Asistencias', value: 'Event_Statistics.assists'},
            {text: 'Faltas', value: 'Event_Statistics.fouls'},
            {text: 'Tarjetas', value: 'Event_Statistics.cards'},
            {text: 'Goles Exitosos', value: 'Event_Statistics.successful_goals'},
            {text: 'Atajadas', value: 'Event_Statistics.tackles'},

            ]
            this.team_headers =
            [
            {text: 'Intentos de Gol', value: 'Event_Statistics.goal_attempts'},
            {text: 'Asistencias', value: 'Event_Statistics.assists'},
            {text: 'Faltas', value: 'Event_Statistics.fouls'},
            {text: 'Tarjetas', value: 'Event_Statistics.cards'},
            {text: 'Goles Exitosos', value: 'Event_Statistics.successful_goals'},
            {text: 'Atajadas', value: 'Event_Statistics.tackles'},
            
            ]
        }
        else if (this.sport_id == this.BASEBALL_IDM || this.sport_id == this.SOFTBALL_IDF){
            this.headers = 
            [
            // {
            //     text:'Athlete',
            //     align: 'start',
            //     sortable: true,
            //     value: 'Athlete.first_name'
            // },
            {text: "Atleta", align:'start', sortable: true, value: "full_name" },
            {text: 'Turnos al Bate', value: 'Event_Statistics.at_bats'},
            {text: 'Carreras', value: 'Event_Statistics.runs'},
            {text: 'Hits', value: 'Event_Statistics.hits'},
            {text: 'Carreras Empujadas', value: 'Event_Statistics.runs_batted_in'},
            {text: 'Bases por Bolas', value: 'Event_Statistics.base_on_balls'},
            {text: 'Ponches', value: 'Event_Statistics.strikeouts'},
            {text: 'Dejados en Base', value: 'Event_Statistics.left_on_base'},

            ]
            this.team_headers =
            [
            {text: 'Turnos al Bate', value: 'Event_Statistics.at_bats'},
            {text: 'Carreras', value: 'Event_Statistics.runs'},
            {text: 'Hits', value: 'Event_Statistics.hits'},
            {text: 'Carreras Empujadas', value: 'Event_Statistics.runs_batted_in'},
            {text: 'Bases por Bolas', value: 'Event_Statistics.base_on_balls'},
            {text: 'Ponches', value: 'Event_Statistics.strikeouts'},
            {text: 'Dejados en Base', value: 'Event_Statistics.left_on_base'},
            
            ]
          }
        else if (this.sport_id == this.ATHLETICS_IDM || this.sport_id == this.ATHLETICS_IDF){
          this.headers = 
          [
          {text: "Atleta", align:'start', sortable: true, value: "full_name" },
          {text: 'Categoria', value: 'Event_Statistics.category_name'},
          {text: 'Tipo de Medalla', value: 'Event_Statistics.type_of_medal'},
          {text: 'Numero de Medallas', value: 'Event_Statistics.medals_earned'},


          ]
          this.team_headers = 
          [
          {text: 'Categoria', value: 'Event_Statistics.category_name'},
          {text: 'Tipo de Medalla', value: 'Event_Statistics.type_of_medal'},
          {text: 'Numero de Medallas', value: 'Event_Statistics.medals_earned'},
          ]
        }
        else if (this.sport_id == this.FIELD_TENNIS_IDM || this.sport_id == this.FIELD_TENNIS_IDF
            || this.sport_id == this.TABLE_TENNIS_IDM || this.sport_id == this.TABLE_TENNIS_IDF){
            this.headers = 
            [
            {text: "Atleta", align:'start', sortable: true, value: "full_name" },
            {text: 'Categoria', value: 'Event_Statistics.category_name'},
            {text: 'Partidas Jugadas', value: 'Event_Statistics.matches_played'},
            {text: 'Partidas Ganadas', value: 'Event_Statistics.matches_won'},


            ]
            this.team_headers = 
            [
            {text: 'Categoria', value: 'Event_Statistics.category_name'},
            {text: 'Partidas Jugadas', value: 'Event_Statistics.matches_played'},
            {text: 'Partidas Ganadas', value: 'Event_Statistics.matches_won'},
            ]
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
        if(this.sport_id == this.BASKETBALL_IDM || this.sport_id == this.BASKETBALL_IDF){this.sport_route = "basketball"}
        else if(this.sport_id == this.VOLLEYBALL_IDM || this.sport_id == this.VOLLEYBALL_IDF){this.sport_route = "volleyball"}
        else if(this.sport_id == this.SOCCER_IDM || this.sport_id == this.SOCCER_IDF){this.sport_route = "soccer"}
        else if(this.sport_id == this.BASEBALL_IDM || this.sport_id == this.SOFTBALL_IDF){this.sport_route = "baseball"}
        else if (this.sport_id == this.ATHLETICS_IDM || this.sport_id == this.ATHLETICS_IDF){this.sport_route = "medalbased"}
        else if (this.sport_id == this.FIELD_TENNIS_IDM || this.sport_id == this.FIELD_TENNIS_IDF
                || this.sport_id == this.TABLE_TENNIS_IDM || this.sport_id == this.TABLE_TENNIS_IDF){this.sport_route ="matchbased"}
        else{this.sport_route = ''}
        console.log("[SPORT ROUTE CONFIRMED]",this.sport_route)
      },
			async getSeasonData(){
          this.setQueryLoading()
          this.setNullTeam()
          this.setNullTeamMembers()
          this.setNullMembersStats()
          this.setNullTeamStats()
          this.setNullEvents()
          this.current_team = null
          this.statistics_per_season = null
          this.team_statistics_per_season = null
          this.members = null
          this.events = null
          const team_params = {
            sport_id: String(this.sport_id),
            season_year: String(this.season)
          }
          //console.log("At the index level inside the getSeasonData, request params look like",team_params)
          await this.getTeamByYear(team_params)   
          await this.setEventQueryLoading()
          await this.getTeamEvents(this.current_team_id)
          if (this.team_events){
            console.log("Team Events (INDEX):",this.team_events)
            this.events = this.team_events.Events
          }
          // this.getMemberStatistics(team_params)    
          // this.getTeamStatistics(team_params)   
			}
    },

    computed: {
      // current_team: {
      //   // getter
      //   get: function () {
      //     return this.team
      //   },
      //   // setter
      //   set: function (newValue) {
      //     var names = newValue.split(' ')
      //     this.firstName = names[0]
      //     this.lastName = names[names.length - 1]
      //   }
      // },
			...mapGetters({
        team:"teams/team",
        team_members:"teams/team_members",
        readyForMembers:"teams/readyForMembers",
        readyForMemberStats:"teams/readyForMemberStats",
        readyForTeamStats:"teams/readyForTeamStats",
        loadingQuery:"teams/loadingQuery",
        member_statistics:"teams/member_statistics",
        team_statistics:"teams/team_statistics",
        team_events:"teams/team_events",
        loadingEventQuery:"teams/loadingEventQuery"
        

			})
		}

		// mounted(){
      
    
    //   // // console.log("The request will have:",this.sport_id,this.season)
    //   // const team_params = {
    //   //   sport_id: String(this.sport_id),
    //   //   season_year: String(this.season)
    //   // }
    //   // // console.log("At the index level, request params look like",team_params)
    //   // this.getTeamByYear(team_params)
      
    //   // // console.log("WE GOT THE TEAM BOI (from index):",this.team)
		// }
}
</script>