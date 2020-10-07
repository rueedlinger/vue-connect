<template>
  <div>
    <h1>{{$route.name}}</h1>
    <table class="pure-table pure-table-bordered" v-if="data">
      <thead>
        <tr>
          <th>Key</th>
          <th>Value</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td>Connect worker version</td>
          <td>{{ data.version }}</td>
        </tr>
         <tr>
          <td>Connect git commit ID</td>
          <td>{{ data.commit }}</td>
        </tr>
          <tr>
          <td>Kafka cluster ID</td>
          <td>{{ data.kafka_cluster_id }}</td>
        </tr>
        <tr>
          <td>Connect endpoint</td>
          <td>{{ data.endpoint }}</td>
        </tr>
         <tr>
          <td>vue-connect version</td>
          <td>{{ meta.version }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import connect from '../common/connect'
import meta from '../../package.json';


export default {
  data() {
    return {
      data: [],
      meta: {},
      errors: []
    }
  },

  // Fetches posts when the component is created.
  created() {
    this.meta = meta
    connect.getInfo()
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