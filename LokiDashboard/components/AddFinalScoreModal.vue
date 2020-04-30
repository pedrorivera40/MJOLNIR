<template>
    <v-row justify="center">
        <v-dialog v-model="dialog" persistent max-width="600px">
            <v-card width="800" class="elevation-12 mx-auto">

                <h1>AMAZING MODAL</h1>
                <v-row>
                    <v-spacer/>
                    <v-spacer/>
                    <v-col>
                        <v-btn color="primary ligthen-1" text @click="close()">close</v-btn>
                    </v-col>
                    <!-- <v-col>
                        <v-btn color="primary ligthen-1" text @click="submit" :loading="loadingQuery">submit</v-btn>
                    </v-col>
                    <v-col>
                        <v-btn color="primary ligthen-1" text @click="clear">clear</v-btn>
                    </v-col> -->
                </v-row> 
            </v-card>
        </v-dialog>
    </v-row>
</template>

<script>
    import rules from "@/utils/validations"  
    import {mapActions,mapGetters} from "vuex"
  export default {
      name:"AddTeamModal",
      props:{
        dialog: Boolean
      },
    data: () => ({
        //For Validation
        valid:false,

        
        
    }),
           
      
      
    created(){
       
    }, 

    methods: {
        ...rules,

        ...mapActions({
           
        }),

        close() {
            this.$emit("update:dialog", false);
        },
        async submit () {
            
        },
        
        clear () {
           
        },
        
    },
    computed: {
	    ...mapGetters({
        })
    }
  }
</script>