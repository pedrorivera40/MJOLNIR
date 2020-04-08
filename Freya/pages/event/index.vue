<template>
  <v-card width="800" class="elevation-12 mx-auto">
    <v-toolbar color="green darken-1" dark flat>
      <v-spacer />
      <v-toolbar-title>Evento</v-toolbar-title>
      <v-spacer />
    </v-toolbar>
    <v-card-text>            
      <ValidationObserver ref="observer" v-slot="{ validate, reset }">
        <form>
          <v-container>            
            <v-row>            
							<v-col
                cols="1"
                md="3"
            	>	

              <h2>Fecha del Evento:</h2>
               
            	</v-col>

              <v-col
                cols="12"
                
              >
							<v-date-picker
								v-model="date"
								full-width
								:landscape="$vuetify.breakpoint.smAndUp"
                :show-current="true"
								class="mt-4"
                locale="es-419"
							></v-date-picker>
                
              </v-col>
            </v-row>

						<v-row>
              <v-col
                cols="1"
                md="3"
            	>	

              <h2>Localizacion:</h2>
              
              </v-col>

              <v-col
                cols="12"
                md="3"
              >
                <ValidationProvider v-slot="{ errors }" name="Localizacion" rules="required">
                  <v-select
                    v-model="locality"
                    :items="localities"
                    :error-messages="errors"
                    label ="Localizacion"
                    prepend-icon=""
                  ></v-select>
                </ValidationProvider>
              </v-col>

              <v-col
                cols="12"
                md="4"
              >
                <ValidationProvider v-slot="{ errors }" name="Lugar del Evento" rules="alpha_spaces">
                  <v-text-field
                    v-model="venue"
                    :error-messages="errors"                    
                    label="Lugar del Evento"
                    required
                  ></v-text-field>
                </ValidationProvider>
              </v-col>
						</v-row>

            <v-row>
              <v-col
                cols="1"
                md="3"
            	>	

              <h2>Equipo de Tarzanes:</h2>
               
            	</v-col>

              <v-col
                cols="1"
                md="3"
            	>
               <v-select
                    v-model="teamSport"
                    :items="sportsList"
                    name="sportName"                    
                    label ="Deporte del Equipo"
                    item-text="sportName"
                    item-value="id"                    
                    prepend-icon=""
                ></v-select>
              </v-col>

              <v-col
                cols="1"
                md="3"
            	>
               <v-select
                    v-model="year"
                    :items="yearList"                                       
                    label ="A~no del equipo"                                        
                    prepend-icon=""
                ></v-select>
              </v-col>

            </v-row>

            <v-row>
              <v-col
                cols="1"
                md="3"
              >	

                <h2>Nombre de Oponente:</h2>
                
              </v-col>

              <v-col
                cols="12"
                md="4"
              >
                <ValidationProvider v-slot="{ errors }" name="Nombre de Oponente" rules="alpha_spaces">
                  <v-text-field
                    v-model="opponent_name"
                    :error-messages="errors"                    
                    label="Oponente"
                    required
                  ></v-text-field>
                </ValidationProvider>
              </v-col>
            </v-row>


            <v-row>
              <v-spacer/>
              <v-spacer/>
              <v-col>
                <v-btn class="mr-4" @click="submit">submit</v-btn>
                <v-btn @click="clear">clear</v-btn>
              </v-col>
            </v-row>
            
          </v-container>
        </form>
      </ValidationObserver>
    </v-card-text>
  </v-card>
</template>

