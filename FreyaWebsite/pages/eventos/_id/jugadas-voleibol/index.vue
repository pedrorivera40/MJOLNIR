<template>
  <v-card fixed>
    <v-toolbar :color="uprm_color" dark flat>
      <v-spacer />
      <v-toolbar-title class="title">{{sportName}}</v-toolbar-title>
      <v-spacer />
    </v-toolbar>
    <v-row v-if="loading">
      <v-col>
        <div>
          <v-overlay opacity="0.3">
            <v-progress-circular indeterminate></v-progress-circular>
          </v-overlay>
        </div>
      </v-col>
    </v-row>
    <v-container v-if="!loading && !dialog">
      <v-row align="center" justify="center">
        <VolleyballScore
          :uprm_team="uprm_team_name"
          :opp_team="opponentName"
          :uprm_score="uprmScore"
          :opp_score="oppScore"
          :current_set="currentSet"
          :current_uprm_score="currentUPRMSet"
          :current_opp_score="currentOppSet"
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
          <h4 align="center" v-if="gameActions.length === 0">En espera de acciones de juego.</h4>
          <v-container v-for="action in gameActions" :key="action.id">
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
            />
            <VolleyballGameAction
              v-else-if="action.team === opp_keyword"
              align="center"
              justify="center"
              :action_type="action.action_type"
              :message="action.text"
              :athlete_number="findAthleteNumber(action.athlete_id, oppRoster)"
              :athlete_name="findAthleteName(action.athlete_id, oppRoster, 'oponente')"
              :athlete_img="action.athlete_img"
              :in_color="oppColor"
              :id="action.key"
            />
            <VolleyballGameAction
              v-else
              align="center"
              justify="center"
              :action_type="action.action_type"
              :message="action.text"
              :athlete_number="findAthleteNumber(action.athlete_id, uprmRoster)"
              :athlete_name="findAthleteName(action.athlete_id, uprmRoster, 'uprm')"
              :athlete_img="findAthleteImg(action.athlete_id, uprmRoster)"
              :in_color="uprm_color"
              :id="action.key"
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
                      <tr :key="uprm_team_name">
                        <td class="text-center">{{ uprm_team_name }}</td>
                        <td class="text-center">{{ uprmSets[0] }}</td>
                        <td class="text-center">{{ uprmSets[1] }}</td>
                        <td class="text-center">{{ uprmSets[2] }}</td>
                        <td class="text-center">{{ uprmSets[3] }}</td>
                        <td class="text-center">{{ uprmSets[4] }}</td>
                      </tr>
                      <tr :key="opponentName">
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
    <v-row>
      <v-col>
        <v-snackbar
          color="white"
          v-model="dialog"
          max-width="425"
          max-height="100"
          class="text-center ma-2 black--text"
        >
          {{error_string}}
          <v-btn color="rgb(67, 160, 71)" text @click="dialog = false">Cerrar</v-btn>
        </v-snackbar>
      </v-col>
    </v-row>
  </v-card>
</template>

<script>
import VolleyballScore from "@/components/VolleyballScore";
import VolleyballStatistics from "@/components/VolleyballStatistics";
import PBPRosterEntry from "@/components/PBPRosterEntry";
import VolleyballGameAction from "@/components/VolleyballGameAction";
import { mapGetters, mapActions } from "vuex";

export default {
  components: {
    VolleyballScore,
    VolleyballStatistics,
    PBPRosterEntry,
    VolleyballGameAction
  },
  data: () => ({
    error_string: "This emulates an error comming from the database",
    loading: false,
    dialog: false,

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

    uprm_color: "#168F09",
    opp_color: "red",
    notification: "Notification",
    opp_keyword: "opponent",
    uprm_team_name: ""
  }),
  methods: {
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
      detachGameActions: "volleyballPBP/detachGameActions"
    }),
    findAthleteName(athlete_id, roster, team) {
      let athlete_index = -1;
      for (let index in roster) {
        if (roster[index].key == athlete_id) {
          athlete_index = index;
          continue;
        }
      }

      if (athlete_index === -1) {
        return "Atleta Desconocido";
      }

      // If it is opponent athlete, only return the name attribute.
      if (team === "oponente") {
        return roster[athlete_index].name;
      }

      // Otherwise return first, middle, and last names.
      let athlete_name = roster[athlete_index].first_name;
      if (roster[athlete_index].middle_name !== "") {
        athlete_name += " " + roster[athlete_index].middle_name;
      }
      athlete_name += " " + roster[athlete_index].last_names;

      return athlete_name;
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
  beforeMount() {
    let event_id = this.$route.params.id;
    this.getEvent(event_id).then(() => {
      this.getValidUPRMRoster(this.teamId);
      this.handleSetScores(event_id);
      this.handleCurrentSet(event_id);
      this.handleUPRMRoster(event_id);
      this.handleOPPRoster(event_id);
      this.handleGameOver(event_id);
      this.handleOppColor(event_id);
      this.handleGameActions(event_id);
      if (this.branch === "Masculino") {
        this.uprm_team_name = "Tarzanes";
      } else {
        this.uprm_team_name = "Juanas";
      }
    });
  },

  beforeDestroy() {
    let event_id = this.$route.params.id;
    this.detachSetScores(event_id);
    this.detachCurrentSet(event_id);
    this.detachUPRMRoster(event_id);
    this.detachOPPRoster(event_id);
    this.detachGameOver(event_id);
    this.detachOppColor(event_id);
    this.detachGameActions(event_id);
  }
};
</script>