<template>
  <h1 @click="click"> Dashboard </h1>
</template>

<script>
import { mapActions } from "vuex";
export default {
  methods:{
    click(){
      this.$store.dispatch('notifications/setSnackbar',{text:'hello im am writing a ', color: 'error'})
      console.log(this.$store.state.snackbars)
    }
  }
}
</script>

<style>

</style>