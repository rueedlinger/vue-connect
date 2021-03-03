<template>
  <div>
    <div class="box notification is-primary">
      <div class="columns">
        <div class="column is-1">
          <p class="title">
            {{ $route.name }}
          </p>
        </div>
        <div class="column is-8 is-offset-1"></div>
        <div class="column is-1 is-offset-1">
          <button
            v-on:click="reload()"
            v-bind:class="[isLoading != `` ? `is-loading` : ``]"
            class="button"
          >
            <font-awesome-icon icon="sync-alt"></font-awesome-icon>
          </button>
        </div>
      </div>
    </div>

    <div class="box content">
      <error-message :errors="errors"></error-message>
      <h2>Plugins</h2>

      <div v-for="cluster in data" :key="cluster.id">
        <h4>Cluster {{ cluster.name }} ({{ cluster.url }})</h4>

        <ul>
          <li><b>Cluster ID:</b> {{ cluster.id }}</li>
          <li v-if="cluster.name"><b>Cluster Name:</b> {{ cluster.name }}</li>
          <li v-if="cluster.plugins">
            <b>Total Plugins:</b> {{ cluster.plugins.length }}
          </li>
          <li><b>Endpoint:</b> {{ cluster.url }}</li>
        </ul>

        <div class="message is-danger" v-if="cluster.error">
          <div class="message-header">
            <p>Error</p>
          </div>
          <div class="message-body">
            {{ cluster.error }}
          </div>
        </div>

        <table v-if="cluster.plugins" class="table is-hoverable">
          <thead>
            <tr>
              <th></th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="plugin in cluster.plugins" :key="plugin.class">
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
                  v-on:click="
                    newConnector(cluster.id, plugin.class, plugin.type)
                  "
                  ><font-awesome-icon icon="plus-circle"></font-awesome-icon
                  ><span class="pl-1">New connector</span></a
                >
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>
<script>
import connect from "../common/connect";
import errorHandler from "../common/error";
import ErrorMessage from "../components/ErrorMessage.vue";

function loadData() {
  this.isLoading = "plugins";
  this.errors = [];
  connect
    .getPlugins()
    .then((response) => {
      this.data = response.data;
      this.isLoading = "";
    })
    .catch((e) => {
      this.errors.push(errorHandler.transform(e));
      this.isLoading = "";
    });
}

export default {
  components: { ErrorMessage },
  data() {
    return {
      data: [],
      errors: [],
      isLoading: "",
    };
  },

  created() {
    loadData.bind(this)();
  },

  methods: {
    newConnector: function(clusterId, pluginClass, pluginType) {
      this.$router.push(
        "/new/" + clusterId + "/" + pluginClass + "/" + pluginType
      );
    },
    reload: function() {
      loadData.bind(this)();
    },
  },
};
</script>
