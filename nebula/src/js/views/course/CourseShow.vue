<script setup lang="ts">
import { courseStore } from "@/stores/courseStore";
import { computed, watch, onMounted, ref, nextTick } from "vue";
import BreadCrumbs from "@/components/BreadCrumbs.vue";
import { questionStore } from "@/stores/questionStore";
import QuestionListItem from "@components/question/QuestionListItem.vue";
import { canCreateQuestion } from "@/lib/permissionHelpers";

const props = defineProps<{
    id: string;
}>();

const course = computed(() => courseStore.getters.byId(props.id).value);
const questions = computed(() => {
    const questions = questionStore.getters.byCourseId(props.id).value;

    const filteredQuestions = questions.filter(
        (question) =>
            question.title
                .toLowerCase()
                .includes(questionFilter.value.toLowerCase()) ||
            question.content
                .toLowerCase()
                .includes(questionFilter.value.toLowerCase()) ||
            question.subject_tags?.some((tag) =>
                tag.name
                    .toLowerCase()
                    .includes(questionFilter.value.toLowerCase())
            ) ||
            question.answers?.some((answer) =>
                answer.content
                    .toLowerCase()
                    .includes(questionFilter.value.toLowerCase())
            ) ||
            question.answers?.some((answer) =>
                answer.title
                    .toLowerCase()
                    .includes(questionFilter.value.toLowerCase())
            )
    );

    return filteredQuestions;
});

watch(props, () => {
    loading.value = true;
    loadData();
});

const loading = ref(true);

const loadData = async () => {
    const promises = [];
    let shouldLoadFirst = false;
    // courses are less likely to change, only fetch them if they are not in the store
    if (!course.value) {
        promises.push(courseStore.actions.getById(props.id));
        shouldLoadFirst = true;
    }

    if (!shouldLoadFirst) {
        // questions are more likely to change more often, always fetch them
        loading.value = false;
    }

    // questions are more likely to change more often, always fetch them
    promises.push(questionStore.actions.getByCourseId(props.id));

    await Promise.all(promises);

    nextTick(() => {
        document.title = (course.value.name ?? "Course") + " | Nebula";
    });

    loading.value = false;
};

onMounted(() => {
    loadData();
});

const breadcrumbs = computed(() => [
    {
        name: "Courses",
        to: { name: "course.index" },
    },
    {
        name: course.value?.course_level?.name || "Loading...",
        to: {
            name: "course.level.show",
            params: { id: course.value.course_level.id },
        },
    },
    {
        name: course.value?.name || "Loading...",
        to: { name: "course.show", params: { id: props.id } },
    },
]);

const questionFilter = ref("");
</script>

<template>
    <main id="content">
        <div
            v-if="loading"
            class="container flex h-full w-full items-center justify-center"
        >
            Loading...
        </div>
        <div v-else class="container py-2">
            <BreadCrumbs :breadcrumbs="breadcrumbs" class="pt-2 pb-4" />
            <section
                class="course-container rounded-md bg-secondary-bg px-4 py-2"
            >
                <div class="course-header">
                    <h1 class="course-header__title text-3xl font-bold">
                        {{ course.name }} {{ course.code }}
                    </h1>
                    <div
                        class="course-header__questions-amount"
                        id="course-question-amount"
                    >
                        {{ questions.length }} Questions
                    </div>
                    <div class="course-header__description">
                        {{ course.description }}
                    </div>
                    <input
                        class="search-bar input w-full rounded-md border-0 bg-tertiary-bg p-2 text-sm placeholder:font-semibold placeholder:text-secondary-text focus:bg-primary-bg focus:ring-primary-active"
                        id="course-search-input-field"
                        type="text"
                        :placeholder="`Search in ${course.name}...`"
                        v-model="questionFilter"
                    />
                    <RouterLink
                        v-if="canCreateQuestion()"
                        :to="{
                            name: 'question.create',
                            query: { courseId: course.id },
                        }"
                        class="btn btn-outline add-question-button"
                        >Add a question</RouterLink
                    >
                </div>
                <div
                    class="question-list-container"
                    id="question-list-container"
                >
                    <QuestionListItem
                        v-for="question in questions"
                        :key="question.id"
                        :question="question"
                    />
                </div>
            </section>
        </div>
    </main>
</template>

<style lang="scss" scoped>
@use "@scss/abstracts/mixins" as *;

/*
    Course Page
*/

.course-header {
    margin-bottom: 1rem;

    &__questions-amount {
        font-family: "Poppins", "Open Sans", "Arial", sans-serif;
        font-style: normal;
        font-weight: 600;
        font-size: var(--font-size-h4);
        line-height: 30px;
    }

    &__description {
        font-family: "Lato";
        font-style: normal;
        font-weight: 400;
        font-size: var(--font-size-h3);
        line-height: 25px;
        color: var(--color-text-primary);
    }

    .add-question-button {
        font-size: var(--font-size-h4);
    }
}
@include mq(md) {
    .course-header {
        display: flex;
        flex-direction: row;
        align-items: baseline;
        justify-content: space-between;
        // grid-template-columns: 5fr 1fr auto auto;
        gap: 0.5rem;
        flex-wrap: wrap;

        &__title {
            margin-bottom: 0;
            flex: 1 1 40%;
        }

        &__questions-amount {
            margin-bottom: 0;
            text-align: end;
            flex: 0 1 content;
        }

        &__description {
            margin-bottom: 0;
            flex: 1 1 60%;
            order: 2;
        }

        .search-bar {
            margin-bottom: 0;
            flex: 1 0 20rem;
            order: 2;
        }

        .add-question-button {
            margin-bottom: 0;
            flex: 0 1 content;
            order: 1;
        }
    }
}
</style>
