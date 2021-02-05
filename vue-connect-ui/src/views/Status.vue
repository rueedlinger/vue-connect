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

    <article class="message is-info" v-if="data.length == 0 && !errors">
      <div class="message-header">
        <p>Info</p>
      </div>
      <div class="message-body">
        <strong>No running connectors!</strong>
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
          <tr v-for="item in data" v-bind:key="item.hash">
            <td>
              <button
                v-bind:class="item.connector.state"
                class="button is-rounded is-small is-fullwidth"
              >
                {{ item.connector.state }}
              </button>
            </td>
            <td>
              <ul id="detail">
                <li><b>Connector ID:</b> {{ item.name }}</li>
                <li><b>Type:</b> {{ item.type }}</li>
                <li><b>Worker ID:</b> {{ item.connector.worker_id }}</li>
              </ul>
            </td>
            <td>
              <table class="table">
                <tr>
                  <td>
                    <a
                      class="button is-primary is-small"
                      v-on:click="detail(item.name)"
                      ><font-awesome-icon icon="info-circle"></font-awesome-icon
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
                      ><font-awesome-icon icon="trash-alt"></font-awesome-icon
                    ></a>
                  </td>
                  <td>
                    <a
                      class="button is-primary is-small"
                      v-on:click="resume(`resume-${item.name}`)"
                      v-bind:class="[
                        isLoading == `resume-${item.name}` ? `is-loading` : ``,
                      ]"
                    >
                      <font-awesome-icon icon="play-circle"></font-awesome-icon
                    ></a>
                  </td>
                  <td>
                    <a
                      class="button is-primary is-small"
                      v-on:click="pause(`pause-${item.name}`)"
                      v-bind:class="[
                        isLoading == `pause-${item.name}` ? `is-loading` : ``,
                      ]"
                    >
                      <font-awesome-icon icon="pause-circle"></font-awesome-icon
                    ></a>
                  </td>
                  <td>
                    <a
                      class="button is-primary is-small"
                      v-on:click="restart(`restart-${item.name}`)"
                      v-bind:class="[
                        isLoading == `restart-${item.name}` ? `is-loading` : ``,
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
                        class="button is-rounded is-small is-fullwidth"
                      >
                        {{ task.state }}
                      </button>
                    </td>
                    <td>
                      <ul id="detail">
                        <li><b>Task ID:</b> {{ task.id }}</li>
                        <li><b>Worker ID:</b> {{ task.worker_id }}</li>
                      </ul>
                    </td>
                    <td>
                      <a
                        class="button is-primary is-small"
                        v-on:click="restartTask(item.name, task.id)"
                        v-bind:class="[
                        isLoading == item.name ? `is-loading` : ``,
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
    let isFailed = (e.connector.state.toUpperCase() == "FAILED"),
      isPaused = (e.connector.state.toUpperCase() == "PAUSED");

    for (let t of e.tasks) {
      isFailed = (isFailed || t.state.toUpperCase() == "FAILED");
      isPaused = (isPaused && t.state.toUpperCase() == "PAUSED")
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

  return [...failedCollection, ...runningCollection, ...pausedCollection]
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
        connect.getAllConnectorStatus().then((response) => {
          this.data = sortedConnectors(response.data);
          this.isLoading = "";
          this.errors = "";
        })
        .catch((e) => {
          if (e.response) {
            this.errors = e.response.data.message;
          } else {
            this.errors = { message: e.message };
          }
        });
      }.bind(this),
      60000
    );
  },

  beforeDestroy() {
    clearInterval(this.polling);
  },

  methods: {
    reRender: function() {
      this.$forceUpdate();
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
      this.isLoading = id;
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
      this.isLoading = id;
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
      this.isLoading = id;
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
      this.isLoading = id;
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
