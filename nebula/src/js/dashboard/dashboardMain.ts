// try to login, start as early as possible
try {
	await fetchUser();
} catch (e) {
	console.log("Error fetching logged in user", e);
}

import Dashboard from "@/dashboard/Dashboard.vue";
import { createApp } from "vue";
import router from "@/router";
import { fetchUser, FetchUserFailedError } from "@/stores/sessionStore";

const app = createApp(Dashboard);

app.use(router);

app.mount("#app");
