<template>
  <v-row justify="center">
    <v-dialog v-model="dialog" persistent max-width="350">
      <v-card>
        <v-toolbar flat color="primary_dark">
          <v-toolbar-title class="headline white--text">
            Borrar Usuario
          </v-toolbar-title>
        </v-toolbar>
        <v-card-title>
          <p style="word-break: normal;">
            ¿Seguro que quieres borrar la cuenta de {{ username }}?
          </p>
        </v-card-title>
        <v-card-text>
          <div class="body">Esta acción es <strong>irreversible</strong>.</div>
          <v-checkbox v-model="terms">
            <template v-slot:label>
              <div>
                Aun así desea borrar la cuenta de <strong>{{ username }}</strong> ?
              </div>
            </template>
          </v-checkbox>
        </v-card-text>

        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="grey darken-3" text @click="close()"> Cancelar </v-btn>
          <v-btn
            color="green darken-1"
            :disabled="!terms"
            :loading="isLoading"
            text
            @click="delete_User()"
          >
            Borrar
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-row>
</template>

<script>
import { mapActions } from "vuex";
export default {
  name: "DeleteUserModal",
  props: {
    dialog: Boolean,
    username: String,
    id: Number
  },
  data() {
    return {
      terms: false,
      isLoading: false
    };
  },
  methods: {
    ...mapActions({
      deleteUser: "dashboardUsers/deleteUser"
    }),

    close() {
      this.terms = false;
      this.$emit("update:dialog", false);
    },
    async delete_User() {
      this.isLoading = true;
      const payload = {
        id: this.id,
        username: this.username
      };
      await this.deleteUser(payload);
      this.terms = false;
      this.$emit("update:dialog", false);
      this.isLoading = false;
    }
  }
};
</script>

<style lang="scss" scoped>
p {
  hyphens: auto;
}

.body {
  font-size: 1.1rem;
}
</style>