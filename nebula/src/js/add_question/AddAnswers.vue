<script setup lang="ts">
// @ts-nocheck
import { ref, computed } from "vue";
import type { Computed } from "vue";

import AnswerVue from "./EditAnswer.vue";

let nextId = 0;

const answers = ref([] as Answer[]);
const answersJson: Computed<Answer[]> = computed(() => {
	// remove empty answers
	const answersWithoutEmpty = answers.value.filter((answer) => {
		return answer.title != "" && answer.content != "";
	});
	try {
		return JSON.stringify(answersWithoutEmpty);
	} catch (e) {
		console.log(e);
		return [];
	}
});

const removeAnswer = (answerId: number) => {
	answers.value = answers.value.filter((a) => a.id != answerId);
};

const addAnswer = () => {
	answers.value.push({ title: "", content: "", id: nextId++ });
};
</script>
<template>
	<input type="hidden" name="answers" v-model="answersJson" />

	<div id="answers">
		<div
			v-for="answer in answers"
			:key="answer.id"
			class="background-card my-2">
			<AnswerVue :answer="answer" @remove="removeAnswer" />
		</div>
	</div>

	<div>
		<button
			type="button"
			class="btn btn-primary"
			@click.prevent="addAnswer">
			{{ answers.length == 0 ? "Add an answer" : "Add another answer" }}
		</button>
	</div>
</template>
