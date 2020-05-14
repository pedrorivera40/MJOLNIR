<template>
  <v-container class="wrapper" v-if="formated_event_info()">
    <v-container v-if="formated_event_info()">
        <h1 class="primary_dark--text pl-3">Resultados {{sport_name}} {{branch_name_local}}</h1>
        <!-- TODO: HOW TO MAKE THIS SIMPLER FORMAT DATE? -->
        <h3>Evento de {{event_date}}</h3>
    </v-container>
    <div class="content-area pa-4 pt-12">
        <v-container  v-if="formated_member_stats()">
            <v-row align="center" justify="center">
            <v-card width=400 class="mx-lg-auto" outlined>
                <v-card-title>
                    <v-row justify="center">
                        <h3>Puntuación Final</h3>
                    </v-row>
                    </v-card-title>
                <v-container>
                    <v-row v-if="formated_final_score()">  
                        <v-col >
                            <v-row justify="center">
                                <h1>{{uprm_score}}</h1>
                            </v-row>
                            <v-row justify="center">
                                <h3>UPRM</h3>
                            </v-row>
                        </v-col>
                        
                        <v-col align="center">
                            <v-row justify="center">
                                <h2>-</h2>
                            </v-row>
                        </v-col>
                        
                        <v-col>
                            <v-row justify="center">
                                <h1>{{opponent_score}}</h1>
                            </v-row>
                            <v-row justify="center">
                                <h3 v-if="opponent_name">{{opponent_name}}</h3>
                                <h3 v-else>Oponente</h3>
                            </v-row>
                        </v-col>
                        
                    </v-row>
                    <v-row v-else-if="loadingQuery" justify = center>
                        <!-- <v-progress-circular
                            :active="loadingQuery"
                            indeterminate
                            :size="50"
                            color="primary"
                        ></v-progress-circular> -->
                        <v-progress-linear
                            :active="loadingQuery"
                            indeterminate
                            absolute
                            bottom
                            color = "primary"
                        ></v-progress-linear>
                    </v-row>
                    <v-row v-else-if="!loadingQuery" justify="center">
                        <v-col align="center">
                            <h3>No Hay Puntuación Final Disponible</h3>
                        </v-col>
                    </v-row>
                </v-container>
            </v-card>   
            </v-row> 
            <v-container>  
                <v-tabs centered>
                    <v-tabs-slider/>
                    <v-tab>
                        POR ATLETA
                    </v-tab>

                    <v-tab>
                        POR EQUIPO
                    </v-tab>
                    <v-tab-item>
                        <v-card>
                            <!-- :headers="headers"
                            :items="users"
                            :search="search"
                            :loading="isLoadingU" -->
                            <!-- THE SPORTS STATS TABLE TABLE! -->
                            <v-data-table
                            dense 
                            :headers="headers" 
                            :items="payload_stats.athlete_statistic"
                            item-key="payload_stats.athlete_statistic" 
                            class="elevation-1"	
                            v-if="formated_event_info()||formated_member_stats()"
                            :loading="loadingQuery"	
                            loading-text="Cargando Estadísticas..."						
                            >
                            <template #item.full_name="{ item }">{{ item.athlete_info.first_name }} {{item.athlete_info.middle_name}} {{ item.athlete_info.last_names }}</template>
                            </v-data-table>
                            <v-container v-else-if="!loadingQuery">
                                <v-row align = "center" justify = "center">
                                <v-col justify = "center" align = "center">
                                    <h2>No Se Encontraron Resultados</h2>
                                </v-col>
                                </v-row>
                            </v-container>
                        </v-card>
                    </v-tab-item>
                    <v-tab-item>
                        <v-card>
                            <!-- :headers="headers"
                            :items="users"
                            :search="search"
                            :loading="isLoadingU" -->
                            <v-data-table
                            dense 
                            :headers="team_headers" 
                            :items="team_statistics"
                            item-key="team_statistics" 
                            class="elevation-1"	
                            v-if="formated_event_info()||formated_member_stats()"
                            :loading="loadingQuery"	
                            loading-text="Cargando Estadísticas..."							
                            >
                            </v-data-table>
                            <v-container v-else-if="!loadingQuery">
                                <v-row align = "center" justify = "center">
                                <v-col justify = "center" align = "center">
                                    <h2>No Se Encontraron Resultados de Equipo</h2>
                                </v-col>
                                </v-row>
                            </v-container>
                        </v-card>
                    </v-tab-item>
                </v-tabs>
            </v-container>
        </v-container>
        <v-container v-else>
            <v-row justify = center>
                <v-progress-circular
                    :active="loadingQuery"
                    indeterminate
                    :size="50"
                    color="primary"
                ></v-progress-circular>
                <!-- <v-progress-linear
                    :active="loadingQuery"
                    indeterminate
                    absolute
                    bottom
                    color = "primary"
                ></v-progress-linear> -->
            </v-row>
        </v-container>
    </div>
    
  </v-container>
  <v-container v-else-if="!loadingQuery">
    <v-row justify="center">
        <v-col align="center">
            <h3>Evento No Existe</h3>
        </v-col>
    </v-row>
  </v-container>
