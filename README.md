# Web UI for Apache Kafka Connect (vue-connect)

**vue-connect** is a simple and open-source Web UI for managing _Apache Kafka Connect_ connectors.

> **Note**: This project is under development and was build as proof of concept.

## Features

- Connector status overview
- Delete, pause and resume connectors
- Restart tasks and connectors
- Install new connectors
- Update connector configurations

![vue-connect ui](docs/images/demo.gif)

## Architecture & Components

see [Architecture](docs/ARCHITECTURE.md)

## Releases & Docker Images

The Docker images are published to Docker Hub.

- See https://hub.docker.com/r/rueedlinger/vue-connect

| Docker Tag                | Description                                                        |
| ------------------------- | ------------------------------------------------------------------ |
| `master`                  | This is the current release of the master branch.                  |
| `<major>.<minor>.<patch>` | For example Docker tag `0.1.0` corresponds to the git tag `v0.1.0` |

## Run vue-connect

`CONNECT_URL` is the Kafka Connect Rest Endpoint URL which you want to access
with vue-connect. You can also configure multiple connect clusters with `CONNECT_URL="http://connect-a:8083,Cluster A;http://connect-b:8084,Cluster B"`

```
docker run --rm -it -p 8080:8080 \
           -e "CONNECT_URL=http://CONNECT_REST_ENDPOINT:PORT" \
           rueedlinger/vue-connect:master
```

The _vue-connect_ Web UI will be available at http://localhost:8080

> **Note:** When you want to access the Connect Rest API from another Docker container you could use `host.docker.internal` as endpoint hostname. `CONNECT_URL=http://host.docker.internal:8083`

You can modify the Docker Compose file [docker-compose.yml](docker-compose.yml) and use the latest vue-connect Docker image version from Docker Hub.

```
vue-connect:
  image: rueedlinger/vue-connect:master
  hostname: vue-connect

  depends_on:
    - connect

  ports:
    - "8080:8080"

  environment:
    CONNECT_URL: "http://connect:8083"
```

## Configuration Options

The following environment variables can be used to configure _vue-connect_.

| Environment Variable      | Description                                                                                                                                                                                                                                                                             | Default Value         |
| ------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------- |
| `CONNECT_URL`             | The URL of the Connect API. You can use the cluster url's separator (`;`) to add multiple connect clsuters. `"http://connect-a:8083;http:/connect-b:8084"`. You can also add a name separator (`,`) to the clusters `"http://connect-a:8083,Cluster A;http://connect-b:8084,Cluster B"` | http://localhost:8083 |
| `VC_POLLING_INTERVAL_SEC` | The Connect API polling interval in seconds. If the value is smaller than 1 the polling is deactivated.                                                                                                                                                                                 | 60 seconds            |
| `VC_REQUEST_TIMEOUT_SEC`  | The default request timeout when communicating with the Connect API.                                                                                                                                                                                                                    | 5 seconds             |
| `VC_RUN_SCHEDULER`        | Option to enable (`true`) or disable (`false`) the backend scheduler.                                                                                                                                                                                                                   | true                  |
| `TZ`                      | Set the timezone.                                                                                                                                                                                                                                                                       | `UTC`                 |

## Issues / Improvements / Feature Requests / Contributing

- see [Issues](https://github.com/rueedlinger/vue-connect/issues)
- see [Contributing](docs/CONTRIBUTING.md)

## License

This project is licensed under the terms of the [Apache](LICENSE) license.
