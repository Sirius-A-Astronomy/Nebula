<script setup lang="ts">
import type { Answer } from "@stores/questionStore";
import dayjs from "dayjs";
import relativeTime from "dayjs/plugin/relativeTime";
import { ref } from "vue";
import MarkdownDisplay from "@components/MarkdownDisplay.vue";

dayjs.extend(relativeTime);
defineProps<{
    answer: Answer;
}>();

const expanded = ref(false);
</script>

<template>
    <div class="rounded-lg bg-secondary-bg p-3" aria-label="answer card">
        <div class="flex flex-col justify-start md:flex-row">
            <h1 class="text-xl md:flex-grow md:text-2xl">
                <MarkdownDisplay
                    :content="answer.title"
                    class="!font-bold"
                    :options="{
                        disableMarkdown: true,
                    }"
                />
            </h1>

            <div class="font-semibold text-tertiary-text md:text-end">
                Posted
                {{ dayjs(answer.meta.created_at).fromNow() }}
                by {{ answer.user.first_name }}
                {{ answer.user.last_name }}

                <div
                    class="md:text-md text-sm"
                    v-if="
                        answer.meta.updated_at &&
                        answer.meta.updated_at !== answer.meta.created_at
                    "
                >
                    (Last updated
                    {{ dayjs(answer.meta.updated_at).fromNow() }})
                </div>
            </div>
        </div>

        <template v-if="answer.content">
            <button
                @click="expanded = !expanded"
                :aria-label="`${expanded ? 'Collapse' : 'Expand'} answer`"
                class="btn btn-outline"
            >
                {{ expanded ? "Collapse" : "Expand" }} answer
            </button>
            <MarkdownDisplay :content="answer.content" v-if="expanded" />
        </template>
    </div>
</template>

<style lang="scss" scoped></style>
