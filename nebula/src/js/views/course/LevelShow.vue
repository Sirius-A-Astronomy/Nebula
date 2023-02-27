<script setup lang="ts">
import { courseLevelStore } from "@stores/courseLevelStore";
import { courseStore } from "@stores/courseStore";
import {
    ref,
    computed,
    watch,
    onMounted,
    type ComputedRef,
    nextTick,
} from "vue";
import BreadCrumbs, { type BreadCrumb } from "@/components/BreadCrumbs.vue";
import CourseListItem from "@views/course/components/CourseListItem.vue";

import useFlashStore from "@stores/flashStore";
import type { ApiResponse } from "@/http/api";

const flash = useFlashStore();
const props = defineProps<{
    id: string;
}>();

const courseLevel = computed(
    () => courseLevelStore.getters.byId(props.id).value
);

const courses = computed(() =>
    courseStore.getters.byCourseLevelId(props.id).value.filter((course) => {
        if (!courseFilter.value) {
            return true;
        }

        const filter = courseFilter.value.toLowerCase();

        if (course.name.toLowerCase().includes(filter)) {
            return true;
        }

        if (course.description.toLowerCase().includes(filter)) {
            return true;
        }

        if (course.code.toLowerCase().includes(filter)) {
            return true;
        }

        return false;
    })
);

watch(props, () => {
    loading.value = true;
    loadData();
});

const loading = ref(true);

const loadData = async () => {
    const promises: Promise<ApiResponse<any>>[] = [];
    if (!courseLevelStore.getters.byId(props.id).value) {
        promises.push(courseLevelStore.actions.getById(props.id));
    }

    if (!courseStore.getters.byCourseLevelId(props.id).value) {
        promises.push(courseStore.actions.getByCourseLevelId(props.id));
    }

    const results = await new Promise<ApiResponse<any>[]>((resolve) => {
        Promise.all(promises).then((res) => {
            resolve(res);
        });
    });

    for (const result of results) {
        if (!result.ok) {
            flash.add(`Error loading course level: ${result.message}`, "error");
        }
    }

    nextTick(() => {
        document.title = courseLevel.value.name
            ? `${courseLevel.value.study_type} ${courseLevel.value?.name} | Nebula`
            : "Course Level | Nebula";
    });

    loading.value = false;
};

const breadcrumbs: ComputedRef<BreadCrumb[]> = computed(() => {
    if (!courseLevel.value) {
        return [];
    }

    return [
        {
            name: "Courses",
            to: {
                name: "course.index",
            },
        },
        {
            name: courseLevel.value.name,
            to: {
                name: "course.level.show",
                params: { id: courseLevel.value.id },
            },
        },
    ];
});

const courseFilter = ref("");

onMounted(() => {
    loadData();
});
</script>

<template>
    <main id="content">
        <div
            v-if="loading"
            class="container flex h-full w-full items-center justify-center"
        >
            Loading...
        </div>
        <div v-else class="container py-2">
            <BreadCrumbs :breadcrumbs="breadcrumbs" class="pt-2 pb-4" />
            <section class="rounded-md bg-secondary-bg px-4 py-2">
                <div>
                    <h1 class="text-3xl font-bold">
                        {{ courseLevel.study_type }} {{ courseLevel.name }}
                    </h1>
                    <div class="flex flex-row">
                        <span class="flex-[1_1_60%]">
                            {{ courses.length }} Course{{
                                courses.length !== 1 ? "s" : ""
                            }}
                        </span>
                        <input
                            class="search-bar input w-full flex-[1_0_20rem] rounded-md border-0 bg-tertiary-bg p-2 text-sm placeholder:font-semibold placeholder:text-secondary-text focus:bg-primary-bg focus:ring-primary-active"
                            id="course-search-input-field"
                            type="text"
                            :placeholder="`Search in ${courseLevel.study_type} ${courseLevel.name}...`"
                            v-model="courseFilter"
                        />
                    </div>
                </div>
                <div class="py-2">
                    <div
                        v-if="courses.length === 0"
                        class="text-center text-secondary-text"
                    >
                        No courses found
                    </div>
                    <ul v-else class="flex flex-col gap-2">
                        <li
                            v-for="course in courses"
                            class="transition-colors duration-75 hover:text-accent-clr"
                            :key="course.id"
                        >
                            <CourseListItem :course="course" />
                        </li>
                    </ul>
                </div>
            </section>
        </div>
    </main>
</template>

<style lang="scss" scoped></style>
