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
                @click.native="start_edit_opp_player()"
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
          <v-btn color="gray darken-3" text @click="delete_dialog = false">No</v-btn>
          <v-btn color="green darken-1" :loading="button_loading" text @click="deleteAthlete()">Sí</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
    <v-dialog v-model="edit_opp_athlete_dialog" persistent max-width="600px">
      <v-card>
        <v-card-title>
          <span class="headline">Editar Atleta Oponente</span>
        </v-card-title>
        <v-container>
          <v-row allign="center">
            <v-col>
              <v-card-title>Número de Atleta: {{this.athlete_number}}</v-card-title>
              <v-form ref="edit_opp_form">
                <v-text-field
                  label="Nombre del atleta *"
                  required
                  v-model="new_athlete_name"
                  counter="200"
                  :rules="athlete_name_rules"
                  outlined
                ></v-text-field>
                <small>* Indica que es un valor requerido</small>
              </v-form>
            </v-col>
          </v-row>
        </v-container>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="gray darken-3" text @click="close_edit_dialog()">Cerrar</v-btn>
          <v-btn
            color="primary darken-1"
            :loading="button_loading"
            text
            @click.native="edit_opp_player()"
          >Enviar</v-btn>
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
    delete_dialog: false,
    edit_opp_athlete_dialog: false,

    // Data to be temporarily used during edits.
    new_athlete_name: "",
    new_number: 0,

    button_loading: false,

    // Validation rules.
    athlete_name_rules: [
      v =>
        (v && v.length > 0 && v.length <= 200) ||
        "Las notificaciones deben tener entre 1 y 200 caracteres."
    ],

    athlete_number_rules: [
      v => {
        // Validate is integer between 0 and 1000.
        if (!isNaN(parseInt(v)) && v >= 0 && v <= 1000) return true;
        // Notify error.
        return "El número de atleta debe ser un entero entre 0 y 1000.";
      }
    ]
  }),

  methods: {
    ...mapActions({
      updateOppAthlete: "volleyballPBP/updateOppAthlete",
      removeAthlete: "volleyballPBP/removeAthlete"
    }),

    async deleteAthlete() {
      const params = `event_id=${this.event_id}&athlete_id=${this.athlete_number}&team=opponent`;
      this.button_loading = true;
      if (await this.removeAthlete(params)) {
        this.delete_dialog = false;
      }
      this.button_loading = false;
    },

    close_edit_dialog() {
      this.edit_opp_athlete_dialog = false;
      this.$refs.edit_opp_form.reset();
    },

    start_edit_opp_player() {
      this.new_athlete_name = this.athlete_name;
      this.new_number = this.athlete_number;
      this.edit_opp_athlete_dialog = true;
    },

    async edit_opp_player() {
      const payload = {
        event_id: this.event_id,
        data: {
          number: this.athlete_number,
          name: this.new_athlete_name
        },
        team: "opponent"
      };

      this.button_loading = true;
      if (
        this.$refs.edit_opp_form.validate() &&
        (await this.updateOppAthlete(payload))
      ) {
        this.edit_opp_athlete_dialog = false;
      }
      this.button_loading = false;
    }
  }
};
</script>