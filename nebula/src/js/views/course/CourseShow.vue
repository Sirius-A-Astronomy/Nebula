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
            <section class="rounded-md bg-secondary-bg px-4 py-2 shadow-md">
                <div
                    class="mb-4 flex flex-col flex-wrap gap-2 md:flex-row md:items-baseline md:justify-between"
                >
                    <h1 class="text-3xl font-bold md:flex-[1_1_40%]">
                        {{ course.name }} {{ course.code }}
                    </h1>
                    <div
                        class="order-3 font-semibold md:order-1 md:flex-[0_1_content] md:text-end"
                    >
                        {{ questions.length }} Questions
                    </div>
                    <div class="order-2 font-body md:flex-[1_1_60%]">
                        {{ course.description }}
                    </div>
                    <input
                        class="order-3 w-full rounded-md border-0 bg-tertiary-bg p-2 text-sm placeholder:font-semibold placeholder:text-secondary-text focus:bg-primary-bg focus:ring-primary-active md:flex-[1_0_20rem]"
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
                        class="btn btn-outline order-1 md:order-1 md:flex-[0_1_content]"
                        >Add a question</RouterLink
                    >
                </div>
                <div class="flex flex-col gap-2">
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
