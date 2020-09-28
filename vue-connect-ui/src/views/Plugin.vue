<template>
  <div>
    <h1>{{$route.name}}</h1>
    <table class="u-full-width" v-if="data">
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
          <td><a class="button" href="#">New connector</a></td>
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
      data: [],
      errors: []
    }
  },

  // Fetches posts when the component is created.
  created() {
    axios.get('http://localhost:5000/api/plugins')
    .then(response => {
      // JSON responses are automatically parsed.
      this.data = response.data
    })
    .catch(e => {
      this.errors.push(e)
    })
  }
}
</script>