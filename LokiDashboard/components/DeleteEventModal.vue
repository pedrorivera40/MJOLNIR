<template>
 <v-row justify="center">
   <v-dialog v-model="dialog" persistent max-width="400">            
      <v-card>
        <v-card-title class="headline">¿Estás seguro de que quieres eliminar el evento con id:{{id}}?</v-card-title>
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
          <v-btn color="green darken-1" text @click="close()">Cancelar</v-btn>
          <v-btn
           color="green darken-1" 
           :disabled="!terms" 
           text 
           :loading="deleting"
           @click="deleteEvent()">Borrar</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>       
 </v-row>
</template>

<script>
import { mapActions } from "vuex"

export default {
  name:"DeleteEventModal",
  props:{
    dialog:Boolean,
    id:Number, //ID of the event in the database
    trigger:Boolean,
  },

  data:() =>({
    terms:false,
    deleting:false,
  }),

  methods:{
    ...mapActions({
      removeEvent:"events/removeEvent"
    }),

    /**
     * Function to be called  after 
     * the user has agreed to the terms and has 
     * pressed the remove button.
     */
    async deleteEvent(){
      if(this.id > 0 && this.terms) { 
        this.deleting = true 
        //Call vuex action and store response
        const response = await this.removeEvent(this.id)
        this.deleting = false
        if(response !== 'error'){
          this.$emit("update:trigger",false)
          this.close()
        }
      } 
    },
    /**
     * Closes the DeleteEventModal
     */
    close(){      
      this.terms = false
      this.$emit("update:dialog",false);
      
    }
  }
}
</script>