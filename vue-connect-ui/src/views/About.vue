<template>
  <div>
    <h1>About</h1>
    <table v-if="info">
      <thead>
        <tr>
          <th>Key</th>
          <th>Value</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td>Version</td>
          <td>{{ info.version }}</td>
        </tr>
         <tr>
          <td>Commit</td>
          <td>{{ info.commit }}</td>
        </tr>
          <tr>
          <td>Kafka Cluster ID</td>
          <td>{{ info.kafka_cluster_id }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      info: null,
      errors: null
    }
  },

  // Fetches posts when the component is created.
  created() {
    axios.get(`http://localhost:8083`)
    .then(response => {
      // JSON responses are automatically parsed.
      this.info = response.data
    })
    .catch(e => {
      this.errors.push(e)
    })
  }
}
</script>