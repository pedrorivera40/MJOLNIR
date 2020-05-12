<template>
  <v-container>
    <v-row>
      <v-col>
        <div v-if="loading === true">
          <v-overlay opacity="0.3">
            <v-progress-circular indeterminate></v-progress-circular>
          </v-overlay>
        </div>
      </v-col>
    </v-row>
    <v-dialog v-model="invalid_event_dialog " persistent max-width="600px">
      <v-card>
        <v-card-title>Evento Inválido</v-card-title>
        <v-card-text>El evento seleccionado no existe en el sistema.</v-card-text>
      </v-card>
    </v-dialog>
    <v-dialog
      v-if="invalid_event_dialog === false"
      v-model="no_pbp_dialog"
      persistent
      max-width="600px"
    >
      <v-card>
        <v-card-title>Evento Inválido</v-card-title>
        <v-card-text>El evento seleccionado no tiene la funcionalidad PBP.</v-card-text>
      </v-card>
    </v-dialog>
    <v-dialog
      v-if="invalid_event_dialog === false && no_pbp_dialog === false"
      v-model="invalid_sport_dialog"
      persistent
      max-width="600px"
    >
      <v-card>
        <v-card-title>Evento Inválido</v-card-title>
        <v-card-text>El evento seleccionado no corresponde a un partido de Voleibol.</v-card-text>
      </v-card>
    </v-dialog>
    <v-card
      fixed
      v-if="!invalid_event_dialog && loading === false && !invalid_sport_dialog && !no_pbp_dialog"
    >
      <v-toolbar color="green darken-1" dark flat>
        <v-spacer />
        <v-toolbar-title class="title">{{sportName}}</v-toolbar-title>
        <v-spacer />
      </v-toolbar>
      <v-container>
        <v-row align="center" justify="center">
          <VolleyballScore
            :uprm_team="uprm_team_name"
            :opp_team="opponentName"
            :uprm_score="uprmScore"
            :opp_score="oppScore"
            :current_set="currentSet"
            :current_uprm_score="currentUPRMSet"
            :current_opp_score="currentOppSet"
            :event_id="event_id"
          />
        </v-row>
        <v-row>
          <v-col>
            <v-divider class="mx-4" horizontal></v-divider>
          </v-col>
        </v-row>
        <v-tabs align-with-title centered grow :color="uprm_color">
          <v-tabs-slider :color="uprm_color" />
          <v-tab>JUGADA A JUGADA</v-tab>

          <v-tab>ESTADÍSTICAS POR EQUIPO</v-tab>

          <v-tab>ESTADÍSTICAS POR ATLETAS</v-tab>

          <v-tab-item>
            <v-row justify="center">
              <v-card-title>Administrador de Jugadas</v-card-title>
            </v-row>
            <v-row>
              <VolleyballPBPActionsAdder
                :event_id="event_id"
                :uprm_team_name="uprm_team_name"
                :opp_team_name="opponentName"
                :uprm_roster="uprmRoster"
                :valid_uprm_roster="validUPRMRoster"
                :opp_roster="oppRoster"
                :opp_color="oppColor"
              />
            </v-row>
            <v-row>
              <v-divider class="mx-4" horizontal></v-divider>
            </v-row>

            <v-row justify="center">
              <v-card-title>Acciones Generales</v-card-title>
            </v-row>

            <v-row justify="center">
              <v-tooltip bottom>
                <template v-slot:activator="{ on }">
                  <v-btn
                    class="ma-6"
                    color="primary"
                    dark
                    v-on="on"
                    width="175"
                    @click.native="on_notification_pressed()"
                  >
                    <v-icon class="mx-1">mdi-android-messages</v-icon>Notificación
                  </v-btn>
                </template>
                <span>Crear notificación de juego</span>
              </v-tooltip>

              <v-tooltip bottom>
                <template v-slot:activator="{ on }">
                  <v-btn
                    class="ma-6"
                    color="primary"
                    dark
                    v-on="on"
                    width="225"
                    @click.native="startChooseColor()"
                  >
                    <v-icon class="mx-1">mdi-palette</v-icon>Color de Oponente
                  </v-btn>
                </template>
                <span>Seleccionar color de equipo oponente</span>
              </v-tooltip>

              <v-tooltip bottom>
                <template v-slot:activator="{ on }">
                  <v-btn
                    class="ma-6"
                    color="primary"
                    dark
                    v-on="on"
                    width="175"
                    @click.native="end_pbp_dialog = true"
                  >
                    <v-icon class="mx-1">mdi-file-excel-box</v-icon>Finalizar
                  </v-btn>
                </template>
                <span>Finalizar secuencia de jugadas</span>
              </v-tooltip>
            </v-row>
            <v-row justify="center">
              <v-card-title>Lista de Jugadas</v-card-title>
            </v-row>
            <v-container v-for="action in gameActions" :key="action.key + 500">
              <VolleyballGameAction
                v-if="action.action_type === notification"
                align="center"
                justify="center"
                :action_type="action.action_type"
                :message="action.message"
                :athlete_number="action.athlete_number"
                :athlete_name="action.athlete_name"
                :athlete_img="action.athlete_img"
                in_color="gray"
                :id="action.key"
                :event_id="event_id"
              />
              <VolleyballGameAction
                v-else-if="action.team === opp_keyword"
                align="center"
                justify="center"
                :action_type="action.action_type"
                :message="action.text"
                :athlete_number="findAthleteNumber(action.athlete_id, oppRoster)"
                :athlete_name="findAthleteName(action.athlete_id, 'opponent')"
                :athlete_id="action.athlete_id"
                :athlete_img="action.athlete_img"
                :in_color="oppColor"
                :id="action.key"
                :event_id="event_id"
                :uprmAthletes="uprmRoster"
                :oppAthletes="oppRoster"
                team="Oponente"
              />
              <VolleyballGameAction
                v-else
                align="center"
                justify="center"
                :action_type="action.action_type"
                :message="action.text"
                :athlete_number="findAthleteNumber(action.athlete_id, uprmRoster)"
                :athlete_name="findAthleteName(action.athlete_id, 'uprm')"
                :athlete_img="findAthleteImg(action.athlete_id, uprmRoster)"
                :athlete_id="action.athlete_id"
                :in_color="uprm_color"
                :id="action.key"
                :event_id="event_id"
                :uprmAthletes="uprmRoster"
                :oppAthletes="oppRoster"
                team="UPRM"
              />
            </v-container>
          </v-tab-item>

          <v-tab-item>
            <v-spacer />
            <v-container>
              <v-row align="center" justify="center">
                <v-card-title>ANOTACIONES POR PARCIAL</v-card-title>
              </v-row>

              <v-row>
                <v-col>
                  <v-simple-table>
                    <template v-slot:default>
                      <thead>
                        <tr>
                          <th class="text-center">EQUIPO</th>
                          <th class="text-center">PARCIAL 1</th>
                          <th class="text-center">PARCIAL 2</th>
                          <th class="text-center">PARCIAL 3</th>
                          <th class="text-center">PARCIAL 4</th>
                          <th class="text-center">PARCIAL 5</th>
                        </tr>
                      </thead>
                      <tbody>
                        <tr :key="2525">
                          <td class="text-center">{{ uprm_team_name }}</td>
                          <td class="text-center">{{ uprmSets[0] }}</td>
                          <td class="text-center">{{ uprmSets[1] }}</td>
                          <td class="text-center">{{ uprmSets[2] }}</td>
                          <td class="text-center">{{ uprmSets[3] }}</td>
                          <td class="text-center">{{ uprmSets[4] }}</td>
                        </tr>
                        <tr :key="2526">
                          <td class="text-center">{{ opponentName }}</td>
                          <td class="text-center">{{ oppSets[0] }}</td>
                          <td class="text-center">{{ oppSets[1] }}</td>
                          <td class="text-center">{{ oppSets[2] }}</td>
                          <td class="text-center">{{ oppSets[3] }}</td>
                          <td class="text-center">{{ oppSets[4] }}</td>
                        </tr>
                      </tbody>
                    </template>
                  </v-simple-table>
                </v-col>
              </v-row>

              <v-row>
                <v-col>
                  <v-divider class="mx-4" horizontal></v-divider>
                </v-col>
              </v-row>

              <v-tabs centered :color="uprm_color">
                <v-tabs-slider :color="uprm_color" />

                <v-tab>{{uprm_team_name}}</v-tab>
                <v-tab>{{opponentName}}</v-tab>
                <v-tab-item>
                  <VolleyballStatistics :volleyball_stats="uprmStatistics" />
                </v-tab-item>
                <v-tab-item>
                  <VolleyballStatistics :volleyball_stats="oppStatistics" />
                </v-tab-item>
              </v-tabs>
            </v-container>
          </v-tab-item>
          <v-tab-item>
            <v-spacer />
            <v-container>
              <v-tabs centered :color="uprm_color">
                <v-tabs-slider :color="uprm_color" />
                <v-tab>{{ uprm_team_name }}</v-tab>
                <v-tab>{{ opponentName }}</v-tab>
                <v-tab-item>
                  <v-simple-table>
                    <template v-slot:default>
                      <thead>
                        <tr>
                          <th class="text-center">Atleta</th>
                          <th
                            v-for="(play, idx) in plays_map"
                            :key="idx + 150"
                            class="text-center"
                          >{{ play.esp }}</th>
                        </tr>
                      </thead>
                      <tbody>
                        <tr v-for="(athlete, idx) in uprmAthleteStatistics" :key="idx + 50">
                          <td class="text-left">#{{ athlete.number }}. {{ athlete.name }}</td>
                          <td class="text-center">{{ athlete.killPoints }}</td>
                          <td class="text-center">{{ athlete.attackErrors }}</td>
                          <td class="text-center">{{ athlete.aces }}</td>
                          <td class="text-center">{{ athlete.serviceErrors }}</td>
                          <td class="text-center">{{ athlete.blocks }}</td>
                          <td class="text-center">{{ athlete.blockingPoints }}</td>
                          <td class="text-center">{{ athlete.blockingErrors }}</td>
                          <td class="text-center">{{ athlete.assists }}</td>
                          <td class="text-center">{{ athlete.digs }}</td>
                          <td class="text-center">{{ athlete.receptionErrors }}</td>
                        </tr>
                      </tbody>
                    </template>
                  </v-simple-table>
                </v-tab-item>
                <v-tab-item>
                  <v-simple-table>
                    <template v-slot:default>
                      <thead>
                        <tr>
                          <th class="text-center">Atleta</th>
                          <th
                            v-for="(play, idx) in plays_map"
                            :key="idx + 200"
                            class="text-center"
                          >{{ play.esp }}</th>
                        </tr>
                      </thead>
                      <tbody>
                        <tr v-for="(athlete, idx) in oppAthleteStatistics" :key="idx + 100">
                          <td class="text-left">#{{ athlete.number }}. {{ athlete.name }}</td>
                          <td class="text-center">{{ athlete.killPoints }}</td>
                          <td class="text-center">{{ athlete.attackErrors }}</td>
                          <td class="text-center">{{ athlete.aces }}</td>
                          <td class="text-center">{{ athlete.serviceErrors }}</td>
                          <td class="text-center">{{ athlete.blocks }}</td>
                          <td class="text-center">{{ athlete.blockingPoints }}</td>
                          <td class="text-center">{{ athlete.blockingErrors }}</td>
                          <td class="text-center">{{ athlete.assists }}</td>
                          <td class="text-center">{{ athlete.digs }}</td>
                          <td class="text-center">{{ athlete.receptionErrors }}</td>
                        </tr>
                      </tbody>
                    </template>
                  </v-simple-table>
                </v-tab-item>
              </v-tabs>
            </v-container>
          </v-tab-item>
        </v-tabs>
      </v-container>
      <v-dialog v-model="notification_dialog" persistent max-width="600px">
        <v-form ref="create_form">
          <v-card>
            <v-card-title>
              <span class="headline">Enviar Notificación</span>
            </v-card-title>
            <v-card-text>
              <v-container>
                <v-row allign="center">
                  <v-col>
                    <v-text-field
                      label="Texto de notificación *"
                      required
                      v-model="notification_text"
                      counter="100"
                      :rules="notification_rules"
                      outlined
                    ></v-text-field>
                    <small>* Indica que es un valor requerido</small>
                  </v-col>
                </v-row>
              </v-container>
            </v-card-text>
            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn color="gray darken-3" text @click="reset_notification()">Cerrar</v-btn>
              <v-btn
                color="primary darken-1"
                :loading="button_loading"
                text
                @click.native="send_notification()"
              >Enviar</v-btn>
            </v-card-actions>
          </v-card>
        </v-form>
      </v-dialog>
      <v-dialog v-model="end_pbp_dialog" persistent max-width="300">
        <v-card>
          <v-card-title
            class="text-center"
            style="word-break: normal;"
          >Terminar Secuencia de Jugadas</v-card-title>
          <v-card-text>Terminar una secuencia de jugadas es irreversible. ¿Aún que desea terminar la secuencia de jugadas?</v-card-text>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn color="gray darken-3" text @click="end_pbp_dialog = false">No</v-btn>
            <v-btn color="green darken-1" text @click="startEndPBPSequence()">Sí</v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
      <v-dialog v-model="color_dialog" persistent max-width="300">
        <v-card>
          <v-card-title class="text-center" style="word-break: normal;">Color del Equipo Oponente</v-card-title>
          <v-color-picker v-model="color" show-swatches></v-color-picker>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn color="gray darken-3" text @click="cancelColorUpdate()">Cancelar</v-btn>
            <v-btn
              color="green darken-1"
              text
              :loading="button_loading"
              @click="updateColor()"
            >Guardar</v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
    </v-card>
  </v-container>
