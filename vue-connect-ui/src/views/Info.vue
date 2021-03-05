<template>
  <div>
    <title-header
      :isLoading="isLoading"
      :title="$route.name"
      :reloadData="reload"
    ></title-header>

    <div class="box content">
      <error-message :errors="errors"></error-message>

      <h2>Application Info</h2>
      <table class="table is-hoverable">
        <thead>
          <tr>
            <th></th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>Version</td>
            <td>{{ app_info.vc_version }}</td>
          </tr>
          <tr>
            <td>Build time</td>
            <td>{{ app_info.build_time }}</td>
          </tr>
          <tr>
            <td>GIT SHA</td>
            <td>{{ app_info.sha }}</td>
          </tr>
        </tbody>
      </table>
    </div>

    <div
      v-for="cluster in cluster_info"
      v-bind:key="cluster.id"
      class="box content"
    >
      <h2 v-if="cluster.name">{{ cluster.name }}</h2>
      <h2 v-else>
        {{ cluster.url }}
      </h2>
      <div class="message is-danger" v-if="cluster.error">
        <div class="message-header">
          <p>Error</p>
        </div>
        <div class="message-body">
          {{ cluster.error }}
        </div>
      </div>

      <table class="table is-hoverable">
        <thead>
          <tr>
            <th></th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>ID</td>
            <td>{{ cluster.id }}</td>
          </tr>
          <tr v-if="cluster.name">
            <td>Name</td>
            <td>{{ cluster.name }}</td>
          </tr>
          <tr v-if="cluster.info">
            <td>Connect worker version</td>
            <td>{{ cluster.info.version }}</td>
          </tr>
          <tr v-if="cluster.info">
            <td>Connect git commit ID</td>
            <td>{{ cluster.info.commit }}</td>
          </tr>
          <tr v-if="cluster.info">
            <td>Kafka cluster ID</td>
            <td>{{ cluster.info.kafka_cluster_id }}</td>
          </tr>
          <tr>
            <td>Connect API endpoint</td>
            <td>
              <a v-bind:href="cluster.url">{{ cluster.url }}</a>
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
import TitleHeader from "../components/TitleHeader";
import ErrorMessage from "../components/ErrorMessage";
import axios from "axios";

function loadData() {
  this.isLoading = "info";
  this.errors = [];

  axios
    .all([connect.getAppInfo(), connect.getInfo()])
    .then((respAll) => {
      this.app_info = respAll[0].data;
      this.cluster_info = respAll[1].data;
      this.isLoading = "";
    })
    .catch((e) => {
      this.errors.push(errorHandler.transform(e));
      this.isLoading = "";
    });
}

export default {
  components: { ErrorMessage, TitleHeader },
  data() {
    return {
      cluster_info: {},
      app_info: {},
      errors: [],
      isLoading: "",
    };
  },

  created() {
    loadData.bind(this)();
  },
  methods: {
    reload: function() {
      loadData.bind(this)();
    },
  },
};
</script>
