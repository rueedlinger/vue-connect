<template>
  <div id="app" class="content">
    <div id="nav">
      | <router-link to="/">Status</router-link> |
      <router-link to="/plugins">Plugins</router-link> |
      <router-link to="/info">Info</router-link> |
    </div>
    <hr>
    <div class="content">
      <router-view/>
    </div>
  </div>
</template>


<style>
@import '../node_modules/normalize.css';
@import '../node_modules/purecss/build/pure.css';
@import './assets/css/custom.css';
</style>
