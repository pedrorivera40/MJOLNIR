<template>
  <v-row justify="center">
    <v-dialog v-model="dialog" persistent max-width="350">
      <v-card>
        <v-toolbar flat color="primary_dark">
          <v-toolbar-title class="headline white--text">
            Remover Estadisticas
          </v-toolbar-title>
        </v-toolbar>
        <v-card-title
          >¿Está seguro quiere remover las estadisticas seleccionadas?</v-card-title
        >
        <v-card-text>
          <v-checkbox
            v-model="terms"
            :label="`Confirmar`"
          ></v-checkbox>
        </v-card-text>

        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="green darken-1" text @click="close()"> Cancelar </v-btn>
          <v-btn
            color="green darken-1"
            :disabled="!terms"
            :loading="isLoading"
            text
            @click="removeIndividualStatsLocal()"
          >
            Remover
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-row>
</template>

<script>
import { mapActions } from "vuex";
export default {
  name: "DeleteIndividualStatsModal",
  props: {
    dialog: Boolean,
    event_id: Number,
    athlete_id: Number,
    refresh_stats: Boolean,
    sport_route: String,
    category_id: Number
  },
  data() {
    return {
      terms: false,
      isLoading: false
    };
  },
  methods: {
    ...mapActions({
      removeIndividualStatistics: "results/removeIndividualStatistics",
      setQueryLoading: "results/setQueryLoading"
    }),
    
    close() {
      this.terms = false;
      this.$emit("update:dialog", false);
    },
    async removeIndividualStatsLocal() {
      this.isLoading = true;
      if (this.category_id != '' && this.category_id != null){
        const param_json1 = {
          sport_route: this.sport_route,
          athlete_id: Number(this.athlete_id),
          event_id: Number(this.event_id),
          category_id: Number(this.category_id)
        };
        console.log("HEY WE GONNA REMOVE!",param_json1)
        await this.setQueryLoading();
        await this.removeIndividualStatistics(param_json1);
      }
      else{
        const param_json2 = {
          sport_route: this.sport_route,
          athlete_id: Number(this.athlete_id),
          event_id: Number(this.event_id)
        };
        console.log("HEY WE GONNA REMOVE!",param_json2)
        await this.setQueryLoading();
        await this.removeIndividualStatistics(param_json2);
      }
      
     
      this.terms = false;
      this.$emit("update:refresh_stats",true);
      this.$emit("update:dialog", false);
      this.isLoading = false;
      
    }
  }
};
</script>

<style>
</style>