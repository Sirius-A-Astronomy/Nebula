<script setup lang="ts">
import QuestionEditor from "@/components/question/QuestionEditor.vue";
import { computed, onMounted, ref, watch } from "vue";
import type { NewQuestion, UpdatedQuestion } from "@stores/questionStore";
import { questionStore } from "@stores/questionStore";
import { courseStore } from "@stores/courseStore";

import {
    faUpRightAndDownLeftFromCenter,
    faDownLeftAndUpRightToCenter,
} from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";

import { useRouter, useRoute } from "vue-router";

import useFlashStore from "@stores/flashStore";

const router = useRouter();
const route = useRoute();
const flash = useFlashStore();

const props = defineProps<{
    id?: string;
}>();

const loadData = async () => {
    if (props.id && !questionStore.getters.byId(props.id).value) {
        await questionStore.actions.getById(props.id);
    }
};

watch(
    props,
    () => {
        if (props.id) {
            loadData();
        }
    },
    { immediate: true }
);

const errors = ref<Record<string, string[]>>({});

const onCreate = async (values: NewQuestion) => {
    const response = await questionStore.actions.create<NewQuestion>(values);

    if (response.ok) {
        flash.add(
            `Question '${response.data.title}' created successfully`,
            "success"
        );
        router.push({
            name: "question.show",
            params: { id: response.data.id },
        });

        // update the course to which this question belongs
        courseStore.actions.getById(response.data.course.id);
        return;
    }

    flash.add(
        `Question '${values.title}' could not be created: ${response.message}`,
        "error"
    );

    if (!response.data) {
        return;
    }

    errors.value = (
        response.data as { errors: Record<string, string[]> }
    ).errors;
};

const onUpdate = async (values: UpdatedQuestion) => {
    const response = await questionStore.actions.update<UpdatedQuestion>(
        values
    );

    if (response.ok) {
        flash.add(
            `Question '${response.data.title}' updated successfully`,
            "success"
        );
        router.push({
            name: "question.show",
            params: { id: response.data.id },
        });
        return;
    }

    flash.add(
        `Question '${values.title}' could not be updated: ${response.message}`,
        "error"
    );
};

const onCancel = () => {
    if (props.id) {
        router.push({
            name: "question.show",
            params: { id: props.id },
        });
        return;
    }

    if (route.query.courseId) {
        router.push({
            name: "course.show",
            params: { id: route.query.courseId as string },
        });
        return;
    }

    router.go(-1);
};

const fullWidth = ref(false);

const question = computed(() =>
    props.id ? questionStore.getters.byId(props.id).value : null
);

onMounted(() => {
    if (props.id) {
        loadData();
    }
});
</script>

<template>
    <main
        id="content"
        class="h-auto w-auto max-w-[100%] py-4 transition-all duration-500"
        :class="{
            '!container': !fullWidth,
            'mx-auto px-4 md:px-8': fullWidth,
        }"
    >
        <div class="flex flex-row items-center justify-between transition-all">
            <h1 class="text-2xl font-bold transition-all">
                {{ id ? "Edit" : "Create" }} a Question
            </h1>

            <label
                for="fullWidthToggle"
                class="hidden cursor-pointer md:block"
                :title="
                    fullWidth
                        ? 'Collapse question editor'
                        : 'Expand question editor'
                "
            >
                <span class="sr-only">Show editor at full width</span>
                <FontAwesomeIcon
                    :icon="
                        fullWidth
                            ? faDownLeftAndUpRightToCenter
                            : faUpRightAndDownLeftFromCenter
                    "
                />
                <input
                    type="checkbox"
                    name="fullWidth"
                    id="fullWidthToggle"
                    v-model="fullWidth"
                    class="sr-only"
                    @change="
                        (e) =>
                            // @ts-ignore
                            e.target.checked
                                ? (fullWidth = true)
                                : (fullWidth = false)
                    "
                />
            </label>
        </div>
        <QuestionEditor
            :question="question"
            :errors="errors"
            :course-id="(route.query.courseId as string)"
            @create:question="onCreate"
            @update:question="onUpdate"
            @cancel="onCancel"
        />
    </main>
</template>

<style lang="scss" scoped></style>
