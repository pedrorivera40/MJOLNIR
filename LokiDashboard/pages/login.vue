<template>
  <div class="wrapper d-flex align-center justify-center">
    <v-card width="500" class="elevation-12 mx-auto">
      <v-toolbar color="primary" dark flat>
        <v-toolbar-title>Login</v-toolbar-title>
        <v-spacer />
      </v-toolbar>
      <v-card-text>
        <v-container>
          <v-form>
            <v-text-field
              label="Username"
              name="login"
              prepend-icon="mdi-account"
              type="text"
              v-model="username"
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
            />
          </v-form>
        </v-container>
      </v-card-text>
      <v-card-actions>
        <a color="warning" class="ml-6">Forgot Password?</a>
        <v-spacer />
        <v-btn
          dark
          color="primary_light"
          class="ma-5"
          @click="login({username: username, password: password})"
        >Login</v-btn>
      </v-card-actions>
    </v-card>
  </div>
</template>

<script>
import { mapActions } from "vuex"
export default {
  midleware: 'guest',
  layout: 'guest',
  data() {
    return {
      show: false,
      username: "newUser27",
      password: "ninjaTurtles1!"
    };
  },
  methods: {
    ...mapActions({
      login: 'userAuth/login'
    })
  },
};
</script>

<style lang="scss" scoped>
.wrapper {
  height: 100%;
}
</style>