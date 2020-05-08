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
          <v-btn color="primary" text @click="notification_dialog = false">Cerrar</v-btn>
          <v-btn color="primary" text @click.native="editNotification()">Enviar</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
    <v-dialog v-model="delete_dialog" persistent max-width="300">
      <v-card>
        <v-card-title class="text-center" style="word-break: normal;">Eliminar Acción de Juego</v-card-title>
        <v-card-text>Por favor confirme si desea eliminar la acción de juego seleccionada.</v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="green darken-1" text @click="delete_dialog = false">No</v-btn>
          <v-btn color="green darken-1" text @click="deleteGameAction()">Sí</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
    <v-hover v-slot:default="{ hover }" open-delay="25">
      <v-card v-if="action_type === notification" width="550px" :elevation="hover ? 16 : 2">
        <v-toolbar :color="in_color" dark flat>
          <v-row justify="center" align="center">
            <v-card-title>{{ map_action(action_type) }}</v-card-title>
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
            <v-card-title>{{ map_action(action_type) }}</v-card-title>
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
                    @click.native="edit_action()"
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
    athlete_img: String,
    in_color: String,
    id: String,
    event_id: Number
  },
  data: () => ({
    notification: "Notification", // ADD ACTION TYPES AND A DICTIONARY TO MAP THEM FROM ENGLISH TO SPANISH...
    notification_dialog: false,
    delete_dialog: false,
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

    edit_action() {
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
    }
  }
};
</script>