<template>
  <div class="wrapper">
    <h1>Usermanagement</h1>
    <div class="content-area pa-4 pt-12">
      <v-card>
        <v-card-title>
          <v-btn color="primary_light" class="white--text">
            <v-icon left>
              mdi-plus
            </v-icon>
            Add New User
          </v-btn>
          <v-spacer />
          <v-text-field
            v-model="search"
            append-icon="mdi-magnify"
            label="Search"
            round
            single-line
            hide-details
          />
        </v-card-title>
        <v-data-table
          :headers="headers"
          :items="users"
          :search="search"
          :loading="isLoading"
        >
          <template v-slot:item.is_active="{ item }">
            {{setStatus(item.is_active)}}
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
        { text: "Iron (%)", value: "iron" }
      ]
    };
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