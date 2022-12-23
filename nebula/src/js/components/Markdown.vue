<script setup lang="ts">
import useMarkdown from "markdown-it";
import { onMounted, ref, watch, type Ref } from "vue";

import DOMPurify from "dompurify";

import { throttle } from "throttle-debounce";

const props = defineProps<{
	content: string;
}>();

const markdown = useMarkdown();

// @ts-ignore
let mathjax = window.MathJax;

const markdownElement: Ref<HTMLDivElement | null> = ref(null);
const renderMarkdown = throttle(1000, (value) => {
	sanitizedMarkdown.value = markdown.render(
		DOMPurify.sanitize(value.trim(), {
			ALLOWED_TAGS: [],
		})
	);
	setTimeout(() => {
		mathjax.typesetPromise([markdownElement.value]);
	}, 0);
});

watch(
	() => props.content,
	(value) => {
		renderMarkdown(value);
	}
);

onMounted(() => {
	renderMarkdown(props.content);
});

const sanitizedMarkdown: Ref<string> = ref("");
</script>

<template>
	<div v-html="sanitizedMarkdown" ref="markdownElement"></div>
</template>
