import { nextTick } from "vue";
import { createRouter, createWebHistory } from "vue-router";
import { isAuthenticated } from "./stores/sessionStore";

import CoursesView from "./views/dashboard/CoursesView.vue";

const router = createRouter({
	history: createWebHistory(),
	routes: [
		{
			path: "/dashboard",
			component: CoursesView,
			name: "dashboard",
			meta: {
				title: "Dashboard - Courses",
				requiredAccessLevel: 3,
			},
		},

		{
			path: "/dashboard/test",
			component: () => import("./views/dashboard/TestView.vue"),
			name: "test",
			meta: {
				title: "Dashboard - Test",
				requiredAccessLevel: 3,
			},
		},

		{
			// Change the window location here to do a full page reload
			path: "/login",
			name: "login",
			component: () => null,
			beforeEnter: () => {
				window.location.href = "/login";
			},
		},
	],
});

router.afterEach((to) => {
	nextTick(() => {
		document.title = (to.meta.title as string) || "Nebula";
	});
});
const excludedRoutes: string[] = [];
const authGuard = (to, from) => {
	if (
		!(isAuthenticated.value || excludedRoutes.includes(to.name as string))
	) {
		// flash.add("You must be logged in to view this page", "danger", 5000);
		document.location.href = "/login";
	}
	return true;
};

router.beforeEach(authGuard);

export default router;
