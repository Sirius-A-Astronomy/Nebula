import Dashboard from "./Dashboard.vue";

import { createApp } from "vue";

import router from "@/router";

const app = createApp(Dashboard);

app.use(router);

app.mount("#app");
