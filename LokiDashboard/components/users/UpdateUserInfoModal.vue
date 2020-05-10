<template>
  <v-row justify="center">
    <v-dialog v-model="dialog" persistent max-width="600px">
      <v-card>
        <v-toolbar flat color="primary_dark">
          <v-toolbar-title class="headline white--text">
            {{ setFormTitle }}
          </v-toolbar-title>
        </v-toolbar>
        <v-card-text>
          <v-container>
            <v-form v-model="valid">
              <v-row>
                <v-col cols="12">
                  <v-text-field
                    label="Nombre completo*"
                    v-model="fullName_"
                    required
                    :rules="[required('Nombre', 'Por favor, ingrese su nombre completo.')]"
                  />
                </v-col>
                <v-col cols="12">
                  <v-text-field
                    v-model="email_"
                    label="Correo electrónico*"
                    required
                    :rules="[
                      required('email', 'Por favor, ingrese su correo electrónico.'),
                      emailFormat()
                    ]"
                  ></v-text-field>
                </v-col>
                <v-col cols="12">
                  <v-text-field
                    v-model="username_"
                    label="Nombre de usuario*"
                    required
                    :rules="[
                      required('Nombre de usuario', 'Por favor, ingrese su nombre de usuario.'),
                      minLength('El nombre de usuario', 3),
                      maxLength('El nombre de usuario', 20),
                    ]"
                  ></v-text-field>
                </v-col>
                <v-col cols="12">
                  <v-text-field
                    v-model="password_"
                    label="Contraseña*"
                    required
                    :type="showP ? 'text' : 'password'"
                    :append-icon="showP ? 'mdi-eye-off' : 'mdi-eye'"
                    @click:append="showP = !showP"
                    v-if="nameSelector === -1"
                    :rules="[
                      required('contraseña', 'Por favor, ingrese su contraseña.'),
                      minLength('La contraseña', 10),
                      maxLength('La contraseña', 64),
                      passwordFormat()
                    ]"
                  ></v-text-field>
                </v-col>
                <v-col cols="12">
                  <v-text-field
                    v-model="repeat_"
                    label="Confirmar contraseña*"
                    required
                    :type="showC ? 'text' : 'password'"
                    :append-icon="showC ? 'mdi-eye-off' : 'mdi-eye'"
                    @click:append="showC = !showC"
                    v-if="nameSelector === -1"
                    :rules="[
                      required('password', 'Por favor, confirme su nueva contraseña.'),
                      passwordMatch(password_)
                    ]"
                  ></v-text-field>
                </v-col>
                <v-col cols="12" sm="6">
                  <v-switch
                    v-model="isActive_"
                    :label="`Cuenta activa`"
                    v-if="nameSelector !== -1"
                  ></v-switch>
                </v-col>
              </v-row>
            </v-form>
            <v-checkbox v-model="reviewed" label="He revisado mis cambios*." />
          </v-container>
          <small>*indica un campo requerido.</small>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="primary darken-1" text @click="close()">
            Cerrar
          </v-btn>
          <v-btn
            color="primary darken-1"
            text
            @click="save()"
            :disabled="!(valid  && reviewed)"
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
import { mapActions } from "vuex";
import rules from "@/utils/validations";
export default {
  name: "UpdateUserInfoModal",
  props: {
    dialog: Boolean,
    username: String,
    fullName: String,
    email: String,
    isActive: Boolean,
    nameSelector: Number,
    id: Number
  },
  data() {
    return {
      valid: false,
      isLoading: false,
      showP: false,
      showC: false,
      reviewed: false,
      formTitle: "",
      username_: "",
      fullName_: "",
      email_: "",
      password_: "",
      repeat_: "",
      isActive_: ""
    };
  },
  methods: {
    ...mapActions({
      addNewUser: "dashboardUsers/addUser",
      editUser: "dashboardUsers/editUser"
    }),
    close() {
      this.$emit("update:dialog", false); //this is to avoid mutation dialog prop directly when closing dialog.
      // This was to avoid having the user info set when clicking add user, after clicking on edit a user.
      // but it introduced a bug where validation was already showing errors. Fixed it with v-if on modal.
      // This would have also fixed the permissions issue, but loading screen took care of that
      // this.username_ = "";
      // this.fullName_ = "";
      // this.email_ = "";
      // this.password_ = "";
      // this.repeat_ = "";
      // this.isActive_ = "";
    },
    async save() {
      this.isLoading = true;
      if (this.nameSelector === -1) {
        const response = await this.addNewUser({
          email: this.email_,
          full_name: this.fullName_,
          password: this.password_,
          username: this.username_
        });

        if (response !== "error") {
          //so modal does not close when there is an error.
          this.close();
        }
      } else {
        const response = await this.editUser({
          email: this.email_,
          full_name: this.fullName_,
          username: this.username_,
          is_active: this.isActive_,
          id: this.id
        });
        if (response !== "error") {
          //so modal does not close when there is an error.
          this.close();
        }
      }
      this.isLoading = false;
    },
    ...rules
  },
  computed: {
    setFormTitle() {
      if (this.nameSelector === -1) {
        return "New User";
      }
      this.fullName_ = this.fullName;
      this.email_ = this.email;
      this.username_ = this.username;
      this.isActive_ = this.isActive;
      return "Edit User";
    }
  }
};
</script>

<style>
</style>