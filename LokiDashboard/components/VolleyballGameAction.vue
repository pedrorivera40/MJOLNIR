<template>
  <v-container>
    <v-dialog v-model="notification_dialog" persistent max-width="600px">
      <v-card>
        <v-card-title>
          <span class="headline">Editar Notificación</span>
        </v-card-title>
        <v-card-text>
          <v-container>
            <v-row allign="center">
              <v-col>
                <v-text-field
                  label="Texto de notificación *"
                  required
                  v-model="newMessage"
                  counter="100"
                  :rules="notification_rules"
                  outlined
                ></v-text-field>
                <small>* Indica que es un valor requerido</small>
              </v-col>
            </v-row>
          </v-container>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="gray darken-3" text @click="notification_dialog = false">Cerrar</v-btn>
          <v-btn color="primary" text @click.native="editNotification()">Enviar</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
    <v-dialog v-model="edit_play_dialog" persistent max-width="500px">
      <v-card>
        <v-card-title>
          <span class="headline">Editar Jugada</span>
        </v-card-title>

        <v-row justify="center">
          <v-col cols="12" sm="4">
            <v-card-title class="body-1" style="word-break: normal;">Jugada:</v-card-title>
          </v-col>
          <v-col cols="12" sm="6" allign="center">
            <v-select
              v-model="current_play"
              :items="plays"
              menu-props="auto"
              label="Jugada"
              hide-details
              single-line
            ></v-select>
          </v-col>
        </v-row>
        <v-row justify="center">
          <v-col cols="12" sm="4">
            <v-card-title class="body-1" style="word-break: normal;">Equipo:</v-card-title>
          </v-col>
          <v-col cols="12" sm="6">
            <v-select
              v-model="current_team"
              :items="teams"
              menu-props="auto"
              label="Equipo"
              hide-details
              single-line
            ></v-select>
          </v-col>
        </v-row>
        <v-row justify="center">
          <v-col cols="12" sm="4">
            <v-card-title class="body-1" style="word-break: normal;">Atleta:</v-card-title>
          </v-col>
          <v-col cols="12" sm="6">
            <v-select
              v-if="current_team === 'UPRM'"
              v-model="current_athlete"
              :items="uprmAthletes"
              :item-text="get_uprm_item_text"
              item-val="athlete_id"
              menu-props="auto"
              label="Debe seleccionar un atleta"
              hide-details
              single-line
              :rules="[(v) => (v != null) || 'Debe seleccionar un atleta']"
              required
            ></v-select>
            <v-select
              v-if="current_team === 'Oponente'"
              v-model="current_athlete"
              :items="oppAthletes"
              :item-text="get_opp_item_text"
              item-val="number"
              menu-props="auto"
              label="Debe seleccionar un atleta"
              hide-details
              single-line
              :rules="[(v) => v != null || 'Debe seleccionar un atleta']"
              required
            ></v-select>
          </v-col>
        </v-row>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="primary" text @click="edit_play_dialog = false">Cerrar</v-btn>
          <v-btn color="primary" text @click.native="editPlay()">Guardar</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
    <v-dialog v-model="delete_dialog" persistent max-width="300">
      <v-card>
        <v-card-title class="text-center" style="word-break: normal;">Eliminar Acción de Juego</v-card-title>
        <v-card-text>Por favor confirme si desea eliminar la acción de juego seleccionada.</v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="gray darken-3" text @click="delete_dialog = false">No</v-btn>
          <v-btn color="green darken-1" text @click="deleteGameAction()">Sí</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
    <v-hover v-slot:default="{ hover }" open-delay="25">
      <v-card v-if="action_type === notification" width="550px" :elevation="hover ? 16 : 2">
        <v-toolbar :color="in_color" dark flat>
          <v-row justify="center" align="center">
            <v-card-title>{{ game_actions_map[action_type] }}</v-card-title>
          </v-row>
        </v-toolbar>
        <v-row align="center">
          <v-col :cols="4" justify="center">
            <v-avatar size="100" class="mx-10">
              <v-icon x-large :color="in_color" v-if="!athlete_img" height="100px">mdi-bell-outline</v-icon>
            </v-avatar>
          </v-col>
          <v-col justify="center">
            <v-row allign="center">
              <v-col>
                <v-card-title class="text-center" style="word-break: normal;">{{ message }}</v-card-title>
              </v-col>
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
                    @click.native="startEditNotification()"
                    v-on="on"
                  >
                    <v-icon>mdi-pencil</v-icon>
                  </v-btn>
                </template>
                <span>Editar notificación</span>
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
                <span>Eliminar notificación</span>
              </v-tooltip>
            </v-row>
          </v-col>
        </v-row>
      </v-card>
      <v-card v-else width="550px" :elevation="hover ? 16 : 2">
        <v-toolbar :color="in_color" dark flat>
          <v-row justify="center" align="center">
            <v-card-title>{{ game_actions_map[action_type] }}</v-card-title>
          </v-row>
        </v-toolbar>
        <v-row>
          <v-col :cols="3">
            <v-avatar size="100" class="mx-10">
              <v-icon x-large :color="in_color" v-if="!athlete_img" height="100px">mdi-account</v-icon>
              <v-img v-else :src="athlete_img" alt="ATHLETE" height="100px">
                <template v-slot:placeholder>
                  <v-layout fill-height align-center justify-center ma-0>
                    <v-progress-circular indeterminate :color="in_color"></v-progress-circular>
                  </v-layout>
                </template>
              </v-img>
            </v-avatar>
          </v-col>
          <v-col allign="center">
            <v-row class="mx-10" justify="center">
              <v-card-title
                class="text-center"
                style="word-break: normal;"
              >#{{athlete_number}}. {{athlete_name}}</v-card-title>
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
                    @click.native="startEditPlay()"
                    v-on="on"
                  >
                    <v-icon>mdi-pencil</v-icon>
                  </v-btn>
                </template>
                <span>Editar jugada</span>
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
                <span>Eliminar jugada</span>
              </v-tooltip>
            </v-row>
          </v-col>
        </v-row>
      </v-card>
    </v-hover>
  </v-container>
