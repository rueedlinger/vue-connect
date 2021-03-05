# How to Build the Project

- See [Readme (vue-connect-ui)](../vue-connect-ui/README.md) how to build the _Vue.js_ frontend.
- See [Readme (vue-connect-api)](../vue-connect-api/README.md) how to build the _Python_ backend.

## Docker Image

To run the vue-connect on your local machine, you can use the Docker image. This image will bundle the frontend and backend together in one Docker image.

```
docker build . -t vue-connect
```

With `CONNECT_URL`you can set the _Connect Rest Endpoint_ that should be used by vue-connect. The vue-connect Web UI will be listening on port `8080`.

```
docker run --rm -it -p 8080:8080 -e "CONNECT_URL=http://localhost:8083" vue-connect
```

### Docker Compose

Or you can use the Docker Compose file [docker-compose.yml](../docker-compose.yml) to build and start a vue-connect.

```
docker-compose up --build
```
