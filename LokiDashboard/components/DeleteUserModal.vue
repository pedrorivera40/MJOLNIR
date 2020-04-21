<template>
  <v-row justify="center">
    <v-dialog v-model="dialog" persistent max-width="350">
      <v-card>
        <v-toolbar flat color="primary_dark">
          <v-toolbar-title class="headline white--text">
            Delete User
          </v-toolbar-title>
        </v-toolbar>
        <v-card-title
          >Are you sure you want to delete {{ username }}'s
          account?</v-card-title
        >
        <v-card-text>
          This action is <strong>irreversible</strong>.
          <v-checkbox
            v-model="terms"
            :label="`I accept the consequences.`"
          ></v-checkbox>
        </v-card-text>

        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="green darken-1" text @click="close()"> Cancel </v-btn>
          <v-btn
            color="green darken-1"
            :disabled="!terms"
            :loading="isLoading"
            text
            @click="delete_User()"
          >
            Delete
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-row>
</template>

<script>
import { mapActions } from "vuex";
export default {
  name: "DeleteUserModal",
  props: {
    dialog: Boolean,
    username: String,
    id: Number
  },
  data() {
    return {
      terms: false,
      isLoading: false
    };
  },
  methods: {
    ...mapActions({
      deleteUser: "dashboardUsers/deleteUser"
    }),
    
    close() {
      this.terms = false;
      this.$emit("update:dialog", false);
    },
    async delete_User() {
      this.isLoading = true;
      const payload = {
        id: this.id,
        username: this.username
      };
      await this.deleteUser(payload);
      this.terms = false;
      this.$emit("update:dialog", false);
      this.isLoading = false;
    }
  }
};
</script>

<style>
</style>