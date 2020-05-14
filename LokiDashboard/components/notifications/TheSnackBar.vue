<template>
  <div>
    <v-snackbar
      v-for="(snackbar, index) in snackbars.filter(s => s.showing)"
      :key="snackbar.text + Math.random()"
      v-model="snackbar.showing"
      :timeout="snackbar.timeout"
      :color="snackbar.color"
      :multiLine="snackbar.multiline"
      :style="`bottom: ${(index * 60) + 100}px`"
    >
      {{snackbar.text}}
      <v-btn text @click="snackbar.showing = false">Cerrar</v-btn>
    </v-snackbar>
  </div>
</template>

<script>
  import { mapState, mapActions } from 'vuex';
  export default {
    name: 'TheSnackBar',
    computed: {
      ...mapState({
        snackbars: state => state.notifications.snackbars
      })
    },
  }
</script>
