<template>
  <v-card fixed>
    <v-toolbar color="green darken-1" dark flat>
      <v-spacer />
      <v-toolbar-title class="title">{{sport_name}}</v-toolbar-title>
      <v-spacer />
    </v-toolbar>
    <v-container>
      <v-row align="center" justify="center">
        <VolleyballScore
          uprm_team="UPRM"
          opp_team="UPRM-RP"
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
          <v-row justify="center">
            <v-card-title>Administrador de Jugadas</v-card-title>
          </v-row>
          <v-row>
            <VolleyballPBPActionsAdder />
          </v-row>
          <v-row>
            <v-divider class="mx-4" horizontal></v-divider>
          </v-row>
          <v-row justify="center">
            <v-card-title>Lista de Jugadas</v-card-title>
          </v-row>
          <v-container v-for="action in gameActions" :key="action.key">
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
            />
            <VolleyballGameAction
              v-else-if="action.team === opp_keyword"
              align="center"
              justify="center"
              :action_type="action.action_type"
              :message="action.text"
              :athlete_number="action.athlete_number"
              :athlete_name="action.athlete_name"
              :athlete_img="action.athlete_img"
              :in_color="oppColor"
            />
            <VolleyballGameAction
              v-else
              align="center"
              justify="center"
              :action_type="action.action_type"
              :message="action.text"
              :athlete_number="action.athlete_number"
              :athlete_name="action.athlete_name"
              :athlete_img="action.athlete_img"
              :in_color="uprm_color"
            />
          </v-container>
        </v-tab-item>

        <v-tab-item>
          <v-spacer />
          <v-container>
            <v-row align="center" justify="center">
              <v-card-title>ANOTACIONES POR SET</v-card-title>
            </v-row>

            <v-row>
              <v-col>
                <v-simple-table>
                  <template v-slot:default>
                    <thead>
                      <tr>
                        <th class="text-center">EQUIPO</th>
                        <th class="text-center">SET 1</th>
                        <th class="text-center">SET 2</th>
                        <th class="text-center">SET 3</th>
                        <th class="text-center">SET 4</th>
                        <th class="text-center">SET 5</th>
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
                      <tr :key="opponent_team_name">
                        <td class="text-center">{{ opponent_team_name }}</td>
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
              <v-tab>{{opponent_team_name}}</v-tab>
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
              <v-tab>{{ opponent_team_name }}</v-tab>
              <v-tab-item>
                <v-container v-for="athlete in uprm_roster" :key="athlete.number">
                  <v-row justify="center">
                    <PBPRosterEntry
                      :athlete_name="athlete.name"
                      :athlete_number="athlete.number"
                      :athlete_img="athlete.img"
                      :athlete_statistics="uprmStatistics"
                      :in_color="uprm_color"
                    />
                  </v-row>
                </v-container>
              </v-tab-item>
              <v-tab-item>
                <v-container v-for="athlete in opp_roster" :key="athlete.number">
                  <v-row justify="center">
                    <PBPRosterEntry
                      :athlete_name="athlete.name"
                      :athlete_img="athlete.img"
                      :athlete_number="athlete.number"
                      :athlete_statistics="oppStatistics"
                      :in_color="oppColor"
                    />
                  </v-row>
                </v-container>
              </v-tab-item>
            </v-tabs>
          </v-container>
        </v-tab-item>
      </v-tabs>
    </v-container>
  </v-card>
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
    sport_name: "Voleibol",
    uprm_team_name: "Tarzanes",
    opponent_team_name: "Gallitos",
    opp_keyword: "opponent",

    uprm_roster: [
      {
        img:
          "https://scontent.fsig2-1.fna.fbcdn.net/v/t1.0-9/14202778_1104681222954044_4221871197184292482_n.jpg?_nc_cat=108&_nc_sid=e007fa&_nc_ohc=SkJYpfLrBpsAX_hQbOU&_nc_ht=scontent.fsig2-1.fna&oh=7cd68e75d22f20eaedb7423fbb516719&oe=5EB86212",
        name: "Jose Juan Barea",
        number: 11
      },
      {
        img:
          "https://scontent.fsig2-1.fna.fbcdn.net/v/t1.0-9/14102251_1104681199620713_3292201927945481377_n.jpg?_nc_cat=110&_nc_sid=e007fa&_nc_ohc=ZdEZhrqoi18AX-4DRJc&_nc_ht=scontent.fsig2-1.fna&oh=3f4cdce453e1ad2a85ac6e44ee82c5c0&oe=5EB9FCD9",
        name: "Jose Juan Barea",
        number: 11
      },
      {
        img: "",
        name: "Jose Juan Barea",
        number: 11
      },
      {
        img:
          "https://a.espncdn.com/combiner/i?img=/i/headshots/nba/players/full/3055.png",
        name: "Jose Juan Barea",
        number: 11
      },
      {
        img:
          "https://a.espncdn.com/combiner/i?img=/i/headshots/nba/players/full/3055.png",
        name: "Jose Juan Barea",
        number: 11
      },
      {
        img:
          "https://a.espncdn.com/combiner/i?img=/i/headshots/nba/players/full/3055.png",
        name: "Jose Juan Barea",
        number: 11
      },
      {
        img:
          "https://a.espncdn.com/combiner/i?img=/i/headshots/nba/players/full/3055.png",
        name: "Jose Juan Barea",
        number: 11
      }
    ],
    opp_roster: [
      {
        img:
          "https://tvguide1.cbsistatic.com/i/2013/06/19/013edf20-d17d-4caf-85cb-2aa74c834221/948c49a5e70fc6efb5b10fdb2abe74ec/130619mag-martin-lawrence1.jpg",
        name: "MARTIN LAWRENCE",
        number: 11
      },
      {
        img:
          "https://tvguide1.cbsistatic.com/i/2013/06/19/013edf20-d17d-4caf-85cb-2aa74c834221/948c49a5e70fc6efb5b10fdb2abe74ec/130619mag-martin-lawrence1.jpg",
        name: "Martin Lawrence",
        number: 11
      },
      {
        img:
          "https://tvguide1.cbsistatic.com/i/2013/06/19/013edf20-d17d-4caf-85cb-2aa74c834221/948c49a5e70fc6efb5b10fdb2abe74ec/130619mag-martin-lawrence1.jpg",
        name: "Martin Lawrence",
        number: 11
      },
      {
        img:
          "https://tvguide1.cbsistatic.com/i/2013/06/19/013edf20-d17d-4caf-85cb-2aa74c834221/948c49a5e70fc6efb5b10fdb2abe74ec/130619mag-martin-lawrence1.jpg",
        name: "Martin Lawrence",
        number: 11
      },
      {
        img:
          "https://tvguide1.cbsistatic.com/i/2013/06/19/013edf20-d17d-4caf-85cb-2aa74c834221/948c49a5e70fc6efb5b10fdb2abe74ec/130619mag-martin-lawrence1.jpg",
        name: "Martin Lawrence",
        number: 11
      },
      {
        img: "",
        name: "Martin Lawrence",
        number: 15
      },
      {
        img:
          "https://tvguide1.cbsistatic.com/i/2013/06/19/013edf20-d17d-4caf-85cb-2aa74c834221/948c49a5e70fc6efb5b10fdb2abe74ec/130619mag-martin-lawrence1.jpg",
        name: "Martin Lawrence",
        number: 11
      }
    ],
    uprm_player_statistics: [
      {
        id: 12345,
        name: "Jose Juan Barea",
        number: 11,
        killPoints: 0,
        aces: 0,
        blockPoints: 0,
        assists: 0,
        blocks: 0,
        digs: 0,
        attackErrors: 0,
        serviceErrors: 0,
        blockingErrors: 0,
        receptionErrors: 0
      },
      {
        id: 12345,
        name: "Jose Juan Barea",
        number: 11,
        killPoints: 0,
        aces: 0,
        blockPoints: 0,
        assists: 0,
        blocks: 0,
        digs: 0,
        attackErrors: 0,
        serviceErrors: 0,
        blockingErrors: 0,
        receptionErrors: 0
      },
      {
        id: 12345,
        name: "Jose Juan Barea",
        number: 11,
        killPoints: 0,
        aces: 0,
        blockPoints: 0,
        assists: 0,
        blocks: 0,
        digs: 0,
        attackErrors: 0,
        serviceErrors: 0,
        blockingErrors: 0,
        receptionErrors: 0
      },
      {
        id: 12345,
        name: "Jose Juan Barea",
        number: 11,
        killPoints: 0,
        aces: 0,
        blockPoints: 0,
        assists: 0,
        blocks: 0,
        digs: 0,
        attackErrors: 0,
        serviceErrors: 0,
        blockingErrors: 0,
        receptionErrors: 0
      },
      {
        id: 12345,
        name: "Jose Juan Barea",
        number: 11,
        killPoints: 0,
        aces: 0,
        blockPoints: 0,
        assists: 0,
        blocks: 0,
        digs: 0,
        attackErrors: 0,
        serviceErrors: 0,
        blockingErrors: 0,
        receptionErrors: 0
      },
      {
        id: 12345,
        name: "Jose Juan Barea",
        number: 11,
        killPoints: 0,
        aces: 0,
        blockPoints: 0,
        assists: 0,
        blocks: 0,
        digs: 0,
        attackErrors: 0,
        serviceErrors: 0,
        blockingErrors: 0,
        receptionErrors: 0
      },
      {
        id: 12345,
        name: "Jose Juan Barea",
        number: 11,
        killPoints: 0,
        aces: 0,
        blockPoints: 0,
        assists: 0,
        blocks: 0,
        digs: 0,
        attackErrors: 0,
        serviceErrors: 0,
        blockingErrors: 0,
        receptionErrors: 0
      }
    ],
    opp_player_statistics: [
      {
        name: "Jose Juan Barea",
        number: 11,
        killPoints: 0,
        aces: 0,
        blockPoints: 0,
        assists: 0,
        blocks: 0,
        digs: 0,
        attackErrors: 0,
        serviceErrors: 0,
        blockingErrors: 0,
        receptionErrors: 0
      },
      {
        name: "Jose Juan Barea",
        number: 11,
        killPoints: 0,
        aces: 0,
        blockPoints: 0,
        assists: 0,
        blocks: 0,
        digs: 0,
        attackErrors: 0,
        serviceErrors: 0,
        blockingErrors: 0,
        receptionErrors: 0
      },
      {
        name: "Jose Juan Barea",
        number: 11,
        killPoints: 0,
        aces: 0,
        blockPoints: 0,
        assists: 0,
        blocks: 0,
        digs: 0,
        attackErrors: 0,
        serviceErrors: 0,
        blockingErrors: 0,
        receptionErrors: 0
      },
      {
        name: "Jose Juan Barea",
        number: 11,
        killPoints: 0,
        aces: 0,
        blockPoints: 0,
        assists: 0,
        blocks: 0,
        digs: 0,
        attackErrors: 0,
        serviceErrors: 0,
        blockingErrors: 0,
        receptionErrors: 0
      },
      {
        name: "Jose Juan Barea",
        number: 11,
        killPoints: 0,
        aces: 0,
        blockPoints: 0,
        assists: 0,
        blocks: 0,
        digs: 0,
        attackErrors: 0,
        serviceErrors: 0,
        blockingErrors: 0,
        receptionErrors: 0
      },
      {
        name: "Jose Juan Barea",
        number: 11,
        killPoints: 0,
        aces: 0,
        blockPoints: 0,
        assists: 0,
        blocks: 0,
        digs: 0,
        attackErrors: 0,
        serviceErrors: 0,
        blockingErrors: 0,
        receptionErrors: 0
      },
      {
        name: "Jose Juan Barea",
        number: 11,
        killPoints: 0,
        aces: 0,
        blockPoints: 0,
        assists: 0,
        blocks: 0,
        digs: 0,
        attackErrors: 0,
        serviceErrors: 0,
        blockingErrors: 0,
        receptionErrors: 0
      }
    ],
    uprm_color: "green",
    notification: "Notification"
  }),
  methods: {
    // Functions for init/detach callbacks for maintaining data models based on Firebase updates.
    ...mapActions({
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
    })
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
      oppStatistics: "volleyballPBP/oppStatistics"
    })
  },
  beforeMount() {
    this.handleSetScores(this.$route.params.id);
    this.handleCurrentSet(this.$route.params.id);
    this.handleUPRMRoster(this.$route.params.id);
    this.handleOPPRoster(this.$route.params.id);
    this.handleGameOver(this.$route.params.id);
    this.handleOppColor(this.$route.params.id);
    this.handleGameActions(this.$route.params.id);
  },
  beforeDestroy() {
    this.detachSetScores(this.$route.params.id);
    this.detachCurrentSet(this.$route.params.id);
    this.detachUPRMRoster(this.$route.params.id);
    this.detachOPPRoster(this.$route.params.id);
    this.detachGameOver(this.$route.params.id);
    this.detachOppColor(this.$route.params.id);
    this.detachGameActions(this.$route.params.id);
  }
};
</script>