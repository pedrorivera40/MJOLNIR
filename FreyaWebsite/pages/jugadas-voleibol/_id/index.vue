<template>
  <v-card fixed>
    <v-toolbar color="green darken-1" dark flat>
      <v-spacer />
      <v-toolbar-title class="title">{{sport_name}}</v-toolbar-title>
      <v-spacer />
    </v-toolbar>
    <v-container>
      <v-row align="center" justify="center">
        <VolleyballScore></VolleyballScore>
      </v-row>
      <v-row></v-row>
      <v-tabs align-with-title centered grow color="green">
        <v-tabs-slider color="green" />
        <v-tab>JUGADA A JUGADA</v-tab>

        <v-tab>ESTADÍSTICAS POR EQUIPO</v-tab>

        <v-tab>ESTADÍSTICAS POR ATLETAS</v-tab>

        <v-tab-item>
          <v-timeline>
            <v-container v-for="action in actions" :key="action.id" :color="uprm_color">
              <v-timeline-item left v-if="action.team === opponent_team_name" color:opp_color>
                <v-row align="center" justify="center">{{action.text}}</v-row>
              </v-timeline-item>
              <v-timeline-item right v-else color:uprm_color>
                <v-row align="center" justify="center">{{action.text}}</v-row>
              </v-timeline-item>
            </v-container>
          </v-timeline>
        </v-tab-item>

        <v-tab-item>
          <v-spacer />
          <v-container>
            <v-tabs centered color="green">
              <v-tabs-slider color="green" />
              <v-tab>{{opponent_team_name}}</v-tab>
              <v-tab>{{uprm_team_name}}</v-tab>

              <v-tab-item>
                <v-simple-table fixed-header>
                  <thead>
                    <tr>
                      <th class="text-center">ESTADÍSTICAS DE INTERÉS</th>
                      <th class="text-center">VALOR DE ESTADÍSTICAS</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr>
                      <td class="text-center">PUNTOS EN ATAQUE</td>
                      <td class="text-center">{{ uprm_team_statistics.killPoints }}</td>
                    </tr>
                    <tr>
                      <td class="text-center">ERRORES DE ATAQUE</td>
                      <td class="text-center">{{ uprm_team_statistics.attackErrors }}</td>
                    </tr>
                    <tr>
                      <td class="text-center">SERVICIOS DIRECTOS</td>
                      <td class="text-center">{{ uprm_team_statistics.aces }}</td>
                    </tr>
                    <tr>
                      <td class="text-center">ERRORES DE SERVICIO</td>
                      <td class="text-center">{{ uprm_team_statistics.serviceErrors }}</td>
                    </tr>
                    <tr>
                      <td class="text-center">ASSISTENCIAS</td>
                      <td class="text-center">{{ uprm_team_statistics.assists }}</td>
                    </tr>
                    <tr>
                      <td class="text-center">BLOQUEOS</td>
                      <td class="text-center">{{ uprm_team_statistics.blocks }}</td>
                    </tr>
                    <tr>
                      <td class="text-center">PUNTOS DE BLOQUEO</td>
                      <td class="text-center">{{ uprm_team_statistics.blockPoints }}</td>
                    </tr>
                    <tr>
                      <td class="text-center">ERRORES DE BLOQUEO</td>
                      <td class="text-center">{{ uprm_team_statistics.blockingErrors }}</td>
                    </tr>
                    <tr>
                      <td class="text-center">RECEPCIONES/BOMPEOS</td>
                      <td class="text-center">{{ uprm_team_statistics.digs }}</td>
                    </tr>
                    <tr>
                      <td class="text-center">ERRORES DE RECEPCIÓN</td>
                      <td class="text-center">{{ uprm_team_statistics.receptionErrors }}</td>
                    </tr>
                  </tbody>
                </v-simple-table>
              </v-tab-item>
              <v-tab-item></v-tab-item>
            </v-tabs>
          </v-container>
        </v-tab-item>
        <v-tab-item>
          <v-spacer />
          <v-container>
            <v-tabs centered color="green">
              <v-tabs-slider color="green" />
              <v-tab>{{opponent_team_name}}</v-tab>
              <v-tab>{{uprm_team_name}}</v-tab>
            </v-tabs>
          </v-container>
        </v-tab-item>
      </v-tabs>
    </v-container>
  </v-card>
</template>

<script>
import VolleyballScore from "../../../components/VolleyballScore";

export default {
  components: {
    VolleyballScore
  },
  data: () => ({
    sport_name: "Voleibol",
    uprm_team_name: "Tarzanes",
    opponent_team_name: "Gallitos",
    actions: [{ id: 1, team: "Tarzanes", text: "SOMETHING" }],
    currentSet: 0,
    score: {
      uprm_set1: 0,
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
    opp_team_statistics: {},
    uprm_roster: [
      {
        id: 12345,
        name: "Jose Juan Barea",
        number: 11
      },
      {
        id: 12345,
        name: "Jose Juan Barea",
        number: 11
      },
      {
        id: 12345,
        name: "Jose Juan Barea",
        number: 11
      },
      {
        id: 12345,
        name: "Jose Juan Barea",
        number: 11
      },
      {
        id: 12345,
        name: "Jose Juan Barea",
        number: 11
      },
      {
        id: 12345,
        name: "Jose Juan Barea",
        number: 11
      },
      {
        id: 12345,
        name: "Jose Juan Barea",
        number: 11
      }
    ],
    opp_roster: [
      {
        name: "Jose Juan Barea",
        number: 11
      },
      {
        name: "Jose Juan Barea",
        number: 11
      },
      {
        name: "Jose Juan Barea",
        number: 11
      },
      {
        name: "Jose Juan Barea",
        number: 11
      },
      {
        name: "Jose Juan Barea",
        number: 11
      },
      {
        name: "Jose Juan Barea",
        number: 11
      },
      {
        name: "Jose Juan Barea",
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
    opp_color: "red"
  })
};
</script>