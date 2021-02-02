# Web UI for Apache Kafka Connect (vue-connect)

**vue-connect** is a simple and open source Web UI for managing *Apache Kafka Connect* connectors. 

> **Note**: This project is under development and fare away from production ready.

## Features
- Connector status overview
- Delete, pause and resume connectors
- Restart tasks and connectors
- Install new connectors
- Update connector configurations

![vue-connect ui](docs/images/ui.png)

## Components
vue-connect is build with [Vue.js](https://vuejs.org/) and [Python](https://www.python.org/).

- [vue-connect-api](vue-connect-api) - the backend service project. ![Build API](https://github.com/rueedlinger/vue-connect/workflows/Build%20API/badge.svg)
- [vue-connect-ui](vue-connect-ui) - the ui project. ![Build UI](https://github.com/rueedlinger/vue-connect/workflows/Build%20UI/badge.svg)
- The UI and API are bundled together in a [Docker](Dockerfile) image with the nginx  web server. ![Build Docker](https://github.com/rueedlinger/vue-connect/workflows/Build%20Docker/badge.svg)

![vue-connect ui](docs/images/architecture.png)


## Run vue-connect

`CONNECT_URL` is the Kafka Connect Rest Endpoint URL which you want to access
with vue-connect.

```
docker run --rm -it -p 8080:8080 \
           -e "CONNECT_URL=http://CONNECT_REST_ENDPOINT:PORT" \
           rueedlinger/vue-connect:v0.2.0
```

The *vue-connect* Web UI will be available at http://localhost:8080

> **Note:** When you want to access the Connect Rest API from another Docker container you could use `host.docker.internal` as endpoint hostname. For example `CONNECT_URL=http://host.docker.internal:8083`

You can modify the Docker Compose file [docker-compose.yml](docker-compose.yml) and use the latest vue-connect Docker image version from Docker Hub.
```
vue-connect:
  image: rueedlinger/vue-connect:v0.2.0
  hostname: vue-connect
    
  depends_on:
    - connect
  
  ports:
    - "8080:8080"
  
  environment:
    CONNECT_URL: "http://connect:8083"
```


## Build from scratch
- See [vue-connect-ui](vue-connect-ui/README.md) how to build the *Vue.js* frontend.
- See [vue-connect-api](vue-connect-api/README.md) how to build the *Python* backend.


### Docker Image
To run the vue-connect locally you can use the Docker image. This image will
bundle the frontend and backend together in one Docker image.

```
docker build . -t vue-connect
```

Next we can start the Docker image. With `CONNECT_URL`you can set the *Connect Rest Endpoint* which should be used by vue-connect. The vue-connect Web UI will be listening on port `8080`.

```
docker run --rm -it -p 8080:8080 -e "CONNECT_URL=http://localhost:8083" vue-connect 
```

### Docker Compose 
Or you can use the Docker Compose file [docker-compose.yml](docker-compose.yml) which starts a Kafka Connect cluster with the latest vue-connect version from this branch. 

```
docker-compose up --build
```

## License
The project is licensed under the [Apache](LICENSE) license.
