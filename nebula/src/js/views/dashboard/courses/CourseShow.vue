<script setup lang="ts">
import { ref, onMounted, watch, computed } from "vue";
import { courseStore, type Course } from "@stores/courseStore";

import type { Updatable } from "@stores/factory/storeFactory";
import CourseForm from "@components/course/CourseForm.vue";
import useFlashStore from "@/stores/flashStore";

import { useRouter } from "vue-router";
import useModalStore from "@/stores/modalStore";

const flash = useFlashStore();

const modal = useModalStore();

const props = defineProps<{
    id: string;
}>();

const course = computed(() => courseStore.getters.byId(props.id).value);

const router = useRouter();

watch(props, () => {
    loading.value = true;
    loadData();
});

const loading = ref(true);

const loadData = async () => {
    if (!course.value) {
        await courseStore.actions.getById(props.id);
    }

    loading.value = false;
};

const awaitingResponse = ref(false);

const updateCourse = async (course: Updatable<Course>) => {
    awaitingResponse.value = true;
    const response = await courseStore.actions.update(course);
    awaitingResponse.value = false;

    if (response.status !== 200) {
        flash.add(
            `Failed to update course '${course.name}': ${response.message}`,
            "error"
        );
        return;
    }
    flash.add(`Course '${course.name}' updated successfully`, "success");
    editting.value = false;
};

const onDeleteClicked = () => {
    modal.add({
        title: "Delete Course",
        body: `Are you sure you want to delete course '${course.value?.name}'?`,
        actions: [
            {
                text: "Cancel",
                type: "neutral",
            },
            {
                text: "Delete",
                type: "danger",
                action: deleteCourse,
            },
        ],
    });
};

const deleteCourse = async () => {
    awaitingResponse.value = true;
    const response = await courseStore.actions.delete(props.id);
    awaitingResponse.value = false;

    if (response.status !== 200) {
        flash.add(
            `Failed to delete course '${course.value?.name}': ${response.message}`,
            "error"
        );
        return;
    }
    router.push({ name: "dashboard.course.index" });
    const data = response.data as Course;
    flash.add(`Course '${data.name}' deleted successfully`, "success");
};

const editting = ref(false);

onMounted(loadData);
</script>

<template>
    <div v-if="loading">Loading...</div>

    <template v-else>
        <template v-if="!editting && course">
            <div class="flex flex-row items-baseline justify-between">
                <h1 class="text-3xl">{{ course.name }}</h1>

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
                    <span class="font-bold">Code: </span>
                    <span>{{ course.code }}</span>
                </div>

                <div class="flex flex-row items-center gap-1">
                    <span class="font-bold">Semester: </span>
                    <span>{{ course.semester }}</span>
                </div>

                <div class="flex flex-row items-center gap-1">
                    <span class="font-bold">Course Level: </span>
                    <span
                        >{{ course.course_level.name }} -
                        {{ course.course_level.study_type }}</span
                    >
                </div>

                <div class="flex flex-col items-start">
                    <span class="font-bold">Description: </span>
                    <span>{{ course.description }}</span>
                </div>
            </div>
        </template>

        <CourseForm
            v-if="editting"
            :course="course"
            submitText="Update"
            @cancel="editting = false"
            :awaiting-response="awaitingResponse"
            @submit="updateCourse"
        />
    </template>
</template>

<style lang="scss" scoped></style>
