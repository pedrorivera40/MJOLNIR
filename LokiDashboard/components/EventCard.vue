<template>
  <v-card height="100%"  width="100%">
    <v-img
      v-if="img != ''"
      class="black--text"
      height="150px"
      :src="img"
    >
   
    </v-img>
    <v-card-title>Deporte: {{sportName}}</v-card-title> 
    <v-card-subtitle>Fecha: {{eventDate}}</v-card-subtitle>    
    <v-card-text class="text--primary" v-if="opponentName !='' ">
      <div>UPRM vs {{opponentName}} </div>
    </v-card-text>
    <v-card-text class="text--primary">
      <div>Puntos {{localScore}} - {{opponentScore}} </div>
    </v-card-text>
     <v-card-text class="text--primary">
      <div>Resumen: {{eventSummary}} </div>
    </v-card-text>
    <v-card-actions> 
      <v-spacer/>   
      <v-btn @click="editEvent" >Editar</v-btn>
      <v-btn @click="goToEvent" >Detalles</v-btn>
      
    </v-card-actions> 
    <v-card-actions> 
      <v-spacer/>
      <v-btn v-if="sportName == 'Voleibol'">Ver Play-by-Play</v-btn>
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
  },
  methods:{
    goToEvent(){
      this.$router.push('/event/'+this.eventID)
    },

    editEvent(){

       this.$router.push('/event/'+this.eventID+'/edit')

    }

  }
}
</script>