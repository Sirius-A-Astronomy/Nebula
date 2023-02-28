<script setup lang="ts">
import type {
    Question,
    NewQuestion,
    UpdatedQuestion,
} from "@stores/questionStore";
import { reactive, computed, onMounted, watch, ref, type Ref } from "vue";
import MarkdownEditor from "@components/MarkdownEditor.vue";
import { courseStore } from "@/stores/courseStore";

import { faPlus } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";

import SubjectTagEditor from "@components/subjectTag/SubjectTagEditor.vue";

import EditAnswer from "@components/question/EditAnswer.vue";

import type { ErrorBin } from "@/types";

const props = defineProps<{
    courseId?: string;
    question?: Question | null;
    errors?: ErrorBin;
}>();

const emit = defineEmits<{
    (event: "update:question", question: UpdatedQuestion): void;
    (event: "create:question", question: NewQuestion): void;
    (event: "cancel"): void;
}>();

watch(
    () => props.question,
    () => {
        if (props.question) {
            values.title = props.question.title;
            values.content = props.question.content;
            values.subject_tags = props.question.subject_tags
                ? props.question.subject_tags.map((tag) => tag.name)
                : [];
            values.answers = props.question.answers?.map((answer) => ({
                title: answer.title,
                content: answer.content,
                id: answer.id,
            }))
                ? props.question.answers
                : [];
            values.course_id = props.question.course.id;
        }
    }
);

watch(
    () => props.errors,
    () => {
        feedback.value.title = (props.errors?.title || []) as string[];
        feedback.value.content = (props.errors?.content || []) as string[];
        feedback.value.subject_tags = (props.errors?.subject_tags ||
            []) as string[];
        feedback.value.course_id = (props.errors?.course_id || []) as string[];

        if (props.errors?.answers) {
            feedback.value.answers = props.errors.answers as ErrorBin;
        }
    }
);

const feedback = ref({
    title: (props.errors?.title || []) as string[],
    content: (props.errors?.content || []) as string[],
    subject_tags: (props.errors?.subject_tags || []) as string[],
    answers: (props.errors?.answers || {}) as ErrorBin,
    course_id: (props.errors?.course_id || []) as string[],
});

const values = reactive({
    title: props.question?.title || "",
    content: props.question?.content || "",
    subject_tags: props.question?.subject_tags?.map((tag) => tag.name) || [],
    answers:
        props.question?.answers?.map((answer) => ({
            title: answer.title,
            content: answer.content,
            id: answer.id,
        })) || [],
    course_id: props.question?.course?.id ?? props.courseId ?? "",
});

const shouldShowSideBySide = computed(() => {
    return window.innerWidth > 768;
});

const courses = courseStore.getters.all;
let nextId = 0;

const addAnswer = () => {
    values.answers.push({
        title: "",
        content: "",
        id: `${nextId++}`,
    });
};

const removeAnswer = (id: string) => {
    values.answers = values.answers.filter((answer) => answer.id !== id);
};

const onSubmit = () => {
    if (props.question) {
        emit("update:question", { ...values, id: props.question.id });
    } else {
        emit("create:question", values);
    }
};

onMounted(async () => {
    if (courseStore.state.shouldLoadAll()) await courseStore.actions.getAll();
});
</script>

<template>
    <div class="question-editor flex flex-col gap-2 py-2">
        <div
            class="question-editor__course rounded-lg bg-primary-bg text-primary-text"
        >
            <label for="course_id" class="">Course</label>
            <select
                v-model="values.course_id"
                class="w-full rounded-lg border-secondary-bg bg-primary-bg text-primary-text"
            >
                <option value="">Select a course</option>
                <option
                    v-for="course in courses"
                    :key="course.id"
                    :value="course.id"
                >
                    {{ course.name }}
                </option>
            </select>

            <div v-if="feedback.course_id.length" class="text-red-500">
                <ul>
                    <li v-for="error in feedback.course_id" :key="error">
                        {{ error }}
                    </li>
                </ul>
            </div>
        </div>

        <div class="question-editor__subject-tags">
            <SubjectTagEditor v-model="values.subject_tags" />

            <div v-if="feedback.subject_tags.length" class="text-red-500">
                <ul>
                    <li v-for="error in feedback.subject_tags" :key="error">
                        {{ error }}
                    </li>
                </ul>
            </div>
        </div>

        <div class="question-editor__title">
            <MarkdownEditor
                class="!my-0 -mx-3"
                v-model="values.title"
                title="Title"
                placeholder="Enter a title for your question..."
                :options="{
                    defaultTab: shouldShowSideBySide
                        ? 'side-by-side'
                        : 'source',
                }"
            />

            <div v-if="feedback.title.length" class="text-red-500">
                <ul>
                    <li v-for="error in feedback.title" :key="error">
                        {{ error }}
                    </li>
                </ul>
            </div>
        </div>
        <div class="question-editor__content">
            <MarkdownEditor
                class="!my-0 -mx-3"
                v-model="values.content"
                placeholder="Enter your question here..."
                title="Content"
                :options="{
                    defaultTab: shouldShowSideBySide
                        ? 'side-by-side'
                        : 'source',
                    tabToIndentToggle: true,
                }"
            />

            <div v-if="feedback.content.length" class="text-red-500">
                <ul>
                    <li v-for="error in feedback.content" :key="error">
                        {{ error }}
                    </li>
                </ul>
            </div>
        </div>

        <div class="question-editor__answers">
            <div class="flex flex-row">
                <h2 class="mr-auto text-xl">Answers</h2>
                <button
                    @click="addAnswer"
                    :title="
                        values.answers?.length
                            ? 'Add another answer'
                            : 'Add an answer'
                    "
                    :aria-label="
                        values.answers?.length
                            ? 'Add another answer'
                            : 'Add an answer'
                    "
                >
                    <FontAwesomeIcon :icon="faPlus" />
                </button>
            </div>

            <Transition name="fade">
                <div v-if="!values.answers?.length">
                    <p>You haven't added any answers yet.</p>
                </div>
                <TransitionGroup
                    class="flex flex-col gap-2"
                    tag="div"
                    name="fade"
                    v-else
                >
                    <EditAnswer
                        v-for="answer in values.answers"
                        :key="answer.id"
                        :answer="answer"
                        :errors="((feedback.answers?.[answer.id] || {}) as Record<string, string[]>)"
                        @remove="removeAnswer(answer.id)"
                        @update="
                            (answer) =>
                                (values.answers = values.answers.map((a) =>
                                    a.id === answer.id ? answer : a
                                ))
                        "
                    />
                </TransitionGroup>
            </Transition>
        </div>

        <div
            class="flex flex-row items-end justify-between py-4 md:justify-end"
        >
            <button
                @click="emit('cancel')"
                class="btn btn-secondary sm:order-1"
            >
                Cancel
            </button>
            <button @click="onSubmit" class="btn btn-primary order-1">
                {{ props.question ? "Update" : "Create" }}
            </button>
        </div>
    </div>
</template>

<style scoped>
.fade-enter-active,
.fade-move,
.fade-leave-active {
    transition: all 0.5s;
}

.fade-enter-from,
.fade-leave-to {
    opacity: 0;
}

.fade-enter-from {
    transform: translateY(10px);
}

.fade-leave-to {
    transform: translateY(-10px);
}

.fade-leave-active {
    position: absolute;
    @apply sr-only;
}

.fade-enter-to,
.fade-leave-from {
    opacity: 1;
}
</style>
