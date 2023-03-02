<script setup lang="ts">
import { onMounted, ref } from "vue";
import { RouterLink } from "vue-router";

import { questionStore } from "@stores/questionStore";

const questions = questionStore.getters.all;

const loading = ref(true);

const navigate = (url: string) => {
    document.location.href = url;
};

onMounted(async () => {
    if (questionStore.state.shouldLoadAll()) {
        await questionStore.actions.getAll();
    }
    loading.value = false;
});
</script>

<template>
    <div>
        <div class="flex flex-row items-center justify-between gap-2 py-2">
            <h1 class="text-3xl">Questions</h1>
            <RouterLink
                :to="{
                    name: 'dashboard.question.create',
                }"
                class="rounded-md bg-primary-active px-4 py-2 font-bold text-primary-bg hover:text-primary-text"
                >Create</RouterLink
            >
        </div>

        <ul class="flex flex-col gap-2 py-2">
            <li
                v-for="question in questions"
                :key="question.id"
                class="rounded-md bg-secondary-bg px-4 py-2 transition-colors duration-75 hover:bg-tertiary-bg"
            >
                <RouterLink
                    :to="{
                        name: 'dashboard.question.show',
                        params: { id: question.id },
                    }"
                >
                    <div class="flex flex-row items-start justify-between">
                        <span class="text-primary text-xl">{{
                            question.title
                        }}</span>
                        <span class="text-secondary-text"
                            >{{ question.user.first_name }}
                            {{ question.user.last_name }}</span
                        >
                    </div>
                    <div class="flex flex-row items-start justify-between">
                        <a
                            class="text-end text-sm text-accent-clr hover:text-accent-focus hover:underline"
                            :href="`/q/${question.course.course_level.code}/${question.course.code}/${question.id}`"
                            @click.prevent="
                                navigate(
                                    `/q/${question.course.course_level.code}/${question.course.code}/${question.id}`
                                )
                            "
                            >View in nebula</a
                        >
                        <RouterLink
                            :to="{
                                name: 'dashboard.course.show',
                                params: { id: question.course.id },
                            }"
                            class="text-end text-sm text-accent-clr hover:text-accent-focus hover:underline"
                            >{{ question.course.name }}</RouterLink
                        >
                    </div>
                </RouterLink>
            </li>
        </ul>
    </div>
</template>

<style lang="scss" scoped></style>
