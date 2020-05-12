
<template>
  <!-- WHEN WE GET HERE: we have the sport id. we have the event id. -->
    <v-row justify="center">
        <v-dialog v-model="dialog" persistent max-width="600px">
            <v-card width="800" class="elevation-12 mx-auto">
                <v-toolbar color="green darken-1" dark flat>
                    <v-toolbar-title>Añadir Estadísticas Atleta {{sport_name}} - {{branch_name}}</v-toolbar-title>
                    <v-spacer />
                </v-toolbar>
                <v-card-text>            
                
                    <v-form v-model="valid">
                        <v-container>   
                            <v-row v-if="isBasketball">
                                <v-col>  
                                    <v-row>
                                        <h2>Seleccionar Atleta:</h2>
                                    </v-row>
                                    <v-row 
                                        align ="center"
                                        justify = "center"
                                        >
                                            <v-col                   
                                            >
                                                <v-autocomplete
                                                    v-model="payload_stats_individual.athlete_id"
                                                    :items="team_members"
                                                    filled
                                                    chips
                                                    color="blue-grey lighten-2"
                                                    label="Seleccione Atleta"
                                                    item-text="first_name"
                                                    item-value="athlete_id"
                                                    :rules="[scoreRequired('Atleta')]"
                                                    required
                                                    :filter="customFilter"
                                                    >
                                                    <template v-slot:selection="data">
                                                        <v-chip
                                                        v-bind="data.attrs"
                                                        :input-value="data.selected"
                                                        @click="data.select"
                                                        >
                                                        <v-avatar left>
                                                            <v-icon v-if="data.item.profile_image_link == null" height="100"> mdi-account </v-icon>
                                                            <v-img v-else :src="data.item.profile_image_link"/>
                                                        </v-avatar>
                                                        {{ data.item.first_name }} {{data.item.middle_name}}  {{data.item.last_names}}
                                                        </v-chip>
                                                    </template>
                                                    <template v-slot:item="data">
                                                        <template v-if="typeof data.item !== 'object'">
                                                        <v-list-item-content v-text="data.item"></v-list-item-content>
                                                        </template>
                                                        <template v-else>
                                                        <v-list-item-avatar>
                                                            <v-icon v-if="data.item.profile_image_link == null" height="100"> mdi-account </v-icon>
                                                            <v-img v-else :src="data.item.profile_image_link"/>
                                                        </v-list-item-avatar>
                                                        <v-list-item-content>
                                                            <!-- <v-list-item-title v-html="data.item.first_name"></v-list-item-title> -->
                                                            <v-list-item-title v-html="data.item.first_name+' '+data.item.middle_name+' '+data.item.last_names" v-if="data.item.middle_name"></v-list-item-title>
                                                            <v-list-item-title v-html="data.item.first_name+' '+data.item.last_names" v-else></v-list-item-title>
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
                                           
                                                <v-text-field
                                                    v-model="payload_stats_individual.attributes.points"                      
                                                    label="Puntos"
                                                    outlined
                                                    required
                                                    :rules="[numeric('Puntos'),scoreRequired('Puntos')]"
                                                ></v-text-field>
                                            
                                        </v-col>
                                        <v-col             
                                        >
                                           
                                                <v-text-field
                                                    v-model="payload_stats_individual.attributes.rebounds"                      
                                                    
                                                    label="Rebotes"
                                                    outlined
                                                    required
                                                    :rules="[numeric('Rebotes'),scoreRequired('Rebotes')]"
                                                ></v-text-field>
                                          
                                        </v-col>
                                        <v-col             
                                        >
                                          
                                                <v-text-field
                                                    v-model="payload_stats_individual.attributes.assists"                      
                                                    :rules="[numeric('Asistencias'),scoreRequired('Asistencias')]"
                                                    label="Asistencias"
                                                    outlined
                                                    required
                                                ></v-text-field>
                                          
                                        </v-col>
                                    </v-row>
                                    <v-row 
                                    align ="center"
                                    justify = "center"
                                    >
                                        <v-col             
                                        >
                                          
                                                <v-text-field
                                                    v-model="payload_stats_individual.attributes.steals"                      
                                                    :rules="[numeric('Robos'),scoreRequired('Robos')]"
                                                    label="Robos"
                                                    required
                                                    outlined
                                                ></v-text-field>
                                            
                                        </v-col>
                                        <v-col             
                                        >
                                            
                                                <v-text-field
                                                    v-model="payload_stats_individual.attributes.blocks"                      
                                                    :rules="[numeric('Bloqueos'),scoreRequired('Bloqueos')]"
                                                    label="Bloqueos"
                                                    required
                                                    outlined
                                                ></v-text-field>
                                            
                                        </v-col>
                                        <v-col             
                                        >
                                            
                                                <v-text-field
                                                    v-model="payload_stats_individual.attributes.turnovers"                      
                                                    :rules="[numeric('Pérdidas de Balón'),scoreRequired('Pérdidas de Balón')]"
                                                    label="Pérdidas de Balón"
                                                    required
                                                    outlined
                                                ></v-text-field>
                                            
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
                                           
                                                <v-text-field
                                                    v-model="payload_stats_individual.attributes.field_goal_attempt"                      
                                                    :rules="[numeric('Tiro de Campo'),scoreRequired('Tiro de Campo')]"
                                                    label="Tiro de Campo"
                                                    required
                                                    outlined
                                                ></v-text-field>
                                           
                                        </v-col>
                                        <v-col             
                                        >
                                           
                                                <v-text-field
                                                    v-model="payload_stats_individual.attributes.three_point_attempt"                      
                                                    :rules="[numeric('Tiro de Tres Puntos'),scoreRequired('Tiro de Tres Puntos')]"
                                                    label="Tiro de Tres Puntos"
                                                    required
                                                    outlined
                                                ></v-text-field>
                                            
                                        </v-col>
                                        <v-col             
                                        >
                                            
                                                <v-text-field
                                                    v-model="payload_stats_individual.attributes.free_throw_attempt"                      
                                                    :rules="[numeric('Tiro Libre'),scoreRequired('Tiro Libre')]"
                                                    label="Tiro Libre"
                                                    required
                                                    outlined
                                                ></v-text-field>
                         
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
                                           
                                                <v-text-field
                                                    v-model="payload_stats_individual.attributes.successful_field_goal"                      
                                                    :rules="[numeric('Tiro de Campo'),scoreRequired('Tiro de Campo')]"
                                                    label="Tiro de Campo"
                                                    required
                                                    outlined
                                                ></v-text-field>
                                            
                                        </v-col>
                                        <v-col             
                                        >
                                            
                                                <v-text-field
                                                    v-model="payload_stats_individual.attributes.successful_three_point"                      
                                                    :rules="[numeric('Tiro de Tres Puntos'),scoreRequired('Tiro de Tres Puntos')]"
                                                    label="Tiro de Tres Puntos"
                                                    required
                                                    outlined
                                                ></v-text-field>
                                           
                                        </v-col>
                                        <v-col             
                                        >
                                            
                                                <v-text-field
                                                    v-model="payload_stats_individual.attributes.successful_free_throw"                      
                                                    :rules="[numeric('Tiro Libre'),scoreRequired('Tiro Libre')]"
                                                    label="Tiro Libre"
                                                    required
                                                    outlined
                                                ></v-text-field>
                                            
                                        </v-col>
                                    </v-row>
                                </v-col>
                            </v-row>
                            <v-row v-if="isVolleyball">
                                <v-col> 
                                    <v-row>
                                        <h2>Seleccionar Atleta:</h2>
                                    </v-row> 
                                    <v-row 
                                        align ="center"
                                        justify = "center"
                                        >
                                            <v-col                   
                                            >
                                                <v-autocomplete
                                                    v-model="payload_stats_individual.athlete_id"
                                                    :items="team_members"
                                                    filled
                                                    chips
                                                    color="blue-grey lighten-2"
                                                    label="Seleccione Atleta"
                                                    item-text="first_name"
                                                    item-value="athlete_id"
                                                    required
                                                    :rules="[scoreRequired('Atleta')]"
                                                    :filter="customFilter"
                                                    >
                                                    <template v-slot:selection="data">
                                                        <v-chip
                                                        v-bind="data.attrs"
                                                        :input-value="data.selected"
                                                        @click="data.select"
                                                        >
                                                        <v-avatar left>
                                                            <v-icon v-if="data.item.profile_image_link == null" height="100"> mdi-account </v-icon>
                                                            <v-img v-else :src="data.item.profile_image_link"/>
                                                        </v-avatar>
                                                        {{ data.item.first_name }} {{data.item.middle_name}}  {{data.item.last_names}}
                                                        </v-chip>
                                                    </template>
                                                    <template v-slot:item="data">
                                                        <template v-if="typeof data.item !== 'object'">
                                                        <v-list-item-content v-text="data.item"></v-list-item-content>
                                                        </template>
                                                        <template v-else>
                                                        <v-list-item-avatar>
                                                            <v-icon v-if="data.item.profile_image_link == null" height="100"> mdi-account </v-icon>
                                                            <v-img v-else :src="data.item.profile_image_link"/>
                                                        </v-list-item-avatar>
                                                        <v-list-item-content>
                                                             <!-- <v-list-item-title v-html="data.item.first_name"></v-list-item-title> -->
                                                            <v-list-item-title v-html="data.item.first_name+' '+data.item.middle_name+' '+data.item.last_names" v-if="data.item.middle_name"></v-list-item-title>
                                                            <v-list-item-title v-html="data.item.first_name+' '+data.item.last_names" v-else></v-list-item-title>
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
                                                <v-text-field
                                                    v-model="payload_stats_individual.attributes.kill_points"                      
                                                    :rules="[numeric('Puntos de Ataque'),scoreRequired('Puntos de Ataque')]"
                                                    label="Puntos de Ataque"
                                                    outlined
                                                    required
                                                ></v-text-field>
                                        </v-col>
                                        <v-col             
                                        >
                                                <v-text-field
                                                    v-model="payload_stats_individual.attributes.attack_errors"                      
                                                    :rules="[numeric('Errores de Ataque'),scoreRequired('Errores de Ataque')]"
                                                    label="Errores de Ataque"
                                                    outlined
                                                    required
                                                ></v-text-field>
                                        </v-col>
                                        <v-col             
                                        >
                                                <v-text-field
                                                    v-model="payload_stats_individual.attributes.assists"                      
                                                    :rules="[numeric('Asistencias'),scoreRequired('Asistencias')]"
                                                    label="Asistencias"
                                                    outlined
                                                    required
                                                ></v-text-field>
                                        </v-col>
                                    </v-row>
                                    <v-row 
                                    align ="center"
                                    justify = "center"
                                    >
                                        <v-col             
                                        >
                                                <v-text-field
                                                    v-model="payload_stats_individual.attributes.aces"                      
                                                    :rules="[numeric('Servicio Directo'),scoreRequired('Servicio Directo')]"
                                                    label="Servicio Directo"
                                                    required
                                                    outlined
                                                ></v-text-field>
                                        </v-col>
                                        <v-col             
                                        >
                                                <v-text-field
                                                    v-model="payload_stats_individual.attributes.service_errors"                      
                                                    :rules="[numeric('Errores de Servicio'),scoreRequired('Errores de Servicio')]"
                                                    label="Errores de Servicio"
                                                    required
                                                    outlined
                                                ></v-text-field>
                                        </v-col>
                                        <v-col             
                                        >
                                                <v-text-field
                                                    v-model="payload_stats_individual.attributes.digs"                      
                                                    :rules="[numeric('Recepciones'),scoreRequired('Recepciones')]"
                                                    label="Recepciones"
                                                    required
                                                    outlined
                                                ></v-text-field>
                                        </v-col>
                                    </v-row>
                                    <v-row 
                                    align ="center"
                                    justify = "center"
                                    >
                                        <v-col             
                                        >
                                                <v-text-field
                                                    v-model="payload_stats_individual.attributes.blocks"                      
                                                    :rules="[numeric('Bloqueos'),scoreRequired('Bloqueos')]"
                                                    label="Bloqueos"
                                                    required
                                                    outlined
                                                ></v-text-field>
                                        </v-col>
                                        <v-col             
                                        >
                                                <v-text-field
                                                    v-model="payload_stats_individual.attributes.blocking_errors"                      
                                                    :rules="[numeric('Errores de Bloqueo'),scoreRequired('Errores de Bloqueo')]"
                                                    label="Errores de Bloqueo"
                                                    required
                                                    outlined
                                                ></v-text-field>
                                        </v-col>
                                        <v-col             
                                        >
                                                <v-text-field
                                                    v-model="payload_stats_individual.attributes.reception_errors"                      
                                                    :rules="[numeric('Errores de Recepcion'),scoreRequired('Errores de Recepcion')]"
                                                    label="Errores de Recepcion"
                                                    required
                                                    outlined
                                                ></v-text-field>
                                        </v-col>
                                    </v-row>
                                </v-col>
                            </v-row>
                            <v-row v-if="isSoccer">
                                <v-col>
                                    <v-row>
                                        <h2>Seleccionar Atleta:</h2>
                                    </v-row>  
                                    <v-row 
                                        align ="center"
                                        justify = "center"
                                        >
                                            <v-col                   
                                            >
                                                <v-autocomplete
                                                    v-model="payload_stats_individual.athlete_id"
                                                    :items="team_members"
                                                    filled
                                                    chips
                                                    color="blue-grey lighten-2"
                                                    label="Seleccione Atleta"
                                                    item-text="first_name"
                                                    item-value="athlete_id"
                                                    required
                                                    :rules="[scoreRequired('Atleta')]"
                                                    :filter="customFilter"
                                                    >
                                                    <template v-slot:selection="data">
                                                        <v-chip
                                                        v-bind="data.attrs"
                                                        :input-value="data.selected"
                                                        @click="data.select"
                                                        >
                                                        <v-avatar left>
                                                            <v-icon v-if="data.item.profile_image_link == null" height="100"> mdi-account </v-icon>
                                                            <v-img v-else :src="data.item.profile_image_link"/>
                                                        </v-avatar>
                                                        {{ data.item.first_name }} {{data.item.middle_name}}  {{data.item.last_names}}
                                                        </v-chip>
                                                    </template>
                                                    <template v-slot:item="data">
                                                        <template v-if="typeof data.item !== 'object'">
                                                        <v-list-item-content v-text="data.item"></v-list-item-content>
                                                        </template>
                                                        <template v-else>
                                                        <v-list-item-avatar>
                                                            <v-icon v-if="data.item.profile_image_link == null" height="100"> mdi-account </v-icon>
                                                            <v-img v-else :src="data.item.profile_image_link"/>
                                                        </v-list-item-avatar>
                                                        <v-list-item-content>
                                                             <!-- <v-list-item-title v-html="data.item.first_name"></v-list-item-title> -->
                                                            <v-list-item-title v-html="data.item.first_name+' '+data.item.middle_name+' '+data.item.last_names" v-if="data.item.middle_name"></v-list-item-title>
                                                            <v-list-item-title v-html="data.item.first_name+' '+data.item.last_names" v-else></v-list-item-title>
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
                                                <v-text-field
                                                    v-model="payload_stats_individual.attributes.goal_attempts"                      
                                                    :rules="[numeric('Intentos de Gol'),scoreRequired('Intentos de Gol')]"
                                                    label="Intentos de Gol"
                                                    outlined
                                                    required
                                                ></v-text-field>
                                        </v-col>
                                        <v-col             
                                        >
                                                <v-text-field
                                                    v-model="payload_stats_individual.attributes.assists"                      
                                                    :rules="[numeric('Asistencias'),scoreRequired('Asistencias')]"
                                                    label="Asistencias"
                                                    outlined
                                                    required
                                                ></v-text-field>
                                        </v-col>
                                        <v-col             
                                        >
                                                <v-text-field
                                                    v-model="payload_stats_individual.attributes.fouls"                      
                                                    :rules="[numeric('Faltas'),scoreRequired('Faltas')]"
                                                    label="Faltas"
                                                    outlined
                                                    required
                                                ></v-text-field>
                                        </v-col>
                                    </v-row>
                                    <v-row 
                                    align ="center"
                                    justify = "center"
                                    >
                                        <v-col             
                                        >
                                                <v-text-field
                                                    v-model="payload_stats_individual.attributes.cards"                      
                                                    :rules="[numeric('Tarjetas'),scoreRequired('Tarjetas')]"
                                                    label="Tarjetas"
                                                    required
                                                    outlined
                                                ></v-text-field>
                                        </v-col>
                                        <v-col             
                                        >
                                                <v-text-field
                                                    v-model="payload_stats_individual.attributes.successful_goals"                      
                                                    :rules="[numeric('Goles Exitosos'),scoreRequired('Goles Exitosos')]"
                                                    label="Goles Exitosos"
                                                    required
                                                    outlined
                                                ></v-text-field>
                                        </v-col>
                                        <v-col             
                                        >
                                                <v-text-field
                                                    v-model="payload_stats_individual.attributes.tackles"                      
                                                    :rules="[numeric('Atajadas'),scoreRequired('Atajadas')]"
                                                    label="Atajadas"
                                                    required
                                                    outlined
                                                ></v-text-field>
                                        </v-col>
                                    </v-row>
                                </v-col>
                            </v-row>
                            <v-row v-if="isBaseball">
                                <v-col>  
                                    <v-row>
                                        <h2>Seleccionar Atleta:</h2>
                                    </v-row>
                                    <v-row 
                                        align ="center"
                                        justify = "center"
                                        >
                                            <v-col                   
                                            >
                                                <v-autocomplete
                                                    v-model="payload_stats_individual.athlete_id"
                                                    :items="team_members"
                                                    filled
                                                    chips
                                                    color="blue-grey lighten-2"
                                                    label="Seleccione Atleta"
                                                    item-text="first_name"
                                                    item-value="athlete_id"
                                                    required
                                                    :rules="[scoreRequired('Atleta')]"
                                                    :filter="customFilter"
                                                    >
                                                    <template v-slot:selection="data">
                                                        <v-chip
                                                        v-bind="data.attrs"
                                                        :input-value="data.selected"
                                                        @click="data.select"
                                                        >
                                                        <v-avatar left>
                                                            <v-icon v-if="data.item.profile_image_link == null" height="100"> mdi-account </v-icon>
                                                            <v-img v-else :src="data.item.profile_image_link"/>
                                                        </v-avatar>
                                                        {{ data.item.first_name }} {{data.item.middle_name}}  {{data.item.last_names}}
                                                        </v-chip>
                                                    </template>
                                                    <template v-slot:item="data">
                                                        <template v-if="typeof data.item !== 'object'">
                                                        <v-list-item-content v-text="data.item"></v-list-item-content>
                                                        </template>
                                                        <template v-else>
                                                        <v-list-item-avatar>
                                                            <v-icon v-if="data.item.profile_image_link == null" height="100"> mdi-account </v-icon>
                                                            <v-img v-else :src="data.item.profile_image_link"/>
                                                        </v-list-item-avatar>
                                                        <v-list-item-content>
                                                             <!-- <v-list-item-title v-html="data.item.first_name"></v-list-item-title> -->
                                                            <v-list-item-title v-html="data.item.first_name+' '+data.item.middle_name+' '+data.item.last_names" v-if="data.item.middle_name"></v-list-item-title>
                                                            <v-list-item-title v-html="data.item.first_name+' '+data.item.last_names" v-else></v-list-item-title>
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
                                                <v-text-field
                                                    v-model="payload_stats_individual.attributes.at_bats"                      
                                                    :rules="[numeric('Turnos al Bate'),scoreRequired('Turnos al Bate')]"
                                                    label="Turnos al Bate"
                                                    outlined
                                                    required
                                                ></v-text-field>
                                        </v-col>
                                        <v-col             
                                        >
                                                <v-text-field
                                                    v-model="payload_stats_individual.attributes.runs"                      
                                                    :rules="[numeric('Carreras'),scoreRequired('Carreras')]"
                                                    label="Carreras"
                                                    outlined
                                                    required
                                                ></v-text-field>
                                        </v-col>
                                        <v-col             
                                        >
                                                <v-text-field
                                                    v-model="payload_stats_individual.attributes.hits"                      
                                                    :rules="[numeric('Hits'),scoreRequired('Hits')]"
                                                    label="Hits"
                                                    outlined
                                                    required
                                                ></v-text-field>
                                        </v-col>
                                    </v-row>
                                    <v-row 
                                    align ="center"
                                    justify = "center"
                                    >
                                        <v-col             
                                        >
                                                <v-text-field
                                                    v-model="payload_stats_individual.attributes.runs_batted_in"                      
                                                    :rules="[numeric('Carreras Empujadas'),scoreRequired('Carreras Empujadas')]"
                                                    label="Carreras Empujadas"
                                                    required
                                                    outlined
                                                ></v-text-field>
                                        </v-col>
                                        <v-col             
                                        >
                                                <v-text-field
                                                    v-model="payload_stats_individual.attributes.base_on_balls"                      
                                                    :rules="[numeric('Base por Bolas'),scoreRequired('Base por Bolas')]"
                                                    label="Base por Bolas"
                                                    required
                                                    outlined
                                                ></v-text-field>
                                        </v-col>
                                        <v-col             
                                        >
                                                <v-text-field
                                                    v-model="payload_stats_individual.attributes.strikeouts"                      
                                                    :rules="[numeric('Ponches'),scoreRequired('Ponches')]"
                                                    label="Ponches"
                                                    required
                                                    outlined
                                                ></v-text-field>
                                        </v-col>
                                    </v-row>
                                    <v-row 
                                    align ="center"
                                    justify = "center"
                                    >
                                        <v-col             
                                        >
                                                <v-text-field
                                                    v-model="payload_stats_individual.attributes.left_on_base"                      
                                                    :rules="[numeric('Dejados en Base'),scoreRequired('Dejados en Base')]"
                                                    label="Dejados en Base"
                                                    required
                                                    outlined
                                                ></v-text-field>
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
                            <v-row v-if="isMedalBased">
                                <v-col>  
                                    <v-row>
                                        <h2>Seleccionar Atleta:</h2>
                                    </v-row>
                                    <v-row 
                                        align ="center"
                                        justify = "center"
                                        >
                                            <v-col                   
                                            >
                                                <v-autocomplete
                                                    v-model="payload_stats_individual.athlete_id"
                                                    :items="team_members"
                                                    filled
                                                    chips
                                                    color="blue-grey lighten-2"
                                                    label="Seleccione Atleta"
                                                    item-text="first_name"
                                                    item-value="athlete_id"
                                                    required
                                                    :rules="[scoreRequired('Atleta')]"
                                                    :filter="customFilter"
                                                    >
                                                    <template v-slot:selection="data">
                                                        <v-chip
                                                        v-bind="data.attrs"
                                                        :input-value="data.selected"
                                                        @click="data.select"
                                                        >
                                                        <v-avatar left>
                                                            <v-icon v-if="data.item.profile_image_link == null" height="100"> mdi-account </v-icon>
                                                            <v-img v-else :src="data.item.profile_image_link"/>
                                                        </v-avatar>
                                                        {{ data.item.first_name }} {{data.item.middle_name}}  {{data.item.last_names}}
                                                        </v-chip>
                                                    </template>
                                                    <template v-slot:item="data">
                                                        <template v-if="typeof data.item !== 'object'">
                                                        <v-list-item-content v-text="data.item"></v-list-item-content>
                                                        </template>
                                                        <template v-else>
                                                        <v-list-item-avatar>
                                                            <v-icon v-if="data.item.profile_image_link == null" height="100"> mdi-account </v-icon>
                                                            <v-img v-else :src="data.item.profile_image_link"/>
                                                        </v-list-item-avatar>
                                                        <v-list-item-content>
                                                             <!-- <v-list-item-title v-html="data.item.first_name"></v-list-item-title> -->
                                                            <v-list-item-title v-html="data.item.first_name+' '+data.item.middle_name+' '+data.item.last_names" v-if="data.item.middle_name"></v-list-item-title>
                                                            <v-list-item-title v-html="data.item.first_name+' '+data.item.last_names" v-else></v-list-item-title>
                                                        </v-list-item-content>
                                                        </template>
                                                    </template>
                                                </v-autocomplete>  
                                            </v-col>
                                        </v-row>       
                                    <v-row>
                                        <h2>Categoria de Deporte:</h2>
                                    </v-row>
                                    <v-row 
                                    align ="center"
                                    justify = "center"
                                    >
                                        <v-col             
                                        >
                                                <v-autocomplete
                                                    v-model="payload_stats_individual.attributes.category_id"
                                                    :items="sport_categories"
                                                    filled
                                                    color="blue-grey lighten-2"
                                                    label="Seleccione Categoria"
                                                    item-text="category_name"
                                                    item-value="category_id"
                                                    required
                                                    :rules="[scoreRequired('Categoria')]"
                                                    >
                                                </v-autocomplete>
                                        </v-col>
                                    </v-row>
                                    <v-row>
                                        <h2>Medalla Obtenida:</h2>
                                    </v-row>
                                    <v-row 
                                    align ="center"
                                    justify = "center"
                                    >
                                        <v-col             
                                        >
                                                <v-autocomplete
                                                    v-model="payload_stats_individual.attributes.medal_id"
                                                    :items="medals"
                                                    filled
                                                    color="blue-grey lighten-2"
                                                    label="Seleccione Medalla"
                                                    item-text="medal_type"
                                                    item-value="medal_id"
                                                    required
                                                    :rules="[scoreRequired('Medalla')]"
                                                    >
                                                </v-autocomplete>
                                        </v-col>
                                    </v-row>
                                </v-col>
                            </v-row>
                            <v-row v-if="isMatchBased">
                                <v-col>  
                                    <v-row>
                                        <h2>Seleccionar Atleta:</h2>
                                    </v-row>
                                    <v-row 
                                        align ="center"
                                        justify = "center"
                                        >
                                            <v-col                   
                                            >
                                                <v-autocomplete
                                                    v-model="payload_stats_individual.athlete_id"
                                                    :items="team_members"
                                                    filled
                                                    chips
                                                    color="blue-grey lighten-2"
                                                    label="Seleccione Atleta"
                                                    item-text="first_name"
                                                    item-value="athlete_id"
                                                    required
                                                    :rules="[scoreRequired('Atleta')]"
                                                    >
                                                    <template v-slot:selection="data">
                                                        <v-chip
                                                        v-bind="data.attrs"
                                                        :input-value="data.selected"
                                                        @click="data.select"
                                                        >
                                                        <v-avatar left>
                                                            <v-icon v-if="data.item.profile_image_link == null" height="100"> mdi-account </v-icon>
                                                            <v-img v-else :src="data.item.profile_image_link"/>
                                                        </v-avatar>
                                                        {{ data.item.first_name }} {{data.item.middle_name}}  {{data.item.last_names}}
                                                        </v-chip>
                                                    </template>
                                                    <template v-slot:item="data">
                                                        <template v-if="typeof data.item !== 'object'">
                                                        <v-list-item-content v-text="data.item"></v-list-item-content>
                                                        </template>
                                                        <template v-else>
                                                        <v-list-item-avatar>
                                                            <v-icon v-if="data.item.profile_image_link == null" height="100"> mdi-account </v-icon>
                                                            <v-img v-else :src="data.item.profile_image_link"/>
                                                        </v-list-item-avatar>
                                                        <v-list-item-content>
                                                             <!-- <v-list-item-title v-html="data.item.first_name"></v-list-item-title> -->
                                                            <v-list-item-title v-html="data.item.first_name+' '+data.item.middle_name+' '+data.item.last_names" v-if="data.item.middle_name"></v-list-item-title>
                                                            <v-list-item-title v-html="data.item.first_name+' '+data.item.last_names" v-else></v-list-item-title>
                                                        </v-list-item-content>
                                                        </template>
                                                    </template>
                                                </v-autocomplete>  
                                            </v-col>
                                        </v-row>       
                                    <v-row>
                                        <h2>Categoria de Deporte:</h2>
                                    </v-row>
                                    <v-row 
                                    align ="center"
                                    justify = "center"
                                    >
                                        <v-col             
                                        >
                                                <v-autocomplete
                                                    v-model="payload_stats_individual.attributes.category_id"
                                                    :items="sport_categories"
                                                    filled
                                                    color="blue-grey lighten-2"
                                                    label="Seleccione Categoria"
                                                    item-text="category_name"
                                                    item-value="category_id"
                                                    required
                                                    :rules="[scoreRequired('Categoria')]"
                                                    >
                                                </v-autocomplete>
                                        </v-col>
                                    </v-row>
                                    <v-row>
                                        <h2>Medalla Obtenida:</h2>
                                    </v-row>
                                    <v-row 
                                    align ="center"
                                    justify = "center"
                                    >
                                        <v-col             
                                        >
                                                <v-text-field
                                                    v-model.number="payload_stats_individual.attributes.matches_played"       
                                                    type="number"               
                                                    label="Matches Played"
                                                    outlined
                                                    required
                                                    :rules="[numeric('Puntos'),scoreRequired('Puntos')]"
                                                ></v-text-field>
                                        </v-col>
                                        <v-col             
                                        >
                                                <v-text-field
                                                    v-model.number="payload_stats_individual.attributes.matches_won"   
                                                    type="number"                   
                                                    label="Matches Won"
                                                    outlined
                                                    required
                                                    :rules="[numeric('Puntos'),scoreRequired('Puntos')]"
                                                ></v-text-field>
                                        </v-col>
                                    </v-row>
                                </v-col>
                            </v-row>
                            <v-row>
                                <v-spacer/>
                                <v-spacer/>
                                <v-col>
                                    <v-btn color="grey darken-3" text @click="close()" :disabled="loadingQuery">cerrar</v-btn>
                                </v-col>
                                <v-col>
                                    <v-btn color="grey darken-3" text @click="clear()" :disabled="loadingQuery">borrar</v-btn>
                                </v-col>
                                <v-col>
                                    <v-btn color="primary darken-1" text @click="submitAthleteStats()" :loading="loadingQuery" :disabled="!valid">guardar</v-btn>
                                </v-col>
                            </v-row>   
                        </v-container>
                    </v-form>
                </v-card-text>
            </v-card>
        </v-dialog>
    </v-row>
