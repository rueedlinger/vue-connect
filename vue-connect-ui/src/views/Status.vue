<template>
  <div>
    <div class="box notification is-primary">
      <div class="columns">
        <div class="column">
          <p class="title">
            {{ $route.name }}
          </p>
        </div>
        <div class="column is-two-thirds">
          <input
            class="input is-primary is-rounded"
            type="text"
            placeholder="Name"
            v-model="searchText"
          />
        </div>
        <div class="column">
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

    <div class="box">
      <error-message :error="errors"></error-message>

      <div class="table-container is-size-7">
        <table v-if="filterdata.length > 0" class="table is-hoverable">
          <thead>
            <tr>
              <th>State</th>
              <th>Connector</th>
              <th></th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="item in filterdata" v-bind:key="item.name">
              <td>
                <button
                  v-bind:class="item.connector.state"
                  v-on:click="detail(item.name)"
                  v-bind:data-tooltip="item.connector.traceShort"
                  class="button is-rounded is-small is-fullwidth has-tooltip-right has-tooltip-multiline has-tooltip-danger"
                >
                  {{ item.connector.state }}
                </button>
              </td>
              <td>
                <ul id="detail">
                  <li><b>Connector ID:</b> {{ item.name }}</li>
                  <li><b>Type:</b> {{ item.type }}</li>
                  <li><b>Worker ID:</b> {{ item.connector.worker_id }}</li>
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
                        v-on:click="detail(item.name)"
                        ><font-awesome-icon
                          icon="info-circle"
                        ></font-awesome-icon
                      ></a>
                    </td>
                    <td>
                      <a
                        class="button is-primary is-small"
                        v-on:click="edit(item.name)"
                        ><font-awesome-icon icon="edit"></font-awesome-icon
                      ></a>
                    </td>
                    <td>
                      <a
                        class="button is-primary is-small"
                        v-on:click="del(item.name)"
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
                        v-on:click="resume(item.name)"
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
                        v-on:click="pause(item.name)"
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
                        v-on:click="restart(item.name)"
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
                          v-on:click="detail(item.name)"
                        >
                          {{ task.state }}
                        </button>
                      </td>
                      <td>
                        <ul id="detail">
                          <li><b>Task ID:</b> {{ task.id }}</li>
                          <li><b>Worker ID:</b> {{ task.worker_id }}</li>
                          <li class="has-text-danger" v-if="task.traceMessage">
                            <b>Error:</b> {{ task.traceMessage }}
                          </li>
                        </ul>
                      </td>
                      <td>
                        <a
                          class="button is-primary is-small"
                          v-on:click="restartTask(item.name, task.id)"
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
  this.isLoading = `status`;
  this.errors = null;

  connect
    .getAllConnectorStatus()
    .then((response) => {
      this.data = sortedConnectors(response.data);
      this.isLoading = "";
    })
    .catch((e) => {
      // check if there is cached state in error response
      if (e.response && e.response.data.cache) {
        this.data = sortedConnectors(e.response.data.cache);
      }
      this.errors = errorHandler.transform(e);
      this.isLoading = "";
    });
}

function runConnectOperation(operation, operationName, connectorId, taskId) {
  if (taskId != null) {
    this.isLoading = `${operationName}-${connectorId}-${taskId}`;
  } else {
    this.isLoading = `${operationName}-${connectorId}`;
  }

  this.errors = null;
  operation(connectorId, taskId)
    .then((resp) => {
      this.data = sortedConnectors(resp.data);
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
      data: [],
      errors: null,
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

    this.polling = setInterval(
      function() {
        connect
          .pollConnectorStatus()
          .then((response) => {
            if (response.data.state != null && response.data.state.length > 0) {
              this.data = sortedConnectors(response.data.state);
              if (response.data.isConnectUp) {
                // connect is running again
                this.errors = null;
              }
              if (!response.data.isConnectUp && this.errors == null) {
                // set error from cache
                this.errors = { message: response.data.message };
              }
            }
          })
          .catch((e) => {
            this.errors = errorHandler.transform(e);
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
    detail: function(id) {
      this.$router.push("/detail/" + id);
    },
    edit: function(id) {
      this.$router.push("/edit/" + id);
    },
    del: function(id) {
      runConnectOperation.bind(this)(connect.deleteConnector, "delete", id);
    },
    restart: function(id) {
      runConnectOperation.bind(this)(connect.restartConnector, "restart", id);
    },
    pause: function(id) {
      runConnectOperation.bind(this)(connect.pauseConnector, "pause", id);
    },
    resume: function(id) {
      runConnectOperation.bind(this)(connect.resumeConnector, "resume", id);
    },
    restartTask: function(id, task_id) {
      runConnectOperation.bind(this)(
        connect.restartTask,
        "restart",
        id,
        task_id
      );
    },
  },
};
</script>
