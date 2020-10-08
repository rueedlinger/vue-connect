<template>


  <div>
   <h1><font-awesome-icon icon="layer-group"></font-awesome-icon> {{$route.name}}</h1>

    <table v-if="data" class="pure-table pure-table-bordered">
      <thead>
        <tr>
          <th>Connector</th>
          <th></th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="plugin in data" :key="plugin.class">
          <td> 
             {{ plugin.name }}
            <ul>
              <li>Class: {{ plugin.class }}</li>
              <li>Type: {{ plugin.type  }}</li>
              <li>Version: {{ plugin.version }}</li>
            </ul>

          </td>
          <td><a class="pure-button pure-button-primary" v-on:click="newConnector(plugin.class, plugin.type)"> <font-awesome-icon icon="plus-circle"></font-awesome-icon> New connector</a></td>
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
    connect.getPlugins()
    .then(response => {
      // JSON responses are automatically parsed.
      this.data = response.data
    })
    .catch(e => {
      this.errors.push(e)
    })
  },

  methods: {
    newConnector: function (pluginClass, pluginType) {
        this.$router.push('/new/' + pluginClass + '/' + pluginType)
    }
  }
}
</script>