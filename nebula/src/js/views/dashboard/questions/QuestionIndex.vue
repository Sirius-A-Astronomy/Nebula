<script setup lang="ts">
import { computed, onMounted, ref } from "vue";
import { RouterLink } from "vue-router";

import { questionStore } from "@stores/questionStore";

const questions = questionStore.getters.all;

const loading = ref(true);

const navigate = (url: string) => {
	document.location.href = url;
};

onMounted(async () => {
	await questionStore.actions.getAll();
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
				class="px-4 py-2 bg-primary-active text-primary-bg rounded-md font-bold hover:text-primary-text"
				>Create</RouterLink
			>
		</div>

		<ul class="flex flex-col gap-2 py-2">
			<li
				v-for="question in questions"
				:key="question.id"
				class="bg-secondary-bg hover:bg-tertiary-bg px-4 py-2 rounded-md transition-colors duration-75">
				<RouterLink
					:to="{
						name: 'dashboard.question.show',
						params: { id: question.id },
					}">
					<div class="flex flex-row justify-between items-start">
						<span class="text-xl text-primary">{{
							question.title
						}}</span>
						<span class="text-secondary-text"
							>{{ question.user.first_name }}
							{{ question.user.last_name }}</span
						>
					</div>
					<div class="flex flex-row justify-between items-start">
						<a
							class="text-accent-clr hover:text-accent-focus hover:underline text-sm text-end"
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
							class="text-accent-clr hover:text-accent-focus hover:underline text-sm text-end"
							>{{ question.course.name }}</RouterLink
						>
					</div>
				</RouterLink>
			</li>
		</ul>
	</div>
</template>

<style lang="scss" scoped></style>
