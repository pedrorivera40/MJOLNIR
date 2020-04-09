<template>
  <v-hover v-slot:default="{ hover }" open-delay="25">
    <v-card class="mx-auto" max-width="400" :elevation="hover ? 16 : 2">
      <v-img class="white--text align-end" height="300px" :src="img">
        <v-card-title class="sport-span" hover="true">{{sport_name}}</v-card-title>
      </v-img>
    </v-card>
  </v-hover>
</template>

<script>
export default {
  props: {
    sport_name: String,
    img: String
  }
};
</script>

<style>
.sport-span {
  background-color: rgb(67, 160, 71);
  color: white;
  font-weight: bold;
  margin-right: 0;
}
</style>