<script setup lang="ts">
import { courseLevelStore } from "@stores/courseLevelStore";

import type { CourseLevel } from "@/stores/courseLevelStore";
import useFlashStore from "@stores/flashStore";
import useModalStore from "@stores/modalStore";
import { ref, computed, watch, onMounted } from "vue";
import { useRouter } from "vue-router";
import type { Updatable } from "@/stores/factory/storeFactory";
import CourseLevelForm from "@components/courseLevel/CourseLevelForm.vue";

const flash = useFlashStore();

const modal = useModalStore();

const props = defineProps<{
    id: string;
}>();

const courseLevel = computed(
    () => courseLevelStore.getters.byId(props.id).value
);

const router = useRouter();

watch(props, () => {
    loading.value = true;
    loadData();
});

const loading = ref(true);

const loadData = async () => {
    if (!courseLevel.value) {
        await courseLevelStore.actions.getById(props.id);
    }

    loading.value = false;
};

const awaitingResponse = ref(false);

const updateCourseLevel = async (courseLevel: Updatable<CourseLevel>) => {
    awaitingResponse.value = true;
    const response = await courseLevelStore.actions.update(courseLevel);
    awaitingResponse.value = false;

    if (response.status !== 200) {
        flash.add(
            `Failed to update course level '${courseLevel.name}': ${response.message}`,
            "error"
        );
        return;
    }
    flash.add(
        `Course level '${courseLevel.name}' updated successfully`,
        "success"
    );
    editting.value = false;
};

const onDeleteClicked = () => {
    modal.add({
        title: "Delete Course level",
        body: `Are you sure you want to delete course level '${courseLevel.value?.name}'? This will also delete all courses, questions, and answers associated with this course level and cannot be undone.`,
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
    const response = await courseLevelStore.actions.delete(props.id);
    awaitingResponse.value = false;

    if (response.status !== 200) {
        flash.add(
            `Failed to delete course level '${courseLevel.value?.name}': ${response.message}`,
            "error"
        );
        return;
    }
    router.push({ name: "dashboard.course.index" });
    const data = response.data as CourseLevel;
    flash.add(`Course level '${data.name}' deleted successfully`, "success");
};

const editting = ref(false);

onMounted(loadData);
</script>

<template>
    <div v-if="loading" class="flex h-full items-center justify-center">
        Loading...
    </div>
    <template v-else>
        <template v-if="editting">
            <course-level-form
                :course-level="courseLevel"
                :awaiting-response="awaitingResponse"
                @cancel="editting = false"
                @submit="updateCourseLevel"
            />
        </template>
        <template v-else>
            <div class="flex items-center justify-between">
                <h1 class="text-2xl font-bold">
                    {{ courseLevel.study_type }} - {{ courseLevel.name }}
                </h1>
                <div class="flex items-center">
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
            <div class="mt-4 flex flex-col">
                <div class="flex flex-row gap-1">
                    <span class="font-bold">Study Type</span>
                    <span>{{ courseLevel.study_type }}</span>
                </div>

                <div class="flex flex-row gap-1">
                    <span class="font-bold">Name</span>
                    <span>{{ courseLevel.name }}</span>
                </div>

                <div class="flex flex-row gap-1">
                    <span class="font-bold">Code</span>
                    <span>{{ courseLevel.code }}</span>
                </div>
            </div>
        </template>
    </template>
</template>

<style lang="scss" scoped></style>
