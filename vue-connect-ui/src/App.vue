<template>
  <div id="app">

    <header>
      <nav id="menu">
        <ul>
          <li><router-link to="/">Status</router-link></li>
          <li><router-link to="/plugins" >Plugins</router-link></li>
          <li><router-link to="/info">Info</router-link></li>
        </ul>
      </nav>
    </header>

    <div id="content">
        <router-view/>
    </div>
    <footer>
      <hr>
      <a href="https://github.com/rueedlinger/vue-connect">vue-connect</a>
    </footer>
  </div>
    
  
</template>


<style>
@import '../node_modules/normalize.css';
@import '../node_modules/purecss';
@import './assets/css/custom.css';
</style>
