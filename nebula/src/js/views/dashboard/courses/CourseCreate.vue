<script setup lang="ts">
import CourseForm from "@components/course/CourseForm.vue";
import { ref } from "vue";

import { useRouter } from "vue-router";
import useFlash from "@stores/flashStore";

import { courseStore } from "@stores/courseStore";
import type { Course } from "@stores/courseStore";
import type { Updatable, New } from "@/stores/factory/storeFactory";

const router = useRouter();
const flash = useFlash();

const awaitingResponse = ref(false);

const submitCourse = async (course: Updatable<Course>) => {
	awaitingResponse.value = true;
	const response = await courseStore.actions.create(course as New<Course>);
	awaitingResponse.value = false;

	if (response.status !== 201) {
		flash.add(`Failed to create course: ${response.message}`, "error");
		return;
	}
	const data = response.data as Course;

	router.push({
		name: "dashboard-course-show",
		params: { id: data.id },
	});

	flash.add(`Course '${data.name}' created successfully`, "success");
	return;
};
</script>

<template>
	<div>
		<CourseForm
			submitText="Create"
			@submit="submitCourse"
			:awaiting-response="awaitingResponse"
			@cancel="$router.back()" />
	</div>
</template>

<style lang="scss" scoped></style>
