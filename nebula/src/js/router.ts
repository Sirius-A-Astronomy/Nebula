import { createRouter, createWebHistory } from "vue-router";

import CoursesView from "./views/dashboard/CoursesView.vue";

const router = createRouter({
	history: createWebHistory(),
	routes: [
		{
			path: "/dashboard",
			component: CoursesView,
			name: "dashboard",
		},

		{
			path: "/dashboard/test",
			component: () => import("./views/dashboard/TestView.vue"),
			name: "test",
		},
	],
});

export default router;
