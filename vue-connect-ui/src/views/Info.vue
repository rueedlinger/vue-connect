<template>
  <div>
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
      <article class="message is-danger" v-if="errors">
        <div class="message-header">
          <p>Error</p>
        </div>
        <div class="message-body">
          {{ errors }}
        </div>
      </article>

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

      <h2>Cluster Info</h2>

      <table class="table is-hoverable">
        <thead>
          <tr>
            <th></th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>Connect worker version</td>
            <td>{{ cluster_info.version }}</td>
          </tr>
          <tr>
            <td>Connect git commit ID</td>
            <td>{{ cluster_info.commit }}</td>
          </tr>
          <tr>
            <td>Kafka cluster ID</td>
            <td>{{ cluster_info.kafka_cluster_id }}</td>
          </tr>
          <tr>
            <td>Connect API endpoint</td>
            <td>
              <a v-bind:href="cluster_info.endpoint">{{
                cluster_info.endpoint
              }}</a>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
import connect from "../common/connect";

export default {
  data() {
    return {
      cluster_info: {},
      app_info: {},
      errors: "",
      isLoading: "",
    };
  },

  created() {
    this.isLoading = "info";

    connect
      .getAppInfo()
      .then((response) => {
        this.app_info = response.data;
      })
      .catch(() => {
        // ignore
      });

    connect
      .getInfo()
      .then((response) => {
        this.cluster_info = response.data;
        this.isLoading = "";
      })
      .catch((e) => {
        if (e.response) {
          this.errors = e.response.data.message;
        } else {
          this.errors = { message: e.message };
        }
        this.isLoading = "";
      });
  },
  methods: {
    reload: function() {
      this.isLoading = "plugins";
      this.errors = "";
      connect
        .getInfo()
        .then((response) => {
          this.cluster_info = response.data;
          this.isLoading = "";
          this.errors = "";
        })
        .catch((e) => {
          if (e.response) {
            this.errors = e.response.data.message;
          } else {
            this.errors = { message: e.message };
          }
          this.isLoading = "";
        });
    },
  },
};
</script>
