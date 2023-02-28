<script setup lang="ts">
import questionStore from "@/stores/questionStore";
import { computed, nextTick, onMounted, ref, watch } from "vue";
import { useRouter, RouterLink } from "vue-router";
import MarkdownDisplay from "@components/MarkdownDisplay.vue";
import useFlashStore from "@stores/flashStore";
import useModalStore from "@stores/modalStore";
import { courseStore } from "@/stores/courseStore";
import BreadCrumbs from "@/components/BreadCrumbs.vue";
import SubjectTag from "@/components/subjectTag/SubjectTag.vue";
import { canEditQuestion } from "@/lib/permissionHelpers";
import AnswerShow from "@/components/question/AnswerShow.vue";
import dayjs from "dayjs";
import relativeTime from "dayjs/plugin/relativeTime";
import MarkdownEditor from "@/components/MarkdownEditor.vue";
import { isAuthenticated } from "@/stores/sessionStore";
import CommentShow from "@/components/question/CommentShow.vue";

import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";
import { faEdit, faTrash } from "@fortawesome/free-solid-svg-icons";

dayjs.extend(relativeTime);

const props = defineProps<{
    id: string;
}>();

const question = computed(() => questionStore.getters.byId(props.id).value);

const router = useRouter();
const modal = useModalStore();
const flash = useFlashStore();

watch(props, () => {
    loading.value = true;
    loadData();
});

const loading = ref(true);

const loadData = async () => {
    if (!question.value) {
        await questionStore.actions.getById(props.id);
    }

    nextTick(() => {
        document.title = (question.value.title || "Question") + " | Nebula";
    });

    loading.value = false;
    canEditQuestionAwaited.value = await canEditQuestion(props.id);
};

const breadcrumbs = computed(() => {
    if (!question.value) {
        return [];
    }
    return [
        {
            name: "Courses",
            to: { name: "course.index" },
        },
        {
            name: question.value.course.course_level.name,
            to: {
                name: "course.level.show",
                params: { id: question.value.course.course_level.id },
            },
        },
        {
            name: question.value.course.name,
            to: {
                name: "course.show",
                params: { id: question.value.course.id },
            },
        },
        {
            name: question.value.title,
            to: { name: "question.show", params: { id: question.value.id } },
        },
    ];
});

const canEditQuestionAwaited = ref(false);

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
    const question = { ...questionStore.getters.byId(props.id).value };
    const response = await questionStore.actions.delete(props.id);

    if (!response.ok) {
        flash.add(
            `Failed to delete question '${question.title}': ${response.message}`,
            "error"
        );
        return;
    }
    // update the course to remove the question
    courseStore.actions.getById(question.course.id);

    flash.add(`Question '${question.title}' deleted successfully`, "success");
    router.push({ name: "course.show", params: { id: question.course.id } });
};

const commentContent = ref("");

const onCommentSubmit = async () => {
    const response = await questionStore.actions.addComment(
        props.id,
        commentContent.value
    );

    if (!response.ok) {
        flash.add(`Failed to add comment: ${response.message}`, "error");
        return;
    }

    flash.add(`Comment added successfully`, "success");
    commentContent.value = "";
};

onMounted(loadData);
</script>

