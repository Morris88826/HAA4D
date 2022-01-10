import { createRouter, createWebHashHistory } from "vue-router";
import Layout from "../views/Layout.vue";
import Home from "../views/Home.vue";
import Dataset from "../views/Dataset.vue";
import AnnotationTool from "../views/AnnotationTool.vue";
import Explore from "../views/Explore.vue";
import Others from "../views/Others.vue";

const routes = [
  {
    path: "/",
    name: "home",
    component: Home,
    meta: { layout: Layout },
  },
  {
    name: "dataset",
    path: "/dataset",
    component: Dataset,
    meta: { layout: Layout },
  },
  {
    name: "annotationTool",
    path: "/annotationTool",
    component: AnnotationTool,
    meta: { layout: Layout },
  },
  {
    name: "explore",
    path: "/explore",
    component: Explore,
    meta: { layout: Layout },
  },
  {
    name: "others",
    path: "/others",
    component: Others,
    meta: { layout: Layout },
  },
];

const router = createRouter({
  history: createWebHashHistory(),
  routes,
});

export default router;
