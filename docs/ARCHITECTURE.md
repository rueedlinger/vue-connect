# Architecture

## Components

vue-connect is build with [Vue.js](https://vuejs.org/) and [Python](https://www.python.org/).

- [vue-connect-api](vue-connect-api) - the backend service project (API). ![Build API](https://github.com/rueedlinger/vue-connect/workflows/Build%20API/badge.svg)
- [vue-connect-ui](vue-connect-ui) - the UI project. ![Build UI](https://github.com/rueedlinger/vue-connect/workflows/Build%20UI/badge.svg)
- The UI and API are bundled together in a [Docker](Dockerfile) image with the _nginx_ web server and _gunicorn_. ![Build Docker](https://github.com/rueedlinger/vue-connect/workflows/Build%20Docker/badge.svg)

![architecture](images/architecture.png)

## Syncing Cluster State and UI State

- The _scheduler_ is polling the Kafka Connect cluster and stores the result in the cache (SQLite DB).
- The _UI_ is continuously polling the cache and updating the view. The main operation by the user are not cached and redirect to the Kafka Connect cluster. If the cluster is not available the last sate from the cache is returned with an error message.

![cache](images/cache.png)
