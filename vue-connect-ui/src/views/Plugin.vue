<template>
  <div>
    <h1>{{$route.name}}</h1>
    <table v-if="data">
      <thead>
        <tr>
          <th>Connector</th>
          <th>Class</th>
          <th>Type</th>
          <th>Version</th>
          <th>Operation</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="plugin in data" :key="plugin.class">
          <td>{{ plugin.name }}</td>
          <td>{{ plugin.class }}</td>
          <td>{{ plugin.type }}</td>
          <td>{{ plugin.version }}</td>
          <td><a class="button" v-on:click="newConnector(plugin.class, plugin.type)">New connector</a></td>
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