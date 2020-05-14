<template>
  <v-row
      class="text-center loadingScreen"
      align="center"
      justify="center"
    >
      <v-col>
        <v-row>
          <v-col>
            <h2 class="font-weight-light">Cargando {{nameOfData}}...</h2>
          </v-col>
        </v-row>
        <v-row>
          <v-col>
            <v-progress-circular
              indeterminate
              color="primary"
            ></v-progress-circular>
          </v-col>
        </v-row>
      </v-col>
    </v-row>
</template>

<script>
export default {
  name: 'LoadingScreen',
  props:{
    nameOfData:  String
  }
}
</script>

<style lang="scss" scoped>
.loadingScreen{
  height: 50vh;
}
</style>