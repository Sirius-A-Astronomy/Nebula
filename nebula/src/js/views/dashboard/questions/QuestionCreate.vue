<script setup lang="ts">
import QuestionForm from "@components/question/QuestionForm.vue";
import { ref } from "vue";

import { useRouter } from "vue-router";
import useFlash from "@stores/flashStore";

import { questionStore } from "@stores/questionStore";
import type { Question } from "@stores/questionStore";
import type { Updatable, New } from "@/stores/factory/storeFactory";

const router = useRouter();
const flash = useFlash();

const awaitingResponse = ref(false);

const submitQuestion = async (question: Updatable<Question>) => {
	awaitingResponse.value = true;
	const response = await questionStore.actions.create(
		question as New<Question>
	);
	awaitingResponse.value = false;

	if (response.status !== 201) {
		flash.add(`Failed to create question: ${response.message}`, "error");
		return;
	}
	const data = response.data as Question;

	router.push({
		name: "dashboard.question.show",
		params: { id: data.id },
	});

	flash.add(`Question '${data.title}' created successfully`, "success");
	return;
};
</script>

<template>
	<div>
		<QuestionForm
			submitText="Create"
			@submit="submitQuestion"
			:awaiting-response="awaitingResponse"
			@cancel="$router.back()" />
	</div>
</template>

<style lang="scss" scoped></style>
