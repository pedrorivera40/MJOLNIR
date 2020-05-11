<template>
  <v-row justify="center">
    <v-dialog v-model="dialog" persistent max-width="480px">
      <v-card class="elevation-12 mx-auto">
        <v-toolbar color="primary" dark flat>
          <v-toolbar-title>Restablecer Contraseña</v-toolbar-title>
          <v-spacer />
        </v-toolbar>
        <v-card-title class="text--secondary">
          Restablecer la contraseña para {{ username }}
        </v-card-title>
        <v-card-text>
          <v-container>
            <v-form v-model="valid">
              <v-text-field
                id="new-password"
                label="Nueva contraseña"
                name="new-password"
                prepend-icon="mdi-lock"
                :append-icon="showNew ? 'mdi-eye' : 'mdi-eye-off'"
                :type="showNew ? 'text' : 'password'"
                v-model="newPassword"
                @click:append="showNew = !showNew"
                :rules="[
                  required(
                    'contraseña',
                    'Por favor, ingrese una nueva contraseña.'
                  ),
                  minLength('La contraseña', 10),
                  maxLength('La contraseña', 64),
                  passwordFormat()
                ]"
              />
              <v-text-field
                id="confirm-password"
                label="Confirmar contraseña"
                name="confirm-password"
                prepend-icon="mdi-lock-check"
                :append-icon="showConf ? 'mdi-eye' : 'mdi-eye-off'"
                :type="showConf ? 'text' : 'password'"
                v-model="repeat"
                @click:append="showConf = !showConf"
                :rules="[
                  required(
                    'contraseña',
                    'Por favor, confirme su nueva contraseña.'
                  ),
                  passwordMatch(newPassword)
                ]"
              />
            </v-form>
            <v-checkbox
              v-model="sure"
            >
              <template v-slot:label>
                <div>
                  Desea actualizar contraseña de <strong>{{username}}</strong> ?
                </div>
              </template>
            </v-checkbox>
          </v-container>
        </v-card-text>
        <v-card-actions>
          <v-spacer />
          <v-btn color="primary darken-1" text @click="close()">
            Cerrar
          </v-btn>
          <v-btn
            color="primary darken-1"
            text
            @click="save()"
            :disabled="!(valid && sure)"
            :loading="isLoading"
          >
            Guardar
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