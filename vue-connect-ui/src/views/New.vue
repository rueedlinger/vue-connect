<template>
  <div>
    <title-header
      :isLoading="isLoading"
      :title="$route.name"
      :reloadData="reload"
    ></title-header>

    <div class="box content">
      <h2>Connector {{ connectorName }}</h2>
      <error-message :errors="errors"></error-message>

      <div v-if="configParams.length">
        <key-value-list
          :keys="['Class', 'Type', 'Cluster']"
          :values="[
            $route.params.id,
            $route.params.type,
            $route.params.cluster,
          ]"
        ></key-value-list>

        <div class="field">
          <label class="label">Configuration</label>
          <div class="control">
            <v-jsoneditor
              v-model="jsonConfig"
              :options="options"
              height="400px"
            ></v-jsoneditor>
          </div>
        </div>

        <div class="control">
          <button
            :disabled="isSaveDisabled"
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
          <tr v-for="(cfg, index) in configParams" :key="index">
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
import TitleHeader from "../components/TitleHeader.vue";
import ErrorMessage from "../components/ErrorMessage.vue";
import KeyValueList from "../components/KeyValueList.vue";
import vJsoneditor from "v-jsoneditor";

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
      this.jsonConfig = data;
    })
    .catch((e) => {
      this.isLoading = "";
      this.errors.push(errorHandler.transform(e));
    });
}

export default {
  components: { ErrorMessage, KeyValueList, TitleHeader, vJsoneditor },
  data() {
    return {
      connectorName: "",
      configParams: [],
      errors: [],
      jsonConfig: {},
      isLoading: "",
      isSaveDisabled: false,
      options: {
        mode: "code",
        mainMenuBar: false,
        onChangeText: (data) => {
          try {
            // validate json
            JSON.parse(data);
            this.errors = [];
            this.isSaveDisabled = false;
          } catch (e) {
            this.errors = [errorHandler.transform(e)];
            this.isSaveDisabled = true;
          }
        },
      },
    };
  },

  created() {
    loadData.bind(this)();
  },

  methods: {
    save: function(clusterId) {
      connect
        .newConnector(clusterId, this.jsonConfig)
        .then(() => {
          this.$router.push("/");
        })
        .catch((e) => {
          this.errors = [errorHandler.transform(e)];
        });
    },
    reload: function() {
      loadData.bind(this)();
    },
  },
};
</script>
