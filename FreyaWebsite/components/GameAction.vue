<template>
  <v-container>
    <v-row v-if="action_type === notification">
      <v-col></v-col>
    </v-row>
  </v-container>
</template>

<script>
export default {
  props: {
    action_type: String, // After this, the following props are optional depending on the action_type.
    message: String,
    team: String,
    athlete_name: String,
    athlete_number: Number,
    athlete_position: String
  },
  data() {
    notification: "Notification";
  }
};
</script>