<script setup lang="ts">
import type { Question, Answer } from "@stores/questionStore";
import type { New, Updatable } from "@stores/factory/storeFactory";
import { ref, reactive, type Ref, onMounted, computed } from "vue";

import MarkdownEditor from "../MarkdownEditor.vue";

import { courseStore } from "@stores/courseStore";

const props = defineProps<{
	question?: Updatable<Question>;
	submitText: string;
	awaitingResponse?: boolean;
}>();

const emit = defineEmits<{
	(e: "submit", course: Updatable<Question>): void;
	(e: "cancel"): void;
}>();

const values = ref({
	title: props.question?.title ?? "",
	content: props.question?.content ?? "",
	answers: props.question?.answers ?? [],
	course: {
		id: props.question?.course?.id ?? "",
	},
	subject_tags: props.question?.subject_tags ?? [],
});

const errors = reactive({
	title: "",
	content: "",
	answers: "",
	course_id: "",
	subject_tags: "",
});

const loading = ref(false);

const courses = computed(() =>
	courseStore.getters.all.value.sort((a, b) =>
		a.course_level.name.localeCompare(b.course_level.name)
	)
);

const loadData = async () => {
	if (courses.value.length === 0) {
		await courseStore.actions.getAll();
	}
	loading.value = false;
};

onMounted(loadData);

const submit = async () => {
	emit("submit", { ...values.value, id: props.question?.id });
};
</script>

<template>
	<div>
		<div class="flex flex-row justify-between items-center">
			<h1 class="text-3xl">
				{{ props.question ? "Edit" : "Create" }} Question
			</h1>

			<button
				@click="emit('cancel')"
				class="px-4 py-2 bg-primary-active text-primary-bg rounded-md font-bold hover:text-primary-text">
				Cancel
			</button>
		</div>

		<form class="flex flex-col gap-2" @submit.prevent="submit">
			<div class="flex flex-col">
				<label for="course_id" class="text-base font-bold"
					>Course</label
				>
				<select
					name="course_id"
					id="course_id"
					class="border-2 focus:border-primary-active border-primary-bg px-2 py-1 rounded-md focus:outline-none transition-colors bg-secondary-bg focus:bg-tertiary-bg focus:ring-primary-active"
					v-model="values.course.id">
					<option value="" disabled selected>Select a course</option>
					<option v-for="course in courses" :value="course.id">
						{{ course.name }}
					</option>
				</select>
			</div>

			<MarkdownEditor
				v-model="values.title"
				title="Title"
				:options="{
					maxRows: 1,
				}" />

			<MarkdownEditor v-model="values.content" title="Content" />

			<button
				type="submit"
				class="px-4 py-2 bg-primary-clr text-on-primary-text rounded-md font-bold hover:bg-primary-active hover:text-primary-bg focus:text-primary-bg focus:bg-primary-active transition-colors"
				:disabled="loading || awaitingResponse">
				{{
					awaitingResponse
						? "Loading..."
						: props.submitText
						? props.submitText
						: "Submit"
				}}
			</button>
		</form>
	</div>
</template>

<style lang="scss" scoped></style>
