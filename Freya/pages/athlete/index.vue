<template>
  <v-card width="800" class="elevation-12 mx-auto">
    <v-toolbar color="green darken-1" dark flat>
      <v-toolbar-title>Atleta</v-toolbar-title>
      <v-spacer />
    </v-toolbar>
    <v-card-text>            
      <ValidationObserver ref="observer" v-slot="{ validate, reset }">
        <form>
          <v-container>
            <v-row>
              <v-col
                cols="12"
                md="4"
              >
                <ValidationProvider v-slot="{ errors }" name="Nombre" rules="required|alpha|max:20">
                  <v-text-field
                    v-model="first_name"          
                    :error-messages="errors"
                    :counter="20"
                    label="Nombre"
                    required
                  ></v-text-field>
                </ValidationProvider>
              </v-col>

              <v-col
                cols="12"
                md="4"
              >
                <ValidationProvider v-slot="{ errors }" name="Segundo Nombre" rules="alpha">
                  <v-text-field
                    v-model="middle_name"
                    :error-messages="errors"
                    :counter="20"
                    label="Segundo Nombre"
                    required
                  ></v-text-field>
                </ValidationProvider>
              </v-col>

              <v-col
                cols="12"
                md="4"
              >
                <ValidationProvider v-slot="{ errors }" name="Apellidos" rules="required|alpha_spaces|alpha_dash">
                  <v-text-field
                    v-model="last_names"
                    :counter="40"
                    :error-messages="errors"
                    label="Apellidos"
                    required
                  ></v-text-field>
                </ValidationProvider> 
              </v-col>
              <v-spacer />
            </v-row>
            
            <ValidationProvider v-slot="{ errors }" name="Biografia" rules="max:1000">
                <v-textarea
                  v-model="short_bio"                      
                  :counter="1000"
                  :error-messages="errors"
                  label="Biografia"
                  auto-grow
                  rows = "3"
                  outlined
                ></v-textarea>
            </ValidationProvider>

            <v-row>
              <v-col
                cols="1"
                md="2"
              >
              <span>Estatura: </span>
               
              </v-col>

              <v-col
                cols="12"
                md="4"
              >
                <v-select
                  v-model="height_feet"
                  :items="feet"
                  label ="Pies"
                  prepend-icon="mdi-human-male-height"
                ></v-select>
              </v-col>

              <v-col
                cols="12"
                md="4"
              >
                <v-select
                  v-model="height_inches"
                  :items="inches"
                  label ="Pulgadas"
                ></v-select>
              </v-col>
            </v-row>

            <v-row>

              <v-col
              cols="12"
              md="4"
              >
                <ValidationProvider v-slot="{ errors }" name="Programa de Estudio" rules="alpha_spaces">
                  <v-text-field
                    v-model="study_program"
                    :error-messages="errors"                    
                    label="Programa de Estudio"
                    prepend-icon="mdi-school"
                    required
                  ></v-text-field>
                </ValidationProvider>
              </v-col>
              
              

              <v-col
              cols="12"
              md="4"
              >
                <ValidationProvider v-slot="{ errors }" name="Escuela de Precedencia" rules="alpha">
                  <v-text-field
                    v-model="school_of_precedence"
                    :error-messages="errors"                    
                    label="Escuela de Precedencia"
                    prepend-icon="mdi-school-outline"
                    required
                  ></v-text-field>
                </ValidationProvider>
              </v-col>

              <v-col
              cols="12"
              md="4"
              >
                <ValidationProvider v-slot="{ errors }" name="Enlace de Imagen de Perfil" rules="">
                  <v-text-field
                    v-model="school_of_precedence"
                    :error-messages="errors"                    
                    label="Enlace de Imagen de Perfil"
                    prepend-icon="mdi-link"
                    required
                  ></v-text-field>
                </ValidationProvider>
              </v-col>
            </v-row>

            <v-row>
               <v-col cols="12" sm="6" md="3">
                <v-menu
                  ref="menu"
                  v-model="menu"
                  :close-on-content-click="false"
                  :return-value.sync="date"
                  transition="scale-transition"
                  offset-y
                  min-width="290px"
                >
               
                  <template v-slot:activator="{ on }">
                    <v-text-field
                      v-model="date"
                      label="Fecha de nacimiento"
                      prepend-icon="mdi-calendar"
                      readonly
                      v-on="on"
                    ></v-text-field>
                  </template>
                  <v-date-picker v-model="date" no-title scrollable>
                    <v-spacer></v-spacer>
                    <v-btn text color="primary" @click="menu = false">Cancel</v-btn>
                    <v-btn text color="primary" @click="$refs.menu.save(date)">OK</v-btn>
                  </v-date-picker>
                </v-menu>
              </v-col>

              <v-col
                cols="12"
                md="4"
              >
                <v-select
                  v-model="sport"
                  :items="sports"
                  label ="Deporte"
                  prepend-icon="mdi-volleyball"
                ></v-select>
              </v-col>

              <v-col
                cols="12"
                md="4"
              >
                <v-select
                  v-model="number"
                  :items="numbers"
                  label ="Numero del Athleta"
                  prepend-icon="mdi-numeric-0-box"
                ></v-select>
              </v-col>
            </v-row>        

            
           
            <v-btn class="mr-4" @click="submit">submit</v-btn>
            <v-btn @click="clear">clear</v-btn>
            
          </v-container>
        </form>
      </ValidationObserver>
    </v-card-text>
  </v-card>
