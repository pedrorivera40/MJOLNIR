<template>
    <v-card class="mx-auto" outlined @click="goToAthlete">								
        <v-container>
            <v-row>
                <v-col>
                    <h2>{{athlete_id}}</h2>
                </v-col>
            </v-row>
            <v-row>
                <v-col>
                    <h2>Estadisticas de Juego:</h2>
                </v-col>
            </v-row>
            <v-row 
            align ="center"
            justify = "center"
            >
                <v-col             
                >
                    <ValidationProvider v-slot="{ errors }" name="Points" rules="numeric">
                        <v-textarea
                            v-model="points"                      
                            :error-messages="errors"
                            label="Puntos"
                            auto-grow
                            rows = "1"
                            outlined
                        ></v-textarea>
                    </ValidationProvider>
                </v-col>
                <v-col             
                >
                    <ValidationProvider v-slot="{ errors }" name="Rebounds" rules="numeric">
                        <v-textarea
                            v-model="rebounds"                      
                            :error-messages="errors"
                            label="Rebotes"
                            auto-grow
                            rows = "1"
                            outlined
                        ></v-textarea>
                    </ValidationProvider>
                </v-col>
                <v-col             
                >
                    <ValidationProvider v-slot="{ errors }" name="Assists" rules="numeric">
                        <v-textarea
                            v-model="assists"                      
                            :error-messages="errors"
                            label="Asistencias"
                            auto-grow
                            rows = "1"
                            outlined
                        ></v-textarea>
                    </ValidationProvider>
                </v-col>
            </v-row>
            <v-row 
            align ="center"
            justify = "center"
            >
                <v-col             
                >
                    <ValidationProvider v-slot="{ errors }" name="Steals" rules="numeric">
                        <v-textarea
                            v-model="steals"                      
                            :error-messages="errors"
                            label="Rebotes"
                            auto-grow
                            rows = "1"
                            outlined
                        ></v-textarea>
                    </ValidationProvider>
                </v-col>
                <v-col             
                >
                    <ValidationProvider v-slot="{ errors }" name="Blocks" rules="numeric">
                        <v-textarea
                            v-model="blocks"                      
                            :error-messages="errors"
                            label="Bloqueos"
                            auto-grow
                            rows = "1"
                            outlined
                        ></v-textarea>
                    </ValidationProvider>
                </v-col>
                <v-col             
                >
                    <ValidationProvider v-slot="{ errors }" name="Turnovers" rules="numeric">
                        <v-textarea
                            v-model="turnovers"                      
                            :error-messages="errors"
                            label="Pérdidas de Balón"
                            auto-grow
                            rows = "1"
                            outlined
                        ></v-textarea>
                    </ValidationProvider>
                </v-col>
            </v-row>
            <v-row >
                <v-col justify = "start">
                    <h3>Intentos de Tiro:</h3>
                </v-col>
            </v-row>
            <v-row 
            align ="center"
            justify = "center"
            >
                <v-col             
                >
                    <ValidationProvider v-slot="{ errors }" name="Field Goal Attempt" rules="numeric">
                        <v-textarea
                            v-model="field_goal_attempt"                      
                            :error-messages="errors"
                            label="Tiro de Campo"
                            auto-grow
                            rows = "1"
                            outlined
                        ></v-textarea>
                    </ValidationProvider>
                </v-col>
                <v-col             
                >
                    <ValidationProvider v-slot="{ errors }" name="Three Point Attempt" rules="numeric">
                        <v-textarea
                            v-model="three_point_attempt"                      
                            :error-messages="errors"
                            label="Tiro de Tres Puntos"
                            auto-grow
                            rows = "1"
                            outlined
                        ></v-textarea>
                    </ValidationProvider>
                </v-col>
                <v-col             
                >
                    <ValidationProvider v-slot="{ errors }" name="Free Throw Attempt" rules="numeric">
                        <v-textarea
                            v-model="free_throw_attempt"                      
                            :error-messages="errors"
                            label="Tiro Libre"
                            auto-grow
                            rows = "1"
                            outlined
                        ></v-textarea>
                    </ValidationProvider>
                </v-col>
            </v-row>
            <v-row >
                <v-col justify = "start">
                    <h3>Tiros Anotados:</h3>
                </v-col>
            </v-row>
            <v-row 
            align ="center"
            justify = "center"
            >
                <v-col             
                >
                    <ValidationProvider v-slot="{ errors }" name="Successful Field Goal" rules="numeric">
                        <v-textarea
                            v-model="successful_field_goal"                      
                            :error-messages="errors"
                            label="Tiro de Campo "
                            auto-grow
                            rows = "1"
                            outlined
                        ></v-textarea>
                    </ValidationProvider>
                </v-col>
                <v-col             
                >
                    <ValidationProvider v-slot="{ errors }" name="Successful Three Point" rules="numeric">
                        <v-textarea
                            v-model="successful_three_point"                      
                            :error-messages="errors"
                            label="Tiro de Tres Puntos"
                            auto-grow
                            rows = "1"
                            outlined
                        ></v-textarea>
                    </ValidationProvider>
                </v-col>
                <v-col             
                >
                    <ValidationProvider v-slot="{ errors }" name="Successful Free Throw" rules="numeric">
                        <v-textarea
                            v-model="successful_free_throw"                      
                            :error-messages="errors"
                            label="Tiro Libre"
                            auto-grow
                            rows = "1"
                            outlined
                        ></v-textarea>
                    </ValidationProvider>
                </v-col>
            </v-row>
            <v-row>
                <v-col>
                    <v-btn class="mr-4" @click="close">Confirmar</v-btn>
                </v-col>
            </v-row>
        </v-container>
    </v-card>
</template>

<script>
export default {
  props: {
    athlete_id: Number,
    // firstName: String,
    // lastNames: String,
    // sportName: String,
    // img: String
  },
  data() {
    return {
    //   valid: false,
    //   isLoading: false,
    //   showP: false,
    //   showC: false,
    //   formTitle: "",
    //   username_: "",
    //   fullName_: "",
    //   email_: "",
    //   password_: "",
    //   repeat_: "",
    //   isActive_: ""
    points: '',
    rebounds: '',
    assists: '',
    steals: '',
    blocks: '',
    turnovers: '',
    field_goal_attempt: '',
    three_point_attempt: '',
    free_throw_attempt: '',
    successful_field_goal: '',
    successful_three_point: '',
    successful_free_throw: '',

    };
  },
  methods: {
      close() {
          
      this.$emit("update:dialog", false); //this is to avoid mutation dialog prop directly when closing dialog.
      // This was to avoid having the user info set when clicking add user, after clicking on edit a user.
      // but it introduced a bug where validation was already showing errors. Fixed it with v-if on modal.
      // This would have also fixed the permissions issue, but loading screen took care of that
      // this.username_ = "";
      // this.fullName_ = "";
      // this.email_ = "";
      // this.password_ = "";
      // this.repeat_ = "";
      // this.isActive_ = "";
    },
  }
};
</script>