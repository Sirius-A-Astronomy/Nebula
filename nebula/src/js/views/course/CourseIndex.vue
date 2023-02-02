<script setup lang="ts">
import type { Course } from "@stores/courseStore";
import { computed, onMounted, ref } from "vue";
import { RouterLink } from "vue-router";

import { courseStore } from "@stores/courseStore";
import { courseLevelStore } from "@/stores/courseLevelStore";

import CourseLevelListItem from "./components/CourseLevelListItem.vue";

const filterCoursesInput = ref<HTMLInputElement | null>(null);

const courseLevels = courseLevelStore.getters.all;

const courseLevelsWithCourses = computed(() => {
    return courseLevels.value.map((courseLevel) => {
        const filter = courseFilter.value.toLowerCase();
        let courses: Course[];
        if (courseLevel.name.toLowerCase().includes(filter) || filter == "")
            courses = courseStore.getters.byCourseLevelId(courseLevel.id).value;
        else {
            courses = courseStore.getters
                .byCourseLevelId(courseLevel.id)
                .value.filter((course: Course) => {
                    if (course.name.toLowerCase().includes(filter)) return true;

                    if (course.description.toLowerCase().includes(filter))
                        return true;

                    if (course.code.toLowerCase().includes(filter)) return true;
                });
        }
        return {
            ...courseLevel,
            courses,
        };
    });
});

const courseFilter = ref("");

const clearFilter = () => {
    courseFilter.value = "";
    filterCoursesInput.value?.focus();
};

const coursesAmount = computed(() => {
    return courseStore.getters.all.value.length;
});

onMounted(async () => {
    const promises = [];
    if (courseStore.state.shouldLoadAll()) {
        promises.push(courseStore.actions.getAll());
    }
    if (courseLevelStore.state.shouldLoadAll()) {
        promises.push(courseLevelStore.actions.getAll());
    }
    await Promise.all(promises);
});
</script>

<template>
    <main id="content" class="container">
        <div class="flex flex-row items-center gap-2 py-2">
            <h1 class="text-3xl">Courses</h1>
            <div class="relative ml-auto">
                <input
                    class="input focus:tertiary-bg w-full rounded-md border-0 bg-secondary-bg p-2 text-sm placeholder:font-semibold placeholder:text-secondary-text focus:ring-primary-active"
                    type="text"
                    name="filter_courses"
                    id="filter_courses"
                    ref="filterCoursesInput"
                    v-model="courseFilter"
                    :placeholder="`Filter courses (${coursesAmount})`"
                />
                <!-- Clear button -->
                <button
                    class="absolute inset-y-0 right-0 flex items-center pr-2"
                    v-if="courseFilter.length > 0"
                    @click.prevent="clearFilter"
                >
                    <svg
                        class="h-4 w-4 hover:text-accent-focus"
                        aria-hidden="true"
                        fill="currentColor"
                        viewBox="0 0 20 20"
                    >
                        <path
                            fill-rule="evenodd"
                            d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.536-11.464a1 1 0 00-1.414 0L10 8.586 8.464 7.05a1 1 0 00-1.414 1.414l1.536 1.536-1.536 1.536a1 1 0 101.414 1.414L10 11.414l1.536 1.536a1 1 0 001.414-1.414L11.414 10l1.536-1.536a1 1 0 000-1.414z"
                            clip-rule="evenodd"
                        />
                    </svg>
                </button>
            </div>
        </div>

        <ul class="flex flex-col gap-2 py-2">
            <CourseLevelListItem
                v-for="level in courseLevelsWithCourses"
                :key="level.id"
                :level="level"
            ></CourseLevelListItem>
        </ul>
    </main>
</template>

<style lang="scss" scoped></style>
