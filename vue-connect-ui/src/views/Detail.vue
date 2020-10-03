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
        <!--
         <tr>
          <td>Topics</td>
          <td>{{ topics }}</td>
        </tr>
        -->
        <tr>
          <td>Worker Id</td>
          <td>{{ status.connector.worker_id }}</td>
        </tr>
         <tr>
          <td>State</td>
          <td>{{ status.connector.state }}</td>
        </tr>
         <tr>
          <td>Config</td>
          <td><pre>{{ config }}</pre></td>
        </tr>
         <tr>
          <td></td>
          <td><a class="button" v-on:click="editConnector($route.params.id)">Edit</a> <a class="button" v-on:click="deleteConnector($route.params.id)">Delete</a></td>
        </tr>
        <tr v-if="status.connector.trace">
          <td>Trace</td>
          <td><pre>{{ status.connector.trace }}</pre></td>
        </tr>
      </tbody>
    </table>


    <div v-for="task in status.tasks" :key="task.id">
      <h2>Task ({{ task.id }})</h2>
      <table class="u-full-width" v-if="status.tasks">
      <thead>
        <tr>
          <th>Key</th>
          <th>Value</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td>Id</td>
          <td>{{task.id}}</td>
        </tr>
        <tr>
          <td>Worker Id</td>
          <td>{{task.worker_id}}</td>
        </tr>
         <tr>
          <td>State</td>
          <td>{{task.state}}</td>
        </tr>
        <tr v-if="task.trace">
          <td>Trace</td>
          <td><pre>{{ task.trace }}</pre></td>
        </tr>
      </tbody>
      </table>
    </div>



    

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
      topics: [],
      errors: []
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
    }).catch(e => {
      this.errors.push(e)
    })
  },
  
  methods: {
    editConnector: function (id) {
      this.$router.push({path: '/edit/' + id })
    },
    deleteConnector: function (id) {
      connect.deleteConnector(id)
      .then(() => {
        this.$router.push('/')
      })
     .catch(e => {
        this.errors.push(e)
      })
    }
  }
}
</script>