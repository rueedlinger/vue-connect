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

      <table class="table is-hoverable">
        <thead>
          <tr>
            <th>Cluster ID</th>
            <th>Name</th>
            <th>URL</th>
            <th>Installed Plugins</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="cluster in data" :key="cluster.id">
            <td>
              <a v-bind:href="'#plugins-' + cluster.id">{{ cluster.id }}</a>
            </td>
            <td>
              <a v-bind:href="'#plugins-' + cluster.id">{{ cluster.name }}</a>
            </td>
            <td>{{ cluster.url }}</td>
            <td>{{ cluster.plugins.length }}</td>
          </tr>
        </tbody>
      </table>
    </div>

    <div
      v-for="cluster in data"
      :key="cluster.id"
      class="box content"
      v-bind:id="'plugins-' + cluster.id"
    >
      <h2 v-if="cluster.name">Installed Plugins {{ cluster.name }}</h2>
      <h2 v-else>Installed Plugins {{ cluster.url }}</h2>

      <table class="table is-hoverable">
        <thead>
          <tr>
            <th>Name</th>
            <th>Type</th>
            <th>Version</th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="plugin in cluster.plugins" :key="plugin.class">
            <td>
              {{ plugin.name }}
            </td>
            <td>{{ plugin.type }}</td>
            <td>{{ plugin.version }}</td>
            <td>
              <a
                class="button is-primary is-small has-tooltip-left"
                v-bind:data-tooltip="plugin.class"
                v-on:click="newConnector(cluster.id, plugin.class, plugin.type)"
                ><font-awesome-icon icon="plus-circle"></font-awesome-icon
              ></a>
            </td>
          </tr>
        </tbody>
      </table>
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
