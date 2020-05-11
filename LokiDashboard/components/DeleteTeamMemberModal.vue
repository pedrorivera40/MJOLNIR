<template>
  <v-row justify="center">
    <v-dialog v-model="dialog" persistent max-width="350">
      <v-card>
        <v-toolbar flat color="primary_dark">
          <v-toolbar-title class="headline white--text">
            Remover Miembro de Equipo
          </v-toolbar-title>
        </v-toolbar>
        <v-card-title
          >¿Está seguro quiere remover atleta del equipo?</v-card-title
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
            color="grey darken-3"
            :disabled="!terms"
            :loading="isLoading"
            text
            @click="removeFromTeam()"
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
  name: "DeleteTeamMemberModal",
  props: {
    dialog: Boolean,
    athlete_id: Number,
    team_id: Number,
    sport_id: Number,
    season_year: Number
  },
  data() {
    return {
      terms: false,
      isLoading: false
    };
  },
  methods: {
    ...mapActions({
      removeTeamMember: "teams/removeTeamMember",
      setQueryLoading: "teams/setQueryLoading",
      setNullTeam:"teams/setNullTeam",
      setNullTeamMembers:"teams/setNullTeamMembers",
      getTeamByYear:"teams/getTeamByYear"
    }),
    getSeasonDataPost(){
      this.setQueryLoading()
      this.setNullTeam()
      this.setNullTeamMembers()
      const team_params = {
        sport_id: String(this.sport_id),
        season_year: String(this.season_year)
      }
      //console.log("At the index level inside the getSeasonData, request params look like",team_params)
      this.getTeamByYear(team_params)   			
    },
    close() {
      this.terms = false;
      this.$emit("update:dialog", false);
    },
    async removeFromTeam() {
      this.isLoading = true;
      const payload = {
        team_id: this.team_id,
        athlete_id: this.athlete_id
      };
      await this.setQueryLoading();
      await this.removeTeamMember(payload);
      this.terms = false;
      await this.getSeasonDataPost()
      this.$emit("update:dialog", false);
      this.isLoading = false;
    }
  }
};
</script>

<style>
</style>