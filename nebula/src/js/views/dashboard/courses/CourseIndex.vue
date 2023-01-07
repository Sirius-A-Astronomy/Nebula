<script setup lang="ts">
import { courseStore } from "@stores/courseStore";
import { computed, onMounted, ref } from "vue";
import { RouterLink } from "vue-router";

import type { CourseLevelWithCourses } from "@/stores/courseLevelStore";

import CourseLevel from "./components/courseLevel.vue";

const filterCoursesInput = ref<HTMLInputElement | null>(null);

const courses = computed(() => {
	const courses = courseStore.getters.all.value;

	if (courseFilter.value) {
		return courses.filter((course) => {
			const filter = courseFilter.value.toLowerCase();
			if (course.name.toLowerCase().includes(filter)) return true;

			if (course.code.toLowerCase().includes(filter)) return true;

			if (course.course_level.name.toLowerCase().includes(filter))
				return true;

			if (course.course_level.study_type.toLowerCase().includes(filter))
				return true;

			return false;
		});
	}
	return courses;
});

const courseLevels = computed(() => {
	const levels: CourseLevelWithCourses[] = [];
	for (const course of courses.value) {
		const level = levels.find(
			(level) => level.id === course.course_level.id
		);

		if (!level) {
			levels.push({
				...course.course_level,
				courses: [course],
			});
		} else {
			if (!level.courses) {
				level.courses = [];
			}
			level.courses.push(course);
		}
	}

	// sort by study type
	levels.sort((a, b) => a.study_type.localeCompare(b.study_type));

	return levels;
});

const courseFilter = ref("");

const clearFilter = () => {
	courseFilter.value = "";
	filterCoursesInput.value?.focus();
};

onMounted(async () => {
	await courseStore.actions.getAll();
});
</script>

<template>
	<div>
		<div class="flex flex-row items-center gap-2 py-2">
			<h1 class="text-3xl">Courses</h1>
			<div class="ml-auto relative">
				<input
					class="w-full p-2 text-sm border-0 rounded-md input placeholder:text-secondary-text placeholder:font-semibold bg-secondary-bg focus:tertiary-bg focus:ring-primary-active"
					type="text"
					name="filter_courses"
					id="filter_courses"
					ref="filterCoursesInput"
					v-model="courseFilter"
					:placeholder="`Filter courses (${courses.length})`" />
				<!-- Clear button -->
				<button
					class="absolute inset-y-0 right-0 flex items-center pr-2"
					v-if="courseFilter.length > 0"
					@click.prevent="clearFilter">
					<svg
						class="w-4 h-4 hover:text-accent-focus"
						aria-hidden="true"
						fill="currentColor"
						viewBox="0 0 20 20">
						<path
							fill-rule="evenodd"
							d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.536-11.464a1 1 0 00-1.414 0L10 8.586 8.464 7.05a1 1 0 00-1.414 1.414l1.536 1.536-1.536 1.536a1 1 0 101.414 1.414L10 11.414l1.536 1.536a1 1 0 001.414-1.414L11.414 10l1.536-1.536a1 1 0 000-1.414z"
							clip-rule="evenodd" />
					</svg>
				</button>
			</div>
			<RouterLink
				to="/dashboard/courses/create"
				class="px-4 py-2 bg-primary-active text-primary-bg rounded-md font-bold hover:text-primary-text"
				>Create</RouterLink
			>
		</div>

		<ul class="flex flex-col gap-2 py-2">
			<CourseLevel
				v-for="level in courseLevels"
				:key="level.id"
				:level="level"></CourseLevel>
		</ul>
	</div>
</template>

<style lang="scss" scoped></style>
