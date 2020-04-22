
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
        <v-toolbar-title>Añadir Estadísticas Atleta {{sport_name}} - {{branch}}</v-toolbar-title>
        <v-spacer />
    </v-toolbar>
    <v-card-text>            
      <ValidationObserver ref="observer" v-slot="{ validate, reset }">
        <form>
            <v-container>   
                <v-row v-if="isBasketball">
                    <v-col>  
                        <v-row 
                            align ="center"
                            justify = "center"
                            >
                                <v-col                   
                                >
                                    <v-autocomplete
                                        v-model="payload_stats.athlete_id"
                                        :items="sport_athletes"
                                        filled
                                        chips
                                        color="blue-grey lighten-2"
                                        label="Select"
                                        item-text="athlete_name"
                                        item-value="athlete_id"
                                        required
                                        >
                                        <template v-slot:selection="data">
                                            <v-chip
                                            v-bind="data.attrs"
                                            :input-value="data.selected"
                                            @click="data.select"
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
                            <h2>Estadisticas de Juego:</h2>
                        </v-row>
                        <v-row 
                        align ="center"
                        justify = "center"
                        >
                            <v-col             
                            >
                                <ValidationProvider v-slot="{ errors }" name="Points" rules="numeric|required">
                                    <v-text-field
                                        v-model="payload_stats.attributes.points"                      
                                        :error-messages="errors"
                                        label="Puntos"
                                        outlined
                                        required
                                    ></v-text-field>
                                </ValidationProvider>
                            </v-col>
                            <v-col             
                            >
                                <ValidationProvider v-slot="{ errors }" name="Rebounds" rules="numeric|required">
                                    <v-text-field
                                        v-model="payload_stats.attributes.rebounds"                      
                                        :error-messages="errors"
                                        label="Rebotes"
                                        outlined
                                        required
                                    ></v-text-field>
                                </ValidationProvider>
                            </v-col>
                            <v-col             
                            >
                                <ValidationProvider v-slot="{ errors }" name="Assists" rules="numeric|required">
                                    <v-text-field
                                        v-model="payload_stats.attributes.assists"                      
                                        :error-messages="errors"
                                        label="Asistencias"
                                        outlined
                                        required
                                    ></v-text-field>
                                </ValidationProvider>
                            </v-col>
                        </v-row>
                        <v-row 
                        align ="center"
                        justify = "center"
                        >
                            <v-col             
                            >
                                <ValidationProvider v-slot="{ errors }" name="Steals" rules="numeric|required">
                                    <v-text-field
                                        v-model="payload_stats.attributes.steals"                      
                                        :error-messages="errors"
                                        label="Rebotes"
                                        required
                                        outlined
                                    ></v-text-field>
                                </ValidationProvider>
                            </v-col>
                            <v-col             
                            >
                                <ValidationProvider v-slot="{ errors }" name="Blocks" rules="numeric|required">
                                    <v-text-field
                                        v-model="payload_stats.attributes.blocks"                      
                                        :error-messages="errors"
                                        label="Bloqueos"
                                        required
                                        outlined
                                    ></v-text-field>
                                </ValidationProvider>
                            </v-col>
                            <v-col             
                            >
                                <ValidationProvider v-slot="{ errors }" name="Turnovers" rules="numeric|required">
                                    <v-text-field
                                        v-model="payload_stats.attributes.turnovers"                      
                                        :error-messages="errors"
                                        label="Pérdidas de Balón"
                                        required
                                        outlined
                                    ></v-text-field>
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
                                <ValidationProvider v-slot="{ errors }" name="Field Goal Attempt" rules="numeric|required">
                                    <v-text-field
                                        v-model="payload_stats.attributes.field_goal_attempt"                      
                                        :error-messages="errors"
                                        label="Tiro de Campo"
                                        required
                                        outlined
                                    ></v-text-field>
                                </ValidationProvider>
                            </v-col>
                            <v-col             
                            >
                                <ValidationProvider v-slot="{ errors }" name="Three Point Attempt" rules="numeric|required">
                                    <v-text-field
                                        v-model="payload_stats.attributes.three_point_attempt"                      
                                        :error-messages="errors"
                                        label="Tiro de Tres Puntos"
                                        required
                                        outlined
                                    ></v-text-field>
                                </ValidationProvider>
                            </v-col>
                            <v-col             
                            >
                                <ValidationProvider v-slot="{ errors }" name="Free Throw Attempt" rules="numeric|required">
                                    <v-text-field
                                        v-model="payload_stats.attributes.free_throw_attempt"                      
                                        :error-messages="errors"
                                        label="Tiro Libre"
                                        required
                                        outlined
                                    ></v-text-field>
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
                                <ValidationProvider v-slot="{ errors }" name="Successful Field Goal" rules="numeric|required">
                                    <v-text-field
                                        v-model="payload_stats.attributes.successful_field_goal"                      
                                        :error-messages="errors"
                                        label="Tiro de Campo "
                                        required
                                        outlined
                                    ></v-text-field>
                                </ValidationProvider>
                            </v-col>
                            <v-col             
                            >
                                <ValidationProvider v-slot="{ errors }" name="Successful Three Point" rules="numeric|required">
                                    <v-text-field
                                        v-model="payload_stats.attributes.successful_three_point"                      
                                        :error-messages="errors"
                                        label="Tiro de Tres Puntos"
                                        required
                                        outlined
                                    ></v-text-field>
                                </ValidationProvider>
                            </v-col>
                            <v-col             
                            >
                                <ValidationProvider v-slot="{ errors }" name="Successful Free Throw" rules="numeric|required">
                                    <v-text-field
                                        v-model="payload_stats.attributes.successful_free_throws"                      
                                        :error-messages="errors"
                                        label="Tiro Libre"
                                        required
                                        outlined
                                    ></v-text-field>
                                </ValidationProvider>
                            </v-col>
                        </v-row>
                    </v-col>
                </v-row>
                <v-row v-if="isVolleyball">
                    <v-col>  
                        <v-row 
                            align ="center"
                            justify = "center"
                            >
                                <v-col                   
                                >
                                    <v-autocomplete
                                        v-model="payload_stats.athlete_id"
                                        :items="sport_athletes"
                                        filled
                                        chips
                                        color="blue-grey lighten-2"
                                        label="Select"
                                        item-text="athlete_name"
                                        item-value="athlete_id"
                                        required
                                        >
                                        <template v-slot:selection="data">
                                            <v-chip
                                            v-bind="data.attrs"
                                            :input-value="data.selected"
                                            @click="data.select"
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
                            <h2>Estadisticas de Juego:</h2>
                        </v-row>
                        <v-row 
                        align ="center"
                        justify = "center"
                        >
                            <v-col             
                            >
                                <ValidationProvider v-slot="{ errors }" name="Kill Points" rules="numeric|required">
                                    <v-text-field
                                        v-model="payload_stats.attributes.kill_points"                      
                                        :error-messages="errors"
                                        label="Puntos de Kill*"
                                        outlined
                                        required
                                    ></v-text-field>
                                </ValidationProvider>
                            </v-col>
                            <v-col             
                            >
                                <ValidationProvider v-slot="{ errors }" name="Attack Errors" rules="numeric|required">
                                    <v-text-field
                                        v-model="payload_stats.attributes.attack_errors"                      
                                        :error-messages="errors"
                                        label="Errores de Ataque"
                                        outlined
                                        required
                                    ></v-text-field>
                                </ValidationProvider>
                            </v-col>
                            <v-col             
                            >
                                <ValidationProvider v-slot="{ errors }" name="Assists" rules="numeric|required">
                                    <v-text-field
                                        v-model="payload_stats.attributes.assists"                      
                                        :error-messages="errors"
                                        label="Asistencias"
                                        outlined
                                        required
                                    ></v-text-field>
                                </ValidationProvider>
                            </v-col>
                        </v-row>
                        <v-row 
                        align ="center"
                        justify = "center"
                        >
                            <v-col             
                            >
                                <ValidationProvider v-slot="{ errors }" name="Aces" rules="numeric|required">
                                    <v-text-field
                                        v-model="payload_stats.attributes.aces"                      
                                        :error-messages="errors"
                                        label="Aces"
                                        required
                                        outlined
                                    ></v-text-field>
                                </ValidationProvider>
                            </v-col>
                            <v-col             
                            >
                                <ValidationProvider v-slot="{ errors }" name="Service Errors" rules="numeric|required">
                                    <v-text-field
                                        v-model="payload_stats.attributes.service_errors"                      
                                        :error-messages="errors"
                                        label="Errores de Servicio"
                                        required
                                        outlined
                                    ></v-text-field>
                                </ValidationProvider>
                            </v-col>
                            <v-col             
                            >
                                <ValidationProvider v-slot="{ errors }" name="Digs" rules="numeric|required">
                                    <v-text-field
                                        v-model="payload_stats.attributes.digs"                      
                                        :error-messages="errors"
                                        label="Digs*"
                                        required
                                        outlined
                                    ></v-text-field>
                                </ValidationProvider>
                            </v-col>
                        </v-row>
                        <v-row 
                        align ="center"
                        justify = "center"
                        >
                            <v-col             
                            >
                                <ValidationProvider v-slot="{ errors }" name="Blocks" rules="numeric|required">
                                    <v-text-field
                                        v-model="payload_stats.attributes.blocks"                      
                                        :error-messages="errors"
                                        label="Bloqueos"
                                        required
                                        outlined
                                    ></v-text-field>
                                </ValidationProvider>
                            </v-col>
                            <v-col             
                            >
                                <ValidationProvider v-slot="{ errors }" name="Blocking Errors" rules="numeric|required">
                                    <v-text-field
                                        v-model="payload_stats.attributes.blocking_errors"                      
                                        :error-messages="errors"
                                        label="Errores de Bloqueo"
                                        required
                                        outlined
                                    ></v-text-field>
                                </ValidationProvider>
                            </v-col>
                            <v-col             
                            >
                                <ValidationProvider v-slot="{ errors }" name="Reception Errors" rules="numeric|required">
                                    <v-text-field
                                        v-model="payload_stats.attributes.reception_errors"                      
                                        :error-messages="errors"
                                        label="Errores de Recepcion*"
                                        required
                                        outlined
                                    ></v-text-field>
                                </ValidationProvider>
                            </v-col>
                        </v-row>
                    </v-col>
                </v-row>
                <v-row v-if="isSoccer">
                    <v-col>  
                        <v-row 
                            align ="center"
                            justify = "center"
                            >
                                <v-col                   
                                >
                                    <v-autocomplete
                                        v-model="payload_stats.athlete_id"
                                        :items="sport_athletes"
                                        filled
                                        chips
                                        color="blue-grey lighten-2"
                                        label="Select"
                                        item-text="athlete_name"
                                        item-value="athlete_id"
                                        required
                                        >
                                        <template v-slot:selection="data">
                                            <v-chip
                                            v-bind="data.attrs"
                                            :input-value="data.selected"
                                            @click="data.select"
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
                            <h2>Estadisticas de Juego:</h2>
                        </v-row>
                        <v-row 
                        align ="center"
                        justify = "center"
                        >
                            <v-col             
                            >
                                <ValidationProvider v-slot="{ errors }" name="Goal Attempts" rules="numeric|required">
                                    <v-text-field
                                        v-model="payload_stats.attributes.goal_attempts"                      
                                        :error-messages="errors"
                                        label="Goal Attempts*"
                                        outlined
                                        required
                                    ></v-text-field>
                                </ValidationProvider>
                            </v-col>
                            <v-col             
                            >
                                <ValidationProvider v-slot="{ errors }" name="Assists" rules="numeric|required">
                                    <v-text-field
                                        v-model="payload_stats.attributes.assists"                      
                                        :error-messages="errors"
                                        label="Asistencias"
                                        outlined
                                        required
                                    ></v-text-field>
                                </ValidationProvider>
                            </v-col>
                            <v-col             
                            >
                                <ValidationProvider v-slot="{ errors }" name="Fouls" rules="numeric|required">
                                    <v-text-field
                                        v-model="payload_stats.attributes.fouls"                      
                                        :error-messages="errors"
                                        label="Fouls*"
                                        outlined
                                        required
                                    ></v-text-field>
                                </ValidationProvider>
                            </v-col>
                        </v-row>
                        <v-row 
                        align ="center"
                        justify = "center"
                        >
                            <v-col             
                            >
                                <ValidationProvider v-slot="{ errors }" name="Cards" rules="numeric|required">
                                    <v-text-field
                                        v-model="payload_stats.attributes.cards"                      
                                        :error-messages="errors"
                                        label="Tarjetas"
                                        required
                                        outlined
                                    ></v-text-field>
                                </ValidationProvider>
                            </v-col>
                            <v-col             
                            >
                                <ValidationProvider v-slot="{ errors }" name="Successful Goals" rules="numeric|required">
                                    <v-text-field
                                        v-model="payload_stats.attributes.successful_goals"                      
                                        :error-messages="errors"
                                        label="Successful Goals*"
                                        required
                                        outlined
                                    ></v-text-field>
                                </ValidationProvider>
                            </v-col>
                            <v-col             
                            >
                                <ValidationProvider v-slot="{ errors }" name="Tackles" rules="numeric|required">
                                    <v-text-field
                                        v-model="payload_stats.attributes.tackles"                      
                                        :error-messages="errors"
                                        label="Tackles*"
                                        required
                                        outlined
                                    ></v-text-field>
                                </ValidationProvider>
                            </v-col>
                        </v-row>
                    </v-col>
                </v-row>
                <v-row v-if="isBaseball">
                    <v-col>  
                        <v-row 
                            align ="center"
                            justify = "center"
                            >
                                <v-col                   
                                >
                                    <v-autocomplete
                                        v-model="payload_stats.athlete_id"
                                        :items="sport_athletes"
                                        filled
                                        chips
                                        color="blue-grey lighten-2"
                                        label="Select"
                                        item-text="athlete_name"
                                        item-value="athlete_id"
                                        required
                                        >
                                        <template v-slot:selection="data">
                                            <v-chip
                                            v-bind="data.attrs"
                                            :input-value="data.selected"
                                            @click="data.select"
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
                            <h2>Estadisticas de Juego:</h2>
                        </v-row>
                        <v-row 
                        align ="center"
                        justify = "center"
                        >
                            <v-col             
                            >
                                <ValidationProvider v-slot="{ errors }" name="At Bats" rules="numeric|required">
                                    <v-text-field
                                        v-model="payload_stats.attributes.at_bats"                      
                                        :error-messages="errors"
                                        label="At Bats*"
                                        outlined
                                        required
                                    ></v-text-field>
                                </ValidationProvider>
                            </v-col>
                            <v-col             
                            >
                                <ValidationProvider v-slot="{ errors }" name="Runs" rules="numeric|required">
                                    <v-text-field
                                        v-model="payload_stats.attributes.runs"                      
                                        :error-messages="errors"
                                        label="Carreras"
                                        outlined
                                        required
                                    ></v-text-field>
                                </ValidationProvider>
                            </v-col>
                            <v-col             
                            >
                                <ValidationProvider v-slot="{ errors }" name="Hits" rules="numeric|required">
                                    <v-text-field
                                        v-model="payload_stats.attributes.hits"                      
                                        :error-messages="errors"
                                        label="Hits*"
                                        outlined
                                        required
                                    ></v-text-field>
                                </ValidationProvider>
                            </v-col>
                        </v-row>
                        <v-row 
                        align ="center"
                        justify = "center"
                        >
                            <v-col             
                            >
                                <ValidationProvider v-slot="{ errors }" name="Runs Batted In" rules="numeric|required">
                                    <v-text-field
                                        v-model="payload_stats.attributes.runs_batted_in"                      
                                        :error-messages="errors"
                                        label="Runs Batted In*"
                                        required
                                        outlined
                                    ></v-text-field>
                                </ValidationProvider>
                            </v-col>
                            <v-col             
                            >
                                <ValidationProvider v-slot="{ errors }" name="Base On Balls" rules="numeric|required">
                                    <v-text-field
                                        v-model="payload_stats.attributes.base_on_balls"                      
                                        :error-messages="errors"
                                        label="Base On Balls*"
                                        required
                                        outlined
                                    ></v-text-field>
                                </ValidationProvider>
                            </v-col>
                            <v-col             
                            >
                                <ValidationProvider v-slot="{ errors }" name="Strikeouts" rules="numeric|required">
                                    <v-text-field
                                        v-model="payload_stats.attributes.strikeouts"                      
                                        :error-messages="errors"
                                        label="Strikeouts*"
                                        required
                                        outlined
                                    ></v-text-field>
                                </ValidationProvider>
                            </v-col>
                        </v-row>
                        <v-row 
                        align ="center"
                        justify = "center"
                        >
                            <v-col             
                            >
                                <ValidationProvider v-slot="{ errors }" name="Left On Base" rules="numeric|required">
                                    <v-text-field
                                        v-model="payload_stats.attributes.left_on_base"                      
                                        :error-messages="errors"
                                        label="Left On Base*"
                                        required
                                        outlined
                                    ></v-text-field>
                                </ValidationProvider>
                            </v-col>
                            <v-col             
                            >
                                
                            </v-col>
                            <v-col             
                            >
                             
                            </v-col>
                        </v-row>
                    </v-col>
                </v-row>
                <v-row>
                    <v-spacer/>
                    <v-spacer/>
                    <v-col>
                        <v-btn class="mr-4" @click="submitAthleteStats">submit</v-btn>
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
        
        //WRITTEN TO/PARAMETERS:
        //Baloncesto
        
        sport_id:'', //comes from route
        // TODO: (Herbert) Verificar como hacer que esto [sport and branch] sea dinamico, pasado por el sport previo
        sport_name:'',    //would have to fetch using sport ID  
        event_id:'',
        branch:'Masculino',    //fetch using sport id and branch, or just getSport if it returns the name
        // //volleyball
        // sport_id:2,
        // sport:'Voleibol',
        // branch:'Masculino',
        // //soccer
        // sport_id:2,
        // sport:'Voleibol',
        // branch:'Masculino',
        // //baseball
        // sport_id:2,
        // sport:'Voleibol',
        // branch:'Masculino',


        season_year:'',        //probably not neccessary, if so would obtain from the Event and its Team
        event_id: 1, //This will come from route
        
        //THE MAIN STATISTICS, SPORTS SPECIFIC
        payload_stats: '',
        
        //CONSTANTS:
        BASKETBALL_IDM: 1,
        BASKETBALL_IDF: 10,
        VOLLEYBALL_IDM: 2,
        VOLLEYBALL_IDF: 12,
        BASEBALL_IDM: 4,
        SOFTBALL_IDF: 16, 
        SOCCER_IDM: 3,
        SOCCER_IDF: 11,

        //CODE HELPERS:
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
        

    }),
                 
    
    created(){
        this.buildDefaultValues()
        this.initializeSportData()

    },
    methods: {
        buildDefaultValues(){
            this.event_id = this.$route.params.id
            if (this.event_id == 1){
                this.sport_id = this.BASKETBALL_IDM
                this.sport_name = "Baloncesto"
            }
            else if (this.event_id == 2){
                this.sport_id =  this.VOLLEYBALL_IDF 
                this.sport_name = "Voleibol"
            }
            else if (this.event_id == 3){
                this.sport_id =  this.SOCCER_IDF 
                this.sport_name = "Futbol"
            }
            else if (this.event_id == 4){
                this.sport_id =  this.BASEBALL_IDM
                this.sport_name = "Beisbol"
            }
        },
        initializeSportData(){
        //console.log(this.season)
		if(this.sport_id!=''){
            if(this.sport_id == this.BASKETBALL_IDM || this.sport_id == this.BASKETBALL_IDF){
                this.payload_stats = {
                "event_id":this.event_id,
                "athlete_id":'',
                "attributes":
                {
                    "points":'',
                    "rebounds":'',
                    "assists":'',
                    "steals":'',
                    "blocks":'',
                    "turnovers":'',
                    "field_goal_attempt":'',
                    "successful_field_goal":'',
                    "three_point_attempt":'',
                    "successful_three_point":'',
                    "free_throw_attempt":'',
                    "successful_free_throw":'',
                }
                }
                
            }
            else if(this.sport_id == this.VOLLEYBALL_IDM || this.sport_id == this.VOLLEYBALL_IDF){
                this.payload_stats = {       
                "event_id": this.event_id,
                "athlete_id":'',
                "attributes":
                {
                    "kill_points":'',
                    "attack_errors":'',
                    "assists":'',
                    "aces":'',
                    "service_errors":'',
                    "digs":'',
                    "blocks":'',
                    "blocking_errors":'',
                    "reception_errors":''
                }
                }
                
            }
            else if(this.sport_id == this.SOCCER_IDM || this.sport_id == this.SOCCER_IDF){
                this.payload_stats = {
                "event_id":this.event_id,
                "athlete_id":'',
                "attributes":
                {
                    "goal_attempts":'',
                    "assists":'',
                    "fouls":'',
                    "cards":'',
                    "successful_goals":'',
                    "tackles":''
                }
                }   
            }
            else if(this.sport_id == this.BASEBALL_IDM || this.sport_id == this.SOFTBALL_IDF){
                this.payload_stats = { 
                "event_id": this.event_id,
                "athlete_id":'',
                "attributes":
                {
                    "at_bats":'',
                    "runs":'',
                    "hits":'',
                    "runs_batted_in":'',
                    "base_on_balls":'',
                    "strikeouts":'',
                    "left_on_base":''
                }
                }
            }
            }
        },

        async submitAthleteStats() {
            const isValid = await this.$refs.observer.validate()     
            if  (!isValid){
                //simply doesn't leave right now, think if want a box. 
            }
            else{
                if (this.payload_stats.athlete_id != ''){
                    console.log(this.payload_stats)
                    this.goToResults()
                }
                
            }
            
        },
        //=================
        // submit () {
        //     this.$refs.observer.validate()
        //     this.goToTeam()
        // },
        
        clear () {
            this.initializeSportData()
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
             this.$router.push("/equipo/")
        },
        goToResults(){
             this.$router.push("/resultados/"+this.event_id)
        }
    },
    computed: {
    // ...mapGetters({
    //   users: "dashboardUsers/users",
    //   isLoadingU: "dashboardUsers/isLoadingU"
    // })
    // a computed getter
    isBasketball: function () {
      // `this` points to the vm instance
      return (this.sport_id == this.BASKETBALL_IDM || this.sport_id == this.BASKETBALL_IDF)
    },
    isVolleyball: function () {
      // `this` points to the vm instance
      return (this.sport_id == this.VOLLEYBALL_IDM || this.sport_id == this.VOLLEYBALL_IDF)
    },
    isSoccer: function () {
      // `this` points to the vm instance
      return (this.sport_id == this.SOCCER_IDM || this.sport_id == this.SOCCER_IDF)
    },
    isBaseball: function () {
      // `this` points to the vm instance
      return (this.sport_id == this.BASEBALL_IDM || this.sport_id == this.SOFTBALL_IDF)
    }
  },
  }

</script>