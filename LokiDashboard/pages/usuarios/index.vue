<template>
  <v-container class="wrapper">
    <h1 class="primary_dark--text pl-3">Manejo de Usuarios</h1>
    <div class="content-area pa-4 pt-12">
      <v-card>
        <v-card-title>
          <v-row>
            <v-col>
              <v-btn
                color="primary_light"
                class="white--text"
                @click="editUser(editedItemIndex)"
                :disabled="!$store.state.userAuth.userPermissions[9]['22']"
              >
                <v-icon left>
                  mdi-plus
                </v-icon>
                Añadir Usuario
              </v-btn>
              <v-spacer />
            </v-col>
            <v-col cols="4">
              <v-text-field
                v-model="search"
                append-icon="mdi-magnify"
                label="Buscar"
                rounded
                dense
                outlined
                single-line
                hide-details
              />
            </v-col>
          </v-row>
        </v-card-title>
        <v-data-table
          :headers="headers"
          :items="users"
          no-data-text="No hay usuarios en este momento."
          loading-text="Cargando usuarios."
          :loading="isLoadingU"
        >
          <template v-slot:item.is_active="{ item }">
            <v-chip class="ma-2" small  :color="item.is_active ? 'primary lighten-2': ''">
              {{ setStatus(item.is_active) }}
            </v-chip>
          </template>

          <template v-slot:item.password="{ item }">
            <v-tooltip bottom>
              <template v-slot:activator="{ on }">
                <v-btn
                  color="primary"
                  outlined
                  small
                  v-on="on"
                  @click="resetPassword(item)"
                >
                  Restablecer
                </v-btn>
              </template>
              <span>Restablecer contraseña</span>
            </v-tooltip>
          </template>

          <template v-slot:item.actions="{ item }">
            <v-tooltip bottom>
              <template v-slot:activator="{ on }">
                <v-icon
                  small
                  class="mr-2 table-actions"
                  v-on="on"
                  :disabled="item.username === $store.state.userAuth.user.username || !$store.state.userAuth.userPermissions[11]['24']"
                  @click.stop="editUser(item)"
                >
                  mdi-pencil
                </v-icon>
              </template>
              <span>Editar información</span>
            </v-tooltip>

            <v-tooltip bottom>
              <template v-slot:activator="{ on }">
                <v-icon
                  small
                  class="mr-2 table-actions"
                  v-on="on"
                  :disabled="item.username === $store.state.userAuth.user.username || !$store.state.userAuth.userPermissions[11]['24']"
                  @click="editPermissions(item)"
                >
                  mdi-shield-lock
                </v-icon>
              </template>
              <span>Edit Permisos</span>
            </v-tooltip>
            <v-tooltip bottom>
              <template v-slot:activator="{ on }">
                <v-icon
                  small
                  class="mr-2 table-actions"
                  v-on="on"
                  :disabled="item.username === $store.state.userAuth.user.username || !$store.state.userAuth.userPermissions[10]['23'] "
                  @click.stop="deleteUser(item)"
                >
                  mdi-delete
                </v-icon>
              </template>
              <span>Borrar usuario</span>
            </v-tooltip>
          </template>
        </v-data-table>
        <DeleteUserModal
          :dialog.sync="dialogDelete"
          :id="editedItem.id"
          :username="editedItem.username"
          v-on:update:dialog="dialogDelete = $event"
        />
        <UpdateUserModal
          v-if="dialogEdit"
          :nameSelector="editedItemIndex"
          :dialog.sync="dialogEdit"
          :username="editedItem.username"
          :fullName="editedItem.full_name"
          :email="editedItem.email"
          :isActive="editedItem.is_active"
          :id="editedItem.id"
        />
        <UpdatePermissionsModal
          v-if="dialogPermissions"
          :dialog.sync="dialogPermissions"
          :id="editedItem.id"
          :username="editedItem.username"
        />
        <PasswordResetModal
          v-if="dialogPassword"
          :dialog.sync="dialogPassword"
          :id="editedItem.id"
          :username="editedItem.username"
        />
      </v-card>
    </div>
  </v-container>
</template>

<script>
import { mapActions, mapGetters } from "vuex";
import DeleteUserModal from "@/components/users/DeleteUserModal";
import UpdatePermissionsModal from "@/components/users/UpdatePermissionsModal";
import UpdateUserModal from "@/components/users/UpdateUserInfoModal";
import PasswordResetModal from "@/components/users/PasswordResetModal";
export default {
  middleware: 'admin',
  data() {
    return {
      search: "",
      dialogEdit: false,
      dialogDelete: false,
      dialogPermissions: false,
      dialogPassword: false,
      headers: [
        {
          text: "ID",
          align: "start",
          value: "id"
        },
        { text: "Nombre Completo", value: "full_name" },
        { text: "Nombre de Usuario", value: "username" },
        { text: "Correo Electrónico", value: "email" },
        { text: "Estatus de Cuenta", align: "center", value: "is_active" },
        { text: "Contraseña",  value: "password" },
        { text: "Acciones", value: "actions", sortable: false }
      ],
      editedItemIndex: -1,
      editedItem: {
        full_name: "",
        username: "",
        email: "",
        is_active: "",
        id: 0
      },
      defaultItem: {
        full_name: "",
        username: "",
        email: "",
        is_active: "",
        id: 0
      }
    };
  },
  head() {
    return {
      title: "User Management",
      meta: [
        {
          hid: "description",
          name: "description",
          content: "Manage system users"
        }
      ]
    };
  },
  components: {
    DeleteUserModal,
    UpdatePermissionsModal,
    UpdateUserModal,
    PasswordResetModal
  },
  methods: {
    ...mapActions({
      getUsers: "dashboardUsers/getUsers",
      getPermissions: "dashboardUsers/getPermissions",
      setUser: "userAuth/setUser"
    }),
    setStatus(status) {
      return status ? "Activa" : "Inactiva";
    },
    deleteUser(user) {
      this.editedItem = Object.assign({}, user); //This hsit is to not mess with vuex state
      this.dialogDelete = true;
    },
    editUser(user) {
      this.editedItemIndex = this.users.indexOf(user);
      this.editedItem = Object.assign({}, user); //This hsit is to not mess with vuex state
      this.dialogEdit = true;
    },
    editPermissions(user) {
      this.editedItem = Object.assign({}, user); //This hsit is to not mess with vuex state
      this.dialogPermissions = true;
      this.getPermissions(user.id);
    },
    resetPassword(user) {
      this.editedItem = Object.assign({}, user); //This hsit is to not mess with vuex state
      this.dialogPassword = true;
    }
  },
  computed: {
    ...mapGetters({
      users: "dashboardUsers/users",
      isLoadingU: "dashboardUsers/isLoadingU"
    })
  },
  mounted() {
    this.getUsers();
    this.setUser();
  }
};
</script>

<style lang="scss" scoped>
@import "@/assets/variables.scss";
.wrapper {
  height: 100%;

  .content-area {
    height: 100%;
    width: 100%;

    .table-actions {
      &:hover {
        color: $primary-color;
      }
    }
  }
}
</style>