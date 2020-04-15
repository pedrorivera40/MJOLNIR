<template>
  <div class="wrapper d-flex align-center justify-center">
    <v-card width="500" class="elevation-12 mx-auto">
      <v-toolbar color="primary" dark flat>
        <v-toolbar-title @click="setSnackbar({text:'hello'})">Login</v-toolbar-title>
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
              id="password"
              label="Password"
              name="password"
              prepend-icon="mdi-lock"
              :append-icon=" show ? 'mdi-eye-off' : 'mdi-eye'"
              :type="show ? 'text' : 'password'"
              v-model="password"
              @click:append="show=!show"
              :rules="[required('password')]"
            />
          </v-form>
        </v-container>
      </v-card-text>
      <v-card-actions>
        <nuxt-link class="ml-6" to="/activate">
          Activate account.
        </nuxt-link>
        <v-spacer />
        <v-btn
          :dark="valid"
          :loading="isLoading"
          :disabled="!valid"
          color="primary_light"
          class="ma-5"
          @click="login({username: username, password: password})"
        > Login </v-btn>
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
      show: false,
      username: "newUser27",
      password: "ninjaTurtles1!",
      ...rules,
    };
  },
  methods: {
    ...mapActions({
      login: "userAuth/login",
      setSnackbar: "notifications/setSnackbar"
    })
  },
  computed: {
    ...mapGetters({
      isLoading: "userAuth/isLoading",
    })
  }
};
</script>

<style lang="scss" scoped>
.wrapper {
  height: 100%;
}
</style>