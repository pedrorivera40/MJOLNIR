<template>
  <v-row justify="center">
    <v-dialog v-model="dialog" persistent max-width="480px">
      <v-card class="elevation-12 mx-auto">
        <v-toolbar color="primary" dark flat>
          <v-toolbar-title>Password Reset</v-toolbar-title>
          <v-spacer />
        </v-toolbar>
        <v-card-title class="text--secondary">
          Reset {{ username }}'s password
        </v-card-title>
        <v-card-text>
          <v-container>
            <v-form v-model="valid">
              <v-text-field
                id="new-password"
                label="New Password"
                name="new-password"
                prepend-icon="mdi-lock"
                :append-icon="showNew ? 'mdi-eye-off' : 'mdi-eye'"
                :type="showNew ? 'text' : 'password'"
                v-model="newPassword"
                @click:append="showNew = !showNew"
                :rules="[
                  required('password', 'You must input a new password.'),
                  minLength('password', 10),
                  maxLength('password', 64),
                  passwordFormat()
                ]"
              />
              <v-text-field
                id="confirm-password"
                label="Comfirm Password"
                name="confirm-password"
                prepend-icon="mdi-lock-check"
                :append-icon="showConf ? 'mdi-eye-off' : 'mdi-eye'"
                :type="showConf ? 'text' : 'password'"
                v-model="repeat"
                @click:append="showConf = !showConf"
                :rules="[
                  required('password', 'You must confirm your new password.'),
                  passwordMatch(newPassword)
                ]"
              />
            </v-form>
            <v-checkbox v-model="sure" label="Update password?" />
          </v-container>
        </v-card-text>
        <v-card-actions>
          <v-spacer />
          <v-btn color="primary darken-1" text @click="close()">
            Close
          </v-btn>
          <v-btn
            color="primary darken-1"
            text
            @click="save()"
            :disabled="!(valid && sure)"
            :loading="isLoading"
          >
            Save
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-row>
</template>

<script>
import { mapActions, mapGetters } from "vuex";
import rules from "@/utils/validations";
export default {
  name: "PasswordResetModal",
  props: {
    dialog: Boolean,
    username: String,
    fullName: String,
    email: String,
    isActive: Boolean,
    id: Number
  },
  data() {
    return {
      valid: false,
      sure: false,
      showNew: false,
      showConf: false,
      isLoading: false,
      newPassword: "",
      repeat: ""
    };
  },
  methods: {
    ...mapActions({
      resetPasswordByAdmin: "dashboardUsers/resetPasswordByAdmin"
    }),
    ...rules,
    close() {
      this.$emit("update:dialog", false);
    },
    async save() {
      this.isLoading = true;
      await this.resetPasswordByAdmin({
        id: this.id,
        username: this.username,
        password: this.repeat
      });
      this.isLoading = false;
      this.close();
    }
  },
  computed: {
    ...mapGetters({
      permissions: "dashboardUsers/permissions",
      isLoadingP: "dashboardUsers/isLoadingP"
    })
  }
};
</script>

<style>
</style>