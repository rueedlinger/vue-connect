<template>
  <div>
    <h1><font-awesome-icon icon="cogs"></font-awesome-icon> {{$route.name}}</h1>
    <blockquote v-if="data.length == 0">
        <p><em>There are no connectors running...</em></p>
    </blockquote>

    

    <table v-if="data.length > 0" class="pure-table pure-table-bordered">
      <thead>
        <tr>
          <th>State</th>
          <th>Connector</th>
          <th>Operation</th>
          <th>Task</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="item in data" :key="item.name">
          <td v-bind:class="item.connector.state">{{ item.connector.state }}</td>
          <td>
            <ul id="detail">
              <li><b>Connector ID:</b> {{ item.name }}</li>
              <li><b>Type:</b> {{ item.type }}</li>
              <li><b>Worker ID:</b> {{ item.connector.worker_id }}</li>
            </ul>


           
          </td>
          <td>
            <table class="operation">
              <tr>
                <td><button class="pure-button pure-button-primary" v-on:click="detail(item.name)"><font-awesome-icon icon="file-alt"></font-awesome-icon></button></td>
                <td><button class="pure-button pure-button-primary" v-on:click="resume(item.name)"> <font-awesome-icon icon="play-circle"></font-awesome-icon></button></td>
                <td><button class="pure-button pure-button-primary" v-on:click="pause(item.name)"> <font-awesome-icon icon="pause-circle"></font-awesome-icon></button></td>
                <td><button class="pure-button pure-button-primary" v-on:click="restart(item.name)"><font-awesome-icon icon="retweet"></font-awesome-icon></button></td>
              </tr>
            </table>
            
               
          </td>
          <td>
            <div class="error" v-if="item.tasks.length == 0">
              <b>Error:</b> No running tasks.
            </div>
            <table class="pure-table pure-table-bordered" v-if="item.tasks.length > 0">
              <thead>
                <tr>
                  <th>State</th>
                  <th>Task</th>
                  <th>Operation</th>
                </tr>
              </thead>
               <tbody>
                 <tr v-for="task in item.tasks" v-bind:key="task.id">
                  <td v-bind:class="task.state">{{ task.state }}</td>
                  <td>
                    <ul id="detail">
                      <li><b>Task ID:</b> {{ task.id }}</li>
                      <li><b>Worker ID:</b> {{ task.worker_id }}</li>
                    </ul>
                  </td>
                  <td> 
                    <button class="pure-button pure-button-primary" v-on:click="restartTask(item.name, task.id)"><font-awesome-icon icon="retweet"></font-awesome-icon></button>
                  </td>
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
    connect.getAllConnectorStatus()
      .then(response => {
        this.data = response.data
      })
      .catch(e => {
        this.errors.push(e)
      })
  },

  methods: {
    detail: function (id) {
      this.$router.push('/detail/' + id)
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