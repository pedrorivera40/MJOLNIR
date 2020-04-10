<template>
  <v-container grid-list-sm>  
    <row>       
    <h1> Eventos: </h1>
    </row>
    
    <v-menu
      v-model="menu"
      bottom
      origin="center center"
      transition="slide-x-transition"
      :close-on-content-click="false"
    >
    <template v-slot:activator="{ on }">
        <v-btn
          color="white"
          @click="goToCreateEvent"                   
        >
        <v-icon left >mdi-pen-plus</v-icon>
          Nuevo Evento
        </v-btn>  
        <v-btn
          color="green darken-1"
          dark
          v-on="on"         
        >
        <v-icon left >mdi-filter-variant</v-icon>
          Filtros
        </v-btn> 
          
    </template>
     
    <v-list>
      <v-list-item>
        <v-menu
          ref="menu"
          v-model="dateMenu"
          :close-on-content-click="false"
          :return-value.sync="date"
          transition="scale-transition"
          offset-y
          min-width="290px"
        >
        
          <template v-slot:activator="{ on }">
            <v-text-field
              v-model="date"
              label="Fecha del Evento"              
              readonly
              v-on="on"
            ></v-text-field>
          </template>
          <v-date-picker v-model="date" no-title scrollable locale="es-419">
            <v-spacer></v-spacer>
            <v-btn text color="primary" @click="dateMenu = false">Cancel</v-btn>
            <v-btn text color="primary" @click="$refs.menu.save(date)">OK</v-btn>
          </v-date-picker>
        </v-menu>

      </v-list-item>
      <v-list-item>
          <v-select
            v-model="sport"
            :items="sports"                    
            label ="Deporte"                 
          ></v-select>              
      </v-list-item>
      <v-list-item>
        <v-select
          v-model="branch"
          :items="branches"                
          label ="Rama"                
        ></v-select>
      </v-list-item>
      <v-list-item>
        <v-select
          v-model="locality"
          :items="localities"                
          label ="Localizacion"                          
        ></v-select>
      </v-list-item>

      <v-list-item>
        <v-btn @click="clearFilters">Borrar</v-btn>
        <v-spacer/>
        <v-btn @click="applyFilters">Filtrar</v-btn>
      </v-list-item>
     
    </v-list>

    </v-menu>
    
  <v-row>
    <v-col v-for="(value,key) in filteredEvents" :key=key md="3">
   
    <EventCard      
      :eventID="value.id"     
      :sportName="value.sport_name"
      :eventDate="value.event_date"
      opponentName='UPRP'
      img='https://scontent.fsig1-1.fna.fbcdn.net/v/t1.0-9/74883001_2671827106239440_2718595271939325952_o.jpg?_nc_cat=111&_nc_sid=e007fa&_nc_ohc=lqrGrpZippsAX_BafZ8&_nc_ht=scontent.fsig1-1.fna&oh=da934963689fa5b8d79b31a40cd62835&oe=5EA9881E'
      :localScore='value.local_score'
      :opponentScore='value.opponent_score' 
      eventSummary="El evento fue entretinido"
     
    />        
    
    </v-col>
  </v-row>
  
    
       
  </v-container>  
 
   
</template>

<script>
import EventCard from '../../components/EventCard'


