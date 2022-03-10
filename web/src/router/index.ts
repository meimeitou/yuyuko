import { createRouter, createWebHistory, RouteRecordRaw } from "vue-router";
import Home from "../views/Home.vue";

const routes: Array<RouteRecordRaw> = [
  {
    path: "/",
    name: "Home",
    component: Home,
  },
  {
    path: "/about",
    name: "About",
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () =>
      import(/* webpackChunkName: "about" */ "../views/About.vue"),
  },
  {
    path: "/terminal",
    name: "Terminal",
    component: () =>
      import(/* webpackChunkName: "terminal" */ "../views/Terminal.vue"),
  },
  {
    path: "/curl",
    name: "Curl",
    component: () => import(/* webpackChunkName: "curl" */ "../views/Curl.vue"),
  },
  {
    path: "/spider",
    name: "Spider",
    component: () =>
      import(/* webpackChunkName: "spider" */ "../views/Spider.vue"),
  },
  {
    path: "/tools",
    name: "Tools",
    component: () =>
      import(/* webpackChunkName: "tools" */ "../views/Tools.vue"),
  },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

export default router;