</template>

<script>
import VolleyballScore from "../../../components/VolleyballScore";
import VolleyballStatistics from "../../../components/VolleyballStatistics";
import PBPRosterEntry from "../../../components/PBPRosterEntry";
import VolleyballGameAction from "../../../components/VolleyballGameAction";
import VolleyballPBPActionsAdder from "../../../components/VolleyballPBPActionsAdder";
import { mapGetters, mapActions } from "vuex";

export default {
  components: {
    VolleyballScore,
    VolleyballStatistics,
    PBPRosterEntry,
    VolleyballGameAction,
    VolleyballPBPActionsAdder
  },
  data: () => ({
    error_string: "This emulates an error comming from the database",
    loading: true,
    invalid_event_dialog: false,
    no_pbp_dialog: false,
    invalid_sport_dialog: false,
    dialog: false,
    event_id: Number,

    end_pbp_dialog: false,
    color_dialog: false,
    prev_color: null,

    button_loading: false,

    notification_dialog: false,
    notification_text: "",
    notification_rules: [
      v =>
        (!!v && v.length > 0 && v.length <= 100) ||
        "Las notificaciones deben tener entre 1 y 100 caracteres."
    ],

    plays_map: [
      { eng: "kills", esp: "Puntos de Ataque" },
      { eng: "attackErrors", esp: "Errores de Ataque" },
      { eng: "aces", esp: "Servicios Directos" },
      { eng: "serviceError", esp: "Errores de Servicio" },
      { eng: "blocks", esp: "Bloqueos" },
      { eng: "blockingPoints", esp: "Puntos de Bloqueo" },
      { eng: "blockingErrors", esp: "Errores de Bloqueo" },
      { eng: "assists", esp: "Asistencias" },
      { eng: "digs", esp: "Bompeos" },
      { eng: "receptionErrors", esp: "Errores de Recepción" }
    ],

    uprm_color: "primary",
    notification: "Notification",
    uprm_team_name: "uprm",
    opp_keyword: "opponent",
    plays_map: [
      { eng: "kills", esp: "Puntos de Ataque" },
      { eng: "attackErrors", esp: "Errores de Ataque" },
      { eng: "aces", esp: "Servicios Directos" },
      { eng: "serviceError", esp: "Errores de Servicio" },
      { eng: "blocks", esp: "Bloqueos" },
      { eng: "blockingPoints", esp: "Puntos de Bloqueo" },
      { eng: "blockingErrors", esp: "Errores de Bloqueo" },
      { eng: "assists", esp: "Asistencias" },
      { eng: "digs", esp: "Bompeos" },
      { eng: "receptionErrors", esp: "Errores de Recepción" }
    ]
  }),
  methods: {
    sendAdjust(team_name, adjust_no) {
      payload = {
        team: team_name,
        action_type: "ScoreAdjust",
        adjust: adjust_no
      };
      console.log(payload);
    },

    // Functions for init/detach callbacks for maintaining data models based on Firebase updates.
    ...mapActions({
      getEvent: "volleyballPBP/getEvent",
      getValidUPRMRoster: "volleyballPBP/getValidUPRMRoster",
      handleSetScores: "volleyballPBP/handleSetScores",
      handleCurrentSet: "volleyballPBP/handleCurrentSet",
      handleUPRMRoster: "volleyballPBP/handleUPRMRoster",
      handleOPPRoster: "volleyballPBP/handleOPPRoster",
      handleGameOver: "volleyballPBP/handleGameOver",
      handleOppColor: "volleyballPBP/handleOppColor",
      handleGameActions: "volleyballPBP/handleGameActions",
      detachSetScores: "volleyballPBP/detachSetScores",
      detachCurrentSet: "volleyballPBP/detachCurrentSet",
      detachUPRMRoster: "volleyballPBP/detachUPRMRoster",
      detachOPPRoster: "volleyballPBP/detachOPPRoster",
      detachGameOver: "volleyballPBP/detachGameOver",
      detachOppColor: "volleyballPBP/detachOppColor",
      detachGameActions: "volleyballPBP/detachGameActions",
      sendGameAction: "volleyballPBP/sendGameAction",
      endPBPSequence: "volleyballPBP/endPBPSequence",
      clearPBPState: "volleyballPBP/clearPBPState",
      updateOpponentColor: "volleyballPBP/updateOpponentColor"
    }),

    startEndPBPSequence() {
      // Set payload format.
      const payload = {
        event_id: this.event_id
      };
      // Send request for ending a PBP sequence.
      this.endPBPSequence(payload);
      this.end_pbp_dialog = false;
    },

    findAthleteName(athlete_id, team) {
      let athlete_index = -1;
      let roster = [];

      // Set the right roster.
      if (team === "uprm") {
        roster = this.uprmRoster;
      } else if (team === "opponent") {
        roster = this.oppRoster;
      }

      // Iterate through each element in roster.
      for (let index in roster) {
        if (roster[index].key == athlete_id) {
          athlete_index = index;
          continue;
        }
      }

      if (athlete_index === -1) {
        return "Atleta Desconocido";
      }

      // If athlete is opponent, just return its name.
      if (team === "opponent") {
        return roster[athlete_index].name;
      }

      // Otherwise, build its name using the structure established by Odin.
      let athlete_name = roster[athlete_index].first_name;
      if (roster[athlete_index].middle_name !== "") {
        athlete_name += " " + roster[athlete_index].middle_name;
      }
      athlete_name += " " + roster[athlete_index].last_names;

      return athlete_name;
    },

    on_notification_pressed() {
      this.notification_dialog = true;
    },

    async send_notification() {
      if (this.$refs.create_form.validate()) {
        const payload = {
          event_id: this.event_id,
          data: {
            message: this.notification_text,
            action_type: "Notification"
          }
        };

        this.button_loading = true;
        if (await this.sendGameAction(payload)) {
          this.$refs.create_form.reset();
        }
        this.button_loading = false;
      }
    },

    reset_notification() {
      this.notification_dialog = false;
      this.$refs.create_form.reset();
    },

    findAthleteNumber(athlete_id, roster) {
      let athlete_index = -1;
      for (let index in roster) {
        if (roster[index].key == athlete_id) {
          athlete_index = index;
          continue;
        }
      }

      if (athlete_index === -1) {
        return "?";
      }

      return roster[athlete_index].number;
    },

    findAthleteImg(athlete_id, roster) {
      let athlete_index = -1;
      for (let index in roster) {
        if (roster[index].key == athlete_id) {
          athlete_index = index;
          continue;
        }
      }

      if (athlete_index === -1) {
        return "";
      }

      return roster[athlete_index].profile_image_link;
    },

    // Set up variables for color update dialog.
    startChooseColor() {
      this.prev_color = this.color;
      this.color_dialog = true;
    },

    // Rollback to previous color in case cancel was pressed.
    cancelColorUpdate() {
      this.color = this.prev_color;
      this.color_dialog = false;
    },

    // Send request to Odin.
    async updateColor() {
      const payload = {
        event_id: this.event_id,
        color: this.color.hexa
      };

      this.button_loading = true;
      if (await this.updateOpponentColor(payload)) {
        this.color_dialog = false;
      }
      this.button_loading = false;
    }
  },
  computed: {
    // Functions for getting values in the data models.
    ...mapGetters({
      uprmSets: "volleyballPBP/uprmSets",
      oppSets: "volleyballPBP/oppSets",
      currentUPRMSet: "volleyballPBP/currentUPRMSet",
      currentOppSet: "volleyballPBP/currentOppSet",
      currentSet: "volleyballPBP/currentSet",
      uprmScore: "volleyballPBP/uprmScore",
      oppScore: "volleyballPBP/oppScore",
      uprmRoster: "volleyballPBP/uprmRoster",
      oppRoster: "volleyballPBP/oppRoster",
      gameOver: "volleyballPBP/gameOver",
      oppColor: "volleyballPBP/oppColor",
      gameActions: "volleyballPBP/gameActions",
      uprmStatistics: "volleyballPBP/uprmStatistics",
      oppStatistics: "volleyballPBP/oppStatistics",
      uprmAthleteStatistics: "volleyballPBP/uprmAthleteStatistics",
      oppAthleteStatistics: "volleyballPBP/oppAthleteStatistics",
      sportName: "volleyballPBP/sportName",
      hasPBP: "volleyballPBP/hasPBP",
      teamId: "volleyballPBP/teamId",
      validUPRMRoster: "volleyballPBP/validUPRMRoster",
      branch: "volleyballPBP/branch",
      opponentName: "volleyballPBP/opponentName"
    })
  },
  async beforeMount() {
    this.loading = true;
    this.event_id = parseInt(this.$route.params.id);
    // Validate a valid event_id was provided.
    if (await this.getEvent(this.event_id)) {
      this.getValidUPRMRoster(this.teamId);
      this.handleSetScores(this.event_id);
      this.handleCurrentSet(this.event_id);
      this.handleUPRMRoster(this.event_id);
      this.handleOPPRoster(this.event_id);
      this.handleGameOver(this.event_id);
      this.handleOppColor(this.event_id);
      this.handleGameActions(this.event_id);
      if (this.branch === "Masculino") {
        this.uprm_team_name = "Tarzanes";
      } else {
        this.uprm_team_name = "Juanas";
      }
      this.invalid_event_dialog = false;
    } else {
      this.invalid_event_dialog = true;
    }

    // Validate the event has PBP functionality.
    if (this.hasPBP === false) {
      this.no_pbp_dialog = true;
    } else {
      this.no_pbp_dialog = false;
    }

    // Validate the PBP sequence corresponds to Volleyball.
    if (this.sportName != "Voleibol") {
      this.invalid_sport_dialog = true;
    } else {
      this.invalid_sport_dialog = false;
    }

    this.loading = false;
  },

  beforeDestroy() {
    this.detachSetScores(this.event_id);
    this.detachCurrentSet(this.event_id);
    this.detachUPRMRoster(this.event_id);
    this.detachOPPRoster(this.event_id);
    this.detachGameOver(this.event_id);
    this.detachOppColor(this.event_id);
    this.detachGameActions(this.event_id);
    this.clearPBPState();
  }
};
</script>