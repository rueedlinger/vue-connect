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
      <error-message :message="errors"></error-message>

      <table v-if="data.length > 0" class="table is-hoverable">
        <thead>
          <tr>
            <th></th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="plugin in data" :key="plugin.class">
            <td>
              <b>{{ plugin.name }}</b>
              <ul>
                <li>Class: {{ plugin.class }}</li>
                <li>Type: {{ plugin.type }}</li>
                <li>Version: {{ plugin.version }}</li>
              </ul>
            </td>
            <td>
              <a
                class="button is-primary is-small"
                v-on:click="newConnector(plugin.class, plugin.type)"
                ><font-awesome-icon icon="plus-circle"></font-awesome-icon
                ><span class="pl-1">New connector</span></a
              >
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>
<script>
import connect from "../common/connect";
import ErrorMessage from "../components/ErrorMessage.vue";

export default {
  components: { ErrorMessage },
  data() {
    return {
      data: [],
      errors: "",
      isLoading: "",
    };
  },

  // Fetches posts when the component is created.
  created() {
    this.isLoading = "plugins";
    connect
      .getPlugins()
      .then((response) => {
        // JSON responses are automatically parsed.
        this.data = response.data;
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
    newConnector: function(pluginClass, pluginType) {
      this.$router.push("/new/" + pluginClass + "/" + pluginType);
    },
    reload: function() {
      this.isLoading = "plugins";
      this.errors = "";
      connect
        .getPlugins()
        .then((response) => {
          // JSON responses are automatically parsed.
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
