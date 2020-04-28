<template>
  <v-container class="wrapper">          
    <h1 class="primary_dark--text pl-3">Atletas:</h1>   
    <div class="content-area pa-4 pt-12">
      <v-card >
        <v-card-title>
          <v-row>
            <v-col>
              <v-btn
                color="green darken-1"
                @click="goToCreateAthlete"                   
              >
                <v-icon left >mdi-plus</v-icon>
                Nuevo Atleta
              </v-btn>
              <v-spacer />
            </v-col>
            <v-col cols="4">
              <v-text-field
                v-model="search"
                append-icon="mdi-magnify"
                label="Search"
                rounded
                dense
                outlined
                single-line
                hide-details
              />
            </v-col>

          </v-row>


        </v-card-title>
        
        <v-data-table
                 
          :headers="headers"
          :items="athletes"
          :search="search"
          :loading="loadingAthletes()"
          no-data-text="No hay atletas."
          loading-text="Buscando atletas."
        >
          <template v-slot:item.actions="{ item }">
            <v-tooltip bottom>
              <template v-slot:activator="{ on }">
                <v-icon
                  small
                  class="mr-2 table-actions"
                  v-on="on"                 
                  @click="viewAthlete(item.id)"
                >
                  mdi-eye-plus
                </v-icon>
              </template>
              <span>Ver Atleta</span>
            </v-tooltip>

            <v-tooltip bottom>
              <template v-slot:activator="{ on }">
                <v-icon
                  small
                  class="mr-2 table-actions"
                  v-on="on"                  
                  @click="editAthlete(item.id)"
                >
                  mdi-pencil
                </v-icon>
              </template>
              <span>Editar Atleta</span>
            </v-tooltip>
            <v-tooltip bottom>
              <template v-slot:activator="{ on }">
                <v-icon
                  small
                  class="mr-2 table-actions"
                  v-on="on"                 
                  @click="prepareAthleteToRemove(item.id)"
                >
                  mdi-delete
                </v-icon>
              </template>
              <span>Borrar Atleta</span>
            </v-tooltip>           
          </template>          
        </v-data-table>

        <v-dialog v-model="dialog" persistent max-width="290">            
            <v-card>
              <v-card-title class="headline">¿Estás seguro de que quieres eliminar el atleta con id:{{aid}}?</v-card-title>
              <v-card-text>
                Esta acción es <strong> irreversible.</strong>
                <v-checkbox
                  v-model="terms"
                  :label="`Yo acepto las consecuencias.`"
                >
                </v-checkbox>
              </v-card-text>
              <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn color="green darken-1" text @click="cancelRemoval">Cancelar</v-btn>
                <v-btn color="green darken-1" :disabled="!terms" text @click="deleteAthlete">Eliminar</v-btn>
              </v-card-actions>
            </v-card>
          </v-dialog>       
        
      </v-card>
    </div>
  </v-container>
</template>

<script>
import AthleteCard from '../../components/AthleteCard'
import { mapActions, mapGetters } from "vuex"

export default {
  components:{
    AthleteCard:AthleteCard
  },

  data: () =>({
    search:'',
    aid:0,
    dialog:false,
    terms:false,
    ready:false,
    name:'',
    sport:'',   
    sports:['Voleibol','Baloncesto','Atletismo'],     
    
    filteredAthletes:'',

    headers:[
      {
        text:"ID",
        align:"start",
        value:"id"
      },
      {text:"Primer Nombre",value:"fName"},
      {text:"Segundo Nombre",value:"mName"},
      {text:"Apellidos",value:"lName"},
      {text:"Deporte",value:"sportName"},
      {text:"Rama",value:"sportBranch"},
      {text:"Acciones",value:"actions",sortable:false}
    ]
  

    
  }),

  

  methods:{
    ...mapActions({
      getAthletes: "athletes/getAthletes",
      removeAthlete:"athletes/removeAthlete"
    }),

    goToCreateAthlete(){
        this.$router.push('/atleta/')
    },
    
    loadingAthletes(){
      if(this.athletes.length > 0){
        return false
      }else{
        return true
      }
    },
    viewAthlete(athleteID){
      this.$router.push('/atleta/'+athleteID)
    },
    editAthlete(athleteID){
      this.$router.push('/atleta/'+athleteID+'/editar')
    },
    deleteAthlete(){
      if(this.aid > 0 && this.terms)            
        this.removeAthlete(this.aid)
        this.dialog = false
        this.terms = false
        this.ready = false
    },

    prepareAthleteToRemove(athleteID){
      this.aid = athleteID
      this.dialog = true
    },
    cancelRemoval(){
      this.aid = 0
      this.dialog = false
      this.terms = false
    }
    
  },
    
  
  computed: {
    ...mapGetters({
      athletes: "athletes/athletes"
    }),
  
  },

  mounted() {
    this.getAthletes();
  }

    
}
</script>