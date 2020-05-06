<template>
  <v-row>
    <v-col justify="center">
      <v-card class="text-center mx-10" outlined>
        <v-row justify="center">
          <v-card-title>{{ uprm_team_name }}</v-card-title>
        </v-row>

        <v-tooltip bottom v-for="athlete in uprm_roster" :key="athlete.number">
          <template v-slot:activator="{ on }">
            <v-btn
              class="mx-2 my-4"
              dark
              color="secondary"
              @click.native="uprm_athlete_action(athlete.number)"
              width="50"
              height="50"
              v-on="on"
            >{{athlete.number}}</v-btn>
          </template>
          <span>{{ athlete.name }}</span>
        </v-tooltip>

        <v-row justify="center">
          <v-tooltip bottom>
            <template v-slot:activator="{ on }">
              <v-btn class="ma-4" color="primary" dark v-on="on">
                <v-icon>mdi-pencil</v-icon>
              </v-btn>
            </template>
            <span>Manejar atletas de UPRM</span>
          </v-tooltip>
        </v-row>
      </v-card>
    </v-col>
    <v-col allign="center">
      <v-row>
        <v-tooltip bottom v-for="button in action_buttons" :key="button.key">
          <template v-slot:activator="{ on }">
            <v-col>
              <v-row>
                <v-row allign="center" justify="center">
                  <v-btn
                    class="mx-4"
                    v-if="button.button_state === true"
                    :pressed="button.button_state"
                    light
                    color="white"
                    @click.native="clear_action_buttons()"
                    width="175"
                    v-on="on"
                  >{{ map_action(button.action_type) }}</v-btn>
                  <v-btn
                    class="mx-4"
                    v-else
                    :pressed="button.button_state"
                    dark
                    color="primary"
                    @click.native="set_action_button(button.key)"
                    width="175"
                    v-on="on"
                  >{{ map_action(button.action_type) }}</v-btn>
                </v-row>
              </v-row>
            </v-col>
          </template>
          <span>Añadir "{{ map_action(button.action_type) }}"</span>
        </v-tooltip>
      </v-row>
    </v-col>
    <v-col justify="center">
      <v-card class="text-center mx-10" outlined>
        <v-row justify="center">
          <v-card-title>{{ opp_team_name }}</v-card-title>
        </v-row>

        <v-tooltip bottom v-for="athlete in opp_roster" :key="athlete.number">
          <template v-slot:activator="{ on }">
            <v-btn
              class="mx-2 my-4"
              dark
              color="secondary"
              @click.native="opp_athlete_action(athlete.number)"
              width="50"
              height="50"
              v-on="on"
            >{{athlete.number}}</v-btn>
          </template>
          <span>{{ athlete.name }}</span>
        </v-tooltip>

        <v-row justify="center">
          <v-tooltip bottom>
            <template v-slot:activator="{ on }">
              <v-btn class="ma-4" color="primary" dark v-on="on">
                <v-icon>mdi-pencil</v-icon>
              </v-btn>
            </template>
            <span>Manejar atletas de equipo oponente</span>
          </v-tooltip>
        </v-row>
      </v-card>
    </v-col>
  </v-row>
</template>

<script>
import { mapActions } from "vuex";

export default {
  props: {
    event_id: String
  },

  data: () => ({
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
      sendGameAction: "volleyballPBP/sendGameAction",
      notifyNotActionSelected: "volleyballPBP/notifyNotActionSelected"
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

    uprm_athlete_action(id) {
      let action = "";
      for (let index in this.action_buttons) {
        if (this.action_buttons[index].button_state === true) {
          action = this.action_buttons[index].action_type;
          this.action_buttons[index].button_state = false;
        }
      }
      if (action === "") {
        this.notifyNotActionSelected();
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
        this.notifyNotActionSelected();
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