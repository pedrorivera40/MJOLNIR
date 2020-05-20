
<template>
  <v-hover v-slot:default="{ hover }" open-delay="25">
    <v-card class="ma-auto" width="400" :elevation="hover ? 16 : 2">
      <v-row>
        <v-col cols="12">
          <v-row>
            <v-avatar size="200" class="mx-auto" justify="center">
              <img :src="img" alt="Developer" height="200px" />
            </v-avatar>
          </v-row>
        </v-col>
      </v-row>
      <v-row>
        <v-col cols="12">
          <v-card-title style="word-break: normal;">{{name}}</v-card-title>
        </v-col>
      </v-row>
      <v-row>
        <v-card-text class="text--primary mx-4" style="word-break: normal;">
          <div>{{bio}}</div>
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
    bio: String
  }
};
</script>

<style>
</style>