<template>
  <v-row justify="center">
    <v-dialog v-model="dialog" persistent max-width="290">
      <v-card>
        <v-toolbar
          flat
          color="primary_dark"
        >
          <v-toolbar-tittle
          class="headline white--text">
            Delete User
          </v-toolbar-tittle>
        </v-toolbar>
        <v-card-title class=""
          >Are you sure you want to delete {{username}}?</v-card-title
        >
        <v-card-text
          >This action is <strong>irreversible</strong>.</v-card-text
        >
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="green darken-1" text @click="dialog = false"
            >Cancel</v-btn
          >
          <v-btn color="green darken-1" text @click="dialog = false"
            >delete</v-btn
          >
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-row>
</template>

<script>
export default {
  name: "DeleteUserModal",
  props: {
    dialog: Boolean,
    username: String,
  },
};
</script>

<style>
</style>