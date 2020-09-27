<template>
  <div>
    <h1>Plugins</h1>
    <table class="u-full-width" v-if="plugins">
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
        <tr v-for="item in plugins" :key="item.class">
          <td>-</td>
          <td>{{ item.class }}</td>
          <td>{{ item.type }}</td>
          <td>{{ item.version }}</td>
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
      plugins: null,
      errors: null
    }
  },

  // Fetches posts when the component is created.
  created() {
    axios.get(`http://localhost:8083/connector-plugins`)
    .then(response => {
      // JSON responses are automatically parsed.
      this.plugins = response.data
    })
    .catch(e => {
      this.errors.push(e)
    })
  }
}
</script>