<script setup lang="ts">
import type { CourseLevelWithCourses } from "@stores/courseLevelStore";
import CourseListItem from "./CourseListItem.vue";
import { ref } from "vue";
import { faChevronDown, faArrowRight } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";

defineProps<{
    level: CourseLevelWithCourses;
}>();

const expanded = ref(true);
</script>

<template>
    <li class="rounded-md bg-secondary-bg px-4 py-2">
        <div class="items center flex justify-between">
            <div class="justify-baseline flex flex-row items-center gap-1">
                <h2 class="text-2xl">
                    {{ level.study_type }} - {{ level.name }}
                </h2>

                <RouterLink
                    :to="{
                        name: 'course.level.show',
                        params: {
                            id: level.id,
                        },
                    }"
                    class="text-sm text-primary-text hover:text-accent-focus hover:underline"
                >
                    <FontAwesomeIcon :icon="faArrowRight" />
                </RouterLink>
            </div>

            <button
                @click="expanded = !expanded"
                :aria-label="`${expanded ? 'Hide' : 'Show'} courses from ${
                    level.study_type
                } - ${level.name}`"
            >
                <FontAwesomeIcon
                    :icon="faChevronDown"
                    class="transition-transform"
                    :class="{
                        '-rotate-180 transform': !expanded,
                    }"
                />
            </button>
        </div>
        <ul class="my-2 flex flex-col gap-2" v-if="expanded && level.courses">
            <li
                v-for="course in [...level.courses].sort((a, b) =>
                    a.semester.localeCompare(b.semester)
                )"
                :key="course.id"
                class="flex flex-col transition-colors duration-75 hover:text-accent-clr"
            >
                <CourseListItem :course="course" />
            </li>
        </ul>
    </li>
</template>

<style lang="scss" scoped></style>
