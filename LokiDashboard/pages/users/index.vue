<template>
  <v-container class="wrapper">
    <h1 class="primary_dark--text pl-3">User Management</h1>
    <div class="content-area pa-4 pt-12">
      <v-card>
        <v-card-title>
          <v-row>
            <v-col>
              <v-btn
                color="primary_light"
                class="white--text"
                @click="editUser(editedItemIndex)"
              >
                <v-icon left>
                  mdi-plus
                </v-icon>
                Add New User
              </v-btn>
              <v-spacer />
            </v-col>
            <v-col cols="4">
              <v-text-field
                v-model="search"
                append-icon="mdi-magnify"
                label="Search"
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
          :search="search"
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
                  Reset
                </v-btn>
              </template>
              <span>Reset User Pasword</span>
            </v-tooltip>
          </template>

          <template v-slot:item.actions="{ item }">
            <v-tooltip bottom>
              <template v-slot:activator="{ on }">
                <v-icon
                  small
                  class="mr-2 table-actions"
                  v-on="on"
                  :disabled="item.username === $store.state.userAuth.user.username"
                  @click.stop="editUser(item)"
                >
                  mdi-pencil
                </v-icon>
              </template>
              <span>Edit User Info</span>
            </v-tooltip>

            <v-tooltip bottom>
              <template v-slot:activator="{ on }">
                <v-icon
                  small
                  class="mr-2 table-actions"
                  v-on="on"
                  :disabled="item.username === $store.state.userAuth.user.username"
                  @click="editPermissions(item)"
                >
                  mdi-shield-lock
                </v-icon>
              </template>
              <span>Edit User Permissions</span>
            </v-tooltip>
            <v-tooltip bottom>
              <template v-slot:activator="{ on }">
                <v-icon
                  small
                  class="mr-2 table-actions"
                  v-on="on"
                  :disabled="item.username === $store.state.userAuth.user.username"
                  @click.stop="deleteUser(item)"
                >
                  mdi-delete
                </v-icon>
              </template>
              <span>Delete User</span>
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
          :dialog.sync="dialogPermissions"
          :id="editedItem.id"
          :username="editedItem.username"
        />
        <PasswordResetModal
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
import DeleteUserModal from "@/components/DeleteUserModal";
import UpdatePermissionsModal from "@/components/UpdatePermissionsModal";
import UpdateUserModal from "@/components/UpdateUserInfoModal";
import PasswordResetModal from "@/components/PasswordResetModal";
export default {
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
        { text: "Full Name", value: "full_name" },
        { text: "Username", value: "username" },
        { text: "Email", value: "email" },
        { text: "Account Status", align: "center", value: "is_active" },
        { text: "Password",  value: "password" },
        { text: "Actions", value: "actions", sortable: false }
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
      getPermissions: "dashboardUsers/getPermissions"
    }),
    setStatus(status) {
      return status ? "Active" : "Inactive";
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