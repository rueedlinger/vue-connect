<template>
  <div id="app" class="content">
    <div id="nav">
      | <router-link to="/">Connectors</router-link> |
      <router-link to="/plugins">Plugins</router-link> |
      <router-link to="/about">About</router-link> |
    </div>
    <hr>
    <router-view/>
  </div>
</template>



<style>

@import './assets/css/normalize.css';
@import './assets/css/skeleton.css';

body {
  padding: 60px;
}

.content {  
  overflow-wrap: break-word;
  word-wrap: break-word;
}

.error {
  color: red;
  font-size: 20px;
}


#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: left;
  color: #2c3e50;
}

#nav {
  font-size: 20px;
}

#nav a {
  font-weight: bold;
  color: #2c3e50;
}

#nav a.router-link-exact-active {
  color: #42b983;
}
</style>
