<template>
  <div class="wrapper d-flex align-center justify-center">
    <v-card width="500" class="elevation-12 mx-auto">
      <v-toolbar color="primary" dark flat>
        <v-toolbar-title> Activar Cuenta </v-toolbar-title>
        <v-spacer />
      </v-toolbar>
      <v-card-text>
        <v-container>
          <v-form v-model="valid">
            <v-text-field
              label="Nombre de usuario"
              name="login"
              prepend-icon="mdi-account"
              type="text"
              v-model="username"
              :rules="[required('username', 'Por favor, ingrese su nombre de usuario.')]"
            />

            <v-text-field
              id="current-password"
              label="Contraseña Temporal"
              name="current-password"
              prepend-icon="mdi-lock-clock"
              :append-icon="showCurr ? 'mdi-eye-off' : 'mdi-eye'"
              :type="showCurr ? 'text' : 'password'"
              v-model="password"
              @click:append="showCurr = !showCurr"
              :rules="[
                required('password', 'Debe ingresar la contraseña temporal.')
              ]"
            />
            <v-text-field
              id="new-password"
              label="Nueva Contraseña"
              name="new-password"
              prepend-icon="mdi-lock"
              :append-icon="showNew ? 'mdi-eye-off' : 'mdi-eye'"
              :type="showNew ? 'text' : 'password'"
              v-model="newPassword"
              @click:append="showNew = !showNew"
              :rules="[
                required('password', 'Por favor, ingrese una nueva contraseña.'),
                minLength('La contraseña', 10),
                maxLength('La contraseña', 64),
                passwordFormat(),
                passwordDiffFromOld(password)
              ]"
            />
            <v-text-field
              id="confirm-password"
              label="Confirma la Contraseña"
              name="confirm-password"
              prepend-icon="mdi-lock-check"
              :append-icon="showConf ? 'mdi-eye-off' : 'mdi-eye'"
              :type="showConf ? 'text' : 'password'"
              v-model="repeat"
              @click:append="showConf = !showConf"
              :rules="[
                required('contrseña', 'Por favor, confirme su nueva contraseña.'),
                passwordMatch(newPassword)
              ]"
            />
          </v-form>
        </v-container>
      </v-card-text>
      <v-card-actions>
        <nuxt-link class="ml-6" to="/login">
          Regresar
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
          Someter
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
      username: "",
      password: "",
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