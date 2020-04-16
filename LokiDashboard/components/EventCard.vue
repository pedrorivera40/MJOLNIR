<template>
  <v-card height="100%"  width="100%">
    <v-img
      v-if="img != ''"
      class="black--text"
      width="300px"
      height="300px"
      :src="img"
    >
   
    </v-img>
    <v-card-title>Deporte: {{sportName}}</v-card-title> 
    <v-card-subtitle>Fecha: {{eventDate}}</v-card-subtitle>    
    <v-card-text class="text--primary" v-if="opponentName !='' | !!opponentName">
      <div>Equipos: UPRM vs {{opponentName}} </div>
    </v-card-text>
    <v-card-text class="text--primary">
      <div>Puntos: {{localScore}} - {{opponentScore}} </div>
    </v-card-text>
     <v-card-text class="text--primary">
      <div>Resumen: {{formatSummary()}} </div>
    </v-card-text>
    <v-card-actions class="justify-center">
        <v-btn  @click="goToEvent">
          <v-icon> mdi-eye-plus-outline </v-icon>            
        </v-btn>

        <v-btn color="green darken-1" dark @click="editEvent">
          <v-icon> mdi-pencil </v-icon>            
        </v-btn>
        <v-btn color="red darken-1" dark @click="removeEvent">
          <v-icon> mdi-delete </v-icon>            
        </v-btn>
        
    </v-card-actions> 
    <v-card-actions class="justify-center"> 
      <v-spacer/>
      <v-btn v-if="hasPBP == true">Ver Play-by-Play</v-btn>
      <v-btn v-if="sportName == 'Voleibol' & hasPBP == false">Añadir Play-by-Play</v-btn>
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
    goToEvent(){
      this.$router.push('/evento/'+this.eventID)
    },
    editEvent(){
      this.$router.push('/evento/'+this.eventID+'/editar')
    },
    removeEvent(){
      console.log("Removing event with id:" + this.eventID)
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