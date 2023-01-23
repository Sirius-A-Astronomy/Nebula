import { nextTick } from "vue";
import {
  createRouter,
  createWebHistory,
  type RouteLocationNormalized,
} from "vue-router";
import { isAuthenticated, authenticatedUser } from "@stores/sessionStore";

import { accessLevels } from "@stores/userStore";

import CoursesView from "@views/dashboard/courses/CourseIndex.vue";
import useFlashStore from "@stores/flashStore";

import baseRoutes from "./baseRoutes";
import courseRoutes from "./courseRoutes";
import userRoutes from "./userRoutes";

const flash = useFlashStore();

const router = createRouter({
  history: createWebHistory(),
  routes: [
    ...baseRoutes,
    ...courseRoutes,
    ...userRoutes,
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
      component: () => import("@/views/dashboard/courses/CourseCreate.vue"),
      name: "dashboard.course.create",
      meta: {
        title: "Dashboard - Create Course",
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

    {
      path: "/dashboard/course-level/:id",
      name: "dashboard.courseLevel.show",
      component: () =>
        import("@/views/dashboard/courseLevels/CourseLevelShow.vue"),
      props: true,
      meta: {
        title: "Course Level",
        description: "View a course level",
        requiredAccessLevel: 3,
      },
    },

    {
      path: "/dashboard/questions",
      name: "dashboard.question.index",
      component: () => import("@/views/dashboard/questions/QuestionIndex.vue"),
      meta: {
        title: "Questions",
        description: "View all questions in nebula",
        requiredAccessLevel: 3,
      },
    },

    {
      path: "/dashboard/question/:id",
      name: "dashboard.question.show",
      component: () => import("@/views/dashboard/questions/QuestionShow.vue"),
      props: true,
      meta: {
        title: "Question",
        description: "View a question",
        requiredAccessLevel: 3,
      },
    },

    {
      path: "/dashboard/question/create",
      name: "dashboard.question.create",
      component: () => import("@views/dashboard/questions/QuestionCreate.vue"),
      meta: {
        title: "Create Question",
        description: "Create a new question in nebula",
        requiredAccessLevel: 1,
      },
    },
  ],
});

router.afterEach((to) => {
  nextTick(() => {
    document.title = (to.meta.title as string) || "Nebula";
  });
});
const protectedRoutes: string[] = [];

// protect all routes that start with name 'dashboard'
const protectedRoutesStartsWith: string[] = ["dashboard"];

const authGuard = (to: RouteLocationNormalized): boolean => {
  if (
    to.name &&
    (protectedRoutes.includes(to.name as string) ||
      protectedRoutesStartsWith.some((route) =>
        (to.name as string).startsWith(route)
      )) &&
    !isAuthenticated.value
  ) {
    flash.add("You must be logged in to view this page", "danger");
    document.location.href = "/login";
    return false;
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
