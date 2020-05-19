<template>
  <v-container>
    <h1 class="primary_dark--text pl-3">Dashboard</h1>
    <v-row>
      <v-col cols="12" md="4">
        <v-card >
          <v-card-text>
            <div class="welcome">¡Bienvenidos!</div>
            <p class="display-1 text--primary">
              Plataforma de Administración para Huella Deportiva Web
            </p>
            <p>Version 1.0</p>
            <div class="text--primary">
              Maneja usuarios, equipos, plantillas, estadistícas, eventos y el jugada a jugada de cada partido de Volleyball. ¡Todo desde un solo lugar!
            </div>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import { mapActions } from "vuex";
export default {
  methods: {}
};
</script>

<style lang="scss" scoped>
  .welcome{
    font-size: 1.2rem;
    margin-bottom: .5rem;
  }
</style>