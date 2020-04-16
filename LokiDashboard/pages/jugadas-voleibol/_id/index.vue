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
          :uprm_score="0"
          :opp_score="0"
          :current_set="currentSet"
          :current_uprm_score="0"
          :current_opp_score="0"
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
          <v-container v-for="action in actions" :key="action.id">
            <VolleyballGameAction
              v-if="action.action_type === notification"
              align="center"
              justify="center"
              :action_type="action.action_type"
              :message="action.text"
              :athlete_number="action.athlete_number"
              :athlete_name="action.athlete_name"
              :athlete_img="action.athlete_img"
              in_color="gray"
            />
            <VolleyballGameAction
              v-else-if="action.team === opponent_team_name"
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
                        <td class="text-center">{{ uprmSet1 }}</td>
                        <td class="text-center">{{ uprmSet2 }}</td>
                        <td class="text-center">{{ uprmSet3 }}</td>
                        <td class="text-center">{{ uprmSet4 }}</td>
                        <td class="text-center">{{ uprmSet5 }}</td>
                      </tr>
                      <tr :key="opponent_team_name">
                        <td class="text-center">{{ opponent_team_name }}</td>
                        <td class="text-center">{{ oppSet1 }}</td>
                        <td class="text-center">{{ oppSet2 }}</td>
                        <td class="text-center">{{ oppSet3 }}</td>
                        <td class="text-center">{{ oppSet4 }}</td>
                        <td class="text-center">{{ oppSet5 }}</td>
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
                <VolleyballStatistics :volleyball_stats="uprm_team_statistics" />
              </v-tab-item>
              <v-tab-item>
                <VolleyballStatistics :volleyball_stats="opp_team_statistics" />
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
                      :athlete_statistics="uprm_team_statistics"
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
                      :athlete_statistics="opp_team_statistics"
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
    scores: {
      uprm: [0, 0, 0, 0, 0],
      opp: [0, 0, 0, 0, 0]
    },
    actions: [
      {
        id: 1,
        action_type: "Notification",
        team: "Tarzanes",
        text:
          "Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean m"
      },
      {
        id: 2,
        action_type: "BlockPoint",
        team: "Gallitos",
        text: "El partido comenzará dentro de 5 minutos.",
        athlete_number: 5,
        athlete_name: "Martin Lawrence",
        athlete_img:
          "https://tvguide1.cbsistatic.com/i/2013/06/19/013edf20-d17d-4caf-85cb-2aa74c834221/948c49a5e70fc6efb5b10fdb2abe74ec/130619mag-martin-lawrence1.jpg"
      },
      {
        id: 2,
        action_type: "KillPoint",
        team: "Tarzanes",
        text: "El partido comenzará dentro de 5 minutos.",
        athlete_number: 11,
        athlete_name: "Jose Juan Barea",
        athlete_img:
          "https://a.espncdn.com/combiner/i?img=/i/headshots/nba/players/full/3055.png"
      }
    ],

    uprm_team_statistics: {
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
    opp_team_statistics: {
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
      uprmSet1: "volleyballPBP/uprmSet1",
      uprmSet2: "volleyballPBP/uprmSet2",
      uprmSet3: "volleyballPBP/uprmSet3",
      uprmSet4: "volleyballPBP/uprmSet4",
      uprmSet5: "volleyballPBP/uprmSet5",
      oppSet1: "volleyballPBP/oppSet1",
      oppSet2: "volleyballPBP/oppSet2",
      oppSet3: "volleyballPBP/oppSet3",
      oppSet4: "volleyballPBP/oppSet4",
      oppSet5: "volleyballPBP/oppSet5",
      uprmSetScore: "volleyballPBP/uprmSetScore",
      oppSetScore: "volleyballPBP/oppSetScore",
      currentSet: "volleyballPBP/currentSet",
      uprmRoster: "volleyballPBP/uprmRoster",
      oppRoster: "volleyballPBP/oppRoster",
      gameOver: "volleyballPBP/gameOver",
      oppColor: "volleyballPBP/oppColor",
      gameActions: "volleyballPBP/gameActions"
    })
  },
  beforeMount() {
    this.handleSetScores("unique-volleyball-game-id-1");
    this.handleCurrentSet("unique-volleyball-game-id-1");
    this.handleUPRMRoster("unique-volleyball-game-id-1");
    this.handleOPPRoster("unique-volleyball-game-id-1");
    this.handleGameOver("unique-volleyball-game-id-1");
    this.handleOppColor("unique-volleyball-game-id-1");
    this.handleGameActions("unique-volleyball-game-id-1");
  },
  beforeDestroy() {
    this.detachSetScores("unique-volleyball-game-id-1");
    this.detachCurrentSet("unique-volleyball-game-id-1");
    this.detachUPRMRoster("unique-volleyball-game-id-1");
    this.detachOPPRoster("unique-volleyball-game-id-1");
    this.detachGameOver("unique-volleyball-game-id-1");
    this.detachOppColor("unique-volleyball-game-id-1");
    this.detachGameActions("unique-volleyball-game-id-1");
  }
};
</script>