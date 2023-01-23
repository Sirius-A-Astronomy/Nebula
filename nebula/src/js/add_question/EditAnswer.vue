<script setup lang="ts">
import type { Answer } from "@/add_question/add_question";

import { ref, type Ref } from "vue";

import MarkdownEditor from "@/components/MarkdownEditor.vue";

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
    <MarkdownEditor
      v-model="answer.title"
      default-tab="source"
      placeholder="Enter answer title here"
      title="Answer Title"
      :custom-text="{
        renderedLabel: 'Preview',
        sourceLabel: 'Edit',
        sideBySideLabel: 'Edit & Preview',
      }"
      :options="{
        maxRows: 1,
        disableMarkdown: true,
      }"
    />

    <MarkdownEditor
      v-model="answer.content"
      default-tab="source"
      placeholder="Enter answer content here"
      title="Answer Content"
      :custom-text="{
        renderedLabel: 'Preview',
        sourceLabel: 'Edit',
        sideBySideLabel: 'Edit & Preview',
      }"
      :options="{
        tabToIndentToggle: true,
      }"
    />

    <button
      type="button"
      class="btn btn-warning mt-2"
      @click.prevent="emit('remove', answer.id)"
    >
      Remove
    </button>
  </div>
</template>

<style lang="scss" scoped></style>
