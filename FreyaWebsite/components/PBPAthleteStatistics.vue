<template>
  <VolleyballStatistics :volleyball_stats="volleyball_athlete_stats" />
</template>

<script>
import VolleyballStatistics from "/VolleyballStatistics";

export default {
  components: {
    VolleyballStatistics
  },
  props: {
    volleyball_athlete_stats: {},
    athlete_name: String,
    athlete_img: String,
    athlete_number: Number
  }
};
</script>