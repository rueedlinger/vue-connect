# vue-connect

**vue-connect** is a simple and open source Kafka Connect UI for setting up and managing connectors. 

> **Note**: This project is under development and there is no release yet.

## Features
- Connector status overview
- Delete, pause and resume connectors
- Restart tasks and connectors
- Install new connectors
- Update connector configuration

![vue-connect ui](docs/images/ui.png)

## Components
vue-connect is build with [Vue.js](https://vuejs.org/) and [Python](https://www.python.org/).

- [vue-connect-api](vue-connect-api) - the backend service project.
- [vue-connect-ui](vue-connect-ui) - the ui project.

## Build

```
docker build . -t vue-connect
```

```
docker run --rm -it -p 8080:8080 -e "CONNECT_UR=http://localhost:8083" vue-connect 
```

## Todo
- Add Tests
- Add build pipeline
- Add changelog and version
- Improve error handling
- Write documentation
- Provide Docker image
- Improve UI for multiple workers (Connect Cluster)

## License
The project is licensed under the [Apache](LICENSE) license.