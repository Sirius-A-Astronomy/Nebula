import { fetchUser, FetchUserFailedError } from "@/stores/sessionStore";
import Dashboard from "@/dashboard/Dashboard.vue";
import { createApp } from "vue";
import router from "@/router";

// try to login, start as early as possible
// using IIFE to have "top level" await
(async () => {
	try {
		await fetchUser();
	} catch (e) {
		console.log("Error fetching logged in user", e);
	}

	const app = createApp(Dashboard);

	app.use(router);

	app.mount("#app");
})();
