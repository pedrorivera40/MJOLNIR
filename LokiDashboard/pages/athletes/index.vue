<template>
  <v-container grid-list-sm>  
    <row>       
    <h1> Atletas: </h1>
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
          @click="goToCreateAthlete"                   
        >
        <v-icon left >mdi-pen-plus</v-icon>
          Nuevo Atleta
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
          <v-select
            v-model="sport"
            :items="sports"                    
            label ="Deporte"                 
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
    <v-col v-for="(value,key) in filteredAthletes" :key=key md="6">
   
    <AthleteCard     
      :athleteID="value.id"  
      :firstName ="value.fName"
      :lastNames ="value.lName"   
      :sportName="value.sportName"      
      :img="value.profilePicLink"
      
    />        
    
    </v-col>
  </v-row>
  
    
       
  </v-container>  
 
   
</template>

<script>
import AthleteCard from '../../components/AthleteCard'


export default {
  components:{
    AthleteCard:AthleteCard
  },

  data: () =>({
    menu:false,
    
    sport:'',   
    sports:['Voleibol','Baloncesto','Atletismo'],     
    
    filteredAthletes:[],

    athletes:{ 
  "Athletes": [
    {
      "bio": null,
      "dBirth": null,
      "fName": "TFNam7",
      "height": null,
      "id": 65,
      "lName": "TLName7",
      "mName": "",
      "number": 98,
      "profilePicLink": null,
      "sProgram": null,
      "school": null,
      "sportName": "TestSportWithCategory",
      "yearOfStudy": null,
      "yearsOfParticipation": null
    },
    {
      "bio": "I sure loved basketball",
      "dBirth": null,
      "fName": "Kobe",
      "height": null,
      "id": 1,
      "lName": "Bryant",
      "mName": null,
      "number": 24,
      "profilePicLink": null,
      "sProgram": null,
      "school": null,
      "sportName": "Baloncesto",
      "yearOfStudy": null,
      "yearsOfParticipation": null
    },
    {
      "bio": "I sure love basketball",
      "dBirth": null,
      "fName": "Lebron",
      "height": null,
      "id": 3,
      "lName": "James",
      "mName": null,
      "number": 23,
      "profilePicLink": null,
      "sProgram": null,
      "school": null,
      "sportName": "Baloncesto",
      "yearOfStudy": null,
      "yearsOfParticipation": null
    },
    {
      "bio": "I sure love 2k",
      "dBirth": null,
      "fName": "Larry",
      "height": null,
      "id": 4,
      "lName": "Bird",
      "mName": null,
      "number": 33,
      "profilePicLink": null,
      "sProgram": null,
      "school": null,
      "sportName": "Baloncesto",
      "yearOfStudy": null,
      "yearsOfParticipation": null
    },
    {
      "bio": "Bio2",
      "dBirth": null,
      "fName": "FName2",
      "height": null,
      "id": 7,
      "lName": "LName2",
      "mName": "",
      "number": 3,
      "profilePicLink": null,
      "sProgram": null,
      "school": null,
      "sportName": "Baloncesto",
      "yearOfStudy": null,
      "yearsOfParticipation": null
    },
    {
      "bio": "Bio3",
      "dBirth": null,
      "fName": "FName3",
      "height": null,
      "id": 11,
      "lName": "LName3",
      "mName": "",
      "number": 5,
      "profilePicLink": null,
      "sProgram": null,
      "school": null,
      "sportName": "Voleibol",
      "yearOfStudy": null,
      "yearsOfParticipation": null
    },
    {
      "bio": "Bio4",
      "dBirth": null,
      "fName": "FName4",
      "height": null,
      "id": 12,
      "lName": "LName4",
      "mName": "",
      "number": 55,
      "profilePicLink": null,
      "sProgram": null,
      "school": null,
      "sportName": "Voleibol",
      "yearOfStudy": null,
      "yearsOfParticipation": null
    },
    {
      "bio": "Bio5",
      "dBirth": null,
      "fName": "FName5",
      "height": null,
      "id": 13,
      "lName": "LName5",
      "mName": "",
      "number": 52,
      "profilePicLink": null,
      "sProgram": null,
      "school": null,
      "sportName": "Voleibol",
      "yearOfStudy": null,
      "yearsOfParticipation": null
    },
    {
      "bio": "Truth",
      "dBirth": "Sat, 21 Jul 1900 00:00:00 GMT",
      "fName": "Diana",
      "height": 86.0,
      "id": 9,
      "lName": "Prince",
      "mName": "Wonder Woman",
      "number": 21,
      "profilePicLink": "dccomics.com",
      "sProgram": "Warrior",
      "school": "Themyschira",
      "sportName": "Fútbol",
      "yearOfStudy": null,
      "yearsOfParticipation": null
    },
    {
      "bio": "Its a bird, its a plane",
      "dBirth": "Wed, 21 Jul 1976 00:00:00 GMT",
      "fName": "Clark",
      "height": 80.0,
      "id": 10,
      "lName": "Kent",
      "mName": "Superman",
      "number": 1,
      "profilePicLink": "dccomics.com",
      "sProgram": "Journalism",
      "school": "Smallville High",
      "sportName": "Voleibol",
      "yearOfStudy": null,
      "yearsOfParticipation": null
    },
    {
      "bio": "Now, this is a story all about how My; life",
      "dBirth": null,
      "fName": "Smill",
      "height": null,
      "id": 15,
      "lName": "With",
      "mName": null,
      "number": null,
      "profilePicLink": null,
      "sProgram": null,
      "school": null,
      "sportName": "Baloncesto",
      "yearOfStudy": null,
      "yearsOfParticipation": null
    },
    {
      "bio": null,
      "dBirth": null,
      "fName": "TenistaUno",
      "height": null,
      "id": 100,
      "lName": "Solo",
      "mName": "",
      "number": null,
      "profilePicLink": null,
      "sProgram": null,
      "school": null,
      "sportName": "Tenis de Campo",
      "yearOfStudy": null,
      "yearsOfParticipation": null
    },
    {
      "bio": "Bio5",
      "dBirth": null,
      "fName": "FName5",
      "height": null,
      "id": 30,
      "lName": "LName5",
      "mName": "",
      "number": 52,
      "profilePicLink": null,
      "sProgram": null,
      "school": null,
      "sportName": "Voleibol",
      "yearOfStudy": null,
      "yearsOfParticipation": null
    },
    {
      "bio": null,
      "dBirth": null,
      "fName": "TenistaDos",
      "height": null,
      "id": 101,
      "lName": "Solo",
      "mName": "",
      "number": null,
      "profilePicLink": null,
      "sProgram": null,
      "school": null,
      "sportName": "Tenis de Campo",
      "yearOfStudy": null,
      "yearsOfParticipation": null
    },
    {
      "bio": null,
      "dBirth": null,
      "fName": "TenistaTres",
      "height": null,
      "id": 102,
      "lName": "Doble",
      "mName": "",
      "number": null,
      "profilePicLink": null,
      "sProgram": null,
      "school": null,
      "sportName": "Tenis de Campo",
      "yearOfStudy": null,
      "yearsOfParticipation": null
    },
    {
      "bio": null,
      "dBirth": null,
      "fName": "TenistaCuatro",
      "height": null,
      "id": 103,
      "lName": "Doble",
      "mName": "",
      "number": null,
      "profilePicLink": null,
      "sProgram": null,
      "school": null,
      "sportName": "Tenis de Campo",
      "yearOfStudy": null,
      "yearsOfParticipation": null
    },
    {
      "bio": "TBio1",
      "dBirth": null,
      "fName": "TFName1",
      "height": null,
      "id": 26,
      "lName": "TLName1",
      "mName": "",
      "number": 99,
      "profilePicLink": null,
      "sProgram": null,
      "school": null,
      "sportName": "TestSportWithPosition",
      "yearOfStudy": null,
      "yearsOfParticipation": null
    },
    {
      "bio": "Bio5",
      "dBirth": null,
      "fName": "FName5",
      "height": null,
      "id": 29,
      "lName": "LName5",
      "mName": "",
      "number": 52,
      "profilePicLink": null,
      "sProgram": null,
      "school": null,
      "sportName": "TestSportWithCategory",
      "yearOfStudy": null,
      "yearsOfParticipation": null
    },
    {
      "bio": "Now, this; is a; story all a;bout how My; life",
      "dBirth": null,
      "fName": "John",
      "height": null,
      "id": 16,
      "lName": "Smith",
      "mName": null,
      "number": null,
      "profilePicLink": null,
      "sProgram": null,
      "school": null,
      "sportName": "Baloncesto",
      "yearOfStudy": null,
      "yearsOfParticipation": null
    },
    {
      "bio": "No fear.",
      "dBirth": null,
      "fName": "Hal",
      "height": null,
      "id": 68,
      "lName": "Jordan",
      "mName": null,
      "number": null,
      "profilePicLink": null,
      "sProgram": "Pilot",
      "school": "Coast City High",
      "sportName": "Voleibol",
      "yearOfStudy": null,
      "yearsOfParticipation": null
    },
    {
      "bio": "Old West",
      "dBirth": null,
      "fName": "Jonah",
      "height": null,
      "id": 69,
      "lName": "Hex",
      "mName": null,
      "number": null,
      "profilePicLink": null,
      "sProgram": "Cowboy",
      "school": "Gotham West High",
      "sportName": "Voleibol",
      "yearOfStudy": null,
      "yearsOfParticipation": null
    },
    {
      "bio": "Master of unlocking",
      "dBirth": null,
      "fName": "Jill",
      "height": null,
      "id": 70,
      "lName": "Valentine",
      "mName": null,
      "number": null,
      "profilePicLink": null,
      "sProgram": "S.T.A.R.S.",
      "school": "Raccoon City High",
      "sportName": "Voleibol",
      "yearOfStudy": null,
      "yearsOfParticipation": null
    },
    {
      "bio": "Mr. X Gon Give it To Ya",
      "dBirth": null,
      "fName": "Claire",
      "height": null,
      "id": 71,
      "lName": "Redfield",
      "mName": null,
      "number": null,
      "profilePicLink": null,
      "sProgram": "Teaching",
      "school": "Raccoon City High",
      "sportName": "Voleibol",
      "yearOfStudy": null,
      "yearsOfParticipation": null
    },
    {
      "bio": "S T R O N K",
      "dBirth": null,
      "fName": "Chris ",
      "height": null,
      "id": 72,
      "lName": "Redfield",
      "mName": null,
      "number": null,
      "profilePicLink": null,
      "sProgram": "S.T.A.R.S.",
      "school": "Raccoon City High",
      "sportName": "Voleibol",
      "yearOfStudy": null,
      "yearsOfParticipation": null
    },
    {
      "bio": "I am vengeance, I am the night.",
      "dBirth": "Mon, 21 Jul 1980 00:00:00 GMT",
      "fName": "Bruce",
      "height": 84.0,
      "id": 8,
      "lName": "Wayne",
      "mName": "Batman",
      "number": 27,
      "profilePicLink": "dccomics.com",
      "sProgram": "Forensics",
      "school": "Gotham High",
      "sportName": "Baloncesto",
      "yearOfStudy": null,
      "yearsOfParticipation": null
    },
    {
      "bio": null,
      "dBirth": null,
      "fName": "Sheva",
      "height": null,
      "id": 73,
      "lName": "Alomar",
      "mName": null,
      "number": null,
      "profilePicLink": null,
      "sProgram": null,
      "school": null,
      "sportName": "Fútbol",
      "yearOfStudy": null,
      "yearsOfParticipation": null
    },
    {
      "bio": null,
      "dBirth": null,
      "fName": "Ada",
      "height": null,
      "id": 74,
      "lName": "Wong",
      "mName": null,
      "number": null,
      "profilePicLink": null,
      "sProgram": null,
      "school": null,
      "sportName": "Fútbol",
      "yearOfStudy": null,
      "yearsOfParticipation": null
    },
    {
      "bio": null,
      "dBirth": null,
      "fName": "Ashley",
      "height": null,
      "id": 75,
      "lName": "Graham",
      "mName": null,
      "number": null,
      "profilePicLink": null,
      "sProgram": null,
      "school": null,
      "sportName": "Softbol",
      "yearOfStudy": null,
      "yearsOfParticipation": null
    },
    {
      "bio": null,
      "dBirth": null,
      "fName": "Sherry ",
      "height": null,
      "id": 76,
      "lName": "Birkin",
      "mName": null,
      "number": null,
      "profilePicLink": null,
      "sProgram": null,
      "school": null,
      "sportName": "Softbol",
      "yearOfStudy": null,
      "yearsOfParticipation": null
    },
    {
      "bio": "Bio9",
      "dBirth": "Sun, 09 Sep 1900 00:00:00 GMT",
      "fName": "FNameNine",
      "height": 82.5,
      "id": 82,
      "lName": "LNameNine",
      "mName": "MNameNine",
      "number": 9,
      "profilePicLink": "www.photo.com",
      "sProgram": "Study9",
      "school": "School9",
      "sportName": "Voleibol",
      "yearOfStudy": 3,
      "yearsOfParticipation": 2
    },
    {
      "bio": "TBio2",
      "dBirth": null,
      "fName": "TFName2",
      "height": null,
      "id": 51,
      "lName": "TLName2",
      "mName": "",
      "number": 99,
      "profilePicLink": null,
      "sProgram": null,
      "school": null,
      "sportName": "Voleibol",
      "yearOfStudy": null,
      "yearsOfParticipation": null
    },
    {
      "bio": null,
      "dBirth": null,
      "fName": "TFNam5",
      "height": null,
      "id": 54,
      "lName": "TLName5",
      "mName": "",
      "number": 99,
      "profilePicLink": null,
      "sProgram": null,
      "school": null,
      "sportName": "Voleibol",
      "yearOfStudy": null,
      "yearsOfParticipation": null
    },
    {
      "bio": null,
      "dBirth": null,
      "fName": "TFNam5",
      "height": null,
      "id": 57,
      "lName": "TLName5",
      "mName": "",
      "number": 99,
      "profilePicLink": null,
      "sProgram": null,
      "school": null,
      "sportName": "Voleibol",
      "yearOfStudy": null,
      "yearsOfParticipation": null
    },
    {
      "bio": "Bio11",
      "dBirth": "Sat, 11 Nov 1911 00:00:00 GMT",
      "fName": "FNameEleven",
      "height": 11.0,
      "id": 86,
      "lName": "Eleven",
      "mName": "Eleven",
      "number": 11,
      "profilePicLink": "www.photo.com",
      "sProgram": "Study11",
      "school": "School11",
      "sportName": "TestSportWithCategory",
      "yearOfStudy": 2,
      "yearsOfParticipation": 1
    },
    {
      "bio": null,
      "dBirth": null,
      "fName": "TFNam6",
      "height": null,
      "id": 61,
      "lName": "TLName6",
      "mName": "",
      "number": 98,
      "profilePicLink": null,
      "sProgram": null,
      "school": null,
      "sportName": "Voleibol",
      "yearOfStudy": null,
      "yearsOfParticipation": null
    }
  ]
}

    
  }),

  created(){
    this.createAthletesList()
  },

  methods:{

    goToCreateAthlete(){
        this.$router.push('/athlete/')
    },

    clearFilters(){
        
        this.sport = ''        
        this.menu=false
        
        console.log("Testing")
        console.log(this.filteredAthletes.length)
        console.log(this.athletes.Athletes.length)
        if(this.filteredAthletes.length != this.athletes.Athletes.length){
          this.filteredAthletes = []
          for(let i = 0; i < this.athletes.Athletes.length; i++){
            this.filteredAthletes.push(this.athletes.Athletes[i])
          }          
        }
          
    },
    createAthletesList(){
     
      this.filteredAthletes = []
      for(let i = 0; i < this.athletes.Athletes.length; i++){
        this.filteredAthletes.push(this.athletes.Athletes[i])
      }
      
         
    },

    applyFilters(){
      
      for(let i = this.filteredAthletes.length-1; i >=0; i--){
        let athlete=this.filteredAthletes[i]
        if(this.sport!=''){
          if(this.sport.localeCompare(athlete['sportName'])!=0){
            this.filteredAthletes.splice(i,1)
            continue
          }
        }
      }
      
      
    }
  }


    
}
</script>