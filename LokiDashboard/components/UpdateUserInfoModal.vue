<template>
  <v-row justify="center">
    <v-dialog v-model="dialog" persistent max-width="600px">
      <v-card>
        <v-toolbar flat color="primary_dark">
          <v-toolbar-title class="headline white--text">
            Delete User
          </v-toolbar-title>
        </v-toolbar>
        <v-card-text>
          <v-container v-model="valid">
            <v-row>
              <v-col cols="12">
                <v-text-field
                  label="Full Name*"
                  required
                  :rules="[required('name', 'Please input Full Name,')]"
                />
              </v-col>
              <v-col cols="12">
                <v-text-field label="Email*" required :rules="[required('email', 'Please input email.'), emailFormat()]"></v-text-field>
              </v-col>
              <v-col cols="12">
                <v-text-field label="Username*" required :rules="[required('username', 'Please input username.')]"></v-text-field>
              </v-col>
              <v-col cols="12" sm="6">
                <v-switch
                  v-model="isActive"
                  :label="`Account Active: ${isActive.toString()}`"
                ></v-switch>
              </v-col>
            </v-row>
          </v-container>
          <small>*indicates required field</small>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="blue darken-1" text @click="close()">Close</v-btn>
          <v-btn color="blue darken-1" text @click="close()" :disabled="!valid">Save</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-row>
</template>

<script>
import rules from "@/utils/validations";
export default {
  name: "UpdateUserInfoModal",
  props: {
    dialog: Boolean,
    username: String,
    fullName: String,
    email: String,
    isActive: Boolean
  },
  data() {
    return {
      valid: false,
    };
  },
  methods: {
    close() {
      console.log(this.valid)
      // this.$emit("update:dialog", false);
    },
    ...rules,
  }
};
</script>

<style>
</style>