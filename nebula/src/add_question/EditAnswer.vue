<script setup lang="ts">
import type { Answer } from "@/add_question/add_question";

import DOMPurify from "dompurify";

import useMarkdown from "markdown-it";
import { throttle } from "throttle-debounce";
import { ref, type Ref } from "vue";

import MarkdownVue from "@/components/Markdown.vue";

defineProps<{
	answer: Answer;
}>();

const emit = defineEmits<{
	(event: "remove", answerId: number): void;
}>();

const answerElement: Ref<HTMLDivElement | null> = ref(null);

const showPreviews = ref({
	"answer-title": false,
	"answer-content": false,
});
</script>

<template>
	<div ref="answerElement">
		<div class="form-group input-field">
			<label for="answer-title">Answer Title</label>
			<input
				type="text"
				class="form-control"
				id="answer-title"
				name="answer-title"
				v-model="answer.title" />
			<button
				class="button-accent"
				@click.prevent="
					showPreviews['answer-title'] = !showPreviews['answer-title']
				">
				{{
					showPreviews["answer-title"]
						? "Hide Preview"
						: "Show Preview"
				}}
			</button>
		</div>

		<h4 v-if="showPreviews['answer-title']">Title Preview</h4>
		<MarkdownVue
			v-if="showPreviews['answer-title']"
			:content="answer.title" />

		<div class="form-group input-field mt-2">
			<label for="answer-content">Answer Content</label>
			<textarea
				class="form-control"
				id="answer-content"
				name="answer-content"
				rows="3"
				v-model="answer.content"></textarea>
			<button
				class="button-accent"
				@click.prevent="
					showPreviews['answer-content'] =
						!showPreviews['answer-content']
				">
				{{
					showPreviews["answer-content"]
						? "Hide Preview"
						: "Show Preview"
				}}
			</button>
		</div>

		<h4 v-if="showPreviews['answer-content']">Answer Preview</h4>
		<MarkdownVue
			v-if="showPreviews['answer-content']"
			:content="answer.content" />

		<button
			type="button"
			class="btn btn-warning mt-2"
			@click.prevent="emit('remove', answer.id)">
			Remove
		</button>
	</div>
</template>

<style lang="scss" scoped></style>
