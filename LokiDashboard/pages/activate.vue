<template>
  <div class="wrapper d-flex align-center justify-center">
    <v-card width="500" class="elevation-12 mx-auto">
      <v-toolbar color="primary" dark flat>
        <v-toolbar-title> Password activateAccount </v-toolbar-title>
        <v-spacer />
      </v-toolbar>
      <v-card-text>
        <v-container>
          <v-form v-model="valid">
            <v-text-field
              label="Username"
              name="login"
              prepend-icon="mdi-account"
              type="text"
              v-model="username"
              :rules="[required('username')]"
            />

            <v-text-field
              id="current-password"
              label="Current Password"
              name="current-password"
              prepend-icon="mdi-lock-clock"
              :append-icon="showCurr ? 'mdi-eye-off' : 'mdi-eye'"
              :type="showCurr ? 'text' : 'password'"
              v-model="password"
              @click:append="showCurr = !showCurr"
              :rules="[
                required('password', 'You must input your current password.')
              ]"
            />
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
                passwordFormat(),
                passwordDiffFromOld(password)
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
        </v-container>
      </v-card-text>
      <v-card-actions>
        <nuxt-link class="ml-6" to="/login">
          Go Back
        </nuxt-link>
        <v-spacer />
        <v-btn
          :loading="isLoading"
          :dark="valid"
          :disabled="!valid"
          color="primary_light"
          class="ma-5"
          @click="activateAccount({ username: username, password: password, new_password: repeat })"
        >
          Submit
        </v-btn>
      </v-card-actions>
    </v-card>
  </div>
</template>

<script>
import { mapActions, mapGetters } from "vuex";
import rules from "@/utils/validations";
export default {
  auth: "guest",
  layout: "guest",
  data() {
    return {
      valid: false,
      showCurr: false,
      showNew: false,
      showConf: false,
      username: "newUser27",
      password: "ninjaTurtles1!",
      newPassword: "",
      repeat: "",
      ...rules
    };
  },
  methods: {
    ...mapActions({
      activateAccount: "userAuth/activateAccount"
    })
  },
  computed: {
    ...mapGetters({
      isLoading: "userAuth/isLoading"
    })
  }
};
</script>

<style lang="scss" scoped>
.wrapper {
  height: 100%;
}
</style>