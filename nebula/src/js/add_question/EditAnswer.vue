<script setup lang="ts">
import type { Answer } from "@/add_question/add_question";

import { ref, watch, type Ref } from "vue";

import MarkdownEditor from "@/components/MarkdownEditor.vue";

const props = defineProps<{
    answer: Answer;
}>();

const answerCopy = ref({ ...props.answer });

watch(
    () => answerCopy.value,
    (newAnswer) => {
        emit("update", newAnswer);
    }
);

const emit = defineEmits<{
    (event: "update", answer: Answer): void;
    (event: "remove", answerId: number): void;
}>();

const answerElement: Ref<HTMLDivElement | null> = ref(null);
</script>

<template>
    <div ref="answerElement">
        <MarkdownEditor
            v-model="answerCopy.title"
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
            v-model="answerCopy.content"
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
