<template>
  <v-container>
    <v-layout column>
      <v-flex xs12 sm8 md6>
        <div class="text-center">
          <v-row>
            <v-col>
              <h1 v-if="$vuetify.breakpoint.smAndDown" class="header display-2 my-12">
                ¡Bienvenida a Huella Deportiva
                <span class="highlight">Web</span>!
              </h1>
              <h1 v-else class="header display-3 my-12">
                ¡Bienvenida a Huella Deportiva
                <span class="highlight">Web</span>!
              </h1>
              <Logo
                :width="$vuetify.breakpoint.smAndDown ? '350px' : ''"
              />
              <h2 class="my-6 headline">¡Orgullo Colegial!</h2>
            </v-col>
          </v-row>
        </div>
      </v-flex>
    </v-layout>
  </v-container>
</template>

<script>
import Logo from "~/components/Logo.vue";
export default {
  components: {
    Logo
  }
};
</script>

<style lang="scss" scoped>
.header {
  margin-top: 6rem;
  font-size: 3rem;
  .highlight {
    color: #168f09;
  }
}
</style>