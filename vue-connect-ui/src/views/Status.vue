<template>
  <div class="">
    <div class="box">
      <button
        v-on:click="reload()"
        data-tooltip="Reload"
        class="button is-small"
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

      <article class="message is-info" v-if="data.length == 0 && !errors">
        <div class="message-header">
          <p>Info</p>
        </div>
        <div class="message-body">
          There are no connectors deployed!
        </div>
      </article>

      <div class="table-container is-size-7">
        <table v-if="data.length > 0" class="table is-hoverable ">
          <thead>
            <tr>
              <th>State</th>
              <th>Connector</th>
              <th></th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="item in data" v-bind:key="item.name">
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
                        v-bind:data-tooltip="'Show details ' + item.name"
                        v-on:click="detail(item.name)"
                        ><font-awesome-icon
                          icon="info-circle"
                        ></font-awesome-icon
                      ></a>
                    </td>
                    <td>
                      <a
                        class="button is-primary is-small"
                        v-bind:data-tooltip="'Edit ' + item.name"
                        v-on:click="edit(item.name)"
                        ><font-awesome-icon icon="edit"></font-awesome-icon
                      ></a>
                    </td>
                    <td>
                      <a
                        class="button is-primary is-small"
                        v-bind:data-tooltip="'Delete ' + item.name"
                        v-on:click="del(item.name)"
                        ><font-awesome-icon icon="trash-alt"></font-awesome-icon
                      ></a>
                    </td>
                    <td>
                      <a
                        class="button is-primary is-small"
                        v-bind:data-tooltip="'Resume ' + item.name"
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
                        v-bind:data-tooltip="'Pause ' + item.name"
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
                        v-bind:data-tooltip="'Restart ' + item.name"
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
                    <tr v-for="task in item.tasks" v-bind:key="task.state">
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
                          v-bind:data-tooltip="
                            'Restart Task ' + item.name + ':' + task.id
                          "
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

export default {
  data() {
    return {
      data: [],
      errors: "",
      polling: null,
      isLoading: "",
    };
  },

  // Fetches posts when the component is created.
  created() {
    connect
      .getAllConnectorStatus()
      .then((response) => {
        this.data = sortedConnectors(response.data);
      })
      .catch((e) => {
        if (e.response) {
          this.errors = e.response.data.message;
        } else {
          this.errors = { message: e.message };
        }
      });

    this.polling = setInterval(
      function() {
        connect
          .pollConnectorStatus()
          .then((response) => {
            if (response.data.state != null && response.data.state.length > 0) {
              this.data = sortedConnectors(response.data.state);
              this.isLoading = "";
            }
          })
          .catch((e) => {
            if (e.response) {
              this.errors = e.response.data.message;
            } else {
              this.errors = { message: e.message };
            }
          });
      }.bind(this),
      5000
    );
  },

  beforeDestroy() {
    clearInterval(this.polling);
  },

  methods: {
    reload() {
      connect
        .getAllConnectorStatus()
        .then((response) => {
          this.data = sortedConnectors(response.data);
          this.errors = "";
          this.isLoading = "";
        })
        .catch((e) => {
          if (e.response) {
            this.errors = e.response.data.message;
          } else {
            this.errors = { message: e.message };
          }
        });
    },

    detail: function(id) {
      this.$router.push("/detail/" + id);
    },
    edit: function(id) {
      this.$router.push("/edit/" + id);
    },
    del: function(id) {
      connect
        .deleteConnector(id)
        .then((resp) => {
          this.data = sortedConnectors(resp.data);
        })
        .catch((e) => {
          if (e.response) {
            this.errors = e.response.data.message;
          } else {
            this.errors = { message: e.message };
          }
        });
    },
    restart: function(id) {
      this.isLoading = `restart-${id}`;
      connect
        .restartConnector(id)
        .then((resp) => {
          this.data = sortedConnectors(resp.data);
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
    pause: function(id) {
      this.isLoading = `pause-${id}`;
      connect
        .pauseConnector(id)
        .then((resp) => {
          this.data = sortedConnectors(resp.data);
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
    resume: function(id) {
      this.isLoading = `resume-${id}`;
      connect
        .resumeConnector(id)
        .then((resp) => {
          this.data = sortedConnectors(resp.data);
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
    restartTask: function(id, task_id) {
      this.isLoading = `restart-${id}-${task_id}`;
      connect
        .restartTask(id, task_id)
        .then((resp) => {
          this.data = sortedConnectors(resp.data);
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
