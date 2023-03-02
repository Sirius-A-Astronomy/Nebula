<script setup lang="ts">
import { authenticatedUser } from "@/stores/sessionStore";
import { computed, onMounted, ref, watch, type Ref } from "vue";
import dayjs from "dayjs";
import relativeTime from "dayjs/plugin/relativeTime";
import {
    questionStore,
    type Answer,
    type Comment,
    type Question,
} from "@/stores/questionStore";
import api from "@/http/api";
import useFlashStore from "@/stores/flashStore";
import useModalStore from "@/stores/modalStore";
import { getAccessLevelName } from "@/stores/userStore";
import { userStore } from "@/stores/userStore";
import { useRouter, RouterLink } from "vue-router";

import QuestionListItem from "@/components/question/QuestionListItem.vue";

dayjs.extend(relativeTime);

const flash = useFlashStore();
const modal = useModalStore();
const router = useRouter();

const user = authenticatedUser;


const userComments: Ref<Comment[]> = ref([]);
const userQuestions: Ref<Question[]> = ref([]);
const userAnswers: Ref<Answer[]> = ref([]);

const showAllComments = ref(false);
const showAllQuestions = ref(false);
const showAllAnswers = ref(false);

const limitedUserComments = computed(() => {
    if (showAllComments.value) {
        return userComments.value;
    }
    return userComments.value.slice(0, 3);
});

const limitedUserQuestions = computed(() => {
    if (showAllQuestions.value) {
        return userQuestions.value;
    }
    return userQuestions.value.slice(0, 3);
});

const limitedUserAnswers = computed(() => {
    if (showAllAnswers.value) {
        return userAnswers.value;
    }
    return userAnswers.value.slice(0, 3);
});

const onDeleteClicked = () => {
    modal.add({
        title: "Delete User",
        body: `Are you sure you want to delete user '${user.value?.first_name} ${user.value?.last_name}'?`,
        actions: [
            {
                text: "Cancel",
                type: "neutral",
            },
            {
                text: "Delete User",
                action: deleteUser,
                type: "danger",
            },
        ],
    });
};

const deleteUser = async () => {
    const response = await userStore.actions.delete(user.value.id);

    if (!response.ok) {
        flash.add(
            `Failed to delete user '${user.value.first_name} ${user.value.last_name}': ${response.message}`,
            "error"
        );
        return;
    }
    router.push({ name: "dashboard.user.index" });
    const data = response.data;
    flash.add(
        `Course '${data.first_name} ${data.last_name}' deleted successfully`,
        "success"
    );
};

const loadData = async () => {
    const promises: Promise<any>[] = [];

    promises.push(
        api
            .get<Comment[]>(`/comments/`, {
                user: user.value.id,
            })
            .then((response) => {
                if (!response.ok) {
                    flash.add(
                        `Failed to load comments: ${response.message}`,
                        "error"
                    );
                    return;
                }
                userComments.value = response.data;
            })
    );

    promises.push(
        api
            .get<Question[]>(`/questions/`, {
                user: user.value.id,
            })
            .then((response) => {
                if (!response.ok) {
                    flash.add(
                        `Failed to load questions: ${response.message}`,
                        "error"
                    );
                    return;
                }
                userQuestions.value = response.data;
            })
    );

    promises.push(
        api
            .get<Answer[]>(`/answers/`, {
                user: user.value.id,
            })
            .then((response) => {
                if (!response.ok) {
                    flash.add(
                        `Failed to load answers: ${response.message}`,
                        "error"
                    );
                    return;
                }
                userAnswers.value = response.data;
            })
    );

    await new Promise<void>((resolve) => {
        Promise.all(promises).then(() => {
            resolve();
        });
    });

    // load all questions referenced by answers
    const referencedQuestionsPromises: Promise<any>[] = [];

    const questionIds = new Set<string>();

    userAnswers.value.forEach((answer) => {
        if (
            questionStore.getters.byId(answer.question_id).value ||
            questionIds.has(answer.question_id)
        ) {
            return;
        }
        referencedQuestionsPromises.push(
            questionStore.actions.getById(answer.question_id)
        );
        questionIds.add(answer.question_id);
    });

    userComments.value.forEach((comment) => {
        if (
            questionStore.getters.byId(comment.question_id).value ||
            questionIds.has(comment.question_id)
        ) {
            return;
        }
        referencedQuestionsPromises.push(
            questionStore.actions.getById(comment.question_id)
        );
        questionIds.add(comment.question_id);
    });

    Promise.all(referencedQuestionsPromises);
};

onMounted(() => {
    loadData();
});
</script>

