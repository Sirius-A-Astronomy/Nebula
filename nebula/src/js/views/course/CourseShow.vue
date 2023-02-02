<script setup lang="ts">
import { courseStore } from "@/stores/courseStore";
import { computed, watch, onMounted, ref } from "vue";
import BreadCrumbs from "@/components/BreadCrumbs.vue";
import { questionStore } from "@/stores/questionStore";

const props = defineProps<{
    id: string;
}>();

const course = computed(() => courseStore.getters.byId(props.id).value);
const questions = computed(
    () => questionStore.getters.byCourseId(props.id).value
);

watch(props, () => {
    loading.value = true;
    loadData();
});

const loading = ref(true);

const loadData = async () => {
    const promises = [];
    if (!course.value) {
        promises.push(courseStore.actions.getById(props.id));
    }

    if (!questions.value) {
        promises.push(questionStore.actions.getAll());
    }

    await Promise.all(promises);

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
</script>

<template>
    <main id="content">
        <div v-if="loading">Loading</div>
        <div v-else class="container py-2">
            <BreadCrumbs :breadcrumbs="breadcrumbs" />
            <section>
                <h1 class="text-3xl">{{ course.name }}</h1>
            </section>
        </div>
    </main>
</template>
