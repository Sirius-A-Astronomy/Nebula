import { getAccessLevelValue } from "@stores/userStore";
import type { RouteRecordRaw } from "vue-router";

export const questionRoutes: RouteRecordRaw[] = [
  {
    path: "/questions/create",
    name: "question.create",
    component: () => import("@views/question/QuestionCreate.vue"),
    meta: {
      title: "Create Question",
      description: "Create a new question",
      requiredAccessLevel: getAccessLevelValue("moderator"),
    },
  },
];

export default questionRoutes;
