<template>
  <div class="box">
    <article class="message is-danger" v-if="errors">
      <div class="message-header">
        <p>Error</p>
      </div>
      <div class="message-body">
        {{ errors }}
      </div>
    </article>

    <table v-if="data.length > 0" class="table is-hoverable">
      <thead>
        <tr>
          <th></th>
          <th></th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="plugin in data" :key="plugin.class">
          <td>
            <b>{{ plugin.name }}</b>
            <ul>
              <li>Class: {{ plugin.class }}</li>
              <li>Type: {{ plugin.type }}</li>
              <li>Version: {{ plugin.version }}</li>
            </ul>
          </td>
          <td>
            <a
              class="button is-primary is-small"
              v-on:click="newConnector(plugin.class, plugin.type)"
              ><font-awesome-icon icon="plus-circle"></font-awesome-icon
              ><span class="pl-1">New connector</span></a
            >
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>
<script>
import connect from "../common/connect";

export default {
  data() {
    return {
      data: [],
      errors: "",
    };
  },

  // Fetches posts when the component is created.
  created() {
    connect
      .getPlugins()
      .then((response) => {
        // JSON responses are automatically parsed.
        this.data = response.data;
      })
      .catch((e) => {
        if (e.response) {
          this.errors = e.response.data.message;
        } else {
          this.errors = { message: e.message };
        }
      });
  },

  methods: {
    newConnector: function(pluginClass, pluginType) {
      this.$router.push("/new/" + pluginClass + "/" + pluginType);
    },
  },
};
</script>
