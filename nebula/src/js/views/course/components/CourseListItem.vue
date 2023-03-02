<script setup lang="ts">
import type { Course } from "@stores/courseStore";
import { RouterLink } from "vue-router";

defineProps<{
    course: Course;
}>();
</script>

<template>
    <RouterLink
        :to="{
            name: 'course.show',
            params: {
                id: course.id,
            },
        }"
    >
        <div class="flex flex-row items-start justify-between">
            <span class="text-primary text-xl">{{ course.name }}</span>

            <!-- <span class="text-primary text-sm"> Semester: {{ course.semester }}</span> -->
            <span
                class="text-primary whitespace-nowrap text-sm"
                v-if="course.meta?.questions_count"
                >Questions: {{ course.meta.questions_count }}
            </span>
        </div>

        <div class="flex flex-row items-start justify-between">
            <span class="text-primary text-sm">{{ course.description }}</span>
        </div>
    </RouterLink>
</template>

<style lang="scss" scoped></style>
