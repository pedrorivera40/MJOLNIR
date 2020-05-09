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
              v-if="action_buton_pressed === true"
              class="mx-2 my-4"
              dark
              color="secondary"
              @click.native="add_athlete_action(athlete.athlete_id, 'uprm')"
              width="50"
              height="50"
              v-on="on"
            >{{athlete.number}}</v-btn>
            <v-btn
              v-else
              class="mx-2 my-4"
              light
              color="#ececec"
              @click.native="add_athlete_action(athlete.athlete_id, 'uprm')"
              width="50"
              height="50"
              v-on="on"
            >{{athlete.number}}</v-btn>
          </template>
          <span
            v-if="action_buton_pressed === true"
          >{{ findAthleteName(athlete.athlete_id, uprm_roster) }}</span>
          <span v-else>Primero debe seleccionar un tipo de jugada</span>
        </v-tooltip>

        <v-row justify="center">
          <v-tooltip bottom>
            <template v-slot:activator="{ on }">
              <v-btn
                class="ma-4"
                color="primary"
                dark
                v-on="on"
                @click="manage_uprm_roster_dialog = true"
              >
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
              v-if="action_buton_pressed === true"
              class="mx-2 my-4"
              dark
              color="secondary"
              @click.native="add_athlete_action(athlete.number, 'opponent')"
              width="50"
              height="50"
              v-on="on"
            >{{athlete.number}}</v-btn>
            <v-btn
              v-else
              class="mx-2 my-4"
              light
              color="#ececec"
              @click.native="add_athlete_action(athlete.number, 'opponent')"
              width="50"
              height="50"
              v-on="on"
            >{{athlete.number}}</v-btn>
          </template>
          <span v-if="action_buton_pressed === true">{{ athlete.name }}</span>
          <span v-else>Primero debe seleccionar un tipo de jugada.</span>
        </v-tooltip>

        <v-row justify="center">
          <v-tooltip bottom>
            <template v-slot:activator="{ on }">
              <v-btn
                class="ma-4"
                color="primary"
                dark
                v-on="on"
                @click.native="manage_opp_roster_dialog = true"
              >
                <v-icon>mdi-pencil</v-icon>
              </v-btn>
            </template>
            <span>Manejar atletas de equipo oponente</span>
          </v-tooltip>
        </v-row>
      </v-card>
    </v-col>
    <v-dialog v-model="manage_uprm_roster_dialog" max-width="600">
      <v-card>
        <v-card-title
          class="headline text-center"
          style="word-break: normal;"
        >Manejo de Atletas UPRM</v-card-title>
        <v-card-text
          class="subtitle-1"
          style="word-break: normal;"
        >Marque los atletas de UPRM que están participando en este evento.</v-card-text>
        <v-divider />
        <UPRMAthlete
          v-for="athlete in valid_uprm_roster"
          :key="athlete.athlete_id + 3000"
          :athlete_first_name="athlete.first_name"
          :athlete_middle_name="athlete.middle_name"
          :athlete_last_names="athlete.last_names"
          :athlete_number="athlete.number"
          :athlete_img="athlete.profile_image_link"
          :event_id="event_id"
          :athlete_id="athlete.athlete_id"
          :roster="uprm_roster"
        />
        <v-divider />
        <v-card-actions fixed>
          <v-spacer></v-spacer>
          <v-btn color="green darken-1" text @click="manage_uprm_roster_dialog = false">Salir</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
    <v-dialog v-model="manage_opp_roster_dialog" max-width="600">
      <v-card>
        <v-card-title
          class="headline text-center"
          style="word-break: normal;"
        >Manejo de Atletas Oponente</v-card-title>
        <v-card-text
          class="subtitle-1"
          style="word-break: normal;"
        >Añada, modifique, o remueva los atletas del equipo oponente que participan en este evento.</v-card-text>
        <v-tooltip bottom>
          <template v-slot:activator="{ on }">
            <v-btn
              class="ma-6"
              color="primary"
              dark
              v-on="on"
              width="175"
              @click.native="add_opp_athlete_dialog = true"
            >
              <v-icon class="mx-1">mdi-plus</v-icon>Añadir Atleta
            </v-btn>
          </template>
          <span>Añadir atleta de equipo oponente</span>
        </v-tooltip>
        <v-divider />

        <OppAthlete
          v-for="athlete in opp_roster"
          :key="athlete.athlete_id + 3000"
          :athlete_name="athlete.name"
          :athlete_number="athlete.number"
          :athlete_img="athlete.profile_image_link"
          :event_id="event_id"
          :roster="opp_roster"
          :opp_color="opp_color"
        />
        <v-divider />
        <v-card-actions fixed>
          <v-spacer></v-spacer>
          <v-btn color="green darken-1" text @click="manage_opp_roster_dialog = false">Salir</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
    <v-dialog v-model="add_opp_athlete_dialog" persistent max-width="600px" ref="add_opp_form">
      <v-card>
        <v-card-title>
          <span class="headline">Añadir Atleta Oponente</span>
        </v-card-title>
        <v-container>
          <v-row allign="center">
            <v-col>
              <v-form ref="add_opp_form">
                <v-text-field
                  label="Nombre del atleta *"
                  required
                  v-model="athlete_name"
                  counter="200"
                  :rules="athlete_name_rules"
                  outlined
                ></v-text-field>
                <v-text-field
                  label="Número del atleta *"
                  required
                  v-model="athlete_number"
                  counter="4"
                  :rules="athlete_number_rules"
                  outlined
                ></v-text-field>
                <small>* Indica que es un valor requerido</small>
              </v-form>
            </v-col>
          </v-row>
        </v-container>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="primary" text @click="close_dialog()">Cerrar</v-btn>
          <v-btn color="primary" text @click.native="add_opp_player()">Enviar</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-row>
