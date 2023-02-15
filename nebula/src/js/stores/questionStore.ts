import { storeModuleFactory } from "@stores/factory/storeFactory";
import type { Course } from "@stores/courseStore";
import type { SubjectTag } from "@stores/subjectTagStore";
import type { User } from "@stores/userStore";
import { computed } from "vue";
import api from "@/http/api";
import type { MetaData } from "@/types";

export type Answer = {
    id: string;
    content: string;
    title: string;
    sources: string[];
    user: User;
    question_id: string;
    meta: MetaData;
};

export type Comment = {
    id: string;
    content: string;
    user: User;
    question_id: string;
    is_suggestion: boolean;
    meta: MetaData;
};

export type Question = {
    id: string;
    title: string;
    content: string;
    course: Course;
    subject_tags?: SubjectTag[];
    answers?: Answer[];
    comments?: Comment[];
    user: User;
    meta: MetaData;
};

export type UpdatedQuestion = {
    id: string;
    title: string;
    content: string;
    course_id: string;
    subject_tags: string[];
    answers: NewAnswer[];
};

export type NewQuestion = {
    title: string;
    content: string;
    course_id: string;
    subject_tags: string[];
    answers: NewAnswer[];
};

export type NewAnswer = {
    title: string;
    content: string;
    id: string;
};

export const questionStoreBase = storeModuleFactory<Question>("questions");

const lastLoadPerCourse: { [courseId: string]: number } = {};

export const questionStore = {
    getters: {
        ...questionStoreBase.getters,
        byCourseId: (courseId: string) =>
            computed(() => {
                return questionStoreBase.getters.all.value.filter(
                    (question) => question.course.id === courseId
                );
            }),
    },

    setters: {
        ...questionStoreBase.setters,
    },

    actions: {
        ...questionStoreBase.actions,
        getByCourseId: async (courseId: string) => {
            const response = await questionStoreBase.actions.getByFilter({
                course: courseId,
            });

            if (response.ok) {
                // replace questions with given course id
                for (const question of response.data) {
                    questionStoreBase.setters.setById(question.id, question);
                }
                lastLoadPerCourse[courseId] = Date.now();
            }
        },
        addComment: async (questionId: string, comment: string) => {
            const response = await api.post<Question, { content: string }>(
                `questions/${questionId}/comments`,
                {
                    content: comment,
                }
            );

            if (response.ok) {
                const question = response.data;

                questionStoreBase.setters.setById(question.id, question);
            }

            return response;
        },
        updateComment: async (
            questionId: string,
            commentId: string,
            commentContent: string
        ) => {
            const response = await api.put<
                Question,
                { content: string; id: string }
            >(`questions/${questionId}/comments/${commentId}`, {
                content: commentContent,
                id: commentId,
            });

            if (response.ok) {
                const question = response.data;

                questionStoreBase.setters.setById(question.id, question);
            }

            return response;
        },
        deleteComment: async (questionId: string, commentId: string) => {
            const response = await api.delete<Question>(
                `questions/${questionId}/comments/${commentId}`
            );

            if (response.ok) {
                const question = response.data;

                questionStoreBase.setters.setById(question.id, question);
            }

            return response;
        },
    },

    state: {
        ...questionStoreBase.state,
        shouldLoadByCourseId: (courseId: string) => {
            const now = Date.now();

            const shouldForceReload = !questionStoreBase.state.isValid.value;
            if (shouldForceReload) {
                return true;
            }

            const isAllLoaded = questionStoreBase.state.loadedAll.value;
            const isAllStale =
                now - questionStoreBase.state.lastLoad.value > 1000 * 60 * 5;

            // Don't load per course if all questions are loaded
            if (isAllLoaded && !isAllStale) {
                return false;
            }

            const isCourseLoaded = lastLoadPerCourse[courseId] !== undefined;

            const isCourseStale =
                now - lastLoadPerCourse[courseId] > 1000 * 60 * 5;

            // Don't load per course if that has been loaded recently
            if (isCourseLoaded && !isCourseStale) {
                return false;
            }

            return true;
        },
    },
};

export default questionStore;
