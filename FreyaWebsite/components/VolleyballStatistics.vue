<template>
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
        <td class="text-center">{{ volleyball_stats.killPoints }}</td>
      </tr>
      <tr>
        <td class="text-center">ERRORES DE ATAQUE</td>
        <td class="text-center">{{ volleyball_stats.attackErrors }}</td>
      </tr>
      <tr>
        <td class="text-center">SERVICIOS DIRECTOS</td>
        <td class="text-center">{{ volleyball_stats.aces }}</td>
      </tr>
      <tr>
        <td class="text-center">ERRORES DE SERVICIO</td>
        <td class="text-center">{{ volleyball_stats.serviceErrors }}</td>
      </tr>
      <tr>
        <td class="text-center">ASSISTENCIAS</td>
        <td class="text-center">{{ volleyball_stats.assists }}</td>
      </tr>
      <tr>
        <td class="text-center">BLOQUEOS</td>
        <td class="text-center">{{ volleyball_stats.blocks }}</td>
      </tr>
      <tr>
        <td class="text-center">PUNTOS DE BLOQUEO</td>
        <td class="text-center">{{ volleyball_stats.blockPoints }}</td>
      </tr>
      <tr>
        <td class="text-center">ERRORES DE BLOQUEO</td>
        <td class="text-center">{{ volleyball_stats.blockingErrors }}</td>
      </tr>
      <tr>
        <td class="text-center">RECEPCIONES/BOMPEOS</td>
        <td class="text-center">{{ volleyball_stats.digs }}</td>
      </tr>
      <tr>
        <td class="text-center">ERRORES DE RECEPCIÓN</td>
        <td class="text-center">{{ volleyball_stats.receptionErrors }}</td>
      </tr>
    </tbody>
  </v-simple-table>
</template>

<script>
export default {
  props: {
    volleyball_stats: {}
  }
};
</script>