export default {
  components:{
    EventCard:EventCard
  },

  data: () =>({
    menu:false,
    dateMenu:false,
    date:'',
    sport:'',
    branch:'',
    locality:'',
    sports:['Voleibol','Baloncesto','Atletismo'],    
    branches:['masculino','femenina','Otro'],
    localities:['Casa','Afuera'],
    filteredEvents:[],

    events:{ "Events": [
    {
      "branch": "masculino",
      "event_date": "Wed, 01 Apr 2020 00:00:00 GMT",
      "id": 5,
      "is_local": true,
      "local_score": 5073,
      "opponent_color": null,
      "opponent_name": null,
      "opponent_score": 1,
      "sport_name": "Baloncesto",
      "team_id": 1,
      "venue": "Mangual"
    },
    {
      "branch": "masculino",
      "event_date": "Mon, 20 Apr 2020 00:00:00 GMT",
      "id": 6,
      "is_local": true,
      "local_score": 0,
      "opponent_color": null,
      "opponent_name": null,
      "opponent_score": 0,
      "sport_name": "Baloncesto",
      "team_id": 1,
      "venue": "Espada"
    },
    {
      "branch": "femenina",
      "event_date": "Mon, 20 Apr 2020 00:00:00 GMT",
      "id": 7,
      "is_local": true,
      "local_score": 200,
      "opponent_color": null,
      "opponent_name": null,
      "opponent_score": 500,
      "sport_name": "Voleibol",
      "team_id": 4,
      "venue": "Mangual"
    },
    {
      "branch": "masculino",
      "event_date": "Mon, 23 Mar 2020 00:00:00 GMT",
      "id": 3,
      "is_local": false,
      "local_score": 200,
      "opponent_color": "red",
      "opponent_name": null,
      "opponent_score": 500,
      "sport_name": "Baloncesto",
      "team_id": 1,
      "venue": "Mangual"
    },
    {
      "branch": "femenina",
      "event_date": "Wed, 01 Apr 2020 00:00:00 GMT",
      "id": 10,
      "is_local": true,
      "local_score": 100,
      "opponent_color": null,
      "opponent_name": null,
      "opponent_score": 50,
      "sport_name": "Fútbol",
      "team_id": 7,
      "venue": "Mangual"
    },
    {
      "branch": "femenina",
      "event_date": "Tue, 05 May 2020 00:00:00 GMT",
      "id": 11,
      "is_local": true,
      "local_score": null,
      "opponent_color": null,
      "opponent_name": null,
      "opponent_score": null,
      "sport_name": "Fútbol",
      "team_id": 7,
      "venue": "Mangual"
    },
    {
      "branch": "masculino",
      "event_date": "Mon, 16 Mar 2020 00:00:00 GMT",
      "id": 17,
      "is_local": false,
      "local_score": null,
      "opponent_color": "black",
      "opponent_name": null,
      "opponent_score": null,
      "sport_name": "Baloncesto",
      "team_id": 1,
      "venue": "Choliseo"
    },
    {
      "branch": "femenina",
      "event_date": "Mon, 20 Apr 2020 00:00:00 GMT",
      "id": 12,
      "is_local": true,
      "local_score": null,
      "opponent_color": null,
      "opponent_name": null,
      "opponent_score": null,
      "sport_name": "Softbol",
      "team_id": 8,
      "venue": "Mangual\n"
    },
    {
      "branch": "femenina",
      "event_date": "Sat, 09 May 2020 00:00:00 GMT",
      "id": 15,
      "is_local": true,
      "local_score": null,
      "opponent_color": null,
      "opponent_name": null,
      "opponent_score": null,
      "sport_name": "Fútbol",
      "team_id": 7,
      "venue": "Mangual"
    },
    {
      "branch": "femenina",
      "event_date": "Wed, 01 Apr 2020 00:00:00 GMT",
      "id": 13,
      "is_local": true,
      "local_score": null,
      "opponent_color": null,
      "opponent_name": null,
      "opponent_score": null,
      "sport_name": "Softbol",
      "team_id": 8,
      "venue": "Mangual"
    },
    {
      "branch": "femenina",
      "event_date": "Wed, 01 Apr 2020 00:00:00 GMT",
      "id": 8,
      "is_local": true,
      "local_score": null,
      "opponent_color": null,
      "opponent_name": null,
      "opponent_score": null,
      "sport_name": "Voleibol",
      "team_id": 4,
      "venue": "Mangual"
    },
    {
      "branch": "masculino",
      "event_date": "Sat, 14 Mar 2020 00:00:00 GMT",
      "id": 4,
      "is_local": true,
      "local_score": null,
      "opponent_color": null,
      "opponent_name": null,
      "opponent_score": null,
      "sport_name": "Baloncesto",
      "team_id": 1,
      "venue": "Espada"
    },
    {
      "branch": "femenina",
      "event_date": "Tue, 05 May 2020 00:00:00 GMT",
      "id": 14,
      "is_local": true,
      "local_score": null,
      "opponent_color": null,
      "opponent_name": null,
      "opponent_score": null,
      "sport_name": "Softbol",
      "team_id": 8,
      "venue": "Mangual"
    },
    {
      "branch": "femenina",
      "event_date": "Mon, 20 Apr 2020 00:00:00 GMT",
      "id": 9,
      "is_local": true,
      "local_score": null,
      "opponent_color": null,
      "opponent_name": null,
      "opponent_score": null,
      "sport_name": "Fútbol",
      "team_id": 7,
      "venue": "Mangual"
    }
  ]},
  
    


    
  }),

  created(){
    this.createEventsList()
  },

  methods:{

    goToCreateEvent(){
        this.$router.push('/event/')
    },

    clearFilters(){
        this.date = ''
        this.sport = ''
        this.branch = ''
        this.locality=''
        this.menu=false
        
        console.log("Testing")
        console.log(this.filteredEvents.length)
        console.log(this.events.Events.length)
        if(this.filteredEvents.length != this.events.Events.length){
          this.filteredEvents = []
          for(let i = 0; i < this.events.Events.length; i++){
            this.filteredEvents.push(this.events.Events[i])
          }          
        }
          
    },
    createEventsList(){
     
      this.filteredEvents = []
      for(let i = 0; i < this.events.Events.length; i++){
        this.filteredEvents.push(this.events.Events[i])
      }
      
      console.log(Date.parse(this.events.Events[0].event_date))    
    },

    applyFilters(){
      
      for(let i = this.filteredEvents.length-1; i >=0; i--){
        event=this.filteredEvents[i]
        if(this.sport!=''){
          if(this.sport.localeCompare(event['sport_name'])!=0){
            this.filteredEvents.splice(i,1)
            continue
          }
        }
        if(this.branch!=''){
          if(this.branch.localeCompare(event['branch'])!=0){
            this.filteredEvents.splice(i,1)
            continue
          }
        }
        if(this.locality!=''){
          if(this.locality.localeCompare("Casa")==0){
            if(event['is_local']!=true){
              this.filteredEvents.splice(i,1)
              continue
            }
          }
          else{
            if(event['is_local']!=false){
              this.filteredEvents.splice(i,1)
              continue
            }
          }
        }
        if(this.date!=''){
          if(Date.parse(this.date)!=Date.parse(event['event_date'])){
            this.filteredEvents.splice(i,1)
            continue
          }
        }

      }
      
      
    }
  }


    
}
</script>