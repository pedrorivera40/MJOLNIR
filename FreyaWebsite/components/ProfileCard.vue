
<template>
  <v-hover v-slot:default="{ hover }" open-delay="25">
    <v-card class="ma-auto" width="400" height="450" :elevation="hover ? 16 : 2">
      <v-row>
        <v-col cols="12">
          <v-row>
            <v-avatar size="200" class="mx-auto my-4" justify="center">
              <img :src="img" alt="Developer" height="200px" />
            </v-avatar>
          </v-row>
        </v-col>
      </v-row>
      <v-row>
        <v-card-text>
          <h1 class="text-center ma-8" style="word-break: normal;">{{name}}</h1>
          <div class="ma-4" style="word-break: normal;">Cargo: {{ position }}</div>
          <div class="ma-4" style="word-break: normal;">Programa de Estudio: {{ major }}</div>
        </v-card-text>
      </v-row>
    </v-card>
  </v-hover>
</template>

<script>
export default {
  props: {
    name: String,
    img: String,
    position: String,
    major: String
  }
};
</script>

<style>
</style>