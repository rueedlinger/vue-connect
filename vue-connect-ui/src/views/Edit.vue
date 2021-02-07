<template>
  <div class="">
    <div class="box">
      <button
        v-on:click="reload()"
        v-bind:class="[isLoading != `` ? `is-loading` : ``]"
        class="button"
      >
        <font-awesome-icon icon="sync-alt"></font-awesome-icon>
      </button>
    </div>

    <div class="box content">
      <error-message :error="errors"></error-message>

      <div v-if="config.name">
        <h2>Conector {{ status.name }}</h2>
        <ul>
          <li>Class: {{ config["connector.class"] }}</li>
          <li>Type: {{ status.type }}</li>
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
            v-on:click="save($route.params.id)"
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
import ErrorMessage from "../components/ErrorMessage.vue";

function loadData() {
  this.isLoading = "edit";
  axios
    .all([
      connect.getConnectorStatus(this.$route.params.id),
      connect.getConnectorConfig(this.$route.params.id),
    ])
    .then((respAll) => {
      this.status = respAll[0].data;
      this.config = respAll[1].data;
      this.jsonConfig = JSON.stringify(respAll[1].data, null, 2);
      this.isLoading = "";
    })
    .catch((e) => {
      this.errors = errorHandler.transform(e);
      this.isLoading = "";
    });
}

export default {
  components: { ErrorMessage },
  data() {
    return {
      status: [],
      config: [],
      jsonConfig: "",
      errors: null,
      isLoading: "",
    };
  },

  // Fetches posts when the component is created.
  created() {
    loadData.bind(this)();
  },

  methods: {
    save: function(id) {
      try {
        let data = JSON.parse(this.jsonConfig);
        connect
          .updateConnector(id, data)
          .then(() => {
            this.$router.push("/");
          })
          .catch((e) => {
            this.errors = errorHandler.transform(e);
          });
      } catch (e) {
        this.errors = errorHandler.transform(e);
      }
    },
    reload: function() {
      loadData.bind(this)();
    },
  },
};
</script>
