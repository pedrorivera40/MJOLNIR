<template>
  <v-card height="100%"  width="100%">
    <v-img
      v-if="img != ''"
      class="black--text"
      width="450px"
      height="300px"
      :src="img"
    >
   
    </v-img>
    <v-card-title>Deporte: {{sportName}}</v-card-title> 
    <v-card-subtitle>
      <span class="text" style="font-size:20px">Fecha: {{formatDate()}}</span>
    </v-card-subtitle>    
    <v-card-text v-if="opponentName !='' | !!opponentName">
      <span class="text" style="font-size:20px">Equipos: UPRM vs {{opponentName}} </span>
    </v-card-text>      
    <v-card-actions> 
      
      <v-btn v-if="hasPBP == true" @click="goToPBPSequence">Ver Play-by-Play</v-btn> 
      <v-spacer/>      
      <v-btn color="green darken-1" dark @click="goToEvent" >Ver Detalles</v-btn>      
    </v-card-actions> 
    
  

  </v-card>
    
</template>

<script>
export default {
  props:{
    eventID:Number,
    sportName:String,
    eventDate:String,
    opponentName:String,
    eventSummary:String,
    img:String,
    localScore:Number,
    opponentScore:Number,
    hasPBP:Boolean,     
  },
  methods:{

    /**
     * Routes user to event viewer page for
     * the event with id given as prop.
     */
    goToEvent(){
      this.$router.push('/eventos/'+this.eventID)
    },  
    /**
     * Routes user to PBP sequence viewer page
     * for the event with the sport and id given as
     * props
     */
    goToPBPSequence(){
      this.$router.push('/jugadas-'+this.sportName.toLowerCase()+'/'+this.eventID)
    },
    /**
     * Formats the date and time for the card.
     */
    formatDate(){

          let eDate = new Date(Date.parse(this.eventDate))
					let date = eDate.toISOString().substr(0,10)
					let hours = eDate.getUTCHours()
					let minutes = eDate.getUTCMinutes()
					
					let amPM = null
					if(hours > 12){
						amPM = 'PM'
						hours -= 12
					}
					else if(hours < 12)
						amPM = 'AM'

          let time = null;
					if(minutes < 10)
						time = hours + ":0"+minutes + amPM
					else if(minutes >=10)
						time = hours + ":" +minutes + amPM
          return date + ' @' + time 
    }

  }
}
</script>