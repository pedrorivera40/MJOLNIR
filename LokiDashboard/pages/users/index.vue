<template>
  <div class="wrapper">
    <h1>Usermanagement</h1>
    <div class="content-area pa-4 pt-12">
      <v-card>
        <v-card-title>
          <v-row>
            <v-col>
              <v-btn color="primary_light" class="white--text">
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
          :loading="isLoading"
        >
          
          <template v-slot:item.is_active="{ item }">
            {{ setStatus(item.is_active) }}
          </template>

          <template v-slot:item.password>
            <v-btn color="primary" outlined small>
              Reset
            </v-btn>
          </template>

          <template v-slot:item.actions>
            <v-tooltip bottom>
              <template v-slot:activator="{ on }">
                <v-icon small class="mr-2" v-on="on" @click="dialogEdit = !dialogEdit">
                  mdi-pencil
                </v-icon>
              </template>
              <span>Edit User Info</span>
            </v-tooltip>
            <v-tooltip bottom>
              <template v-slot:activator="{ on }">
                <v-icon small class="mr-2" v-on="on" @click="dialogPermissions = !dialogPermissions">
                  mdi-shield-lock
                </v-icon>
              </template>
              <span>Edit User Permissions</span>
            </v-tooltip>
            <v-tooltip bottom>
              <template v-slot:activator="{ on }">
                <v-icon small class="mr-2" v-on="on" @click="dialogDelete = !dialogDelete">
                  mdi-delete
                </v-icon>
              </template>
              <span>Delete User</span>
            </v-tooltip>
          </template>
          
        </v-data-table>
      </v-card>
    </div>
  </div>
</template>

<script>
import { mapActions, mapGetters } from "vuex";
export default {
  data() {
    return {
      search: "",
      dialogEdit: false,
      dialogDelete: false,
      dialogPermissions: false,
      headers: [
        {
          text: "ID",
          align: "start",
          sortable: false,
          value: "id"
        },
        { text: "Full Name", value: "full_name" },
        { text: "Username", value: "username" },
        { text: "Email", value: "email" },
        { text: "Account Status", value: "is_active" },
        { text: "Password", value: "password" },
        { text: "Actions", value: "actions", sortable: false }
      ]
    };
  },
  components: {
  },
  methods: {
    ...mapActions({
      getUsers: "dashboardUsers/getUsers"
    }),
    setStatus(status) {
      return status ? "Active" : "Inactive";
    }
  },
  computed: {
    ...mapGetters({
      users: "dashboardUsers/users",
      isLoading: "dashboardUsers/isLoading"
    })
  },
  mounted() {
    this.getUsers();
  }
};
</script>

<style lang="scss" scoped>
.wrapper {
  height: 100%;

  .content-area {
    background-color: red;
    height: 100%;
    width: 100%;
  }
}
</style>