</template>

<script>
import { mapActions, mapGetters } from "vuex";
export default {
  data() {
    return {     
    //   headers: [
    //     {
    //       text: "ID",
    //       align: "start",
    //       sortable: false,
    //       value: "id"
    //     },
    //     { text: "Full Name", value: "full_name" },
    //     { text: "Username", value: "username" },
    //     { text: "Email", value: "email" },
    //     { text: "Account Status", value: "is_active" },
    //     { text: "Password", value: "password" },
    //     { text: "Actions", value: "actions", sortable: false }
    //   ],
      defaultItem: {
        full_name: "",
        username: "",
        email: "",
        is_active: "",
        id: 0
      },
      //====NEW/MODIFIED STUFF==========
      headers:[],
      team_headers:[],
      statistics_per_season:"",
      team_statistics:'',
    //   search_individual: "",
      sport_id:'',
      sport_route:'',
      sport_name: '',
      event_id:'',
      event_date:'',
    //   event_info:'',
      opponent_score:'',
      opponent_name:'', //TODO: MAKE THIS VALUE DYNAMIC
      uprm_score:'',
      payload_stats:'',
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
      //season:''
      //INTEGRATION QUERY VARS
      ready_for_event:false,
      ready_for_stats:true,

      branch_name_local:'',
    };
  },
  
created(){
    this.setQueryLoading()
    this.clearEventInfo()
    this.clearAllStats()
    this.ready_for_stats=true
    this.event_id = this.$route.params.id
    console.log("[1] GOT EVENT ID",this.event_id)
    this.getEventInfo(this.event_id)
    console.log("[2] GOT EVENT INFO",this.event_info)

    // const stat_params = {
    //     event_id: String(this.event_id),
    //     sport_route: String(this.sport_route)
    // }
    // this.getAllEventStatistics(this.stat_params)
    // console.log("[4] GOT EVENT STATS",this.results_payload)

    // this.buildTable()
    // console.log("[3] BUILT TABLE",this.results_payload)
 
}, 
  methods: {
    ...mapActions({
        getAllEventStatistics:"results/getAllEventStatistics",
        getEventInfo:"results/getEventInfo",
        clearEventInfo:"results/clearEventInfo",
        clearAllStats:"results/clearAllStats",
        setQueryLoading:"results/setQueryLoading",
    }),
    formated_event_info(){
        console.log("the event info...(before)",this.results_payload)
        if(this.event_info){
            console.log("GETTING EVENT INFO (from formated method)",this.event_info)
            this.sport_id =  this.event_info.sport_id 
            this.sport_name = this.event_info.sport_name
            this.opponent_name = this.event_info.opponent_name
            this.event_date = this.event_info.event_date
            this.branch_name_local = this.event_info.branch
            if (this.ready_for_stats){
                this.buildTable()
                console.log("[3] BUILT TABLE",this.results_payload)
                this.buildDefaultValues()
                const stat_params = {
                    event_id: String(this.event_id),
                    sport_route: String(this.sport_route)
                }
                console.log("[4.(-1)] STAT PARAMS ARE (INDEX LEVEL)",stat_params)
                this.setQueryLoading()
                this.getAllEventStatistics(stat_params)
                console.log("[4] GOT EVENT STATS",this.results_payload)
                this.ready_for_stats = false
            }
            return true
        }
        else{
            return false
        }
    },
    formated_member_stats(){
        if(this.results_payload){
            console.log(" [5.(-1)] RESULTS PAYLOAD RECEIVED",this.results_payload)
            if(this.sport_id == this.BASKETBALL_IDM || this.sport_id == this.BASKETBALL_IDF){
                this.payload_stats = this.results_payload.Basketball_Event_Statistics
                if (this.payload_stats.team_statistics){
                    this.team_statistics = [this.payload_stats.team_statistics]
                }
                else this.team_statistics = []
            }
            else if(this.sport_id == this.VOLLEYBALL_IDM || this.sport_id == this.VOLLEYBALL_IDF){
                this.payload_stats = this.results_payload.Volleyball_Event_Statistics
                if (this.payload_stats.team_statistics){
                    this.team_statistics = [this.payload_stats.team_statistics]
                }
                else this.team_statistics = []
                }
            else if(this.sport_id == this.SOCCER_IDM || this.sport_id == this.SOCCER_IDF){
                this.payload_stats = this.results_payload.Soccer_Event_Statistics
                if (this.payload_stats.team_statistics){
                    this.team_statistics = [this.payload_stats.team_statistics]
                }
                else this.team_statistics = []
            }
            else if(this.sport_id == this.BASEBALL_IDM || this.sport_id == this.SOFTBALL_IDF){
                this.payload_stats = this.results_payload.Baseball_Event_Statistics
                if (this.payload_stats.team_statistics){
                    this.team_statistics = [this.payload_stats.team_statistics]
                }
                else this.team_statistics = []
            }
            else if (this.sport_id == this.ATHLETICS_IDM || this.sport_id == this.ATHLETICS_IDF){
                this.payload_stats = this.results_payload.Medal_Based_Event_Statistics
                this.team_statistics = []
                if(this.payload_stats.team_statistics.medal_based_statistics){
                    this.team_statistics = this.payload_stats.team_statistics.medal_based_statistics
                }
            }
            else if (this.sport_id == this.FIELD_TENNIS_IDM || this.sport_id == this.FIELD_TENNIS_IDF
                || this.sport_id == this.TABLE_TENNIS_IDM || this.sport_id == this.TABLE_TENNIS_IDF){
                this.payload_stats = this.results_payload.Match_Based_Event_Statistics
                this.team_statistics = []
                if(this.results_payload.Match_Based_Event_Statistics.team_statistics.match_based_statistics.Doble){
                    this.team_statistics.push({category_name:"Doble",statistics:this.results_payload.Match_Based_Event_Statistics.team_statistics.match_based_statistics.Doble})
                }
                if(this.results_payload.Match_Based_Event_Statistics.team_statistics.match_based_statistics.Solo){
                    this.team_statistics.push({category_name:"Solo",statistics:this.results_payload.Match_Based_Event_Statistics.team_statistics.match_based_statistics.Solo})
                }
            }
            else{
                this.payload_stats = null
                return false  
            }
            console.log("[5] WE SHOULD HAVE IT HERE!!!",this.payload_stats)
            // this.team_statistics = [this.payload_stats.team_statistics]
            this.opponent_score = (this.payload_stats.opponent_score)
            this.uprm_score = (this.payload_stats.uprm_score)
            return true
        }
        else{
          return false
        }
    },
    formated_final_score(){
        console.log("[FS] Do we have a final score?",this.uprm_score,this.opponent_score)
        if(Number.isFinite(this.uprm_score)&&Number.isFinite(this.opponent_score)){
            return true
        }
        else return false
    },
    buildDefaultValues(){
        if(this.sport_id == this.BASKETBALL_IDM || this.sport_id == this.BASKETBALL_IDF){this.sport_route = "basketball"}
        else if(this.sport_id == this.VOLLEYBALL_IDM || this.sport_id == this.VOLLEYBALL_IDF){this.sport_route = "volleyball"}
        else if(this.sport_id == this.SOCCER_IDM || this.sport_id == this.SOCCER_IDF){this.sport_route = "soccer"}
        else if(this.sport_id == this.BASEBALL_IDM || this.sport_id == this.SOFTBALL_IDF){this.sport_route = "baseball"}
        else if (this.sport_id == this.ATHLETICS_IDM || this.sport_id == this.ATHLETICS_IDF){this.sport_route = "medalbased"}
        else if (this.sport_id == this.FIELD_TENNIS_IDM || this.sport_id == this.FIELD_TENNIS_IDF
                || this.sport_id == this.TABLE_TENNIS_IDM || this.sport_id == this.TABLE_TENNIS_IDF){this.sport_route ="matchbased"}
        else{this.sport_route = ''}
    },

    buildTable(){
        console.log(this.payload_stats)
        
        if (this.sport_id!=''){
            //Basketball
            if (this.sport_id == this.BASKETBALL_IDM || this.sport_id == this.BASKETBALL_IDF){
                this.headers = 
                [
                {text: "Atleta", align:'start', sortable: true, value: "full_name" },
                {text: 'Asistencias', value: 'statistics.assists'},
                {text: 'Bloqueos', value: 'statistics.blocks'},
                {text: 'Intentos de Tiro de Campo', value: 'statistics.field_goal_attempt'},
                {text: 'Porcentaje de Tiro de Campo (%)', value: 'statistics.field_goal_percentage'},
                {text: 'Intentos de Tiro Libre', value: 'statistics.free_throw_attempt'},
                {text: 'Porcentaje de Tiro Libre (%)', value: 'statistics.free_throw_percentage'},
                {text: 'Puntos', value: 'statistics.points'},
                {text: 'Rebotes', value: 'statistics.rebounds'},
                {text: 'Robos', value: 'statistics.steals'},
                {text: 'Tiros de Campo Exitosos', value: 'statistics.successful_field_goal'},
                {text: 'Tiros Libres Exitosos', value: 'statistics.successful_free_throw'},
                {text: 'Tiros de Tres Puntos Exitosos', value: 'statistics.successful_three_point'},
                {text: 'Intentos de Tiro de Tres', value: 'statistics.three_point_attempt'},
                {text: 'Porcentaje de Tiro de Tres (%)', value: 'statistics.three_point_percentage'},
                {text: 'Perdidas de Balón', value: 'statistics.turnovers'},

                ]
                this.team_headers =
                [
                {text: 'Asistencias', value: 'basketball_statistics.assists'},
                {text: 'Bloqueos', value: 'basketball_statistics.blocks'},
                {text: 'Intentos de Tiro de Campo', value: 'basketball_statistics.field_goal_attempt'},
                {text: 'Porcentaje de Tiro de Campo (%)', value: 'basketball_statistics.field_goal_percentage'},
                {text: 'Intentos de Tiro Libre', value: 'basketball_statistics.free_throw_attempt'},
                {text: 'Porcentaje de Tiro Libre (%)', value: 'basketball_statistics.free_throw_percentage'},
                {text: 'Puntos', value: 'basketball_statistics.points'},
                {text: 'Rebotes', value: 'basketball_statistics.rebounds'},
                {text: 'Robos', value: 'basketball_statistics.steals'},
                {text: 'Tiros de Campo Exitosos', value: 'basketball_statistics.successful_field_goal'},
                {text: 'Tiros Libres Exitosos', value: 'basketball_statistics.successful_free_throw'},
                {text: 'Tiros de Tres Puntos Exitosos', value: 'basketball_statistics.successful_three_point'},
                {text: 'Intentos de Tiro de Tres', value: 'basketball_statistics.three_point_attempt'},
                {text: 'Porcentaje de Tiro de Tres (%)', value: 'basketball_statistics.three_point_percentage'},
                {text: 'Perdidas de Balón', value: 'basketball_statistics.turnovers'},

                ]
            }
            //Volleyball
            else if (this.sport_id == this.VOLLEYBALL_IDM || this.sport_id == this.VOLLEYBALL_IDF){
                this.headers = 
                [
                {text: "Atleta", align:'start', sortable: true, value: "full_name" },
                {text: 'Puntos de Ataque', value: 'statistics.kill_points'},
                {text: 'Errores de Ataque', value: 'statistics.attack_errors'},
                {text: 'Asistencias', value: 'statistics.assists'},
                {text: 'Servicio Directo', value: 'statistics.aces'},
                {text: 'Errores de Servicios', value: 'statistics.service_errors'},
                {text: 'Recepciones', value: 'statistics.digs'},
                {text: 'Bloqueo', value: 'statistics.blocks'},
                {text: 'Errores De Bloqueo', value: 'statistics.blocking_errors'},
                {text: 'Errores de Recepcion', value: 'statistics.reception_errors'},
                {text: 'Puntos de Bloqueo', value: 'statistics.blocking_points'},

                ]
                this.team_headers =
                [
                {text: 'Puntos de Ataque', value: 'volleyball_statistics.kill_points'},
                {text: 'Errores de Ataque', value: 'volleyball_statistics.attack_errors'},
                {text: 'Asistencias', value: 'volleyball_statistics.assists'},
                {text: 'Servicio Directo', value: 'volleyball_statistics.aces'},
                {text: 'Errores de Servicio', value: 'volleyball_statistics.service_errors'},
                {text: 'Recepciones', value: 'volleyball_statistics.digs'},
                {text: 'Bloqueos', value: 'volleyball_statistics.blocks'},
                {text: 'Errores de Bloqueo', value: 'volleyball_statistics.blocking_errors'},
                {text: 'Errores de Recepcion', value: 'volleyball_statistics.reception_errors'},
                {text: 'Puntos de Bloqueo', value: 'volleyball_statistics.blocking_points'},
                

                ]
            }
            //Soccer
            else if (this.sport_id == this.SOCCER_IDM || this.sport_id == this.SOCCER_IDF){
                this.headers = 
                [
                {text: "Atleta", align:'start', sortable: true, value: "full_name" },
                {text: 'Intentos de Gol', value: 'statistics.goal_attempts'},
                {text: 'Asistencias', value: 'statistics.assists'},
                {text: 'Faltas', value: 'statistics.fouls'},
                {text: 'Tarjetas', value: 'statistics.cards'},
                {text: 'Goles', value: 'statistics.successful_goals'},
                {text: 'Atajadas', value: 'statistics.tackles'},

                ]
                this.team_headers =
                [
                {text: 'Intentos de Gol', value: 'soccer_statistics.goal_attempts'},
                {text: 'Asistencias', value: 'soccer_statistics.assists'},
                {text: 'Faltas', value: 'soccer_statistics.fouls'},
                {text: 'Tarjetas', value: 'soccer_statistics.cards'},
                {text: 'Goles', value: 'soccer_statistics.successful_goals'},
                {text: 'Atajadas', value: 'soccer_statistics.tackles'},

                ]
            }
            //Baseball
            else if (this.sport_id == this.BASEBALL_IDM || this.sport_id == this.SOFTBALL_IDF){
                this.headers = 
                [
                {text: "Atleta", align:'start', sortable: true, value: "full_name" },
                {text: 'Turnos al Bate', value: 'statistics.at_bats'},
                {text: 'Carreras', value: 'statistics.runs'},
                {text: 'Hits', value: 'statistics.hits'},
                {text: 'Carreras Empujadas', value: 'statistics.runs_batted_in'},
                {text: 'Bases por Bolas', value: 'statistics.base_on_balls'},
                {text: 'Ponches', value: 'statistics.strikeouts'},
                {text: 'Dejados en Base', value: 'statistics.left_on_base'},

                ]
                this.team_headers =
                [
                {text: 'Turnos al Bate', value: 'baseball_statistics.at_bats'},
                {text: 'Carreras', value: 'baseball_statistics.runs'},
                {text: 'Hits', value: 'baseball_statistics.hits'},
                {text: 'Carreras Empujadas', value: 'baseball_statistics.runs_batted_in'},
                {text: 'Bases por Bolas', value: 'baseball_statistics.base_on_balls'},
                {text: 'Ponches', value: 'baseball_statistics.strikeouts'},
                {text: 'Dejados en Base', value: 'baseball_statistics.left_on_base'},

                ]
            }
            // TODO: make it so this happens for MEDAL-BASED events
            else if (this.sport_id == this.ATHLETICS_IDM || this.sport_id == this.ATHLETICS_IDF){
                this.headers =
                [
                {text: "Atleta", align:'start', sortable: true, value: "full_name" },
                {text: 'Categoria', value: 'statistics.category_name'},
                {text: 'Tipo de Medalla', value: 'statistics.medal_earned'},


                ]
                this.team_headers =
                [
                {text: 'Categoria', value: 'category_name'},
                {text: 'Tipo de Medalla', value: 'type_of_medal'},
                {text: 'Numero de Medallas', value: 'medals_earned'},
                ]
            }
            else if (this.sport_id == this.FIELD_TENNIS_IDM || this.sport_id == this.FIELD_TENNIS_IDF
                || this.sport_id == this.TABLE_TENNIS_IDM || this.sport_id == this.TABLE_TENNIS_IDF){
                this.headers =
                [
                {text: "Atleta", align:'start', sortable: true, value: "full_name" },
                {text: 'Categoria', value: 'statistics.category_name'},
                {text: 'Partidas Jugadas', value: 'statistics.matches_played'},
                {text: 'Partidas Ganadas', value: 'statistics.matches_won'},
 

                ]
                this.team_headers =
                [
                {text: 'Categoria', value: 'category_name'},
                {text: 'Partidas Jugadas', value: 'statistics.matches_played'},
                {text: 'Partidas Ganadas', value: 'statistics.matches_won'},
                ]
            }
        } 
    },
  },
  computed: {
    ...mapGetters({
        results_payload:"results/results_payload",
        event_info:"results/event_info",
        loadingQuery:"results/loadingQuery",
	})
  },
};
</script>

<style lang="scss" scoped>
@import "@/assets/variables.scss";
.wrapper {
  height: 100%;

  .content-area {
    height: 100%;
    width: 100%;
  }
}
</style>