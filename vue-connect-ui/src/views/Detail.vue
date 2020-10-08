<template>
  <div>
   <h1><font-awesome-icon icon="info-circle"></font-awesome-icon> {{$route.name}}</h1>
    <h2>Connector {{ status.name }}</h2>

    <div class="pure-g" v-if="errors">
        <div class="pure-u-5-5 error">{{errors}}</div>
      </div>

      <ul>
        <li>Type: {{ status.type }}</li>
        <li>Worker Id: {{ status.connector.worker_id }}</li>
        <li>State: {{ status.connector.state }}</li>
      </ul>

      <pre>{{ config }}</pre>

      
      <div class="error">
      {{ status.connector.trace }}
      </div>
      

    <div v-for="task in status.tasks" :key="task.id">
      <h2>Task {{ task.id }}</h2>
      <ul>
        <li>Worker Id: {{ task.worker_id }}</li>
        <li>State: {{ task.state }}</li>
      </ul>
       <div class="error">
      {{ task.trace }}
      </div>
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
    }).catch(e => {
      this.errors.push(e)
    })
  }
}
</script>