</template>

<script>
import { mapGetters, mapActions } from "vuex";
import UPRMAthlete from "../components/PBP/UPRMAthlete";
import OppAthlete from "../components/PBP/OppAthlete";

export default {
  // Custom Components for the PBP Actions Adder.
  components: {
    UPRMAthlete,
    OppAthlete
  },

  props: {
    event_id: Number,
    uprm_team_name: String,
    opp_team_name: String,
    uprm_roster: [],
    valid_uprm_roster: [],
    opp_roster: [],
    opp_color: String
  },

  data: () => ({
    // Dialog flags.
    manage_uprm_roster_dialog: false,
    manage_opp_roster_dialog: false,
    add_opp_athlete_dialog: false,

    athlete_name: "",
    athlete_number: "",

    // Action button pressed flag (denotes if there is an action button pressed?).
    action_buton_pressed: false,

    // Action button flags.
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
      sendGameAction: "volleyballPBP/sendGameAction",
      addPBPAthlete: "volleyballPBP/addPBPAthlete",
      notifyNotActionSelected: "volleyballPBP/notifyNotActionSelected"
    }),

    close_dialog() {
      this.manage_uprm_roster_dialog = false;
      this.manage_opp_roster_dialog = false;
      this.add_opp_athlete_dialog = false;
      this.$refs.add_opp_form.reset();
    },

    // Add opponent athlete into the system.
    async add_opp_player() {
      // Prepare payload for athlete to be added.
      const payload = {
        event_id: this.event_id,
        data: {
          number: parseInt(this.athlete_number),
          name: this.athlete_name
        },
        team: "opponent"
      };
      if (
        this.$refs.add_opp_form.validate() &&
        (await this.addPBPAthlete(payload))
      ) {
        this.add_opp_athlete_dialog = false;
      }
    },

    clear_action_buttons() {
      // Reset each action button state to false.
      for (let index in this.action_buttons) {
        this.action_buttons[index].button_state = false;
      }
      this.action_buton_pressed = false;
    },
    set_action_button(button_key) {
      this.clear_action_buttons();
      for (let index in this.action_buttons) {
        if (this.action_buttons[index].key === button_key) {
          this.action_buttons[index].button_state = true;
        }
      }
      this.action_buton_pressed = true;
    },

    add_athlete_action(id, team_val) {
      // If no action pressed, notify the user that needs to choose an action first.
      if (this.action_buton_pressed === false) {
        this.notifyNotActionSelected();
      }

      // At this point, an action has been pressed.

      // Find which game action was pressed.
      let action = "";
      for (let index in this.action_buttons) {
        if (this.action_buttons[index].button_state === true) {
          action = this.action_buttons[index].action_type;
          this.action_buttons[index].button_state = false;
        }
      }

      // Create payload for an UPRM game action.
      const payload = {
        event_id: this.event_id,
        data: {
          athlete_id: id,
          action_type: action,
          team: team_val
        }
      };

      this.sendGameAction(payload);
      this.action_buton_pressed = false;
    },

    findAthleteName(athlete_id, roster) {
      let athlete_index = -1;
      for (let index in roster) {
        if (roster[index].key == athlete_id) {
          athlete_index = index;
          continue;
        }
      }

      if (athlete_index === -1) {
        return "Atleta Desconocido";
      }
      let athlete_name = roster[athlete_index].first_name;
      if (roster[athlete_index].middle_name !== "") {
        athlete_name += " " + roster[athlete_index].middle_name;
      }
      athlete_name += " " + roster[athlete_index].last_names;

      return athlete_name;
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