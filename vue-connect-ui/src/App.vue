<template>
  <div id="app">
    <header class="container is-fluid is-size-4 mt-4 mb-2">
      <router-link class="has-text-primary pr-5" to="/">
        <span class="mr-1">
          <font-awesome-icon icon="cogs"></font-awesome-icon>
        </span>
        <span>Status</span>
      </router-link>

      <router-link class="has-text-primary pr-5" to="/plugins">
        <span class="mr-1">
          <font-awesome-icon icon="layer-group"></font-awesome-icon>
        </span>
        <span>Plugins</span>
      </router-link>

      <router-link class="has-text-primary pr-5" to="/info">
        <span class="mr-1">
          <font-awesome-icon icon="info-circle"></font-awesome-icon>
        </span>
        <span>Info</span>
      </router-link>
    </header>

    <div class="pb-1">
      <section class="hero is-small is-primary">
        <div class="hero-body ml-2">
          <p class="title">
            {{ $route.name }}
          </p>
        </div>
      </section>
    </div>

    <div class="container is-fluid">
      <router-view />
    </div>

    <footer class="footer">
      <div class="content has-text-centered">
        <p>
          <a
            class="has-text-primary"
            href="https://github.com/rueedlinger/vue-connect"
          >
            <strong>vue-connect</strong></a
          >
          - Apache License
        </p>
      </div>
    </footer>
  </div>
</template>

<style>
@import "../node_modules/bulma/css/bulma.css";
@import "../node_modules/bulma-tooltip";
@import "./assets/css/custom.css";
</style>
