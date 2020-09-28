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
          <td>Name</td>
          <td><a v-bind:href="'/detail/' + status.name">{{ status.name }}</a> </td>
        </tr>
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
import axios from 'axios';

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
      axios.get('http://localhost:5000/api/status/' + this.$route.params.id),
      axios.get('http://localhost:5000/api/config/' + this.$route.params.id)])
    .then(respAll => {
      this.status = respAll[0].data
      this.config = respAll[1].data
      this.jsonConfig = JSON.stringify(respAll[1].data, null, 2)
    }).catch(e => {
      console.log(e)
      this.errors.push(e)
    })
  },
  
  methods: {
    save: function (id) {
      
      try {
          let data = JSON.parse(this.jsonConfig)
           axios.post('http://localhost:5000/api/connectors/' + id + '/config', data)
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
    validate: function() {
      try {
        JSON.parse(this.jsonConfig)
    } catch(e) {
      this.errors.push(e)
    }
    }
  }
}
</script>