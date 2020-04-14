
<template>

    <!-- { "event_id": 5,
  "team_statistics": 
   { "basketball_statistics": 
      { "points":500,
		"rebounds":500,
		"assists":500,
		"steals":500,
		"blocks":500,
		"turnovers":500,
		"field_goal_attempt":500,
		"successful_field_goal":500,
		"three_point_attempt":500,
		"successful_three_point":500,
		"free_throw_attempt":500,
		"successful_free_throw":500
      } 
   },
  "athlete_statistics": 
  [
  	{"athlete_id":4,
  	"statistics":
	  	{"basketball_statistics":
		  	{"points":2,
			"rebounds":2,
			"assists":2,
			"steals":2,
			"blocks":2,
			"turnovers":2,
			"field_goal_attempt":2,
			"successful_field_goal":2,
			"three_point_attempt":2,
			"successful_three_point":2,
			"free_throw_attempt":2,
			"successful_free_throw":2
		  	}
	  	}
  	},
  	{"athlete_id":8,
  	"statistics":
	  	{"basketball_statistics":
		  	{"points":1,
			"rebounds":1,
			"assists":1,
			"steals":1,
			"blocks":1,
			"turnovers":1,
			"field_goal_attempt":1,
			"successful_field_goal":1,
			"three_point_attempt":1,
			"successful_three_point":1,
			"free_throw_attempt":1,
			"successful_free_throw":1
		  	}
	  	}
  	}
  	],
  "uprm_score": 0,
  "opponent_score": 0
} -->

  <!-- WHEN WE GET HERE: we have the sport id. we have the event id. -->
  <v-card width="800" class="elevation-12 mx-auto">
    <v-toolbar color="green darken-1" dark flat>
        <v-toolbar-title>Crear Equipo {{sport}} - {{branch}}</v-toolbar-title>
        <v-spacer />
    </v-toolbar>
    <v-card-text>            
      <ValidationObserver ref="observer" v-slot="{ validate, reset }">
        <form>
            <v-container>  
                <v-row>
                    <v-col>
                        <v-row>      
                            <div>                  
                            <h2>
                                Temporada:
                            </h2>
                            </div> 
                        </v-row>
                        <v-row 
                        align ="center"
                        justify = "center"
                        >
                            <v-col                   
                            >
                                <!-- TODO: (Herbert) Verify just how to validate this so it's REQUIRED / NOT NULL -->
                                <v-select
                                v-model="season_year"
                                :items="yearList"
                                label ="Año de Temporada"
                                prepend-icon="mdi-calendar-blank-multiple"
                                ></v-select>
                            </v-col>
                        </v-row>    
                    </v-col>  
                    <v-col>
                        <v-row>
                            <h2>Imagen de Equipo:</h2>
                            </v-row>
                            <v-row 
                            align ="center"
                            justify = "center"
                            >
                            <v-col  
                            >
                                <ValidationProvider v-slot="{ errors }" name="Enlace de Imagen de Equipo" rules="">
                                    <v-text-field
                                        v-model="team_image_url"
                                        :error-messages="errors"                    
                                        label="Enlace de Imagen de Equipo"
                                        prepend-icon="mdi-link"
                                        required
                                    ></v-text-field>
                                </ValidationProvider>
                            </v-col>
                        </v-row>
                    </v-col>
                </v-row>      
                <v-row 
                    align ="center"
                    justify = "center"
                    >
                        <v-col                   
                        >
                            <v-autocomplete
                                v-model="members_to_add"
                                :items="sport_athletes"
                                filled
                                chips
                                color="blue-grey lighten-2"
                                label="Select"
                                item-text="athlete_name"
                                item-value="athlete_id"
                                multiple
                                :readonly="statistics_entry"
                                >
                                <template v-slot:selection="data">
                                    <v-chip
                                    v-bind="data.attrs"
                                    :input-value="data.selected"
                                    close
                                    @click="data.select"
                                    @click:close="remove_from_select(data.item)"
                                    >
                                    <v-avatar left>
                                        <v-img :src="data.item.profile_image_url"></v-img>
                                    </v-avatar>
                                    {{ data.item.athlete_name }}
                                    </v-chip>
                                </template>
                                <template v-slot:item="data">
                                    <template v-if="typeof data.item !== 'object'">
                                    <v-list-item-content v-text="data.item"></v-list-item-content>
                                    </template>
                                    <template v-else>
                                    <v-list-item-avatar>
                                        <img :src="data.item.profile_image_url">
                                    </v-list-item-avatar>
                                    <v-list-item-content>
                                        <v-list-item-title v-html="data.item.athlete_name"></v-list-item-title>
                                    </v-list-item-content>
                                    </template>
                                </template>
                                </v-autocomplete>
                        </v-col>
                    </v-row>
                    <v-row>
                        <v-spacer/>
                        <v-spacer/>
                        <v-col>
                            <v-btn class="mr-4" @click="submitAthletes">Confirmar Seleccion</v-btn>
                        </v-col>
                    </v-row>
                    <v-row v-if="statistics_entry">
                        <v-col>
                            <v-row
                            v-for="member in members_to_add" 
                            :key='member.uuid'
                            align="center" justify="center"
                            > 
                                <v-col >
                                    <h3>{{member}}</h3>
                                </v-col>
                            </v-row>  
                        </v-col>
                    </v-row>  
                       
                <v-row>
                    <h2>Estadisticas de Juego:</h2>
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
                                v-model="successful_free_throwt"                      
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
    import { required, email, max, alpha_spaces, alpha, alpha_dash, regex,required_if, numeric } from 'vee-validate/dist/rules'
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
    message:"El campos es invalido",
  })
  extend('required_if',{
    ...required_if,
    message:"La posicion es requerida para este deporte",
  })
  extend('numeric',{
    ...numeric,
    message:"{_field_} solamente debe tener numeros",
  })

  export default {
    components: {
        ValidationProvider,
        ValidationObserver,
    },
    data: () => ({
        
        date: new Date().toISOString().substr(0,10),
        
        about_team:'',
        
        team_image_url:'',
        sport_id:1,
        // TODO: (Herbert) Verificar como hacer que esto [sport and branch] sea dinamico, pasado por el sport previo
        sport:'Baloncesto',      
        sports:['Voleibol','Baloncesto','Atletismo'],
        branch:'Masculino',
        branches:['Masculino','Femenino','Otro'],
      
        season_year:'',
        yearList:[],
        

        statistics_entry: false,
        sport_athletes:[
            {
                athlete_name: "Bruce Wayne",
                athlete_id: "1",
                profile_image_url: "https://scontent-mia3-2.xx.fbcdn.net/v/t1.0-9/18056978_1321492691261909_7453541174330533269_n.jpg?_nc_cat=102&_nc_sid=8024bb&_nc_oc=AQmWfwxDy-LTXcZv4K0hcL8VNdr4F0JDlBW90Hq3YG157GtEuXYnB-AKL6hNki0uuh4&_nc_ht=scontent-mia3-2.xx&oh=6dc80a0cb41e6c693897b317148b3753&oe=5EB4AFCF"
            },
            {
                athlete_name: "Richard Grayson",
                athlete_id: "2",
                profile_image_url: "https://vignette.wikia.nocookie.net/marvel_dc/images/a/a2/Nightwing_0008.jpg/revision/latest?cb=20111009075845"
                
            },
            {
                athlete_name: "Clark Kent",
                athlete_id: "3",
                profile_image_url:"https://pbs.twimg.com/media/DUOPKlWU0AEGY0S.jpg:large"
            },
            {
                athlete_name: "Hal Jordan",
                athlete_id: "4",
                profile_image_url:"https://pbs.twimg.com/profile_images/671792891333705728/cbj6SLRA_400x400.jpg"
            },
            {
                athlete_name: "John Stewart",
                athlete_id: "5",
                profile_image_url:"https://pbs.twimg.com/profile_images/378800000008348088/c27e2c3cfc006292e4782888419c9a5b.jpeg"
            },
            {
                athlete_name: "Wallace West",
                athlete_id: "6",
                profile_image_url:"https://pbs.twimg.com/profile_images/702836497679040512/VGriLvTv_400x400.jpg"
            },
            {
                athlete_name: "Arthur Curry",
                athlete_id: "7",
                profile_image_url:"https://pbs.twimg.com/profile_images/720648822242852864/4tkk3y8S_400x400.jpg"
            },
            {
                athlete_name: "Jason Todd",
                athlete_id: "8",
                profile_image_url:"https://pbs.twimg.com/profile_images/378800000191599213/de16556e163c156aad36be8520235133.png"
            },
            {
                athlete_name: "Timothy Drake",
                athlete_id: "9",
                profile_image_url:"https://pbs.twimg.com/profile_images/3478040423/a3b79463a31c644dda362f1f4bc845b9.jpeg"
            },
            {
                athlete_name: "Victor Stone",
                athlete_id: "10",
                profile_image_url:"https://www.dccomics.com/sites/default/files/imce/2018/08-AUG/Cyborg_v01_r01_5b6c7d7bef1616.90753062.jpg"
            },
            {
                athlete_name: "John Constantine",
                athlete_id: "11",
                profile_image_url:"https://pbs.twimg.com/profile_images/669770942164238336/pXR6Znwe_400x400.jpg"
            },
            {
                athlete_name: "Simon Baz",
                athlete_id: "12",
                profile_image_url:"https://pbs.twimg.com/profile_images/1030138980011069440/g3ckdN2u_400x400.jpg"
            }
        ],
        members_to_add:[],

    }),
           
      
      
    

    methods: {
        remove_from_select (item) {
            const index = this.members_to_add.indexOf(item.athlete_id)
            if (index >= 0) this.members_to_add.splice(index, 1)
        },
        submitAthletes () {
            this.statistics_entry = true
        },
        //=================
        submit () {
            this.$refs.observer.validate()
            this.goToTeam()
        },
        
        clear () {
            
            
            
            // TODO: (Herbert) Check how this works
            this.$refs.observer.reset()
        },
        updateCategories(key,value){
            console.log(key)
            console.log(!value)
            this.sport_category[key]=!value
            console.log(this.sport_category)
            
        },
        getVal(key)
        {
            return this.sport_category[key]
        },

        getSport(){
            return this.sport
        },
        goToTeam(){
             this.$router.push('/equipo/')
        }
    },
  }
    // The Only Arguments we need. 
    //{
    //"sport_id":1,   -->selected from existing
    //"season_year":"2020", --> selected from yearList
    //"team_image_url":"www.google.com" -->inserted
    //}
</script>