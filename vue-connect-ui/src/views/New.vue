<template>
  <div class="content">
    <div class="box">
      <h2>Connector {{ connectorName }}</h2>
      <ul>
        <li>Class: {{ $route.params.id }}</li>
        <li>Type: {{ $route.params.type }}</li>
      </ul>

      <error-message :message="errors"></error-message>

      <div class="field">
        <label class="label">Configuration</label>
        <div class="control">
          <textarea
            class="textarea is-small is-primary"
            placeholder=""
            v-model="jsonConfig"
          ></textarea>
        </div>
      </div>

      <div class="control">
        <button class="button is-primary is-small" v-on:click="save()">
          <font-awesome-icon icon="save"></font-awesome-icon
          ><span class="pl-1">Save</span>
        </button>
      </div>
    </div>

    <div class="box">
      <h2>Configuration Options for {{ connectorName }}</h2>
      <table class="table is-hoverable is-size-7">
        <thead>
          <tr>
            <th>Name</th>
            <th>Type</th>
            <th>Required</th>
            <th>Default Value</th>
            <th>Documentaion</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="cfg in configParams" :key="cfg.name">
            <td>{{ cfg.name }}</td>
            <td>{{ cfg.type }}</td>
            <td>{{ cfg.required }}</td>
            <td>{{ cfg.default_value }}</td>
            <td>{{ cfg.documentation }}</td>
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
      connectorName: "",
      configParams: [],
      jsonConfig: "",
      errors: "",
    };
  },

  // Fetches posts when the component is created.
  created() {
    let parts = this.$route.params.id.split(".");
    let name = parts[parts.length - 1];
    this.connectorName = name;

    let data = {
      "connector.class": this.$route.params.id,
      "tasks.max": 1,
      name: name,
    };

    if (this.$route.params.type == "sink") {
      data["topics"] =
        "topic" +
        name.replace(/([A-Z])/g, function(g) {
          return "-" + g[0].toLowerCase();
        });
    }

    let self = this;
    connect
      .validateConfig(name, data)
      .then((resp) => {
        let configs = resp.data.configs;

        configs.forEach(function(entry) {
          if (entry.value.errors.length > 0) {
            //console.log(entry.value)
            data[entry.value.name] = "";
          }
          self.configParams.push({
            name: entry.definition.name,
            default_value: entry.definition.default_value,
            type: entry.definition.type,
            required: entry.definition.required,
            documentation: entry.definition.documentation,
          });
        });

        this.jsonConfig = JSON.stringify(data, null, 2);
      })
      .catch((e) => {
        if (e.response) {
          this.errors = e.response.data.message;
        } else {
          this.errors = { message: e.message };
        }
      });
  },

  methods: {
    save: function() {
      try {
        let data = JSON.parse(this.jsonConfig);
        connect
          .newConnector(data)
          .then(() => {
            this.$router.push("/");
          })
          .catch((e) => {
            if (e.response) {
              this.errors = e.response.data.message;
            } else {
              this.errors = { message: e.message };
            }
          });
      } catch (error) {
        this.errors = error;
      }
    },
  },
};
</script>
