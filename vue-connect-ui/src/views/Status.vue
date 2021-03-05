<template>
  <div>
    <title-header
      :isLoading="isLoading"
      :title="$route.name"
      :reloadData="reload"
      :hasSearchText="true"
      v-model="searchText"
    ></title-header>
    <div class="box">
      <error-message :errors="errors"></error-message>

      <div class="table-container">
        <table v-if="filterdata.length > 0" class="table is-hoverable">
          <thead>
            <tr>
              <th>State</th>
              <th>Cluster</th>
              <th>Connector</th>
              <th></th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="item in filterdata"
              v-bind:key="item.cluster.id + '-' + item.name"
            >
              <td>
                <button
                  v-bind:class="item.connector.state"
                  v-on:click="detail(item.cluster.id, item.name)"
                  v-bind:data-tooltip="item.connector.traceShort"
                  class="button is-rounded is-small is-fullwidth has-tooltip-right has-tooltip-multiline has-tooltip-danger"
                >
                  {{ item.connector.state }}
                </button>
              </td>
              <td>
                <span v-if="item.cluster.name">{{ item.cluster.name }}</span>
                <span v-else>{{ item.cluster.url }}</span>
              </td>
              <td>
                <ul id="detail">
                  <li><b>Connector ID:</b> {{ item.name }}</li>
                  <li><b>Type:</b> {{ item.type }}</li>
                  <li><b>Worker ID:</b> {{ item.connector.worker_id }}</li>
                  <li v-if="item.connector.downtime" class="has-text-danger">
                    <b>Downtime:</b>
                    {{ new Date(item.connector.downtime).toLocaleString() }}
                  </li>
                  <li
                    class="has-text-danger"
                    v-if="item.connector.traceMessage"
                  >
                    <b>Error:</b> {{ item.connector.traceMessage }}
                  </li>
                </ul>
              </td>
              <td>
                <table class="table">
                  <tr>
                    <td>
                      <a
                        class="button is-primary is-small"
                        v-on:click="detail(item.cluster.id, item.name)"
                        ><font-awesome-icon
                          icon="info-circle"
                        ></font-awesome-icon
                      ></a>
                    </td>
                    <td>
                      <a
                        class="button is-primary is-small"
                        v-on:click="edit(item.cluster.id, item.name)"
                        ><font-awesome-icon icon="edit"></font-awesome-icon
                      ></a>
                    </td>
                    <td>
                      <a
                        class="button is-primary is-small"
                        v-on:click="del(item.cluster.id, item.name)"
                        v-bind:class="[
                          isLoading == `delete-${item.name}`
                            ? `is-loading`
                            : ``,
                        ]"
                        ><font-awesome-icon icon="trash-alt"></font-awesome-icon
                      ></a>
                    </td>
                    <td>
                      <a
                        class="button is-primary is-small"
                        v-on:click="resume(item.cluster.id, item.name)"
                        v-bind:class="[
                          isLoading == `resume-${item.name}`
                            ? `is-loading`
                            : ``,
                        ]"
                      >
                        <font-awesome-icon
                          icon="play-circle"
                        ></font-awesome-icon
                      ></a>
                    </td>
                    <td>
                      <a
                        class="button is-primary is-small"
                        v-on:click="pause(item.cluster.id, item.name)"
                        v-bind:class="[
                          isLoading == `pause-${item.name}` ? `is-loading` : ``,
                        ]"
                      >
                        <font-awesome-icon
                          icon="pause-circle"
                        ></font-awesome-icon
                      ></a>
                    </td>
                    <td>
                      <a
                        class="button is-primary is-small"
                        v-on:click="restart(item.cluster.id, item.name)"
                        v-bind:class="[
                          isLoading == `restart-${item.name}`
                            ? `is-loading`
                            : ``,
                        ]"
                        ><font-awesome-icon icon="retweet"></font-awesome-icon
                      ></a>
                    </td>
                  </tr>
                </table>
              </td>
              <td>
                <article
                  class="message is-warning is-small"
                  v-if="item.tasks.length == 0"
                >
                  <div class="message-header">
                    <p>Warning</p>
                  </div>
                  <div class="message-body">
                    <strong>No running tasks.</strong>
                  </div>
                </article>

                <table
                  class="pure-table pure-table-bordered"
                  v-if="item.tasks.length > 0"
                >
                  <thead>
                    <tr>
                      <th>State</th>
                      <th>Task</th>
                      <th></th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="task in item.tasks" v-bind:key="task.id">
                      <td>
                        <button
                          v-bind:class="task.state"
                          v-bind:data-tooltip="task.traceShort"
                          class="button is-rounded is-small is-fullwidth has-tooltip-multiline has-tooltip-danger has-tooltip-right"
                          v-on:click="detail(item.cluster.id, item.name)"
                        >
                          {{ task.state }}
                        </button>
                      </td>
                      <td>
                        <ul id="detail">
                          <li><b>Task ID:</b> {{ task.id }}</li>
                          <li><b>Worker ID:</b> {{ task.worker_id }}</li>
                          <li v-if="task.downtime" class="has-text-danger">
                            <b>Downtime:</b>
                            {{ new Date(task.downtime).toLocaleString() }}
                          </li>
                          <li class="has-text-danger" v-if="task.traceMessage">
                            <b>Error:</b> {{ task.traceMessage }}
                          </li>
                        </ul>
                      </td>
                      <td>
                        <a
                          class="button is-primary is-small"
                          v-on:click="
                            restartTask(item.cluster.id, item.name, task.id)
                          "
                          v-bind:class="[
                            isLoading == `restart-${item.name}-${task.id}`
                              ? `is-loading`
                              : ``,
                          ]"
                          ><font-awesome-icon icon="retweet"></font-awesome-icon
                        ></a>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script>
