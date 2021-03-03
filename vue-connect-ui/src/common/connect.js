import axios from "axios";

const connect = {
  getAppInfo: () => {
    return axiosGet("/app/info");
  },
  getInfo: () => {
    return axiosGet("/cluster/info");
  },
  getAllConnectorStatus: () => {
    return axiosGet("/status");
  },
  pollConnectorStatus: () => {
    return axiosGet("/cache");
  },
  getConnectorStatus: (clusterId, connectorName) => {
    return axiosGet("/cluster/" + clusterId + "/status/" + connectorName);
  },
  getConnectorConfig: (clusterId, connectorName) => {
    return axiosGet("/cluster/" + clusterId + "/config/" + connectorName);
  },
  updateConnector: (clusterId, connectorName, config) => {
    return axiosPostWithData(
      "/cluster/" + clusterId + "/connectors/" + connectorName + "/config",
      config
    );
  },
  deleteConnector: (clusterId, connectorName) => {
    return axiosPost(
      "/cluster/" + clusterId + "/connectors/" + connectorName + "/delete"
    );
  },
  validateConfig: (clusterId, pluginName, config) => {
    return axiosPostWithData(
      "/cluster/" + clusterId + "/plugins/" + pluginName + "/config/validate",
      config
    );
  },
  newConnector: (clusterId, config) => {
    return axiosPostWithData("/cluster/" + clusterId + "/connectors", config);
  },
  restartConnector: (clusterId, connectorName) => {
    return axiosPost(
      "/cluster/" + clusterId + "/connectors/" + connectorName + "/restart"
    );
  },
  restartTask: (clusterId, connectorName, taskId) => {
    return axiosPost(
      "/cluster/" +
        clusterId +
        "/connectors/" +
        connectorName +
        "/tasks/" +
        taskId +
        "/restart"
    );
  },
  pauseConnector: (clusterId, connectorName) => {
    return axiosPost(
      "/cluster/" + clusterId + "/connectors/" + connectorName + "/pause"
    );
  },
  resumeConnector: (clusterId, connectorName) => {
    return axiosPost(
      "/cluster/" + clusterId + "/connectors/" + connectorName + "/resume"
    );
  },
  getPlugins: () => {
    return axiosGet("/plugins");
  },
};

function getApiUrl(path) {
  return process.env.VUE_APP_API_URL + path;
}

function axiosGet(path) {
  return axios.get(getApiUrl(path));
}

function axiosPost(path) {
  return axios.post(getApiUrl(path));
}

function axiosPostWithData(path, data) {
  return axios.post(getApiUrl(path), data);
}

export default connect;
