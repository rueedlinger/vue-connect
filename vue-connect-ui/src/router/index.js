import Vue from "vue";
import VueRouter from "vue-router";
import Status from "../views/Status.vue";
import Plugin from "../views/Plugin.vue";
import Detail from "../views/Detail.vue";
import Edit from "../views/Edit.vue";
import New from "../views/New.vue";
import Info from "../views/Info.vue";

Vue.use(VueRouter);

const routes = [
  {
    path: "/",
    name: "Status",
    component: Status,
  },
  {
    path: "/plugins",
    name: "Plugins",
    component: Plugin,
  },
  {
    path: "/detail/:cluster/:id",
    name: "Detail",
    component: Detail,
  },
  {
    path: "/edit/:cluster/:id",
    name: "Edit",
    component: Edit,
  },
  {
    path: "/new/:cluster/:id/:type",
    name: "New",
    component: New,
  },
  {
    path: "/info",
    name: "Info",
    component: Info,
  },
];

const router = new VueRouter({
  mode: "history",
  base: process.env.BASE_URL,
  routes,
});

export default router;
