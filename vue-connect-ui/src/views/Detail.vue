<template>
  <div>
    <div class="box notification is-primary">
      <div class="columns">
        <div class="column is-1">
          <p class="title">
            {{ $route.name }}
          </p>
        </div>
        <div class="column is-8 is-offset-1"></div>
        <div class="column is-1 is-offset-1">
          <button
            v-on:click="reload()"
            v-bind:class="[isLoading != `` ? `is-loading` : ``]"
            class="button"
          >
            <font-awesome-icon icon="sync-alt"></font-awesome-icon>
          </button>
        </div>
      </div>
    </div>

    <div class="box content">
      <h2>Connector {{ $route.params.id }}</h2>
      <error-message :errors="errors"></error-message>

      <div v-if="status.connector">
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
import errorHandler from "../common/error";
import axios from "axios";
import ErrorMessage from "../components/ErrorMessage.vue";

function loadData() {
  this.isLoading = "detail";
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
  components: { ErrorMessage },
  data() {
    return {
      status: [],
      config: [],
      topics: [],
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