import connect from "../common/connect";
import errorHandler from "../common/error";
import TitleHeader from "../components/TitleHeader.vue";
import ErrorMessage from "../components/ErrorMessage.vue";

/**
 * return sorted connector list
 * @param {*} connectors
 */
function sortedConnectors(connectors) {
  let failedCollection = [],
    runningCollection = [],
    pausedCollection = [];

  for (let e of connectors) {
    let isFailed = e.connector.state.toUpperCase() == "FAILED",
      isPaused = e.connector.state.toUpperCase() == "PAUSED";

    for (let t of e.tasks) {
      isFailed = isFailed || t.state.toUpperCase() == "FAILED";
      isPaused = isPaused && t.state.toUpperCase() == "PAUSED";
    }
    // First show failed
    if (isFailed) {
      failedCollection.push(e);
      continue;
    }
    // Last show paused
    if (isPaused) {
      pausedCollection.push(e);
      continue;
    }
    runningCollection.push(e);
  }

  return [...failedCollection, ...runningCollection, ...pausedCollection];
}

function loadData() {
  this.isLoading = "status";
  this.errors = [];
  connect
    .getAllConnectorStatus()
    .then((response) => {
      this.data = sortedConnectors(response.data.state);
      this.errors = response.data.errors;
      this.isLoading = "";
    })
    .catch((e) => {
      this.errors.push(errorHandler.transform(e));
      this.isLoading = "";
    });
}

function runConnectOperation(
  operation,
  operationName,
  clusterId,
  connectorId,
  taskId
) {
  this.errors = [];

  if (taskId != null) {
    this.isLoading = `${clusterId}-${operationName}-${connectorId}-${taskId}`;
  } else {
    this.isLoading = `${clusterId}-${operationName}-${connectorId}`;
  }

  operation(clusterId, connectorId, taskId)
    .then((resp) => {
      this.data = sortedConnectors(resp.data.state);
      this.errors = resp.data.errors;
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
      data: [],
      errors: [],
      polling: null,
      isLoading: "",
      searchText: "",
    };
  },

  computed: {
    filterdata() {
      if (this.searchText != "") {
        return this.data.filter(
          (s) =>
            s.name.toLowerCase().indexOf(this.searchText.toLowerCase()) >= 0
        );
      }
      return this.data;
    },
  },

  // Fetches posts when the component is created.
  created() {
    loadData.bind(this)();

    // polling new data from cache
    this.polling = setInterval(
      function() {
        connect
          .pollConnectorStatus()
          .then((response) => {
            this.data = sortedConnectors(response.data.state);
            this.errors = response.data.errors;
          })
          .catch((e) => {
            this.errors = [errorHandler.transform(e)];
          });
      }.bind(this),
      10000
    );
  },

  beforeDestroy() {
    clearInterval(this.polling);
  },

  methods: {
    reload() {
      loadData.bind(this)();
    },
    detail: function(clusterId, id) {
      this.$router.push("/detail/" + clusterId + "/" + id);
    },
    edit: function(clusterId, id) {
      this.$router.push("/edit/" + clusterId + "/" + id);
    },
    del: function(clusterId, id) {
      runConnectOperation.bind(this)(
        connect.deleteConnector,
        "delete",
        clusterId,
        id
      );
    },
    restart: function(clusterId, id) {
      runConnectOperation.bind(this)(
        connect.restartConnector,
        "restart",
        clusterId,
        id
      );
    },
    pause: function(clusterId, id) {
      runConnectOperation.bind(this)(
        connect.pauseConnector,
        "pause",
        clusterId,
        id
      );
    },
    resume: function(clusterId, id) {
      runConnectOperation.bind(this)(
        connect.resumeConnector,
        "resume",
        clusterId,
        id
      );
    },
    restartTask: function(clusterId, id, task_id) {
      runConnectOperation.bind(this)(
        connect.restartTask,
        "restart",
        clusterId,
        id,
        task_id
      );
    },
  },
};
</script>
