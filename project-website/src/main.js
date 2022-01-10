import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";
import Antd from "ant-design-vue";
import "bootstrap/dist/css/bootstrap.css";
import "bootstrap-vue/dist/bootstrap-vue.css";
import "ant-design-vue/dist/antd.css";
import axios from "axios";
import VueAxios from "vue-axios";

axios.defaults.baseURL = "http://localhost:5000/";

createApp(App).use(Antd).use(router).use(VueAxios, axios).mount("#app");
