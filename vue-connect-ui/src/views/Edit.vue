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
            <v-jsoneditor
              v-model="config"
              :options="options"
              height="400px"
            ></v-jsoneditor>
          </div>
        </div>

        <div class="control">
          <button
            :disabled="isSaveDisabled"
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
import vJsoneditor from "v-jsoneditor";

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
      this.isLoading = "";
    })
    .catch((e) => {
      this.errors.push(errorHandler.transform(e));
      this.isLoading = "";
    });
}

export default {
  components: { ErrorMessage, KeyValueList, TitleHeader, vJsoneditor },
  data() {
    return {
      status: {},
      config: {},
      errors: [],
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

  // Fetches posts when the component is created.
  created() {
    loadData.bind(this)();
  },

  methods: {
    save: function(clusterId, id) {
      connect
        .updateConnector(clusterId, id, this.config)
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
