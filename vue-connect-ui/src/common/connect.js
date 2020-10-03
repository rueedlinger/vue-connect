import axios from 'axios'

let connect = {
    'getInfo': () => {
        return axiosGet('/info')
    },
    'getAllConnectorStatus': () => {
        return axiosGet('/status')
    },
    'getConnectorStatus': (connectorName) => {
        return axiosGet('/status/' + connectorName)
    },
    'getConnectorConfig': (connectorName) => {
        return axiosGet('/config/' + connectorName)
    },
    'updateConnector': (connectorName, config) => {
        return axiosPostWithData('/connectors/' + connectorName + '/config', config)
    },
    'deleteConnector': (connectorName) => {
        return axiosPost('/connectors/' + connectorName + '/delete')
    },
    'validateConfig': (pluginName, config) => {
        return axiosPostWithData('/plugins/' + pluginName + '/config/validate', config)
    },
    'newConnector': (config) => {
        return axiosPostWithData('/connectors/', config)
    },
    'restartConnector': (connectorName) => {
        return axiosPost('/connectors/' + connectorName + '/restart')
    },
    'restartTask': (connectorName, taskId) => {
        return axiosPost('/connectors/' + connectorName + '/tasks/' + taskId + '/restart')
    },
    'pauseConnector': (connectorName) => {
        return axiosPost('/connectors/' + connectorName + '/pause')
    },
    'resumeConnector': (connectorName) => {
        return axiosPost('/connectors/' + connectorName + '/resume')
    },
    'getPlugins': () => {
        return axiosGet('/plugins')
    }
}

function getApiUrl(path) {
    return process.env.VUE_APP_API_URL + path
}

function axiosGet(path) {
    return axios.get(getApiUrl(path))
}

function axiosPost(path) {
    return axios.post(getApiUrl(path))
}

function axiosPostWithData(path, data) {
    return axios.post(getApiUrl(path), data)
}


export default connect
