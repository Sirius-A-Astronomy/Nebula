<script setup lang="ts">
import { ref, onMounted, watch, computed } from "vue";
import { questionStore } from "@/stores/questionStore";
import type { Question } from "@/stores/questionStore";

import type { Updatable } from "@stores/factory/storeFactory";
import QuestionForm from "@/components/question/QuestionForm.vue";
import useFlashStore from "@/stores/flashStore";

import { useRouter } from "vue-router";
import useModalStore from "@/stores/modalStore";
import Markdown from "@/components/MarkdownDisplay.vue";

const flash = useFlashStore();

const modal = useModalStore();

const props = defineProps<{
    id: string;
}>();

const question = computed(() => questionStore.getters.byId(props.id).value);

const router = useRouter();

watch(props, () => {
    loading.value = true;
    loadData();
});

const loading = ref(true);

const loadData = async () => {
    if (!question.value) {
        await questionStore.actions.getById(props.id);
    }

    loading.value = false;
};

const awaitingResponse = ref(false);

const updateCourse = async (question: Updatable<Question>) => {
    awaitingResponse.value = true;
    const response = await questionStore.actions.update(question);
    awaitingResponse.value = false;

    if (response.status !== 200) {
        flash.add(
            `Failed to update question '${question.title}': ${response.message}`,
            "error"
        );
        return;
    }
    flash.add(`question '${question.title}' updated successfully`, "success");
    editting.value = false;
};

const onDeleteClicked = () => {
    modal.add({
        title: "Delete Question",
        body: `Are you sure you want to delete question '${question.value?.title}'?`,
        actions: [
            {
                text: "Cancel",
                type: "neutral",
            },
            {
                text: "Delete",
                type: "danger",
                action: deleteQuestion,
            },
        ],
    });
};

const deleteQuestion = async () => {
    awaitingResponse.value = true;
    const question = { ...questionStore.getters.byId(props.id).value };
    const response = await questionStore.actions.delete(props.id);
    awaitingResponse.value = false;

    if (response.status !== 200) {
        flash.add(
            `Failed to delete question '${question.title}': ${response.message}`,
            "error"
        );
        return;
    }
    flash.add(`Question '${question.title}' deleted successfully`, "success");
    router.push({ name: "dashboard.question.index" });
};

const editting = ref(false);

onMounted(loadData);
</script>

<template>
    <div v-if="loading">Loading...</div>

    <template v-else>
        <template v-if="!editting && question">
            <div class="flex flex-row items-baseline justify-between">
                <h1 class="text-3xl">{{ question.title }}</h1>

                <div class="flex flex-row gap-1">
                    <button
                        @click="editting = true"
                        class="bg-primary rounded-md px-4 py-2 font-bold text-primary-text"
                    >
                        Edit
                    </button>

                    <button
                        @click="onDeleteClicked"
                        class="rounded-md bg-alert-warning px-4 py-2 font-bold text-alert-warning-text"
                    >
                        Delete
                    </button>
                </div>
            </div>

            <div class="flex flex-col">
                <div class="flex flex-row items-center gap-1">
                    <span class="font-bold">Course: </span>
                    <span>{{ question.course.name }}</span>
                </div>

                <div class="flex flex-row items-baseline gap-1">
                    <span class="font-bold">Subject tags: </span>
                    <span
                        v-for="tag in question.subject_tags"
                        :key="tag.id"
                        class="rounded-full bg-accent-clr px-2 text-xs text-on-accent-text"
                    >
                        {{ tag.name }}
                    </span>

                    <span
                        v-if="
                            !question.subject_tags ||
                            question.subject_tags?.length === 0
                        "
                        >None</span
                    >
                </div>

                <div class="flex flex-row items-baseline gap-1">
                    <span class="font-bold">User: </span>
                    <span
                        >{{ question.user.first_name }}
                        {{ question.user.last_name }}</span
                    >
                </div>

                <div class="flex flex-col items-baseline">
                    <h3 class="text-xl font-bold">Content:</h3>
                    <Markdown :content="question.content" />
                </div>
            </div>
        </template>

        <QuestionForm
            v-if="editting"
            :question="question"
            submitText="Update"
            @cancel="editting = false"
            :awaiting-response="awaitingResponse"
            @submit="updateCourse"
        />
    </template>
</template>

<style lang="scss" scoped></style>
