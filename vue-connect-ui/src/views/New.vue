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
      <h2>Connector {{ connectorName }}</h2>
      <error-message :errors="errors"></error-message>

      <div v-if="configParams.length">
        <ul>
          <li>Class: {{ $route.params.id }}</li>
          <li>Type: {{ $route.params.type }}</li>
        </ul>

        <div class="field">
          <label class="label">Configuration</label>
          <div class="control">
            <textarea
              class="textarea is-small is-primary"
              placeholder=""
              v-model="jsonConfig"
            ></textarea>
          </div>
        </div>

        <div class="control">
          <button
            class="button is-primary is-small"
            v-on:click="save($route.params.cluster)"
          >
            <font-awesome-icon icon="save"></font-awesome-icon
            ><span class="pl-1">Save</span>
          </button>
        </div>
      </div>
    </div>

    <div class="box content" v-if="configParams.length">
      <h2>Configuration Options for {{ connectorName }}</h2>
      <table class="table is-hoverable is-size-7">
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
  </div>
</template>

<script>
import connect from "../common/connect";
import errorHandler from "../common/error";
import ErrorMessage from "../components/ErrorMessage.vue";

function loadData() {
  this.isLoading = "new";
  this.errors = [];

  let parts = this.$route.params.id.split(".");
  let clusterId = this.$route.params.cluster;

  let name = parts[parts.length - 1];
  this.connectorName = name;

  let data = {
    "connector.class": this.$route.params.id,
    "tasks.max": 1,
    name: name,
  };

  if (this.$route.params.type == "sink") {
    data["topics"] =
      "topic" +
      name.replace(/([A-Z])/g, function(g) {
        return "-" + g[0].toLowerCase();
      });
  }

  connect
    .validateConfig(clusterId, name, data)
    .then((resp) => {
      let configs = resp.data.configs;

      configs.forEach((entry) => {
        if (entry.value.errors.length > 0) {
          data[entry.value.name] = "";
        }
        this.configParams.push({
          name: entry.definition.name,
          default_value: entry.definition.default_value,
          type: entry.definition.type,
          required: entry.definition.required,
          documentation: entry.definition.documentation,
        });
      });
      this.isLoading = "";
      this.jsonConfig = JSON.stringify(data, null, 2);
    })
    .catch((e) => {
      this.isLoading = "";
      this.errors.push(errorHandler.transform(e));
    });
}

export default {
  components: { ErrorMessage },
  data() {
    return {
      connectorName: "",
      configParams: [],
      jsonConfig: "",
      errors: [],
      isLoading: "",
    };
  },

  created() {
    loadData.bind(this)();
  },

  methods: {
    save: function(clusterId) {
      this.errors = [];
      try {
        let data = JSON.parse(this.jsonConfig);
        connect
          .newConnector(clusterId, data)
          .then(() => {
            this.$router.push("/");
          })
          .catch((e) => {
            this.errors.push(errorHandler.transform(e));
          });
      } catch (error) {
        this.errors.push(errorHandler.transform(error));
      }
    },
    reload: function() {
      loadData.bind(this)();
    },
  },
};
</script>
