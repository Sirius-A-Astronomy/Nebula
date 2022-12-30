<script setup lang="ts">
import { courseLevelStore, type CourseLevel } from "@stores/courseLevelStore";
import type { Course } from "@stores/courseStore";
import type { New, Updatable } from "@stores/factory/storeFactory";
import { ref, reactive, type Ref, onMounted, computed } from "vue";

const props = defineProps<{
	course?: Updatable<Course>;
	submitText: string;
	awaitingResponse?: boolean;
}>();

const emit = defineEmits<{
	(e: "submit", course: Updatable<Course>): void;
	(e: "cancel"): void;
}>();

const semesters = [
	{ value: "1", text: "1" },
	{ value: "1a", text: "1a" },

	{ value: "1b", text: "1b" },
	{ value: "2", text: "2" },
	{ value: "2a", text: "2a" },
	{ value: "2b", text: "2b" },
];

const values: Ref<Updatable<Course>> = ref({
	name: props.course?.name ?? "",
	code: props.course?.code ?? "",
	description: props.course?.description ?? "",
	course_level: {
		id: props.course?.course_level?.id ?? "",
	},
	semester: props.course?.semester ?? "",
});

const errors = reactive({
	name: "",
	code: "",
	description: "",
	course_level_id: "",
	semester: "",
});

const loading = ref(false);

const courseLevels = computed(() =>
	courseLevelStore.getters.all.value.sort((a, b) =>
		a.study_type.localeCompare(b.study_type)
	)
);

const loadData = async () => {
	if (courseLevels.value.length === 0) {
		await courseLevelStore.actions.getAll();
	}
	loading.value = false;
};

onMounted(loadData);

const submit = async () => {
	emit("submit", { ...values.value, id: props.course?.id });
};
</script>

<template>
	<div>
		<div class="flex flex-row justify-between items-center">
			<h1 class="text-3xl">
				{{ props.course ? "Edit" : "Create" }} Course
			</h1>

			<button
				@click="emit('cancel')"
				class="px-4 py-2 bg-primary-active text-primary-bg rounded-md font-bold hover:text-primary-text">
				Cancel
			</button>
		</div>

		<form class="flex flex-col gap-2" @submit.prevent="submit">
			<div class="flex flex-col gap-2">
				<label for="name" class="text-xl font-bold">Name</label>
				<input
					type="text"
					name="name"
					id="name"
					class="border-2 focus:border-primary-active border-primary-bg px-2 py-1 rounded-md focus:outline-none transition-colors"
					v-model="values.name" />
				<p v-if="errors.name" class="text-red-500 text-sm">
					{{ errors.name }}
				</p>
			</div>

			<div class="flex flex-col gap-2">
				<label for="code" class="text-xl font-bold">Code</label>
				<input
					type="text"
					name="code"
					id="code"
					class="border-2 focus:border-primary-active border-primary-bg px-2 py-1 rounded-md focus:outline-none transition-colors"
					v-model="values.code" />
				<p v-if="errors.code" class="text-red-500 text-sm">
					{{ errors.code }}
				</p>
			</div>

			<div class="flex flex-col gap-2">
				<label for="description" class="text-xl font-bold"
					>Description</label
				>
				<textarea
					type="text"
					name="description"
					id="description"
					rows="5"
					class="border-2 focus:border-primary-active border-primary-bg px-2 py-1 rounded-md focus:outline-none transition-colors"
					v-model="values.description" />
				<p v-if="errors.description" class="text-red-500 text-sm">
					{{ errors.description }}
				</p>
			</div>

			<div class="flex flex-col gap-2">
				<label for="semester" class="text-xl font-bold">Semester</label>
				<select
					name="semester"
					id="semester"
					class="border-2 focus:border-primary-active border-primary-bg px-2 py-1 rounded-md focus:outline-none transition-colors"
					v-model="values.semester">
					<option value="" disabled selected>
						Select a semester
					</option>
					<option
						v-for="semester in semesters"
						:value="semester.value">
						{{ semester.text }}
					</option>
				</select>
			</div>

			<div class="flex flex-col gap-2">
				<label for="course_level_id" class="text-xl font-bold"
					>Course Level</label
				>
				<select
					name="course_level_id"
					id="course_level_id"
					class="border-2 focus:border-primary-active border-primary-bg px-2 py-1 rounded-md focus:outline-none transition-colors"
					v-model="values.course_level!.id">
					<option value="" disabled selected>
						Select a course level
					</option>
					<option
						v-for="courseLevel in courseLevels"
						:value="courseLevel.id"
						:key="courseLevel.id">
						{{ courseLevel.study_type }} - {{ courseLevel.name }}
					</option>
				</select>
				<p v-if="errors.course_level_id" class="text-red-500 text-sm">
					{{ errors.course_level_id }}
				</p>
			</div>

			<button
				type="submit"
				class="px-4 py-2 bg-primary-clr text-on-primary-text rounded-md font-bold hover:bg-primary-active hover:text-primary-bg transition-colors"
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
