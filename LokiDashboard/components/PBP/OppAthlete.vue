<template class="justify-center">
  <v-card outlined class="pa-md-4 mx-lg-auto">
    <v-row align="center" justify="space-around">
      <v-col :cols="3">
        <v-row justify="center">
          <v-avatar size="110" class="mx-10">
            <v-icon x-large :color="opp_color" v-if="!athlete_img" height="110px">mdi-account</v-icon>
            <v-img v-else :src="athlete_img" alt="ATHLETE" height="110px" />
            <v-progress-circular indeterminate color="grey lighten-5"></v-progress-circular>
          </v-avatar>
        </v-row>
      </v-col>
      <v-col justify="left">
        <v-row>
          <v-card-text
            class="headline text-left"
            style="headline word-break: normal;"
          >Nombre: {{athlete_name}}</v-card-text>
        </v-row>
        <v-row>
          <v-card-text
            class="subtitle-1 text-left"
            style="word-break: normal;"
          >Número: {{athlete_number}}</v-card-text>
        </v-row>
      </v-col>
      <v-col :cols="2" allign="center" justify="right">
        <v-row>
          <v-tooltip bottom>
            <template v-slot:activator="{ on }">
              <v-btn
                class="ma-2"
                color="gray"
                fab
                small
                dark
                @click.native="edit_action()"
                v-on="on"
              >
                <v-icon>mdi-pencil</v-icon>
              </v-btn>
            </template>
            <span>Editar atleta</span>
          </v-tooltip>
        </v-row>
        <v-row>
          <v-tooltip bottom>
            <template v-slot:activator="{ on }">
              <v-btn
                class="ma-2"
                color="red"
                fab
                small
                dark
                @click.native="delete_dialog = true"
                v-on="on"
              >
                <v-icon>mdi-trash-can</v-icon>
              </v-btn>
            </template>
            <span>Eliminar atleta</span>
          </v-tooltip>
        </v-row>
      </v-col>
    </v-row>
    <v-dialog v-model="delete_dialog" persistent max-width="300">
      <v-card>
        <v-card-title class="text-center" style="word-break: normal;">Eliminar Atleta Oponente</v-card-title>
        <v-card-text>Por favor confirme si desea eliminar el atleta oponente seleccionado.</v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="green darken-1" text @click="delete_dialog = false">No</v-btn>
          <v-btn color="green darken-1" text @click="deleteAthlete()">Sí</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-card>
</template>

<script>
import { mapActions, mapGetters } from "vuex";

export default {
  props: {
    athlete_name: String,
    athlete_img: String,
    athlete_number: Number,
    event_id: Number,
    roster: null,
    opp_color: String
  },

  data: () => ({
    delete_dialog: false
  }),

  methods: {
    ...mapActions({
      addPBPAthlete: "volleyballPBP/addPBPAthlete",
      removeAthlete: "volleyballPBP/removeAthlete"
    }),

    deleteAthlete() {
      const params = `event_id=${this.event_id}&athlete_id=${this.athlete_number}&team=opponent`;
      this.removeAthlete(params);
      this.delete_dialog = false;
    }
  }
};
</script>