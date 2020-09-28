<template>
  <div>
    <h1>{{$route.name}}</h1>
    <h2>Conector {{ status.name}}</h2>
    
    <table v-if="status.connector">
      <thead>
        <tr>
          <th>Key</th>
          <th>Value</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td>Name</td>
          <td>{{ status.name}}</td>
        </tr>
        <tr>
          <td>Type</td>
          <td>{{ status.type }}</td>
        </tr>
         <tr>
          <td>Config</td>
          <td><pre>{{ config }}</pre></td>
        </tr>
         <tr>
          <td></td>
          <td><a class="button" v-on:click="editConnector($route.params.id)">Edit</a></td>
        </tr>
        <tr v-if="status.connector.trace">
          <td>Trace</td>
          <td><pre>{{ status.connector.trace }}</pre></td>
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
      status: [],
      config: [],
      errors: []
    }
  },

  // Fetches posts when the component is created.
  created() {
    axios.all([
      axios.get('http://localhost:5000/api/status/' + this.$route.params.id),
      axios.get('http://localhost:5000/api/config/' + this.$route.params.id)])
    .then(respAll => {
      this.status = respAll[0].data
      this.config = respAll[1].data
    }).catch(e => {
      console.log(e)
      this.errors.push(e)
    })
  },
  
  methods: {
    editConnector: function (id) {
      this.$router.push({path: '/edit/' + id })
    },
    deleteConnector: function (id) {
      axios.post('http://localhost:5000/api/connectors/' + id + '/delete')
      .then(() => {
        this.$router.push('/')
      })
     .catch(e => {
        console.log(e)
        this.errors.push(e)
      })
    }
  }
}
</script>