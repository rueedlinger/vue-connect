<template>
  <div>
    <h1>{{$route.name}}</h1>
    <blockquote v-if="data.length == 0">
        <p><em>There are no connectors running...</em></p>
    </blockquote>

    

    <table class="u-full-width" v-if="data.length > 0">
      <thead>
        <tr>
          <th>State</th>
          <th>Name / Type</th>
          <th>Operation</th>
          <th>Worker ID</th>
          <th>Task</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="item in data" :key="item.name">
          <td v-bind:class="item.connector.state">{{ item.connector.state }}</td>
          <td>
           <a v-bind:href="'/detail/' + item.name">{{ item.name }}</a> ({{ item.type }})
          </td>
          <td class="operation"><a v-bind:href="'/detail/' + item.name"><font-awesome-icon icon="info-circle"></font-awesome-icon></a> <a v-on:click="resume(item.name)"> <font-awesome-icon icon="play-circle"></font-awesome-icon> </a> <a v-on:click="pause(item.name)"> <font-awesome-icon icon="pause-circle"></font-awesome-icon></a> <a v-on:click="restart(item.name)"><font-awesome-icon icon="retweet"></font-awesome-icon></a>
          </td>
          <td>{{ item.connector.worker_id }}</td>
          <td>
            <table class="u-full-width">
              <thead>
                <tr>
                  <th>Task State</th>
                  <th>Id</th>
                  <th>Task Worker ID</th>
                  <th>Operation</th>
                </tr>
              </thead>
               <tbody>
                 <tr v-for="task in item.tasks" v-bind:key="task.id">
                  <td v-bind:class="task.state">{{ task.state }}</td>
                  <td>{{ task.id }}</td>
                  <td>{{ task.worker_id }}</td>
                  <td class="operation"><a v-on:click="restartTask(item.name, task.id)"><font-awesome-icon icon="retweet"></font-awesome-icon></a></td>
                 </tr>
               </tbody>
            </table>
          </td>
         
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import connect from '../common/connect'

export default {
  data() {
    return {
      data: [],
      errors: []
    }
  },

  

  // Fetches posts when the component is created.
  created() {
    this.loadData()
  },

  methods: {
    loadData: function() {
      connect.getAllConnectorStatus()
      .then(response => {
        this.data = response.data
      })
      .catch(e => {
        this.errors.push(e)
      })
    },
    restart: function (id) {
      connect.restartConnector(id)
      .then(resp => {
        this.data = resp.data
      })
     .catch(e => {
        this.errors.push(e)
      })
    },
    pause: function (id) {
      connect.pauseConnector(id)
      .then(resp => {
        this.data = resp.data
      })
      .catch(e => {
        this.errors.push(e)
      })
    },
    resume: function (id) {
      connect.resumeConnector(id)
      .then(resp => {
        this.data = resp.data
      })
      .catch(e => {
        this.errors.push(e)
      })
    },
    restartTask: function (id, task_id) {
      connect.restartTask(id, task_id)
      .then(resp => {
        this.data = resp.data
      })
      .catch(e => {
        this.errors.push(e)
      })
    }
  }
}
</script>