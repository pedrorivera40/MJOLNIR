<template>
  <v-card fixed>
    <v-toolbar color="green darken-1" dark flat>
      <v-spacer />
      <v-toolbar-title class="title">{{sport_name}}</v-toolbar-title>
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
          :opp_team="opponent_team_name"
          :uprm_score="uprm_score"
          :opp_score="opp_score"
          :current_set="current_set"
          :current_uprm_score="current_uprm_score"
          :current_opp_score="current_opp_score"
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
              :in_color="opp_color"
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
                        <td class="text-center">{{ score.uprm_set1 }}</td>
                        <td class="text-center">{{ score.uprm_set2 }}</td>
                        <td class="text-center">{{ score.uprm_set3 }}</td>
                        <td class="text-center">{{ score.uprm_set4 }}</td>
                        <td class="text-center">{{ score.uprm_set5 }}</td>
                      </tr>
                      <tr :key="opponent_team_name">
                        <td class="text-center">{{ opponent_team_name }}</td>
                        <td class="text-center">{{ score.opp_set1 }}</td>
                        <td class="text-center">{{ score.opp_set2 }}</td>
                        <td class="text-center">{{ score.opp_set3 }}</td>
                        <td class="text-center">{{ score.opp_set4 }}</td>
                        <td class="text-center">{{ score.opp_set5 }}</td>
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
                <v-simple-table>
                  <template v-slot:default>
                    <thead>
                      <tr>
                        <th class="text-center">Atleta</th>
                        <th v-for="play in plays_map" :key="play" class="text-center">{{ play.esp }}</th>
                      </tr>
                    </thead>
                    <tbody>
                      <tr v-for="athlete in opp_player_statistics" :key="athlete">
                        <td class="text-left">#{{ athlete.number }}. {{ athlete.name }}</td>
                        <td class="text-center">{{ athlete.killPoints }}</td>
                        <td class="text-center">{{ athlete.attackErrors }}</td>
                        <td class="text-center">{{ athlete.aces }}</td>
                        <td class="text-center">{{ athlete.serviceErrors }}</td>
                        <td class="text-center">{{ athlete.blocks }}</td>
                        <td class="text-center">{{ athlete.blockPoints }}</td>
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
import VolleyballScore from "../../../components/VolleyballScore";
import VolleyballStatistics from "../../../components/VolleyballStatistics";
import PBPRosterEntry from "../../../components/PBPRosterEntry";
import VolleyballGameAction from "../../../components/VolleyballGameAction";

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
    sport_name: "Voleibol",
    uprm_team_name: "Tarzanes",
    opponent_team_name: "Gallitos",
    uprm_score: 2,
    opp_score: 0,
    current_set: 1,
    current_uprm_score: 10,
    current_opp_score: 2,
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
    actions: [
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
        id: 3,
        action_type: "KillPoint",
        team: "Tarzanes",
        text: "El partido comenzará dentro de 5 minutos.",
        athlete_number: 11,
        athlete_name: "Jose Juan Barea",
        athlete_img:
          "https://a.espncdn.com/combiner/i?img=/i/headshots/nba/players/full/3055.png"
      },
      {
        id: 1,
        action_type: "Notification",
        team: "Tarzanes",
        text: "El partido comenzará dentro de 5 minutos."
      }
    ],
    currentSet: 0,
    score: {
      uprm_set1: 1,
      opp_set1: 0,
      uprm_set2: 0,
      opp_set2: 0,
      uprm_set3: 0,
      opp_set3: 0,
      uprm_set4: 0,
      opp_set4: 0,
      uprm_set5: 0,
      opp_set5: 0
    },
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
        number: 12
      },
      {
        img:
          "https://scontent.fsig2-1.fna.fbcdn.net/v/t1.0-9/14102251_1104681199620713_3292201927945481377_n.jpg?_nc_cat=110&_nc_sid=e007fa&_nc_ohc=ZdEZhrqoi18AX-4DRJc&_nc_ht=scontent.fsig2-1.fna&oh=3f4cdce453e1ad2a85ac6e44ee82c5c0&oe=5EB9FCD9",
        name: "Jose Juan Barea",
        number: 13
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
        number: 14
      },
      {
        img:
          "https://a.espncdn.com/combiner/i?img=/i/headshots/nba/players/full/3055.png",
        name: "Jose Juan Barea",
        number: 3
      },
      {
        img:
          "https://a.espncdn.com/combiner/i?img=/i/headshots/nba/players/full/3055.png",
        name: "Jose Juan Barea",
        number: 2
      },
      {
        img:
          "https://a.espncdn.com/combiner/i?img=/i/headshots/nba/players/full/3055.png",
        name: "Jose Juan Barea",
        number: 2
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
    opp_color: "red",
    notification: "Notification"
  })
};
</script>