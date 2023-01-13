<script setup lang="ts">
import { courseLevelStore, studyTypes } from "@stores/courseLevelStore";
import type { CourseLevel, StudyType } from "@stores/courseLevelStore";
import type { New, Updatable } from "@stores/factory/storeFactory";
import { ref, reactive, type Ref, onMounted, computed } from "vue";

const props = defineProps<{
	courseLevel?: Updatable<CourseLevel>;
	submitText?: string;
	awaitingResponse?: boolean;
}>();

const emit = defineEmits<{
	(e: "submit", courseLevel: Updatable<CourseLevel>): void;
	(e: "cancel"): void;
}>();

const values: Ref<Updatable<CourseLevel>> = ref({
	name: props.courseLevel?.name ?? "",
	code: props.courseLevel?.code ?? "",
	study_type: props.courseLevel?.study_type ?? "Bachelor",
});

const errors = reactive({
	name: "",
	code: "",
	study_type: "",
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
	emit("submit", { ...values.value, id: props.courseLevel?.id });
};
</script>

<template>
	<div>
		<div class="flex flex-row justify-between items-center">
			<h1 class="text-3xl">
				{{ props.courseLevel ? "Edit" : "Create" }} Course
			</h1>

			<button
				@click="emit('cancel')"
				class="px-4 py-2 bg-primary-active text-primary-bg rounded-md font-bold hover:text-primary-text">
				Cancel
			</button>
		</div>

		<form class="flex flex-col gap-2" @submit.prevent="submit">
			<div class="flex flex-col gap-2">
				<label for="study_type" class="text-xl font-bold"
					>Study Type</label
				>
				<select
					name="study_type"
					id="study_type"
					class="border-2 focus:border-primary-active border-primary-bg px-2 py-1 rounded-md focus:outline-none transition-colors bg-secondary-bg focus:bg-tertiary-bg focus:ring-primary-active"
					v-model="values.study_type">
					<option v-for="studyType in studyTypes" :value="studyType">
						{{ studyType }}
					</option>
				</select>
				<p v-if="errors.name" class="text-red-500 text-sm">
					{{ errors.name }}
				</p>
			</div>

			<div class="flex flex-col gap-2">
				<label for="name" class="text-xl font-bold">Name</label>
				<input
					type="text"
					name="name"
					id="name"
					class="border-2 focus:border-primary-active border-primary-bg px-2 py-1 rounded-md focus:outline-none transition-colors bg-secondary-bg focus:bg-tertiary-bg focus:ring-primary-active"
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
					class="border-2 focus:border-primary-active border-primary-bg px-2 py-1 rounded-md focus:outline-none transition-colors bg-secondary-bg focus:bg-tertiary-bg focus:ring-primary-active"
					v-model="values.code" />
				<p v-if="errors.code" class="text-red-500 text-sm">
					{{ errors.code }}
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
