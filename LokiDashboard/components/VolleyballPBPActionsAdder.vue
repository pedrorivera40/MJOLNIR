<template>
  <v-row>
    <v-col justify="center">
      <v-card class="text-center mx-10" outlined>
        <v-row justify="center">
          <v-card-title>{{ uprm_team_name }}</v-card-title>
        </v-row>

        <v-btn
          class="ma-4"
          v-for="athlete in uprm_roster"
          :key="athlete.number"
          dark
          color="#a89f9e"
          @click.native="uprm_athlete_action(athlete.id)"
          width="50"
          height="50"
        >{{athlete.number}}</v-btn>
      </v-card>
    </v-col>
    <v-col>
      <v-row>
        <v-col v-for="button in action_buttons" :key="button.key">
          <v-row allign="center" justify="center">
            <v-btn
              class="mx-4"
              v-if="button.button_state === true"
              :pressed="button.button_state"
              light
              color="white"
              @click.native="clear_action_buttons()"
              width="175"
            >{{ map_action(button.action_type) }}</v-btn>
            <v-btn
              class="mx-4"
              v-else
              :pressed="button.button_state"
              dark
              color="green"
              @click.native="set_action_button(button.key)"
              width="175"
            >{{ map_action(button.action_type) }}</v-btn>
          </v-row>
        </v-col>
      </v-row>
      <v-row justify="center">
        <v-btn
          depressed
          dark
          color="#a89f9e"
          width="300"
          @click.native="on_notification_pressed()"
        >NOTIFICACIÓN</v-btn>
      </v-row>
    </v-col>
    <v-col justify="center">
      <v-card class="text-center mx-10" outlined>
        <v-row justify="center">
          <v-card-title>{{ opp_team_name }}</v-card-title>
        </v-row>

        <v-btn
          class="ma-4"
          v-for="athlete in opp_roster"
          :key="athlete.number"
          dark
          color="#a89f9e"
          @click.native="opp_athlete_action(athlete.number)"
          width="50"
          height="50"
        >{{athlete.number}}</v-btn>
      </v-card>
      <v-dialog v-model="notification_dialog" persistent max-width="600px">
        <v-card>
          <v-card-title>
            <span class="headline">Enviar Notificación</span>
          </v-card-title>
          <v-card-text>
            <v-container>
              <v-row allign="center">
                <v-col>
                  <v-text-field
                    label="Texto de notificación *"
                    required
                    v-model="notification_text"
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
            <v-btn color="primary" text @click.native="send_notification()">Enviar</v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
    </v-col>
  </v-row>
</template>

<script>
import { mapActions } from "vuex";

export default {
  props: {
    event_id: Number
  },

  data: () => ({
    notification_dialog: false,
    notification_text: "",
    notification_rules: [
      v =>
        (v.length > 0 && v.length <= 100) ||
        "Las notificaciones deben tener entre 1 y 100 caracteres."
    ],
    action_buttons: [
      { key: 1, action_type: "KillPoint", button_state: false },
      { key: 2, action_type: "AttackError", button_state: false },
      { key: 3, action_type: "Ace", button_state: false },
      { key: 4, action_type: "ServiceError", button_state: false },
      { key: 5, action_type: "Assist", button_state: false },
      { key: 6, action_type: "Block", button_state: false },
      { key: 7, action_type: "BlockPoint", button_state: false },
      { key: 8, action_type: "BlockingError", button_state: false },
      { key: 9, action_type: "Dig", button_state: false },
      { key: 10, action_type: "ReceptionError", button_state: false }
    ],
    uprm_roster: [
      { id: 1, number: 11, name: "Fulano de Tal" },
      { id: 2, number: 1, name: "Don Perenzejo" },
      { id: 3, number: 21, name: "Juan del Pueblo" },
      { id: 4, number: 3, name: "Pepe El De La Esquina" },
      { id: 5, number: 4, name: "Gonzalo Duarte" },
      { id: 6, number: 2, name: "Martes Domingo" },
      { id: 7, number: 6, name: "Tomas Almibar" },
      { id: 8, number: 16, name: "Pepe Trueno" },
      { id: 9, number: 8, name: "Eli Nocente" },
      { id: 10, number: 9, name: "Armando Guerra" },
      { id: 11, number: 14, name: "Armando Pleito" },
      { id: 12, number: 15, name: "Sin Nom Bre" }
    ],
    opp_roster: [
      { number: 11, name: "Fulano de Tal" },
      { number: 1, name: "Don Perenzejo" },
      { number: 21, name: "Juan del Pueblo" },
      { number: 3, name: "Pepe El De La Esquina" },
      { number: 4, name: "Gonzalo Duarte" },
      { number: 2, name: "Martes Domingo" },
      { number: 6, name: "Tomas Almibar" },
      { number: 16, name: "Pepe Trueno" },
      { number: 8, name: "Eli Nocente" },
      { number: 9, name: "Armando Guerra" },
      { number: 14, name: "Armando Pleito" },
      { number: 15, name: "Sin Nom Bre" }
    ],
    uprm_team_name: "Tarzanes",
    opp_team_name: "Gallitos"
  }),
  methods: {
    ...mapActions({
      sendGameAction: "volleyballPBP/sendGameAction"
    }),

    clear_action_buttons() {
      // Reset each action button state to false.
      for (let index in this.action_buttons) {
        this.action_buttons[index].button_state = false;
      }
    },
    set_action_button(button_key) {
      this.clear_action_buttons();
      for (let index in this.action_buttons) {
        if (this.action_buttons[index].key === button_key) {
          this.action_buttons[index].button_state = true;
        }
      }
    },
    on_notification_pressed() {
      this.clear_action_buttons();
      this.notification_text = "";
      this.notification_dialog = true;
    },
    send_notification() {
      if (
        this.notification_text.length > 0 &&
        this.notification_text.length <= 100
      ) {
        let payload = {
          event_id: this.event_id,
          data: {
            message: this.notification_text,
            action_type: "Notification"
          }
        };
        this.sendGameAction(payload);
        this.notification_dialog = false;
      }
    },
    uprm_athlete_action(id) {
      let action = "";
      for (let index in this.action_buttons) {
        if (this.action_buttons[index].button_state === true) {
          action = this.action_buttons[index].action_type;
          this.action_buttons[index].button_state = false;
        }
      }
      if (action === "") {
        console.log("ERROR MUST BE DISPLAYED... NO ACTION PRESSED");
      } else {
        console.log({ athlete_id: id, action_type: action, team: "uprm" });
      }
    },
    opp_athlete_action(number) {
      let action = "";
      for (let index in this.action_buttons) {
        if (this.action_buttons[index].button_state === true) {
          action = this.action_buttons[index].action_type;
          this.action_buttons[index].button_state = false;
        }
      }
      if (action === "") {
        console.log("ERROR MUST BE DISPLAYED... NO ACTION PRESSED");
      } else {
        console.log({
          athlete_id: number,
          action_type: action,
          team: "opponent"
        });
      }
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