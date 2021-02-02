<template>
  <div class="content box">
    <h2>Conector {{ status.name }}</h2>
    <ul>
      <li>Class: {{config['connector.class']}}</li>
      <li>Type: {{status.type}}</li>
    </ul>

    <article class="message is-danger" v-if="errors">
    <div class="message-header">
      <p>Error</p>
     </div>
    <div class="message-body">
      {{errors}}
    </div>
    </article>

    <div class="field">
      <label class="label">Configuration</label>
      <div class="control">
        <textarea class="textarea is-small is-primary" placeholder="" v-model="jsonConfig"></textarea>
      </div>
    </div>

    <div class="control">
      <button class="button is-primary is-small" v-on:click="save($route.params.id)"><font-awesome-icon icon="edit"></font-awesome-icon><span class="pl-1">Save</span></button>
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
       if(e.response) {
            this.errors = e.response.data.message
        } else {
            this.errors = {'message': e.message}
        }
    })
  },
  
  methods: {
    save: function (id) {
      
      try {
          let data = JSON.parse(this.jsonConfig)
            connect.updateConnector(id, data)
            .then(() => {
              this.$router.push('/')
            })
          .catch(e => {
              if(e.response) {
                  this.errors = e.response.data.message
              } else {
                  this.errors = {'message': e.message}
              }
            })
      } catch(e) {
        this.errors = e
      }
    }
  }
}
</script>