<template>
    <main id="content" class="container py-4">
        <div class="grid grid-cols-1 gap-2 md:grid-cols-[1fr_2fr]">
            <div class="rounded-md bg-secondary-bg p-4 shadow-md">
                <h1 class="text-4xl font-semibold">
                    {{ user.first_name }} {{ user.last_name }}
                </h1>

                <div class="mt-4 flex flex-col gap-2">
                    <div class="flex flex-col gap-2">
                        <h2 class="text-2xl font-semibold">About</h2>
                        <p>Email: {{ user.email }}</p>
                        <p>
                            Joined:
                            {{ dayjs(user.created_at).format("DD MMM YYYY") }}
                        </p>
                        <p>Role: {{ getAccessLevelName(user.access_level) }}</p>
                    </div>
                    <div class="flex flex-col gap-2">
                        <h2 class="text-2xl font-semibold">Activity</h2>
                        <div class="flex flex-col gap-2">
                            <p>Questions: {{ userQuestions.length }}</p>
                            <p>Answers: {{ userAnswers.length }}</p>
                            <p>Comments: {{ userComments.length }}</p>
                        </div>
                    </div>
                </div>

                <div class="mt-4 flex flex-row gap-2">
                    <RouterLink
                        class="rounded-lg bg-primary-bg px-4 py-2 text-primary-text"
                        :to="{
                            name: 'user.profile.edit',
                        }"
                    >
                        Edit Account
                    </RouterLink>

                    <button
                        class="rounded-lg bg-alert-error px-4 py-2 text-alert-error-text"
                        @click="onDeleteClicked"
                    >
                        Delete Account
                    </button>
                </div>
            </div>
            <div class="rounded-md bg-secondary-bg p-4 shadow-md">
                <h2 class="text-2xl font-semibold">Questions</h2>
                <div class="mt-4 flex flex-col gap-2">
                    <question-list-item
                        v-for="question in limitedUserQuestions"
                        :key="question.id"
                        :question="question"
                        class="-mx-2 px-2 transition-colors duration-75 hover:!bg-primary-bg"
                    />
                </div>

                <div
                    class="mt-4 flex flex-row justify-center"
                    v-if="userQuestions.length > 3"
                >
                    <button
                        class="text-accent-clr hover:text-accent-focus"
                        @click="showAllQuestions = !showAllQuestions"
                    >
                        {{ showAllQuestions ? "Show less" : "Show more" }}
                    </button>
                </div>

                <h2 class="mt-4 text-2xl font-semibold">Answers</h2>
                <div class="mt-4 flex flex-col gap-2">
                    <RouterLink
                        v-for="answer in limitedUserAnswers"
                        :key="answer.id"
                        :to="{
                            name: 'question.show',
                            params: {
                                id: answer.question_id,
                            },
                        }"
                        class="-mx-2 px-2 transition-colors duration-75 hover:bg-primary-bg"
                    >
                        <div class="flex flex-row justify-between">
                            <div class="flex flex-col">
                                <p
                                    class="text-lg font-semibold text-primary-active"
                                >
                                    {{ answer.title }}
                                </p>
                                <p class="text-sm font-medium">
                                    Answered to:
                                    <span class="italic">
                                        {{
                                            questionStore.getters.byId(
                                                answer.question_id
                                            ).value?.title
                                        }}
                                    </span>
                                    by
                                    <span class="italic">
                                        {{
                                            questionStore.getters.byId(
                                                answer.question_id
                                            ).value?.user.first_name
                                        }}
                                        {{
                                            questionStore.getters.byId(
                                                answer.question_id
                                            ).value?.user.last_name
                                        }}
                                    </span>
                                </p>
                            </div>
                            <div class="flex flex-col items-end justify-start">
                                <p class="text-end font-semibold">
                                    {{
                                        questionStore.getters.byId(
                                            answer.question_id
                                        ).value?.course.name
                                    }}
                                </p>
                                <p class="text-sm">
                                    {{
                                        dayjs(answer.meta.created_at).fromNow()
                                    }}
                                </p>
                            </div>
                        </div>
                    </RouterLink>
                </div>
                <div
                    class="mt-4 flex flex-row justify-center"
                    v-if="userAnswers.length > 3"
                >
                    <button
                        class="text-accent-clr hover:text-accent-focus"
                        @click="showAllAnswers = !showAllAnswers"
                    >
                        {{ showAllAnswers ? "Show less" : "Show more" }}
                    </button>
                </div>

                <h2 class="mt-4 text-2xl font-semibold">Comments</h2>
                <div class="mt-4 flex flex-col gap-2">
                    <RouterLink
                        v-for="comment in limitedUserComments"
                        :key="comment.id"
                        :to="{
                            name: 'question.show',
                            params: {
                                id: comment.question_id,
                            },
                        }"
                        class="-mx-2 px-2 transition-colors duration-75 hover:bg-primary-bg"
                    >
                        <div class="flex flex-row justify-between">
                            <div class="flex flex-col">
                                <p
                                    class="text-lg font-semibold text-primary-active"
                                >
                                    {{
                                        comment.content.length > 50
                                            ? comment.content.substring(0, 50) +
                                              "..."
                                            : comment.content
                                    }}
                                </p>
                                <p class="text-sm font-medium">
                                    Commented on:
                                    <span class="italic">
                                        {{
                                            questionStore.getters.byId(
                                                comment.question_id
                                            ).value?.title
                                        }}
                                    </span>
                                    by
                                    <span class="italic">
                                        {{
                                            questionStore.getters.byId(
                                                comment.question_id
                                            ).value?.user.first_name
                                        }}
                                        {{
                                            questionStore.getters.byId(
                                                comment.question_id
                                            ).value?.user.last_name
                                        }}
                                    </span>
                                </p>
                            </div>
                            <div class="flex flex-col items-end justify-start">
                                <p class="text-end font-semibold">
                                    {{
                                        questionStore.getters.byId(
                                            comment.question_id
                                        ).value?.course.name
                                    }}
                                </p>
                                <p class="text-sm">
                                    {{
                                        dayjs(comment.meta.created_at).fromNow()
                                    }}
                                </p>
                            </div>
                        </div>
                    </RouterLink>
                </div>

                <div
                    class="mt-4 flex flex-row justify-center"
                    v-if="userComments.length > 3"
                >
                    <button
                        class="text-accent-clr hover:text-accent-focus"
                        @click="showAllComments = !showAllComments"
                    >
                        {{ showAllComments ? "Show less" : "Show more" }}
                    </button>
                </div>
            </div>
        </div>
    </main>
</template>

<style lang="scss" scoped></style>
