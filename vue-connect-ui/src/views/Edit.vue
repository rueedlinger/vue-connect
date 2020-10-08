<template>
  <div>
    <h1><font-awesome-icon icon="edit"></font-awesome-icon> {{$route.name}}</h1>
    <h2>Conector {{ status.name }}</h2>
    <ul>
      <li>Class: {{config['connector.class']}}</li>
      <li>Type: {{status.type}}</li>
    </ul>

    <div class="pure-g" v-if="errors">
      <div class="pure-u-5-5 error">{{errors}}</div>
    </div>

     <form class="pure-form pure-form-stacked">
      <fieldset>
        <textarea class="pure-input-1" v-model="jsonConfig"></textarea>
        <a class="pure-button pure-button-primary" v-on:click="save($route.params.id)"><font-awesome-icon icon="edit"></font-awesome-icon> Save</a>
       </fieldset>
    </form>
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
              this.$router.push('/')
            })
          .catch(error => {
              this.errors = error.response.data.message
            })
      } catch(e) {
        this.errors = e
      }
    }
  }
}
</script>