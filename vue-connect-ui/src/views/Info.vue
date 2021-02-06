<template>
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
</template>

<script>
import connect from "../common/connect";

export default {
  data() {
    return {
      data: [],
      meta: {},
      errors: "",
    };
  },

  // Fetches posts when the component is created.
  created() {
    connect
      .getInfo()
      .then((response) => {
        // JSON responses are automatically parsed.
        this.data = response.data;
      })
      .catch((e) => {
        if (e.response) {
          this.errors = e.response.data.message;
          this.data = e.response.data.cache;
        } else {
          this.errors = { message: e.message };
        }
      });
  },
};
</script>
