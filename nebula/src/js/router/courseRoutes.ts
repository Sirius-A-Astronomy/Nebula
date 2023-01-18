import type { RouteRecordRaw } from "vue-router";

export const courseRoutes: RouteRecordRaw[] = [
	{
		path: "/courses",
		name: "course.index",
		component: () => import("@views/course/CourseIndex.vue"),
		meta: {
			title: "Courses",
			description: "List of courses",
		},
	},
	{
		path: "/courses/:id",
		name: "course.show",
		component: () => import("@views/course/CourseShow.vue"),
		meta: {
			title: "Course",
			description: "Course details",
		},
	},
	{
		path: "/courses/levels/:id",
		name: "course.level.show",
		component: () => import("@views/course/LevelShow.vue"),
		meta: {
			title: "Course Level",
			description: "Course level details",
		},
	},
];

export default courseRoutes;
