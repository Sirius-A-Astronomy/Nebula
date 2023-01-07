import { nextTick } from "vue";
import {
	createRouter,
	createWebHistory,
	type RouteLocationNormalized,
} from "vue-router";
import { isAuthenticated, authenticatedUser } from "./stores/sessionStore";

import { accessLevels } from "@stores/userStore";

import CoursesView from "@views/dashboard/courses/CourseIndex.vue";
import useFlashStore from "@stores/flashStore";

const flash = useFlashStore();

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
			name: "dashboard.course.index",
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
			name: "dashboard.course.create",
			meta: {
				title: "Dashboard - Test",
				description: "Create a new course in nebula",
				requiredAccessLevel: 3,
			},
		},

		{
			path: "/dashboard/course/:id",
			component: () => import("@views/dashboard/courses/CourseShow.vue"),
			name: "dashboard.course.show",
			meta: {
				title: "Course",
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

		{
			path: "/dashboard/users/",
			component: () => import("@views/dashboard/users/UserIndex.vue"),
			name: "dashboard.user.index",
			meta: {
				title: "Users",
				description: "View all users in nebula",
				requiredAccessLevel: 3,
			},
		},

		{
			path: "/dashboard/users/create",
			component: () => import("@views/dashboard/users/UserCreate.vue"),
			name: "dashboard.user.create",
			meta: {
				title: "Create User",
				description: "Create a new user in nebula",
				requiredAccessLevel: 3,
			},
		},

		{
			path: "/dashboard/user/:id",
			component: () => import("@views/dashboard/users/UserShow.vue"),
			name: "dashboard.user.show",
			meta: {
				title: "User",
				description: "View a nebula user",
				requiredAccessLevel: 3,
			},
			props: true,
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

	if (to.meta.requiredAccessLevel) {
		const requiredAccessLevel = to.meta.requiredAccessLevel as number;
		if (authenticatedUser.value.access_level < requiredAccessLevel) {
			const requiredAccessLevelName = accessLevels.find(
				(level) => level.value === requiredAccessLevel
			)?.name;

			flash.add(
				`You must be a ${requiredAccessLevelName} to view this page`,
				"danger"
			);
			return false;
		}
	}

	return true;
};

router.beforeEach(authGuard);

export default router;
