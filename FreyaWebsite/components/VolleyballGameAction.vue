<template>
  <v-container>
    <v-alert
      v-if="action_type === notification"
      border="bottom"
      colored-border
      icon="mdi-bell-outline"
      elevation="2"
      width="500px"
    >{{ message }}</v-alert>
    <v-card v-else width="500px">
      <v-toolbar :color="in_color" dark flat>
        <v-row justify="center" align="center">
          <v-card-title>{{ action_type }}</v-card-title>
        </v-row>
      </v-toolbar>
      <v-row>
        <v-col :cols="3">
          <v-avatar size="100" class="mx-10">
            <v-icon x-large :color="in_color" v-if="!athlete_img" height="100px">mdi-account</v-icon>
            <v-img v-else :src="athlete_img" alt="ATHLETE" height="100px" />
            <v-progress-circular indeterminate color="grey lighten-5"></v-progress-circular>
          </v-avatar>
        </v-col>
        <v-col allign="center">
          <v-row class="mx-10" justify="center">
            <v-card-title>#{{athlete_number}}. {{athlete_name}}</v-card-title>
          </v-row>
        </v-col>
      </v-row>
    </v-card>
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
    athlete_img: String,
    in_color: String
  },
  data: () => ({
    notification: "Notification" // ADD ACTION TYPES AND A DICTIONARY TO MAP THEM FROM ENGLISH TO SPANISH...
  })
};
</script>