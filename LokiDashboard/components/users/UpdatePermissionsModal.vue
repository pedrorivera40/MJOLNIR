<template>
  <v-row justify="center">
    <v-dialog v-model="dialog" persistent max-width="600px">
      <v-card>
        <v-toolbar flat color="primary_dark">
          <v-toolbar-title class="headline white--text">
            Permisos de Usuario
          </v-toolbar-title>
        </v-toolbar>
        <v-card-title class="headline text--secondary">
          Permisos de {{ username }} en el sistema.
        </v-card-title>
        <v-card-text>
          <v-container
            class="pl-12"
            v-if="!isLoadingP && permissions.length > 0"
          >
            <v-row align="center">
              <v-col cols="12" sm="4">
                <h2 class="font-weight-medium" v-text="'Eventos:'"></h2>
              </v-col>
              <v-checkbox
                class="mx-3"
                label="Añadir"
                v-model="permissions[0]['13']"
              ></v-checkbox>
              <v-checkbox
                class="mx-3"
                label="Borrar"
                v-model="permissions[1]['14']"
              ></v-checkbox>
              <v-checkbox
                class="mx-3"
                label="Modificar"
                v-model="permissions[2]['15']"
              ></v-checkbox>
            </v-row>
            <v-row align="center">
              <v-col cols="12" sm="4">
                <h2 class="font-weight-medium" v-text="'Play-By-Play:'"></h2>
              </v-col>
              <v-checkbox
                class="mx-3"
                label="Añadir"
                v-model="permissions[3]['16']"
              ></v-checkbox>
              <v-checkbox
                class="mx-3"
                label="Borrar"
                v-model="permissions[4]['17']"
              ></v-checkbox>
              <v-checkbox
                class="mx-3"
                label="Modificar"
                v-model="permissions[5]['18']"
              ></v-checkbox>
            </v-row>
            <v-row align="center">
              <v-col cols="12" sm="4">
                <h2 class="font-weight-medium" v-text="'Estadísticas:'"></h2>
              </v-col>
              <v-checkbox
                class="mx-3"
                label="Añadir"
                v-model="permissions[6]['19']"
              ></v-checkbox>
              <v-checkbox
                class="mx-3"
                label="Borrar"
                v-model="permissions[7]['20']"
              ></v-checkbox>
              <v-checkbox
                class="mx-3"
                label="Modificar"
                v-model="permissions[8]['21']"
              ></v-checkbox>
            </v-row>
            <v-row align="center">
              <v-col cols="12" sm="4">
                <h2 class="font-weight-medium" v-text="'Usuarios:'"></h2>
              </v-col>
              <v-checkbox
                class="mx-3"
                label="Añadir"
                v-model="permissions[9]['22']"
              ></v-checkbox>
              <v-checkbox
                class="mx-3"
                label="Borrar"
                v-model="permissions[10]['23']"
              ></v-checkbox>
              <v-checkbox
                class="mx-3"
                label="Modificar"
                v-model="permissions[11]['24']"
              ></v-checkbox>
            </v-row>
            <v-row align="center">
              <v-col cols="12" sm="4">
                <h2 class="font-weight-medium" v-text="'Perfiles:'"></h2>
              </v-col>
              <v-checkbox
                class="mx-3"
                label="Añadir"
                v-model="permissions[12]['25']"
              ></v-checkbox>
              <v-checkbox
                class="mx-3"
                label="Borrar"
                v-model="permissions[13]['26']"
              ></v-checkbox>
              <v-checkbox
                class="mx-3"
                label="Modificar"
                v-model="permissions[14]['27']"
              ></v-checkbox>
            </v-row>
            <v-checkbox v-model="reviewed" label="He revisado mis cambios.">

            </v-checkbox>
          </v-container>
          <v-container class="text-center" v-else>
            <v-row align="center">
              <v-col justify="center">
                <h3 class="font-weight-light">Cargando Permisos...</h3>
              </v-col>
            </v-row>
            <v-progress-circular
              indeterminate
              color="primary"
            ></v-progress-circular>
          </v-container>
        </v-card-text>
        <v-card-actions >
          <v-spacer></v-spacer>
          <v-btn color="primary ligthen-1" text @click="close()">
            Cerrar
          </v-btn>
          <v-btn
            color="primary ligthen-1"
            text
            @click="save()"
            :loading="isLoading"
            :disabled="!reviewed"
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
export default {
  name: "UpdatePermissionsModal",
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
      isLoading: false,
      loadingPermissions: true,
      reviewed: false
    };
  },
  methods: {
    ...mapActions({
      setPermissions: "dashboardUsers/setPermissions"
    }),
    close() {
      this.$emit("update:dialog", false);
    },
    async save() {
      this.isLoading = true;
      const permissions = this.permissions;
      await this.setPermissions({ id: this.id, permissions: permissions });
      this.isLoading = false;
      this.close()
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