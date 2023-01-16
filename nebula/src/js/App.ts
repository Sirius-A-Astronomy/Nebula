import { fetchUser } from "@/stores/sessionStore";
import App from "@/App.vue";
import { createApp } from "vue";
import router from "@/router";

// try to login, start as early as possible
// using IIFE to have "top level" await
(async () => {
	try {
		await fetchUser();
	} catch (e) {
		console.log("Not logged in", e);
	}

	const app = createApp(App);

	app.use(router);

	app.mount("#app");
})();