</template>

<script>
import { mapActions } from "vuex";

export default {
  props: {
    action_type: String, // After this, the following props are optional depending on the action_type.
    message: String,
    athlete_name: String,
    athlete_number: Number,
    athlete_id: Number,
    athlete_img: String,
    in_color: String,
    id: String,
    event_id: Number,
    uprmAthletes: [],
    oppAthletes: [],
    team: String
  },
  data: () => ({
    // Notification keyword.
    notification: "Notification",

    // Dialog flags.
    notification_dialog: false,
    delete_dialog: false,
    edit_play_dialog: false,

    // Content to be displayed in the Edit Game Action dialog.
    teams: ["Oponente", "UPRM"],

    team_map: {
      Oponente: "opponent",
      UPRM: "uprm"
    },

    plays: [
      "Punto de Ataque",
      "Servicio Directo",
      "Punto de Bloqueo",
      "Asistencia",
      "Bloqueo",
      "Recepción",
      "Error de Ataque",
      "Error de Servicio",
      "Error de Bloqueo",
      "Error de Recepción"
    ],

    current_team: null,
    current_play: "",
    current_athlete: null,

    game_actions_map: {
      Notification: "Notificación",
      Notificación: "Notification",
      KillPoint: "Punto de Ataque",
      "Punto de Ataque": "KillPoint",
      Ace: "Servicio Directo",
      "Servicio Directo": "Ace",
      BlockPoint: "Punto de Bloqueo",
      "Punto de Bloqueo": "BlockPoint",
      Assist: "Asistencia",
      Asistencia: "Assist",
      Block: "Bloqueo",
      Bloqueo: "Block",
      Dig: "Recepción",
      Recepción: "Dig",
      AttackError: "Error de Ataque",
      "Error de Ataque": "AttackError",
      ServiceError: "Error de Servicio",
      "Error de Servicio": "ServiceError",
      BlockingError: "Error de Bloqueo",
      "Error de Bloqueo": "BlockingError",
      ReceptionError: "Error de Recepción",
      "Error de Recepción": "ReceptionError"
    },

    // Rules and placeholders.
    newMessage: "",
    notification_rules: [
      v =>
        (v.length > 0 && v.length <= 100) ||
        "Las notificaciones deben tener entre 1 y 100 caracteres."
    ]
  }),
  methods: {
    ...mapActions({
      updateGameAction: "volleyballPBP/updateGameAction",
      removeGameAction: "volleyballPBP/removeGameAction"
    }),

    // Setup v-models for editting a notification.
    startEditNotification() {
      this.current_team = this.team;
      this.newMessage = this.message;
      this.notification_dialog = true;
    },

    // Edit a notification game action.
    editNotification() {
      // Create payload with new message and notification info.
      if (this.newMessage.length >= 1 && this.newMessage.length <= 100) {
        const payload = {
          event_id: this.event_id,
          action_id: this.id,
          data: {
            action_type: this.notification,
            message: this.newMessage
          }
        };
        // Update notification.
        this.updateGameAction(payload);
        this.notification_dialog = false;
      }
    },

    deleteGameAction() {
      const payload = {
        event_id: this.event_id,
        action_id: this.id
      };
      this.removeGameAction(payload);
      this.delete_dialog = false;
    },

    startEditPlay() {
      this.edit_play_dialog = true;
      this.current_team = this.team;
      this.current_play = this.game_actions_map[this.action_type];

      // Find current UPRM athlete.
      if (this.current_team === "UPRM") {
        let index = -1;
        for (let i = 0; i < this.uprmAthletes.length; i++) {
          if (this.uprmAthletes[i].athlete_id === this.athlete_id) {
            index = i;
            break;
          }
        }

        if (index === -1) {
          this.current_athlete = {
            athlete_id: this.athlete_id,
            number: "?",
            first_name: "Atleta",
            middle_name: "",
            last_names: "Desconocido"
          };
        }

        this.current_athlete = this.uprmAthletes[index];
      }

      // Find current opponent athlete.
      else {
        let index = -1;
        for (let i = 0; i < this.oppAthletes.length; i++) {
          if (this.oppAthletes[i].number === this.athlete_id) {
            index = i;
            break;
          }
        }

        if (index === -1) {
          this.current_athlete = {
            athlete_id: this.athlete_id,
            number: "?",
            first_name: "Atleta",
            middle_name: "",
            last_names: "Desconocido"
          };
        }

        this.current_athlete = this.oppAthletes[index];
      }
    },

    editPlay() {
      // Make sure an athlete was selected.
      console.log(this.current_athlete);
      if (this.current_athlete == null) {
        return;
      }

      const payload = {
        event_id: this.event_id,
        action_id: this.id,
        data: {
          action_type: this.game_actions_map[this.current_play],
          athlete_id:
            this.current_team === "UPRM"
              ? this.current_athlete.athlete_id
              : this.current_athlete.number,
          team: this.team_map[this.current_team]
        }
      };
      console.log(payload);
      console.log("NEED TO EDIT ACTION WITH ID = " + this.id);
    },

    map_action(action_name) {
      switch (action_name) {
        case "Notification":
          return "Notificación";

        case "KillPoint":
          return "Punto de Ataque";

        case "Ace":
          return "Servicio Directo";

        case "BlockPoint":
          return "Punto de Bloqueo";

        case "Assist":
          return "Asistencia";

        case "Block":
          return "Bloqueo";

        case "Dig":
          return "Recepción";

        case "AttackError":
          return "Error de Ataque";

        case "ServiceError":
          return "Error de Servicio";

        case "BlockingError":
          return "Error de Bloqueo";

        case "ReceptionError":
          return "Error de Recepción";

        default:
          return "Acción Desconocida";
      }
    },

    // Given an item (UPRM ATHLETE), return its name.
    get_uprm_item_text(item) {
      let index = -1;

      for (let i = 0; i < this.uprmAthletes.length; i++) {
        if (item.athlete_id === this.uprmAthletes[i].athlete_id) {
          index = i;
          break;
        }
      }

      if (index === -1) {
        return null;
      }

      const athlete = this.uprmAthletes[index];

      if (item.middle_name === "") {
        return (
          "#" + athlete.number + " " + item.first_name + " " + item.last_names
        );
      }
      return (
        "#" +
        athlete.number +
        " " +
        item.first_name +
        " " +
        item.middle_name +
        " " +
        item.last_names
      );
    },
    get_opp_item_text(item) {
      let index = -1;

      for (let i = 0; i < this.oppAthletes.length; i++) {
        if (item.number === this.oppAthletes[i].number) {
          index = i;
          break;
        }
      }

      if (index === -1) {
        return null;
      }

      const athlete = this.oppAthletes[index];

      return "#" + athlete.number + " " + item.name;
    }
  },
  computed: {
    getRoster: function() {
      // UPRM selected.
      if (this.current_team === "UPRM") {
        console.log(this.uprmAthletes);
        return this.uprmAthletes;
      }
      // Opponent selected.
      if (this.current_team === "Oponente") {
        return this.oppAthletes;
      }

      // Otherwise, send an empty list.
      return [];
    }
  }
};
</script>