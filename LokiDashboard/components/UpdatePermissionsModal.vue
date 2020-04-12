<template>
  <v-row justify="center">
    <v-dialog v-model="dialog" persistent max-width="600px">
      <v-card>
        <v-toolbar flat color="primary_dark">
          <v-toolbar-title class="headline white--text">
            User Permissions
          </v-toolbar-title>
        </v-toolbar>
        <v-card-title class="display-1 text--secondary">
          {{username}}'s System Permissions
        </v-card-title>
        <v-card-text >
          <!-- TODO change is loadingf to !isloading -->
          <v-container class="pl-12" v-if="isLoading && permissions.length > 0">
            <v-row align="center">
              <v-col cols="12" sm="3">
                <h2 class="font-weight-regular" v-text="'Events:'"></h2>
              </v-col>
              <v-checkbox
                class="mx-3"
                label="Write"
                v-model="permissions[0].is_invalid"
              ></v-checkbox>
              <v-checkbox
                class="mx-3"
                label="Delete"
                v-model="permissions[1].is_invalid"
              ></v-checkbox>
              <v-checkbox
                class="mx-3"
                label="Modify"
                v-model="permissions[2].is_invalid"
              ></v-checkbox>
            </v-row>
            <v-row align="center">
              <v-col cols="12" sm="3">
                <h2 class="font-weight-regular" v-text="'PBP:'"></h2>
              </v-col>
              <v-checkbox
                class="mx-3"
                label="Write"
                v-model="permissions[3].is_invalid"
              ></v-checkbox>
              <v-checkbox
                class="mx-3"
                label="Delete"
                v-model="permissions[4].is_invalid"
              ></v-checkbox>
              <v-checkbox
                class="mx-3"
                label="Modify"
                v-model="permissions[5].is_invalid"
              ></v-checkbox>
            </v-row>
            <v-row align="center">
              <v-col cols="12" sm="3">
                <h2 class="font-weight-regular" v-text="'Statistics:'"></h2>
              </v-col>
              <v-checkbox
                class="mx-3"
                label="Write"
                v-model="permissions[6].is_invalid"
              ></v-checkbox>
              <v-checkbox
                class="mx-3"
                label="Delete"
                v-model="permissions[7].is_invalid"
              ></v-checkbox>
              <v-checkbox
                class="mx-3"
                label="Modify"
                v-model="permissions[8].is_invalid"
              ></v-checkbox>
            </v-row>
            <v-row align="center">
              <v-col cols="12" sm="3">
                <h2 class="font-weight-regular" v-text="'Users:'"></h2>
              </v-col>
              <v-checkbox
                class="mx-3"
                label="Write"
                v-model="permissions[9].is_invalid"
              ></v-checkbox>
              <v-checkbox
                class="mx-3"
                label="Delete"
                v-model="permissions[10].is_invalid"
              ></v-checkbox>
              <v-checkbox
                class="mx-3"
                label="Modify"
                v-model="permissions[11].is_invalid"
              ></v-checkbox>
            </v-row>
            <v-row align="center">
              <v-col cols="12" sm="3">
                <h2 class="font-weight-regular" v-text="'Profiles:'"></h2>
              </v-col>
              <v-checkbox
                class="mx-3"
                label="Write"
                v-model="permissions[12].is_invalid"
              ></v-checkbox>
              <v-checkbox
                class="mx-3"
                label="Delete"
                v-model="permissions[13].is_invalid"
              ></v-checkbox>
              <v-checkbox
                class="mx-3"
                label="Modify"
                v-model="permissions[14].is_invalid"
              ></v-checkbox>
            </v-row>
          </v-container>
          <v-container class="text-center" v-else>
            <v-row align="center">
              <v-col justify="center">
                <h3 class="font-weight-light">Loading Permissions...</h3>
              </v-col>
            </v-row>
            <v-progress-circular
              indeterminate
              color="primary"
            ></v-progress-circular>
          </v-container>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="primary ligthen-1" text @click="close()">Close</v-btn>
          <v-btn color="primary ligthen-1" text @click="close()">Save</v-btn>
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
    id: Number,
  },
  data() {
    return {
      isLoading: true,
    };
  },
  methods: {
    close() {
      this.$emit('update:dialog', false);
    },
  },
  computed: {
    ...mapGetters({
      permissions: 'dashboardUsers/permissions',
    })
  },
};
</script>

<style>
</style>