<script>
  import { required, email, max, alpha_spaces, alpha, alpha_dash, regex,required_if, is_not } from 'vee-validate/dist/rules'
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
 

  extend('alpha',{
    ...alpha,
    message: "{_field_} solamente debe tener caracteres",
  })

  extend('alpha_spaces',{
    ...alpha_spaces,
    message: "{_field_} solamente debe contener caracters,guiones y/o espacios",
  })
  
  extend('regex',{
    ...regex,
    message:"El campos es invalido",
  })
 

  export default {
    components: {
      ValidationProvider,
      ValidationObserver,
    },
    data: () => ({
      
			date:'', 
			locality:'',
			localities:['Casa','Afuera'],
			venue:'',
			teamSport:'',		
      opponent_name:'',
      yearList:[],
      year:'',
      sportsList:[], 
      sports:[
                  {
                    "branch_name": "masculino ",
                    "sport_id": 13,
                    "sport_image_url": null,
                    "sport_name": "TestSportWithCategory"
                  },
                  {
                    "branch_name": "masculino ",
                    "sport_id": 14,
                    "sport_image_url": null,
                    "sport_name": "TestSportWithPosition"
                  },
                  {
                    "branch_name": "masculino ",
                    "sport_id": 6,
                    "sport_image_url": null,
                    "sport_name": "Judo"
                  },
                  {
                    "branch_name": "masculino ",
                    "sport_id": 8,
                    "sport_image_url": null,
                    "sport_name": "Atletismo"
                  },
                  {
                    "branch_name": "masculino ",
                    "sport_id": 9,
                    "sport_image_url": null,
                    "sport_name": "Tenis de Campo"
                  },
                  {
                    "branch_name": "femenina  ",
                    "sport_id": 15,
                    "sport_image_url": "https://scontent.fsig1-1.fna.fbcdn.net/v/t1.0-9/88102141_2995864247169056_8504767147161944064_o.jpg?_nc_cat=101&_nc_sid=e007fa&_nc_ohc=7iMRLrLUW7AAX_CZufe&_nc_ht=scontent.fsig1-1.fna&oh=a11b1b14f9b0bf3a58ad435bb29c0c9f&oe=5EAAA7AE",
                    "sport_name": "Tenis de Mesa"
                  },
                  {
                    "branch_name": "masculino ",
                    "sport_id": 7,
                    "sport_image_url": "https://scontent.fsig1-1.fna.fbcdn.net/v/t1.0-9/88079647_2995865743835573_4918146400446840832_o.jpg?_nc_cat=107&_nc_sid=e007fa&_nc_ohc=lVEHw0Gk00MAX_npfCs&_nc_ht=scontent.fsig1-1.fna&oh=f51f6c78278be3ede9e9adcc228e07f7&oe=5EAA80F3",
                    "sport_name": "Tenis de Mesa"
                  },
                  {
                    "branch_name": "masculino ",
                    "sport_id": 1,
                    "sport_image_url": "https://scontent.fsig1-1.fna.fbcdn.net/v/t1.0-9/88207403_3003298336425647_2084912734775803904_o.jpg?_nc_cat=109&_nc_sid=e007fa&_nc_ohc=cPJHsQ73nbMAX988FmN&_nc_ht=scontent.fsig1-1.fna&oh=1ff606b6b98ae4bd4d211840ac373a2a&oe=5EAB30D6",
                    "sport_name": "Baloncesto"
                  },
                  {
                    "branch_name": "masculino ",
                    "sport_id": 2,
                    "sport_image_url": "https://scontent.fsig1-1.fna.fbcdn.net/v/t1.0-9/70464070_2501810789907740_7951115497288761344_o.jpg?_nc_cat=111&_nc_sid=e007fa&_nc_ohc=jmq2DHPOaZkAX9edy-A&_nc_ht=scontent.fsig1-1.fna&oh=6ae24f48af684b58f7b7e884aab5adb1&oe=5EACA4BB",
                    "sport_name": "Voleibol"
                  },
                  {
                    "branch_name": "femenina  ",
                    "sport_id": 12,
                    "sport_image_url": "https://scontent.fsig1-1.fna.fbcdn.net/v/t1.0-9/70916818_2501810766574409_3176798918700695552_o.jpg?_nc_cat=102&_nc_sid=e007fa&_nc_ohc=Jokgru5MxFcAX-Iepr4&_nc_ht=scontent.fsig1-1.fna&oh=1e231a8b32569ced072a763ee0270c55&oe=5EA8EF86",
                    "sport_name": "Voleibol"
                  },
                  {
                    "branch_name": "femenina  ",
                    "sport_id": 10,
                    "sport_image_url": "https://scontent.fsig1-1.fna.fbcdn.net/v/t1.0-9/87275067_3003297419759072_5465629605404606464_o.jpg?_nc_cat=107&_nc_sid=e007fa&_nc_ohc=zHfnqen2khcAX-eoOmi&_nc_ht=scontent.fsig1-1.fna&oh=4c49785d0a8dbccdb59b3419f13d1ad1&oe=5EAC3C9E",
                    "sport_name": "Baloncesto"
                  },
                  {
                    "branch_name": "femenina  ",
                    "sport_id": 5,
                    "sport_image_url": "https://scontent.fsig1-1.fna.fbcdn.net/v/t1.0-9/58595547_2226257994129689_639596050000117760_o.jpg?_nc_cat=109&_nc_sid=e007fa&_nc_ohc=xXhLnzI_Ly8AX9TjEXX&_nc_ht=scontent.fsig1-1.fna&oh=61c5bc219d6741df74425df02b5b540f&oe=5EA8C2B7",
                    "sport_name": "Softball"
                  },
                  {
                    "branch_name": "masculino ",
                    "sport_id": 3,
                    "sport_image_url": "https://scontent.fsig1-1.fna.fbcdn.net/v/t1.0-9/74883001_2671827106239440_2718595271939325952_o.jpg?_nc_cat=111&_nc_sid=e007fa&_nc_ohc=lqrGrpZippsAX_BafZ8&_nc_ht=scontent.fsig1-1.fna&oh=da934963689fa5b8d79b31a40cd62835&oe=5EA9881E",
                    "sport_name": "Fútbol"
                  },
                  {
                    "branch_name": "femenina  ",
                    "sport_id": 11,
                    "sport_image_url": "https://scontent.fsig1-1.fna.fbcdn.net/v/t1.0-9/88983239_2989638081125006_5994073246109007872_n.jpg?_nc_cat=104&_nc_sid=e007fa&_nc_ohc=eCtVJEHWHjEAX-4zKxa&_nc_ht=scontent.fsig1-1.fna&oh=b6e46d5ef1e373fa84c065ee433e784a&oe=5EAAE8DB",
                    "sport_name": "Fútbol"
                  },
                  {
                    "branch_name": "masculino ",
                    "sport_id": 4,
                    "sport_image_url": "https://scontent.fsig1-1.fna.fbcdn.net/v/t1.0-9/78952608_2738351966253620_2123712129298071552_o.jpg?_nc_cat=107&_nc_sid=e007fa&_nc_ohc=2yi5Wd4tCSQAX9DgGWk&_nc_ht=scontent.fsig1-1.fna&oh=11cb03d308be92338f1323a7a85270b5&oe=5EAA370E",
                    "sport_name": "Beisbol"
                  },
                  {
                    "branch_name": "femenina  ",
                    "sport_id": 16,
                    "sport_image_url": null,
                    "sport_name": "Softbol"
                  },
                  {
                    "branch_name": "exhibicion",
                    "sport_id": 17,
                    "sport_image_url": null,
                    "sport_name": "Baile"
                  }
              ]


			 
      
      
    }),

    created(){
      this.buildSportsList(),
      this.buildYearList(),
      this.constructDate()
    },   
  

    methods: {
      submit () {
        console.log(this.date) 
        console.log(this.teamSport)      
        this.$refs.observer.validate()
      },
      clear () {
				this.locality =''
				this.date = new Date().toISOString().substr(0,10)
				

        this.$refs.observer.reset()
      },
      buildSportsList(){
        for(let i = 0; i < this.sports.length; i ++)
        {
          let sportObj = this.sports[i]
          this.sportsList.push({'id':sportObj['sport_id'],'sportName':sportObj['sport_name']+'-'+sportObj['branch_name']})

        }
      },
      buildYearList(){
        let yearToAdd = 2020
        let currentYear = new Date(2024,8).getFullYear()
        
        
        while(yearToAdd <= currentYear)
        {
            this.yearList.push(yearToAdd++)
        }
      },
      constructDate()
      {
        let time_zone_offset = new Date().getTimezoneOffset() * 60000
      
        this.date = new Date(Date.now() - time_zone_offset).toISOString().substring(0,10)
        
      }

      
    },
  }
</script>