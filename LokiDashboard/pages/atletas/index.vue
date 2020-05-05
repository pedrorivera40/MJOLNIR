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
                dark
                @click="addAthlete"                   
              >
                <v-icon left >mdi-plus</v-icon>
                Añadir Atleta
              </v-btn>
              <v-spacer />
            </v-col>
            <v-col cols="4">
              <v-text-field
                v-model="search"
                append-icon="mdi-magnify"
                label="Buscar"
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
          class="elevation-1"
          no-data-text="No hay atletas."
          loading-text="Buscando atletas."
        >
          <template v-slot:item.actions="{ item }">
            <v-tooltip bottom>
              <template v-slot:activator="{ on }">
                <v-icon
                  medium
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
                  medium
                  class="mr-2 table-actions"
                  v-on="on"                  
                  @click="editAthlete(item)"
                >
                  mdi-pencil
                </v-icon>
              </template>
              <span>Editar Atleta</span>
            </v-tooltip>
            <v-tooltip bottom>
              <template v-slot:activator="{ on }">
                <v-icon
                  medium
                  class="mr-2 table-actions"
                  v-on="on"                 
                  @click="deleteAthlete(item.id)"
                >
                  mdi-delete
                </v-icon>
              </template>
              <span>Borrar Atleta</span>
            </v-tooltip>           
          </template>          
        </v-data-table>

        <AddAthleteModal
          :dialog.sync="dialogAdd"
        />

        <EditAthleteModal
          :dialog.sync="dialogEdit"
          :first_name="editedItem.fName"
          :middle_name="editedItem.mName"
          :last_names="editedItem.lName"
          :date_of_birth="editedItem.dBirth"
          :short_bio="editedItem.bio"
          :height="editedItem.height"
          :study_program="editedItem.sProgram"
          :school_of_precedence="editedItem.school"
          :years_of_participation="editedItem.yearsOfParticipation"
          :year_of_study="editedItem.yearOfStudy"
          :athlete_positions="editedItem.athlete_positions"
          :athlete_categories="editedItem.athlete_categories"
          :number="editedItem.number"
          :profile_image_link="editedItem.profilePicLink"
          :sport_name="editedItem.sportName"
          :branch="editedItem.sportBranch"
          :sport_id="editedItem.sport_id"
          :id="editedItem.id"
        />
        <DeleteAthleteModal
          :dialog.sync="dialogDelete"
          :id="aid"          
        />      
        
      </v-card>
    </div>
  </v-container>
</template>

<script>
import { mapActions, mapGetters } from "vuex"
import  AddAthleteModal from "@/components/AddAthleteModal"
import EditAthleteModal from "@/components/EditAthleteModal"
import DeleteAthleteModal from "@/components/DeleteAthleteModal"

export default {
  components:{
    AddAthleteModal,
    EditAthleteModal,
    DeleteAthleteModal,
  },

  data: () =>({
    search:'',
    aid:0,
    dialogDelete:false,
    dialogAdd:false,
    dialogEdit:false,
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
    ],

    editedItem:{
      fName:"",
      mName:"",
      lName:"",
      dBirth:"",
      bio:"",
      height:0.0,
      number:0,
      school:"",
      sProgram:"",
      yearOfStudy:0,
      sport_id:0,
      sportName:"",
      sportBranch:"",
      yearsOfParticipation:0,
      profilePicLink:"",
      athlete_positions:{},
      athlete_categories:{},
      id:0,
    },
  

    
  }),

  

  methods:{
    ...mapActions({
      getAthletes: "athletes/getAthletes",
      removeAthlete:"athletes/removeAthlete"
    }),

    addAthlete(){
      this.dialogAdd = true
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
    editAthlete(athlete){
      this.editedItem = Object.assign({},athlete)
      this.dialogEdit = true
    },    

    deleteAthlete(athleteID){
      this.aid = athleteID
      this.dialogDelete = true
    },
    
    
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

<style scoped>
::v-deep .v-data-table th {
  font-size: 14px;
}

::v-deep .v-data-table td {
  font-size: 18px;
}
</style>