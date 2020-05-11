<template>
  <v-row justify="center">
    <v-dialog v-model="dialog" persistent max-width="350">            
      <v-card>
        <v-toolbar flat color="primary_dark">
          <v-toolbar-title class="headline white--text">
            Borrar Atleta
          </v-toolbar-title>
        </v-toolbar>
        <v-card-title>
          <p style="word-break: normal;">¿Seguro de que quieres el atleta con id:{{id}}?</p>
        </v-card-title>
        <v-card-text>
          Esta acción es <strong> irreversible.</strong>
          <v-checkbox
            v-model="terms"
            label="Acepto las consecuencias."
          >
          </v-checkbox>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn text color="grey darken-3" @click="close()">Cancelar</v-btn>
          <v-btn 
            color="primary darken-1" 
            :disabled="!terms" 
            text
            :loading="deleting" 
            @click="deleteAthlete()">Borrar</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>   
  </v-row>
</template>

<script>
import { mapActions } from "vuex"

export default {
  name:"DeleteAthleteModal",
  props:{
    dialog:Boolean,
    id:Number,   
  },

  data:() =>({
    terms:false,
    deleting:false,
  }),

  methods:{
    ...mapActions({
      removeAthlete:"athletes/removeAthlete"
    }),

    /**
     * Function to be called  after 
     * the user has agreed to the terms and has 
     * pressed the remove button.
     */
    async deleteAthlete(){
      if(this.id > 0 && this.terms) { 
        this.deleting = true 
        const response = await this.removeAthlete(this.id)
        this.deleting = false
        if(response !== 'error'){
          this.close()
        }
      } 
    },

    /**
     * Closes the DeleteAthleteModal
     */
    close(){      
      this.terms = false
      this.$emit("update:dialog",false);
     
    }
  }
}
</script>