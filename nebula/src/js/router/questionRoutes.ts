import { getAccessLevelValue } from "@stores/userStore";
import type { RouteRecordRaw } from "vue-router";

import { canEditQuestion } from "@/lib/permissionHelpers";

import useFlashStore from "@stores/flashStore";

const flash = useFlashStore();

export const questionRoutes: RouteRecordRaw[] = [
    {
        path: "/questions/create",
        name: "question.create",
        component: () => import("@/views/question/QuestionEditCreate.vue"),
        meta: {
            title: "Create Question",
            description: "Create a new question",
            requiredAccessLevel: getAccessLevelValue("moderator"),
        },
    },

    {
        path: "/questions/:id/edit",
        name: "question.edit",
        component: () => import("@/views/question/QuestionEditCreate.vue"),
        props: true,
        beforeEnter: async (to, from, next) => {
            let questionId = to.params.id;

            if (typeof questionId !== "string" && questionId?.[0]) {
                questionId = questionId[0] as string;
            }
            questionId = questionId as string;
            if (await canEditQuestion(questionId)) {
                next();
            } else {
                flash.add(
                    "You do not have permission to edit this question.",
                    "warning"
                );
                next({ name: "question.show", params: { id: to.params.id } });
            }
        },
        meta: {
            title: "Edit Question",
            description: "Edit a question",
            requiredAccessLevel: getAccessLevelValue("moderator"),
        },
    },

    {
        path: "/questions/:id",
        name: "question.show",
        component: () => import("@views/question/QuestionShow.vue"),
        props: true,
        meta: {
            title: "Question",
            description: "View a question",
        },
    },
];

export default questionRoutes;
