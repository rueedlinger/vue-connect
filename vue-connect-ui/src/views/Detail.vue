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

      <div v-if="status.connector">

      <h2>Connector {{ status.name }}</h2>

      <table class="table">
        <thead>
          <tr>
            <th></th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>Type</td>
            <td>{{ status.type }}</td>
          </tr>
          <tr>
            <td>Worker ID</td>
            <td>{{ status.connector.worker_id }}</td>
          </tr>
          <tr>
            <td>State</td>
            <td>
              <span v-bind:class="status.connector.state">
                {{ status.connector.state }}
              </span>
            </td>
          </tr>
        </tbody>
      </table>

      <pre>{{ config }}</pre>

      <article class="message is-danger" v-if="status.connector.trace">
        <div class="message-header">
          <p>Error</p>
        </div>
        <div class="message-body">
          <pre>{{ status.connector.trace }}</pre>
        </div>
      </article>
    </div>

    </div>

    <div class="box content" v-for="task in status.tasks" :key="task.id">
      <h2>Task {{ task.id }}</h2>
      <table class="table">
        <thead>
          <tr>
            <th></th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>Worker ID</td>
            <td>{{ task.worker_id }}</td>
          </tr>
          <tr>
            <td>State</td>
            <td>
              <span v-bind:class="task.state">
                {{ status.connector.state }}
              </span>
            </td>
          </tr>
        </tbody>
      </table>

      <article class="message is-danger" v-if="task.trace">
        <div class="message-header">
          <p>Error</p>
        </div>
        <div class="message-body">
          <pre>{{ task.trace }}</pre>
        </div>
      </article>
    </div>
  </div>
</template>

<script>
import connect from "../common/connect";
import axios from "axios";

export default {
  data() {
    return {
      status: [],
      config: [],
      topics: [],
      errors: "",
      isLoading: "",
    };
  },

  // Fetches posts when the component is created.
  created() {
    this.isLoading = "detail";
    axios
      .all([
        connect.getConnectorStatus(this.$route.params.id),
        connect.getConnectorConfig(this.$route.params.id),
      ])
      .then((respAll) => {
        this.status = respAll[0].data;
        this.config = respAll[1].data;
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
      this.isLoading = "detail";
      this.errors = "";
      axios
        .all([
          connect.getConnectorStatus(this.$route.params.id),
          connect.getConnectorConfig(this.$route.params.id),
        ])
        .then((respAll) => {
          this.status = respAll[0].data;
          this.config = respAll[1].data;
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
  },
};
</script>
