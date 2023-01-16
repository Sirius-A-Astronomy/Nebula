import type { RouteRecordRaw } from "vue-router";

export const baseRoutes: RouteRecordRaw[] = [
	{
		path: "/",
		name: "home",
		component: () => import("@views/main/Index.vue"),
		meta: {
			title: "Home",
			description: "Home page of nebula",
		},
	},
];

export default baseRoutes;
