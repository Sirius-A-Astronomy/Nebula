<script setup lang="ts">
import type { CourseLevelWithCourses } from "@stores/courseLevelStore";
import { ref } from "vue";

defineProps<{
    level: CourseLevelWithCourses;
}>();

const expanded = ref(true);

const navigate = (url: string) => {
    window.location.href = url;
};
</script>

<template>
    <li>
        <div class="items center flex justify-between">
            <div class="flex flex-col">
                <h2 class="text-2xl">
                    {{ level.study_type }} - {{ level.name }}
                </h2>

                <RouterLink
                    :to="{
                        name: 'dashboard.courseLevel.show',
                        params: {
                            id: level.id,
                        },
                    }"
                    class="text-sm text-accent-clr hover:text-accent-focus hover:underline"
                >
                    <span>Show course level</span>
                </RouterLink>
            </div>

            <button
                @click="expanded = !expanded"
                :aria-label="`${expanded ? 'Hide' : 'Show'} courses from ${
                    level.study_type
                } - ${level.name}`"
            >
                <svg
                    xmlns="http://www.w3.org/2000/svg"
                    height="24"
                    fill="currentColor"
                    class="transition-transform"
                    :class="expanded ? '' : 'rotate-180'"
                    width="24"
                >
                    <path d="m12 15.375-6-6 1.4-1.4 4.6 4.6 4.6-4.6 1.4 1.4Z" />
                </svg>
            </button>
        </div>
        <ul class="my-2 flex flex-col gap-2" v-if="expanded && level.courses">
            <li
                v-for="course in [...level.courses].sort((a, b) =>
                    a.semester.localeCompare(b.semester)
                )"
                :key="course.id"
                class="flex flex-col rounded-md bg-secondary-bg px-4 py-2 transition-colors duration-75 hover:bg-tertiary-bg"
            >
                <RouterLink :to="`/dashboard/course/${course.id}`">
                    <div class="flex flex-row items-start justify-between">
                        <span class="text-primary text-xl">{{
                            course.name
                        }}</span>

                        <span class="text-primary text-sm">
                            Semester: {{ course.semester }}</span
                        >
                    </div>

                    <div class="flex flex-row items-start justify-between">
                        <span class="text-primary text-sm">{{
                            course.description
                        }}</span>
                    </div>

                    <a
                        :href="`/q/${course.course_level.code}/${course.code}`"
                        class="text-sm text-accent-clr hover:text-accent-focus hover:underline"
                        @click.prevent="
                            // prevent parent link from being triggered
                            navigate(
                                `/q/${course.course_level.code}/${course.code}`
                            )
                        "
                        >View in Nebula</a
                    >
                </RouterLink>
            </li>
        </ul>
    </li>
</template>

<style lang="scss" scoped></style>
