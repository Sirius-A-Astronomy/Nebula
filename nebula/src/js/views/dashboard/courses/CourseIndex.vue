<script setup lang="ts">
import { courseStore, type Course } from "@stores/courseStore";
import { computed, onMounted } from "vue";
import { RouterLink } from "vue-router";

import type { CourseLevel } from "@/stores/courseLevelStore";

type CourseLevelWithCourses = CourseLevel & {
	courses?: Course[];
	expanded?: boolean;
};

const courses = courseStore.getters.all;

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

onMounted(async () => {
	await courseStore.actions.getAll();
});

const navigate = (url: string) => {
	window.location.href = url;
};
</script>

<template>
	<div>
		<div class="flex flex-row justify-between items-center">
			<h1 class="text-3xl">Courses</h1>
			<RouterLink
				to="/dashboard/courses/create"
				class="px-4 py-2 bg-primary-active text-primary-bg rounded-md font-bold hover:text-primary-text"
				>Create</RouterLink
			>
		</div>

		<ul class="flex flex-col gap-2">
			<li v-for="level in courseLevels" :key="level.id">
				<h2 class="text-2xl">
					{{ level.study_type }} - {{ level.name }}
				</h2>
				<ul class="flex flex-col gap-2 my-2">
					<li
						v-for="course in level.courses?.sort((a, b) =>
							a.semester.localeCompare(b.semester)
						)"
						:key="course.id"
						class="flex flex-col bg-secondary-bg hover:bg-tertiary-bg px-4 py-2 rounded-md transition-colors duration-75">
						<RouterLink :to="`/dashboard/course/${course.id}`">
							<div
								class="flex flex-row justify-between items-start">
								<span class="text-primary text-xl">{{
									course.name
								}}</span>

								<span class="text-primary text-sm">
									Semester: {{ course.semester }}</span
								>
							</div>

							<div
								class="flex flex-row justify-between items-start">
								<span class="text-primary text-sm">{{
									course.description
								}}</span>
							</div>

							<a
								:href="`/q/${course.course_level.code}/${course.code}`"
								@click.prevent="
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
		</ul>
	</div>
</template>

<style lang="scss" scoped></style>
