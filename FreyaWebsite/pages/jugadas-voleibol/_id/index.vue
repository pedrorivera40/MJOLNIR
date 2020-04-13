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
            <v-row justify="center">
              <v-simple-table>
                <template v-slot:default>
                  <thead>
                    <tr>
                      <th class="text-left">EQUIPO</th>
                      <th class="text-left">SET 1</th>
                      <th class="text-left">SET 2</th>
                      <th class="text-left">SET 3</th>
                      <th class="text-left">SET 4</th>
                      <th class="text-left">SET 5</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr :key="uprm_team_name">
                      <td>{{ uprm_team_name }}</td>
                      <td>{{ score.uprm_set1 }}</td>
                      <td>{{ score.uprm_set2 }}</td>
                      <td>{{ score.uprm_set3 }}</td>
                      <td>{{ score.uprm_set4 }}</td>
                      <td>{{ score.uprm_set5 }}</td>
                    </tr>
                    <tr :key="opponent_team_name">
                      <td>{{ opponent_team_name }}</td>
                      <td>{{ score.opp_set1 }}</td>
                      <td>{{ score.opp_set2 }}</td>
                      <td>{{ score.opp_set3 }}</td>
                      <td>{{ score.opp_set4 }}</td>
                      <td>{{ score.opp_set5 }}</td>
                    </tr>
                  </tbody>
                </template>
              </v-simple-table>
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
                      :in_color="opp_color"
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

export default {
  components: {
    VolleyballScore,
    VolleyballStatistics,
    PBPRosterEntry,
    VolleyballGameAction
  },
  data: () => ({
    sport_name: "Voleibol",
    uprm_team_name: "Tarzanes",
    opponent_team_name: "Gallitos",
    actions: [
      {
        id: 1,
        action_type: "Notification",
        team: "Tarzanes",
        text: "El partido comenzará dentro de 5 minutos."
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
    opp_color: "red",
    notification: "Notification"
  })
};
</script>