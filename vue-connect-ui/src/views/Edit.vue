<template>
  <div>
    <h1>{{$route.name}}</h1>
    <h2>Conector {{ status.name }}</h2>
    
    <table v-if="status.connector">
      <thead>
        <tr>
          <th>Key</th>
          <th>Value</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td>Type</td>
          <td>{{ status.type }}</td>
        </tr>
         <tr>
          <td>Config</td>
          <td>
            <textarea v-model="jsonConfig"></textarea>
          </td>
        </tr>
        <tr v-if="errors">
          <td>Error</td>
          <td>
            <pre>{{errors}}</pre>
          </td>
        </tr>
         <tr>
          <td></td>
          <td><a class="button" v-on:click="save($route.params.id)">Save</a></td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import connect from '../common/connect'
import axios from 'axios'

export default {
  data() {
    return {
      status: [],
      config: [],
      jsonConfig: "",
      errors: ""
    }
  },

  // Fetches posts when the component is created.
  created() {
    axios.all([
      connect.getConnectorStatus(this.$route.params.id),
      connect.getConnectorConfig(this.$route.params.id)])
    .then(respAll => {
      this.status = respAll[0].data
      this.config = respAll[1].data
      this.jsonConfig = JSON.stringify(respAll[1].data, null, 2)
    }).catch(e => {
      this.errors.push(e)
    })
  },
  
  methods: {
    save: function (id) {
      
      try {
          let data = JSON.parse(this.jsonConfig)
            connect.updateConnector(this.$route.params.id, data)
            .then(() => {
              this.$router.push('/detail/' + id)
            })
          .catch(error => {
              this.errors = error.response.data.message
            })
      } catch(e) {
        this.errors = e
      }
    },
  }
}
</script>