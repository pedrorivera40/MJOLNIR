<template>
  <v-card height="100%"  width="100%">
    <v-card-title>Fecha: {{eventDate}}</v-card-title>    
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