<template>
    <main id="content" class="container pb-2">
        <div v-if="loading">Loading</div>
        <div v-else>
            <div
                class="flex flex-col items-center justify-between py-4 md:flex-row"
            >
                <BreadCrumbs :breadcrumbs="breadcrumbs" />

                <div
                    class="flex flex-row flex-wrap items-center justify-center gap-2"
                >
                    <SubjectTag
                        v-for="subjectTag in question.subject_tags"
                        :key="subjectTag.id"
                        :subject-tag="subjectTag"
                    />
                </div>
            </div>

            <div
                class="rounded-lg bg-secondary-bg p-3"
                aria-label="question card"
            >
                <div class="flex flex-col justify-between md:flex-row">
                    <div class="flex flex-row items-center gap-2">
                        <h1 class="text-3xl md:text-4xl">
                            <MarkdownDisplay
                                :content="question.title"
                                class="!font-bold"
                                :options="{
                                    disableMarkdown: true,
                                }"
                            />
                        </h1>
                        <div
                            class="flex flex-row gap-2"
                            v-if="canEditQuestionAwaited"
                        >
                            <RouterLink
                                :to="{
                                    name: 'question.edit',
                                    params: {
                                        id: question.id,
                                    },
                                }"
                                title="Edit Question"
                                aria-label="Edit Question"
                            >
                                <FontAwesomeIcon :icon="faEdit" />
                            </RouterLink>

                            <button
                                @click="onDeleteClicked"
                                title="Delete Question"
                                aria-label="Delete Question"
                            >
                                <FontAwesomeIcon :icon="faTrash" />
                            </button>
                        </div>
                    </div>
                    <div
                        class="flex flex-col items-end justify-end font-semibold text-tertiary-text md:text-end"
                    >
                        Posted
                        {{ dayjs(question.meta.created_at).fromNow() }} by
                        {{ question.user.first_name }}
                        {{ question.user.last_name }}

                        <div
                            class="md:text-md text-sm"
                            v-if="question.meta.updated_at"
                        >
                            (Last updated
                            {{ dayjs(question.meta.updated_at).fromNow() }})
                        </div>
                    </div>
                </div>

                <MarkdownDisplay :content="question.content" class="mt-4" />
            </div>

            <div aria-label="answers">
                <h2 class="py-4 text-2xl md:text-3xl">Answers</h2>

                <div
                    class="flex flex-col gap-2"
                    v-if="question.answers?.length"
                >
                    <AnswerShow
                        v-for="answer in question.answers"
                        :key="answer.id"
                        :answer="answer"
                    />
                </div>

                <div v-else>
                    <p>No answers yet</p>
                </div>
            </div>

            <div aria-label="comments">
                <h2 class="py-4 text-2xl md:text-3xl">
                    Comments
                    {{
                        question.comments?.length
                            ? `(${question.comments.length})`
                            : ""
                    }}
                </h2>

                <div aria-label="add comment">
                    <p v-if="!isAuthenticated">
                        <RouterLink
                            class="button-accent"
                            :to="{
                                name: 'user.login',
                                query: {
                                    next: encodeURIComponent($route.fullPath),
                                },
                            }"
                            >Login
                        </RouterLink>
                        to add a comment to this question
                    </p>
                    <div class="rounded-lg bg-secondary-bg p-3" v-else>
                        <h2 class="text-xl">Add Comment</h2>
                        <MarkdownEditor
                            v-model="commentContent"
                            placeholder="Enter your comment here..."
                            class="!mt-0 !bg-secondary-bg"
                        />
                        <div class="flex flex-row justify-end">
                            <button
                                class="rounded-lg bg-primary-bg px-4 py-2 text-primary-text"
                                @click="onCommentSubmit"
                            >
                                Submit
                            </button>
                        </div>
                    </div>
                </div>

                <TransitionGroup
                    tag="div"
                    name="fade"
                    v-if="question.comments?.length"
                    class="relative flex flex-col gap-2 pt-4"
                >
                    <CommentShow
                        v-for="comment in question.comments.sort((a, b) =>
                            dayjs(a.meta.created_at).isBefore(
                                dayjs(b.meta.created_at)
                            )
                                ? 1
                                : -1
                        )"
                        :key="comment.id"
                        :comment="comment"
                    />
                </TransitionGroup>

                <div class="pb-4" v-else>
                    <p>No comments yet</p>
                </div>
            </div>
        </div>
    </main>
</template>

<style lang="scss" scoped>
.fade-enter-active,
.fade-move,
.fade-leave-active {
    transition: all 0.5s cubic-bezier(0.55, 0, 0.1, 1);
}

.fade-enter-from {
    opacity: 0;
}
.fade-leave-active {
    position: absolute;
    @apply sr-only;
}
</style>
