<template>
  <div>
    <h1>{{$route.name}}</h1>
    <table v-if="data">
      <thead>
        <tr>
          <th>Key</th>
          <th>Value</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td>Version</td>
          <td>{{ data.version }}</td>
        </tr>
         <tr>
          <td>Commit</td>
          <td>{{ data.commit }}</td>
        </tr>
          <tr>
          <td>Kafka cluster ID</td>
          <td>{{ data.kafka_cluster_id }}</td>
        </tr>
        <tr>
          <td>Endpoint</td>
          <td>{{ data.endpoint }}</td>
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
      data: [],
      errors: []
    }
  },

  // Fetches posts when the component is created.
  created() {
    axios.get('http://localhost:5000/api/info')
    .then(response => {
      // JSON responses are automatically parsed.
      this.data = response.data
    })
    .catch(e => {
      this.errors.push(e)
    })
  }
}
</script>