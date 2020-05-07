<template>
  <v-layout v-if="visible" column class="wrapper">
    <v-flex xs12 sm8 md6>
      <div class="text-center">
        <h1 class="header my-12" dark>
          Welcome to Huella Deportiva Dashboard!
        </h1>
        <logo />
        <h2 class="my-6">Please, proceed to the login page.</h2>
        <v-btn color="primary_dark" dark @click="proceed">
          Continue
        </v-btn>
      </div>
    </v-flex>
  </v-layout>
</template>

<script>
import Logo from "~/components/Logo.vue";

export default {
  auth: false,
  middleware: "guest",
  layout: "guest",
  components: {
    Logo
  },
  data() {
    return {
      visible: true,
    };
  },
  methods: {
    proceed() {
      this.visible = false
      return this.$router.push("/login");
    }
  }
};
</script>

<style lang="scss" scoped>
.wrapper {
  background: linear-gradient(
    -45deg,
    rgb(55, 141, 62),
    rgb(72, 165, 72),
    rgb(55, 141, 66),
    rgb(5, 36, 4)
  );
  background-size: 400% 400%;
  color: whitesmoke;
  -webkit-animation: Gradient 35s ease infinite;
  -moz-animation: Gradient 35s ease infinite;
  animation: Gradient 35s ease infinite;
  height: 100vh;
  position: absolute;
  top: 0;
  left: 0;
  color: gree;
  width: 100vw;
  .header {
    font-size: 3rem;
  }
}
@keyframes Gradient {
  0% {
    background-position: 0% 50%;
  }
  25% {
    background-position: 50% 50%;
  }
  50% {
    background-position: 100% 50%;
  }
  75% {
    background-position: 50% 50%;
  }
  100% {
    background-position: 0% 50%;
  }
}
</style>