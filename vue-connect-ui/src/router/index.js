import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from '../views/Home.vue'
import Plugin from '../views/Plugin.vue'
import Detail from '../views/Detail.vue'
import About from '../views/About.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/plugins',
    name: 'Plugin',
    component: Plugin
  },
  {
    path: '/detail/:id',
    name: 'Detail',
    component: Detail
  },
  {
    path: '/about',
    name: 'About',
    component: About
  }
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
