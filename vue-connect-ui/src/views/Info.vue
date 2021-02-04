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
          <td>Connect endpoint</td>
          <td>
            <a v-bind:href="data.endpoint">{{ data.endpoint }}</a>
          </td>
        </tr>
        <tr>
          <td>vue-connect version</td>
          <td>{{ meta.version }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import connect from "../common/connect";
import meta from "../../package.json";

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
    this.meta = meta;
    connect
      .getInfo()
      .then((response) => {
        // JSON responses are automatically parsed.
        this.data = response.data;
      })
      .catch((e) => {
        if (e.response) {
          this.errors = e.response.data.message;
        } else {
          this.errors = { message: e.message };
        }
      });
  },
};
</script>
