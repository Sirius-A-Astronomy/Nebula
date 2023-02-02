import { storeModuleFactory } from "@stores/factory/storeFactory";
import type { Course } from "@stores/courseStore";
import type { SubjectTag } from "@stores/subjectTagStore";
import type { User } from "@stores/userStore";
import { computed } from "vue";

export type Answer = {
    id: string;
    content: string;
    title: string;
    sources: string[];
    user: User;
    question_id: string;
};

export type Comment = {
    id: string;
    content: string;
    user: User;
    question_id: string;
    is_suggestion: boolean;
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
};

export const questionStoreBase = storeModuleFactory<Question>("questions");

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
    },

    state: {
        ...questionStoreBase.state,
    },
};

export default questionStore;
