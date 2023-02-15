<script setup lang="ts">
import { ref, watch } from "vue";
import type { NewAnswer } from "@stores/questionStore";

import MarkdownEditor from "@components/MarkdownEditor.vue";
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";
import { faTrashCan } from "@fortawesome/free-solid-svg-icons";
import useModalStore from "@stores/modalStore";

const modal = useModalStore();

const props = defineProps<{
    answer: NewAnswer;
}>();

const answerCopy = ref({ ...props.answer });

watch(
    () => answerCopy.value,
    (newAnswer) => {
        emit("update", newAnswer);
    },
    { deep: true }
);

const showDeleteAnswerModal = () => {
    modal.add({
        title: "Delete Answer",
        body: `Are you sure you want to delete answer '${props.answer.title}'?`,
        actions: [
            {
                text: "Cancel",
                type: "neutral",
            },
            {
                text: "Delete",
                type: "danger",
                action: () => emit("remove", props.answer.id),
            },
        ],
    });
};

const emit = defineEmits<{
    (event: "update", answer: NewAnswer): void;
    (event: "remove", answerId: string): void;
}>();

const expanded = ref(true);
</script>

<template>
    <div class="mt-2 rounded-lg bg-secondary-bg px-4 py-2">
        <div class="flex flex-row items-center justify-start gap-2 py-2">
            <h3 class="mr-auto text-xl font-bold">
                <span class="white">Answer</span>
                <Transition>
                    <span class="text-secondary-text" v-if="!expanded"
                        >: {{ answerCopy.title }}
                    </span>
                </Transition>
            </h3>

            <button
                type="button"
                @click.prevent="showDeleteAnswerModal"
                title="Remove Answer"
                aria-label="Remove Answer"
            >
                <FontAwesomeIcon :icon="faTrashCan" />
            </button>

            <button
                @click="expanded = !expanded"
                :aria-label="`${expanded ? 'Collapse' : 'Expand'} answer`"
                :title="`${expanded ? 'Collapse' : 'Expand'} answer`"
            >
                <svg
                    xmlns="http://www.w3.org/2000/svg"
                    height="24"
                    fill="currentColor"
                    class="transition-transform"
                    :class="expanded ? '' : 'rotate-180'"
                    width="24"
                >
                    <path d="m12 15.375-6-6 1.4-1.4 4.6 4.6 4.6-4.6 1.4 1.4Z" />
                </svg>
            </button>
        </div>

        <template v-if="expanded">
            <MarkdownEditor
                class="-mx-3 !mt-0 !bg-secondary-bg"
                v-model="answerCopy.title"
                default-tab="source"
                placeholder="Enter answer title here"
                title="Answer Title"
                :options="{
                    maxRows: 1,
                    disableMarkdown: true,
                }"
            />

            <MarkdownEditor
                class="-mx-3 !bg-secondary-bg"
                v-model="answerCopy.content"
                default-tab="source"
                placeholder="Enter answer content here"
                title="Answer Content"
                :options="{
                    tabToIndentToggle: true,
                }"
            />

            <p class="italic">
                Note: Answer content is hidden from the user until revealed.
                Title is always visible.
            </p>
        </template>
    </div>
</template>

<style lang="scss" scoped></style>
