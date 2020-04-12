<template>
  <v-row justify="center">
    <v-dialog v-model="dialog" persistent max-width="600px">
      <v-card>
        <v-toolbar flat color="primary_dark">
          <v-toolbar-title class="headline white--text">
            User Permissions
          </v-toolbar-title>
        </v-toolbar>
        <v-card-text>
          <v-container v-if="isLoading">
            <p>{{ permissions }}</p>
            <v-row align="center">
              <v-col cols="3">
                <v-subheader v-text="'Events'"></v-subheader>
              </v-col>
              <v-checkbox
                label="Write"
                v-model="permissions[0].is_invalid"
              ></v-checkbox>
              <v-checkbox
                label="Delete"
                v-model="permissions[1].is_invalid"
              ></v-checkbox>
              <v-checkbox
                label="Modify"
                v-model="permissions[2].is_invalid"
              ></v-checkbox>
            </v-row>
            <v-row align="center">
              <v-col cols="3">
                <v-subheader v-text="'PBP'"></v-subheader>
              </v-col>
              <v-checkbox
                label="Write"
                v-model="permissions[3].is_invalid"
              ></v-checkbox>
              <v-checkbox
                label="Delete"
                v-model="permissions[4].is_invalid"
              ></v-checkbox>
              <v-checkbox
                label="Modify"
                v-model="permissions[5].is_invalid"
              ></v-checkbox>
            </v-row>
            <v-row align="center">
              <v-col cols="3">
                <v-subheader v-text="'Statistics'"></v-subheader>
              </v-col>
              <v-checkbox
                label="Write"
                v-model="permissions[6].is_invalid"
              ></v-checkbox>
              <v-checkbox
                label="Delete"
                v-model="permissions[7].is_invalid"
              ></v-checkbox>
              <v-checkbox
                label="Modify"
                v-model="permissions[8].is_invalid"
              ></v-checkbox>
            </v-row>
            <v-row align="center">
              <v-col cols="3">
                <v-subheader v-text="'Users'"></v-subheader>
              </v-col>
              <v-checkbox
                label="Write"
                v-model="permissions[9].is_invalid"
              ></v-checkbox>
              <v-checkbox
                label="Delete"
                v-model="permissions[10].is_invalid"
              ></v-checkbox>
              <v-checkbox
                label="Modify"
                v-model="permissions[11].is_invalid"
              ></v-checkbox>
            </v-row>
            <v-row align="center">
              <v-col cols="3">
                <v-subheader v-text="'Profiles'"></v-subheader>
              </v-col>
              <v-checkbox
                label="Write"
                v-model="permissions[12].is_invalid"
              ></v-checkbox>
              <v-checkbox
                label="Delete"
                v-model="permissions[13].is_invalid"
              ></v-checkbox>
              <v-checkbox
                label="Modify"
                v-model="permissions[14].is_invalid"
              ></v-checkbox>
            </v-row>
          </v-container>
          <v-container v-else>
            <v-progress-circular
              indeterminate
              color="primary"
            ></v-progress-circular>
          </v-container>
          <small>*indicates required field</small>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="blue darken-1" text @click="close()">Close</v-btn>
          <v-btn color="blue darken-1" text @click="close()">Save</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-row>
</template>

<script>
export default {
  name: "UpdatePermissionsModal",
  props: {
    dialog: Boolean,
    username: String,
    fullName: String,
    email: String,
    isActive: Boolean
  },
  data() {
    return {
      isLoading: true,
      permissions: [
        {
          permission_id: 13,
          is_invalid: false
        },
        {
          permission_id: 14,
          is_invalid: false
        },
        {
          permission_id: 15,
          is_invalid: false
        },
        {
          permission_id: 16,
          is_invalid: false
        },
        {
          permission_id: 17,
          is_invalid: false
        },
        {
          permission_id: 18,
          is_invalid: false
        },
        {
          permission_id: 19,
          is_invalid: false
        },
        {
          permission_id: 20,
          is_invalid: false
        },
        {
          permission_id: 21,
          is_invalid: false
        },
        {
          permission_id: 22,
          is_invalid: false
        },
        {
          permission_id: 23,
          is_invalid: false
        },
        {
          permission_id: 24,
          is_invalid: false
        },
        {
          permission_id: 25,
          is_invalid: false
        },
        {
          permission_id: 26,
          is_invalid: false
        },
        {
          permission_id: 27,
          is_invalid: false
        }
      ]
    };
  },
  methods: {
    close() {
      this.$emit("update:dialog", false);
    }
  }
};
</script>

<style>
</style>