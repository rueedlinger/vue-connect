<template>
  <div>
    <h1>{{ $route.params.id }}</h1>

      <h4>Configuration</h4>

      <a class="button" v-on:click="editConnector($route.params.id)">Edit</a> <a class="button" v-on:click="deleteConnector($route.params.id)">Delete</a>

      <pre v-if="config">{{ config }}</pre>

      

      <h4>Connector Type: {{ status.type }}</h4>


      <table class="u-full-width" v-if="status.connector">
      <thead>
        <tr>
          <th>State</th>
          <th>Worker ID</th>
          <th>Trace</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td v-bind:class="status.connector.state">{{ status.connector.state }}</td>
          <td>{{ status.connector.worker_id }}</td>
          <td><pre class="trace">{{ status.connector.trace }}</pre></td>
        </tr>
      </tbody>
    </table>

    <div v-for="task in status.tasks" :key="task.id">
      <h4>Task Id: {{ task.id }}</h4>
      <table class="u-full-width" v-if="status.tasks">
      <thead>
        <tr>
          <th>State</th>
          <th>Worker ID</th>
          <th>Trace</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td v-bind:class="task.state">{{task.state}}</td>
          <td>{{task.worker_id}}</td>
          <td><pre class="trace">{{task.trace}}</pre></td>
        </tr>
      </tbody>
      </table>
    </div>



    

  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      status: [
        {
          connector: [],
          tasks: []
        }
      ],
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