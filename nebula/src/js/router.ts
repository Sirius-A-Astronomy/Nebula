import { nextTick } from "vue";
import {
	createRouter,
	createWebHistory,
	type RouteLocationNormalized,
} from "vue-router";
import { isAuthenticated } from "./stores/sessionStore";

import CoursesView from "@views/dashboard/courses/CourseIndex.vue";

const router = createRouter({
	history: createWebHistory(),
	routes: [
		{
			path: "/dashboard",
			redirect: "/dashboard/courses",
			name: "dashboard",
			meta: {
				title: "Dashboard - Courses",
				description: "View all courses in nebula",
				requiredAccessLevel: 3,
			},
		},

		{
			path: "/dashboard/courses/",
			component: CoursesView,
			name: "dashboard-course-index",
			meta: {
				title: "Dashboard - Courses",
				description: "View all courses in nebula",
				requiredAccessLevel: 3,
			},
		},

		{
			path: "/dashboard/courses/create",
			component: () =>
				import("@/views/dashboard/courses/CourseCreate.vue"),
			name: "test",
			meta: {
				title: "Dashboard - Test",
				description: "Create a new course in nebula",
				requiredAccessLevel: 3,
			},
		},

		{
			path: "/dashboard/course/:id",
			component: () => import("@views/dashboard/courses/CourseShow.vue"),
			name: "dashboard-course-show",
			meta: {
				title: "Dashboard - Course",
				description: "View a nebula course",
				requiredAccessLevel: 3,
			},
			props: true,
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
const authGuard = (to: RouteLocationNormalized): boolean => {
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
