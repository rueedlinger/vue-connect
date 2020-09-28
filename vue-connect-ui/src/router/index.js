import Vue from 'vue'
import VueRouter from 'vue-router'
import Status from '../views/Status.vue'
import Plugin from '../views/Plugin.vue'
import Detail from '../views/Detail.vue'
import Edit from '../views/Edit.vue'
import Info from '../views/Info.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'Status',
    component: Status
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
    path: '/edit/:id',
    name: 'Edit',
    component: Edit
  },
  {
    path: '/info',
    name: 'Info',
    component: Info
  }
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
