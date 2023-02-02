import { computed } from "vue";
import type { StudyType } from "./courseLevelStore";
import { storeModuleFactory } from "./factory/storeFactory";

export type Course = {
    id: string;
    name: string;
    code: string;
    description: string;
    semester: string;
    course_level: {
        id: string;
        code: string;
        name: string;
        study_type: StudyType;
    };
    meta: Record<string, unknown>;
};

const courseStoreBase = storeModuleFactory<Course>("courses");

export const courseStore = {
    getters: {
        ...courseStoreBase.getters,
        byCourseLevelId: (id: string) =>
            computed(() => {
                return courseStoreBase.getters.all.value.filter(
                    (course) => course.course_level.id === id
                );
            }),
    },
    setters: {
        ...courseStoreBase.setters,
    },
    actions: {
        ...courseStoreBase.actions,
    },
    state: {
        ...courseStoreBase.state,
    },
};
