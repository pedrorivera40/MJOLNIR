<template>
  <v-row justify="center">
    <v-dialog v-model="dialog" persistent max-width="290">
      <v-card>
        <v-toolbar flat color="primary_dark">
          <v-toolbar-title class="headline white--text">
            Delete User
          </v-toolbar-title>
        </v-toolbar>
        <v-card-title class=""
          >Are you sure you want to delete {{ username }}?</v-card-title
        >
        <v-card-text>This action is <strong>irreversible</strong>.</v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <!-- TODO emit event on close to handle resetting of edited user object-->
          <v-btn color="green darken-1" text @click="close()">Cancel</v-btn>
          <v-btn color="green darken-1" text @click="close()">Delete</v-btn>
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
    username: String
  },
  methods: {
    close() {
      this.$emit("update:dialog", false);
    }
  }
};
</script>

<style>
</style>