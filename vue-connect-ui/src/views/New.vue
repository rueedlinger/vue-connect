<template>
  <div>
    <h1>{{$route.name}}</h1>
    <h2>Conector {{ connectorName }}</h2>
    <ul>
      <li>Class: {{$route.params.id}}</li>
      <li>Type: {{$route.params.type}}</li>
    </ul>

    <div class="pure-g" v-if="errors">
      <div class="pure-u-5-5 error">{{errors}}</div>

    </div>
    

    <form class="pure-form pure-form-stacked">
      <fieldset>
        <textarea class="pure-input-1" v-model="jsonConfig"></textarea>
        <a class="pure-button pure-button-primary" v-on:click="save()"><font-awesome-icon icon="save"></font-awesome-icon> Save</a>
      </fieldset>
    </form>

<!--   

  <h2>Configuration Options for {{ connectorName }}</h2>
  <table class="pure-table pure-table-bordered">
    <thead>
      <tr>
        <th>Name</th>
        <th>Type</th>
        <th>Required</th>
        <th>Default Value</th>
        <th>Documentaion</th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="cfg in configParams" :key="cfg.name">
        <td>{{ cfg.name }}</td>
        <td>{{ cfg.type }}</td>
        <td>{{ cfg.required }}</td>
        <td>{{ cfg.default_value }}</td>
        <td>{{ cfg.documentation }}</td>
      </tr>
  </tbody>
</table>

-->

  </div>
</template>

<script>
import connect from '../common/connect'

export default {
  data() {
    return {
      connectorName: "",
      configParams: [],
      jsonConfig: "",
      errors: ""
    }
  },

  // Fetches posts when the component is created.
  created() {

    let parts = this.$route.params.id.split(".")
    let name = parts[parts.length-1]
    this.connectorName = name

    let data = {'connector.class': this.$route.params.id, 'tasks.max': 1, 'name': name}

    if(this.$route.params.type == 'sink') {
      data['topics'] = 'topic' + name.replace(/([A-Z])/g, function (g) { return '-' + g[0].toLowerCase() })
    }

    let self = this
    connect.validateConfig(name, data)
    .then(resp => {
      let configs = resp.data.configs
      
      configs.forEach(function(entry) {
        if(entry.value.errors.length > 0) {
          //console.log(entry.value)
          data[entry.value.name] = ''
        }
        self.configParams.push({
          'name': entry.definition.name,
          'default_value': entry.definition.default_value,
          'type': entry.definition.type,
          'required': entry.definition.required,
          'documentation': entry.definition.documentation
        })
      })

      this.jsonConfig = JSON.stringify(data, null, 2)

    }).catch(error => {
      this.errors = error.response.data
    })
  },
  
  methods: {
    save: function () {
      
      try {
          
          let data = JSON.parse(this.jsonConfig)
          connect.newConnector(data)
          .then(() => {
            this.$router.push('/')
          })
          .catch(error => {
            this.errors = error.response.data.message
          })
      } catch(error) {
        this.errors = error
      }
    }
  }
}
</script>