<template>
  <div>
    <h1>{{$route.name}}</h1>
    <h2>Conector {{ connectorName }}</h2>
    
    <table>
      <thead>
        <tr>
          <th>Key</th>
          <th>Value</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td>Class</td>
          <td>{{$route.params.id}}</td>
        </tr>
        <tr>
          <td>Type</td>
          <td>{{$route.params.type}}</td>
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

  <h3>Configuration Options</h3>
  <table>
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

  </div>
</template>

<script>
import axios from 'axios';

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
    axios.post('http://localhost:5000/api/plugins/' + name + '/config/validate', data)
    .then(resp => {
      let configs = resp.data.configs
      console.log(configs)
      
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

      //console.log(data)
      this.jsonConfig = JSON.stringify(data, null, 2)

    }).catch(error => {
      //console.log(error)
      this.errors = error.response.data
    })
  },
  
  methods: {
    save: function () {
      
      try {
          let data = JSON.parse(this.jsonConfig)
           axios.post('http://localhost:5000/api/connectors/', data)
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