</template>

<script>
    import rules from "@/utils/validations"  
    import {mapActions,mapGetters} from "vuex"

  export default {
      name:"AddIndividualStatsModal",
      props:{
        dialog: Boolean,
        event_id: Number,
        sport_route:String,
        payload_stats:Object,
        sport_id:Number,
        team_members:Array,
        refresh_stats:Boolean,
        sport_name:String,
        branch_name:String
      },
    data: () => ({

        valid: false,

        // season_year:'',        //probably not neccessary, if so would obtain from the Event and its Team
        // event_id: 1, //This will come from route
        
        //THE MAIN STATISTICS, SPORTS SPECIFIC
        payload_stats_individual: '',
        
        //CONSTANTS:
        BASKETBALL_IDM: 1,
        BASKETBALL_IDF: 10,
        VOLLEYBALL_IDM: 2,
        VOLLEYBALL_IDF: 12,
        BASEBALL_IDM: 4,
        SOFTBALL_IDF: 16, 
        SOCCER_IDM: 3,
        SOCCER_IDF: 11,
        // OTHER SPORTS (MEDAL BASED)
        ATHLETICS_IDM: 8,
        ATHLETICS_IDF: 19,
        //OTHER SPORTS (MATCH BASED)
        FIELD_TENNIS_IDM: 9,
        FIELD_TENNIS_IDF: 18,
        TABLE_TENNIS_IDM:7,
        TABLE_TENNIS_IDF:15,

        //CODE HELPERS:
        statistics_entry: false,
        sport_categories: '',
        medals: [
            {
                medal_id:1,
                medal_type:"Oro"
            },
            {
                medal_id:2,
                medal_type:"Plata"
            },
            {
                medal_id:3,
                medal_type:"Bronce"
            },
            {
                medal_id:4,
                medal_type:"Ninguna"
            },
        ]

    }),
                 
    
    created(){
        this.buildDefaultValues()
        this.initializeSportData()
        console.log("[TM-ADD_STATS(COMPONENT)]",this.team_members)
    },
    methods: {
        ...rules,
        ...mapActions({
            setQueryLoading:"results/setQueryLoading",
            addIndividualStatistics:"results/addIndividualStatistics",
            getAllEventStatistics:"results/getAllEventStatistics"
            // getSportCategories:"result/getSportCategories"
        }),
        customFilter (item, queryText, itemText) {
            const searchText = queryText.toLowerCase()
            const values = searchText.split(" ");
            if(item.middle_name){
                const textOne = item.first_name.toLowerCase()
                const textTwo = item.middle_name.toLowerCase()
                const textThree = item.last_names.toLowerCase()
                

                if(values.length == 1){
                    return textOne.indexOf(values[0]) > -1 || textTwo.indexOf(values[0]) > -1 || textThree.indexOf(values[0]) > -1
                }
                else if(values.length == 2){
                    return(
                        ((textOne == values[0]) && (textTwo.indexOf(values[1]) > -1 ))
                        ||
                        ((textTwo == values[0]) && (textThree.indexOf(values[1]) > -1 ))
                        ||
                        ((textOne == values[0]) && (textThree.indexOf(values[1]) > -1 ))
                    )
                }
                else if(values.length == 3){
                    return((textOne == values[0]) && (textTwo == values[1]) && (textThree.indexOf(values[2]) > -1 ))
                }
                else{
                    return false
                }
 
            }
            else{
                const textOne = item.first_name.toLowerCase()
                const textTwo = item.last_names.toLowerCase()
                // const searchText = queryText.toLowerCase()
                // return textOne.indexOf(searchText) > -1 || textTwo.indexOf(searchText) > -1


                if(values.length == 1){
                    return textOne.indexOf(values[0]) > -1 || textTwo.indexOf(values[0]) > -1
                }
                else if(values.length == 2){
                    return((textOne == values[0]) && (textTwo.indexOf(values[1]) > -1 ))
                }
                else{
                    return false
                }


            }
        },
        buildDefaultValues(){
            // this.event_id = this.$route.params.id
            // if (this.event_id == 1){
                //TEMPORARY MOCK CATEGORIES
            this.sport_categories=[
                {
                    category_id:5, category_name:"Solo"
                },
                {
                    category_id:7, category_name:"Doble"
                },
                {
                    category_id:12, category_name:"400 Metros"
                },
                {
                    category_id:14, category_name:	"Lanzamiento Martillo"
                },
                {
                    category_id:16, category_name:	"Lanzamiento Disco"
                },
                {
                    category_id:17, category_name:	"Salto Largo"
                },
                {
                    category_id:18, category_name:	"Salto Pértiga"
                },
                {
                    category_id:21, category_name:	"10,000 Metros"
                },
                {
                    category_id:23, category_name:	"Relevo 4 x 100"
                },
                {
                    category_id:25, category_name:	"400 Metros Vallas"
                }
            ]
        },
        initializeSportData(){
        //console.log(this.season)
            if(this.sport_id!=''){
                if(this.sport_id == this.BASKETBALL_IDM || this.sport_id == this.BASKETBALL_IDF){
                    this.payload_stats_individual = {
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
                    this.payload_stats_individual = {       
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
                    this.payload_stats_individual = {
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
                    this.payload_stats_individual = { 
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
                else if (this.sport_id == this.ATHLETICS_IDM || this.sport_id == this.ATHLETICS_IDF){
                    this.payload_stats_individual = {
                        "event_id":Number(this.event_id),
                        "athlete_id":'',
                        "attributes":{
                            "medal_id":'',
                            "category_id":''
                        }
                    }
                }
                else if (this.sport_id == this.FIELD_TENNIS_IDM || this.sport_id == this.FIELD_TENNIS_IDF
                    || this.sport_id == this.TABLE_TENNIS_IDM || this.sport_id == this.TABLE_TENNIS_IDF){
                    this.payload_stats_individual = {
                        "event_id":Number(this.event_id),
                        "athlete_id":'',
                        "attributes":
                        {
                            "matches_played":'',
                            "matches_won":'',
                            "category_id":''
                        }
                    }
                }
            }
        },

        async submitAthleteStats() {
            this.setQueryLoading()
            if (this.payload_stats_individual.athlete_id != ''){
                console.log(this.payload_stats_individual)
                const stats_params = {
                    sport_route: this.sport_route,
                    statistics: this.payload_stats_individual
                }
                await this.addIndividualStatistics(stats_params)
                this.$emit("update:refresh_stats",true);
                this.close()
            }
        },
      
        
        clear () {
            this.initializeSportData()
            // TODO: (Herbert) Check how this works
        },
        close() {
            this.$emit("update:dialog", false);
        }
    },
    computed: {
    ...mapGetters({
        loadingQuery:"results/loadingQuery",
        individual_stats:"results/final_score",
        results_payload:"results/results_payload"
        // categories:"results/categories",
    }),
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
    },
    isMedalBased: function () {
      return (this.sport_id == this.ATHLETICS_IDM || this.sport_id == this.ATHLETICS_IDF)
    },
    isMatchBased: function (){
        return (this.sport_id == this.FIELD_TENNIS_IDM || this.sport_id == this.FIELD_TENNIS_IDF
        || this.sport_id == this.TABLE_TENNIS_IDM || this.sport_id == this.TABLE_TENNIS_IDF)
    }
  },
  }

</script>