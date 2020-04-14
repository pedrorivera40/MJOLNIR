<template>
  <v-row>
    <v-col>
      <v-card></v-card>
    </v-col>
    <v-col>
      <v-row>
        <v-col v-for="button in action_buttons" :key="button.key">
          <v-row allign="center" justify="center">
            <v-btn
              class="mx-4"
              v-if="button.button_state === true"
              :pressed="button.button_state"
              dark
              color="red"
              @click.native="clear_action_buttons()"
              width="150"
            >{{button.action_type}}</v-btn>
            <v-btn
              class="mx-4"
              v-else
              :pressed="button.button_state"
              dark
              color="primary"
              @click.native="set_action_button(button.key)"
              width="150"
            >{{button.action_type}}</v-btn>
          </v-row>
        </v-col>
      </v-row>
      <v-row justify="center">
        <v-btn depressed dark color="black" width="300">NOTIFICACIÓN</v-btn>
      </v-row>
    </v-col>
    <v-col>
      <v-card></v-card>
    </v-col>
  </v-row>
</template>

<script>
export default {
  props: {
    uprm_roster: [],
    opp_roster: [],
    uprm_team_name: String,
    opp_team_name: String
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
    ]
  }),
  methods: {
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
    }
  }
};
</script>