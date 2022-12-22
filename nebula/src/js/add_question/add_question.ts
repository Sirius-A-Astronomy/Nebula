import { createApp } from "vue";

import addAnswers from "@/add_question/AddAnswers.vue";

createApp(addAnswers).mount("#vue-add-answers");

console.log("add_question.ts loaded");

export type Answer = {
	title: string;
	content: string;
	id: number;
};
