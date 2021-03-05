<template>
  <div>
    <title-header
      :isLoading="isLoading"
      :title="$route.name"
      :reloadData="reload"
    ></title-header>

    <div class="box content">
      <h2>Conector {{ $route.params.id }}</h2>
      <error-message :errors="errors"></error-message>

      <div v-if="config.name">
        <key-value-list
          :keys="['Class', 'Type']"
          :values="[status.type, config['connector.class']]"
        ></key-value-list>

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
            v-on:click="save($route.params.cluster, $route.params.id)"
          >
            <font-awesome-icon icon="edit"></font-awesome-icon
            ><span class="pl-1">Save</span>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import connect from "../common/connect";
import errorHandler from "../common/error";
import axios from "axios";
import TitleHeader from "../components/TitleHeader.vue";
import ErrorMessage from "../components/ErrorMessage.vue";
import KeyValueList from "../components/KeyValueList.vue";

function loadData() {
  this.isLoading = "edit";
  this.errors = [];
  axios
    .all([
      connect.getConnectorStatus(
        this.$route.params.cluster,
        this.$route.params.id
      ),
      connect.getConnectorConfig(
        this.$route.params.cluster,
        this.$route.params.id
      ),
    ])
    .then((respAll) => {
      this.status = respAll[0].data;
      this.config = respAll[1].data;
      this.jsonConfig = JSON.stringify(respAll[1].data, null, 2);
      this.isLoading = "";
    })
    .catch((e) => {
      this.errors.push(errorHandler.transform(e));
      this.isLoading = "";
    });
}

export default {
  components: { ErrorMessage, KeyValueList, TitleHeader },
  data() {
    return {
      status: {},
      config: {},
      jsonConfig: "",
      errors: [],
      isLoading: "",
    };
  },

  // Fetches posts when the component is created.
  created() {
    loadData.bind(this)();
  },

  methods: {
    save: function(clusterId, id) {
      try {
        let data = JSON.parse(this.jsonConfig);
        connect
          .updateConnector(clusterId, id, data)
          .then(() => {
            this.$router.push("/");
          })
          .catch((e) => {
            this.errors.push(errorHandler.transform(e));
          });
      } catch (e) {
        this.errors.push(errorHandler.transform(e));
      }
    },
    reload: function() {
      loadData.bind(this)();
    },
  },
};
</script>