</template>

<script>
  import { required, email, max, alpha_spaces, alpha, alpha_dash, regex } from 'vee-validate/dist/rules'
  import { extend, ValidationObserver, ValidationProvider, setInteractionMode } from 'vee-validate'

  setInteractionMode('eager')

  extend('required', {
    ...required,
    message: '{_field_} no puede estar vacio',
  })

  extend('max', {
    ...max,
    message: '{_field_} no puede contener mas de {length} caracteres',
  })

  extend('email', {
    ...email,
    message: 'Email must be valid',
  })

  extend('alpha',{
    ...alpha,
    message: "{_field_} solamente debe tener caracteres",
  })

  extend('alpha_spaces',{
    ...alpha_spaces,
    message: "{_field_} solamente debe contener caracters,guiones y/o espacios",
  })
  extend('alpha_dash',{
    ...alpha_dash,
    message: "{_field_} puede contener un guiones",
  })
  extend('regex',{
    ...regex,
    message:"El campos es invalido,",
  })
  

  export default {
    components: {
      ValidationProvider,
      ValidationObserver,
    },
    data: () => ({
      date: new Date().toISOString().substring(0,10),
      menu: false,
      first_name: '',
      middle_name: '',
      last_names:'',
      short_bio:'',
      height_feet:'',
      height_inches:'',
      study_program:'', 
      date_of_birth:'',
      school_of_precedence:'',
      number:0,
      profile_image_link:'',
      sport_id:0,
      sport:'',
      sports:['Voleibol','Baloncesto'],
      feet: [4,5,6,7],
      inches:[0,1,2,3,4,5,6,7,8,9,10,11,12],
      numbers:[0,1,2,3,4,5,6,7,8,9,10,11,12,
              13,14,15,16,17,18,19,20,21,22,
              23,24,25,26,27,28,29,30,31,32,
              33,34,35,36,37,38,39,40,41,42,
              43,44,45,46,47,48,49,50,51,52,
              53,54,55,56,57,58,59,60,61,62,
              63,64,65,66,67,68,69,70,71,72,
              73,74,75,76,77,78,79,80,81,82,
              83,84,85,86,87,88,89,90,91,92,
              93,94,95,96,97,98,99],
         
      
      
    }),

    methods: {
      submit () {
        this.$refs.observer.validate()
      },
      clear () {
        this.first_name= '',
        this.middle_name= '',
        this.last_names='',
        this.short_bio='',
        this.height_feet='',
        this.height_inches='',
        this.study_program='', 
        this.date_of_birth='',
        this.school_of_precedence='',
        this.number=0,
        this.profile_image_link='',
        this.sport_id=0, 
        this.sport ='', 
        
        this.$refs.observer.reset()
      },
    },
  }
</script>