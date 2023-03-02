<script setup lang="ts">
import type { Question } from "@stores/questionStore";
import type { Updatable } from "@stores/factory/storeFactory";
import { ref, reactive, onMounted, computed } from "vue";

import MarkdownEditor from "../MarkdownEditor.vue";

import { courseStore } from "@stores/courseStore";

const props = defineProps<{
    question?: Updatable<Question>;
    submitText: string;
    awaitingResponse?: boolean;
}>();

const emit = defineEmits<{
    (e: "submit", course: Updatable<Question>): void;
    (e: "cancel"): void;
}>();

const values = ref({
    title: props.question?.title ?? "",
    content: props.question?.content ?? "",
    answers: props.question?.answers ?? [],
    course: {
        id: props.question?.course?.id ?? "",
    },
    subject_tags: props.question?.subject_tags ?? [],
});

// eslint-disable-next-line @typescript-eslint/no-unused-vars
const errors = reactive({
    title: "",
    content: "",
    answers: "",
    course_id: "",
    subject_tags: "",
});

const loading = ref(false);

const courses = computed(() =>
    courseStore.getters.all.value.sort((a, b) =>
        a.course_level.name.localeCompare(b.course_level.name)
    )
);

const loadData = async () => {
    if (courses.value.length === 0) {
        await courseStore.actions.getAll();
    }
    loading.value = false;
};

onMounted(loadData);

const submit = async () => {
    emit("submit", { ...values.value, id: props.question?.id });
};
</script>

<template>
    <div>
        <div class="flex flex-row items-center justify-between">
            <h1 class="text-3xl">
                {{ props.question ? "Edit" : "Create" }} Question
            </h1>

            <button
                @click="emit('cancel')"
                class="rounded-md bg-primary-active px-4 py-2 font-bold text-primary-bg hover:text-primary-text"
            >
                Cancel
            </button>
        </div>

        <form class="flex flex-col gap-2" @submit.prevent="submit">
            <div class="flex flex-col">
                <label for="course_id" class="text-base font-bold"
                    >Course</label
                >
                <select
                    name="course_id"
                    id="course_id"
                    class="rounded-md border-2 border-primary-bg bg-secondary-bg px-2 py-1 transition-colors focus:border-primary-active focus:bg-tertiary-bg focus:outline-none focus:ring-primary-active"
                    v-model="values.course.id"
                >
                    <option value="" disabled selected>Select a course</option>
                    <option
                        v-for="course in courses"
                        :value="course.id"
                        :key="course.id"
                    >
                        {{ course.name }}
                    </option>
                </select>
            </div>

            <MarkdownEditor
                v-model="values.title"
                title="Title"
                :options="{
                    maxRows: 1,
                }"
            />

            <MarkdownEditor v-model="values.content" title="Content" />

            <button
                type="submit"
                class="rounded-md bg-primary-clr px-4 py-2 font-bold text-on-primary-text transition-colors hover:bg-primary-active hover:text-primary-bg focus:bg-primary-active focus:text-primary-bg"
                :disabled="loading || awaitingResponse"
            >
                {{
                    awaitingResponse
                        ? "Loading..."
                        : props.submitText
                        ? props.submitText
                        : "Submit"
                }}
            </button>
        </form>
    </div>
</template>

<style lang="scss" scoped></style>
