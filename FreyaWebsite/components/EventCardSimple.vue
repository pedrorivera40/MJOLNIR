<template>
  <v-card height="100%"  width="100%">
    <v-card-title>Fecha: {{date}}</v-card-title>   
    <v-card-subtitle>Hora: {{time}}</v-card-subtitle>    
    <v-card-text class="text--primary" v-if="opponentName !='' | !!opponentName">
      <div>Equipos: UPRM vs {{opponentName}} </div>
    </v-card-text>
    <v-card-text class="text--primary">
      <div>Puntos: {{localScore}} - {{opponentScore}} </div>
    </v-card-text>
     <v-card-text class="text--primary">
      <div>Resumen: {{formatSummary()}} </div>
    </v-card-text>
    <v-card-actions> 
      <v-spacer/>      
      <v-btn color="green darken-1" dark @click="goToEvent" >Ver Detalles</v-btn>      
    </v-card-actions> 
    <v-card-actions> 
      <v-spacer/>
      <v-btn v-if="hasPBP == true">Ver Play-by-Play</v-btn>     
    </v-card-actions>
  

  </v-card>
    
</template>

<script>
export default {
  props:{
    eventID:Number,
    eventDate:String,
    opponentName:String,
    eventSummary:String,
    localScore:Number,
    opponentScore:Number,
    hasPBP:Boolean,     
  },
  data: () => ({  
    date:'',
    time:'',
  }),
  created(){
    // SET EVENT DATE FORMATED
    let eventDate2 = new Date(Date.parse(this.eventDate));
    this.date = eventDate2.toISOString().substr(0, 10);
    let hours = eventDate2.getUTCHours();
    let minutes = eventDate2.getUTCMinutes();

    let amPM = null;
    if (hours > 12) {
      amPM = "PM";
      hours -= 12;
    } else if (hours < 12) amPM = "AM";
    if (hours == 0) {
      hours = 12;
    }
    if (minutes < 10) this.time = hours + ":0" + minutes + amPM;
    else if (minutes >= 10) this.time = hours + ":" + minutes + amPM;
  }, 
  methods:{
    goToEvent(){
      this.$router.push('/eventos/'+this.eventID)
    },
    
    formatSummary(){
      if(this.eventSummary !== null){
        if(this.eventSummary.length > 20)
          return this.eventSummary.substring(0,20).concat("...")
        else
          return this.eventSummary
      }
      else
        return ''
    }

  }
}
</script>