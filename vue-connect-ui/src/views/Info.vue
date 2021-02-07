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

    <div class="box">
      <article class="message is-danger" v-if="errors">
        <div class="message-header">
          <p>Error</p>
        </div>
        <div class="message-body">
          {{ errors }}
        </div>
      </article>

      <table class="table is-hoverable" v-if="data">
        <thead>
          <tr>
            <th></th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>Version</td>
            <td>{{ data.vc_version }}</td>
          </tr>
          <tr>
            <td>Connect worker version</td>
            <td>{{ data.version }}</td>
          </tr>
          <tr>
            <td>Connect git commit ID</td>
            <td>{{ data.commit }}</td>
          </tr>
          <tr>
            <td>Kafka cluster ID</td>
            <td>{{ data.kafka_cluster_id }}</td>
          </tr>
          <tr>
            <td>Connect API endpoint</td>
            <td>
              <a v-bind:href="data.endpoint">{{ data.endpoint }}</a>
            </td>
          </tr>
          <tr>
            <td>Build time</td>
            <td>{{ data.build_time }}</td>
          </tr>
          <tr>
            <td>GIT SHA</td>
            <td>{{ data.sha }}</td>
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
      data: [],
      meta: {},
      errors: "",
      isLoading: "",
    };
  },

  created() {
    this.isLoading = "info";
    connect
      .getInfo()
      .then((response) => {
        this.data = response.data;
        this.isLoading = "";
      })
      .catch((e) => {
        if (e.response) {
          this.errors = e.response.data.message;
          this.data = e.response.data.cache;
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
          this.data = response.data;
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
