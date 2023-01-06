<script setup lang="ts">
import type { SearchResults } from "./Search.vue";
import { ref, type Ref, computed } from "vue";
import { OrbitSpinner } from "epic-spinners";
import { RouterLink } from "vue-router";
import ArrowBack from "@components/icons/ArrowBack.vue";

import fuzzysort from "fuzzysort";
import HighlightResult from "@components/global_search/HighlightResult.vue";

const props = defineProps<{
	searchQuery: string;
	loading: boolean;
	searchResults: SearchResults;
	dashboard: boolean;
}>();

const emit = defineEmits<{
	(event: "close"): void;
}>();

const courses = computed(() => {
	const courses = props.searchResults.courses;

	if (!courses) {
		return [];
	}

	const sortedResults = fuzzysort.go(props.searchQuery, courses, {
		keys: ["name", "code", "description"],
		scoreFn: (a) => {
			return Math.max(
				a[0] ? a[0].score : -1000,
				a[1] ? a[1].score - 100 : -1000,
				a[2] ? a[2].score - 400 : -1000
			);
		},
	});

	if (expanded.value === "courses") {
		return sortedResults;
	}

	return sortedResults.slice(0, 3);
});

const questions = computed(() => {
	const questions = props.searchResults.questions;

	if (!questions) {
		return [];
	}

	const sortedResults = fuzzysort.go(props.searchQuery, questions, {
		keys: ["title", "content"],
		scoreFn: (a) => {
			return Math.max(
				a[0] ? a[0].score : -1000,
				a[1] ? a[1].score - 100 : -1000
			);
		},
	});

	if (expanded.value === "questions") {
		return sortedResults;
	}

	return sortedResults.slice(0, 3);
});

const users = computed(() => {
	const users = props.searchResults.users;

	if (!users) {
		return [];
	}

	const sortedResults = fuzzysort.go(props.searchQuery, users, {
		keys: ["name", "email"],
		scoreFn: (a) => {
			return Math.max(
				a[0] ? a[0].score : -1000,
				a[2] ? a[2].score - 100 : -1000
			);
		},
	});

	if (expanded.value === "users") {
		return sortedResults;
	}

	return sortedResults.slice(0, 3);
});

const accentColor = computed(() => {
	return getComputedStyle(document.documentElement).getPropertyValue(
		"--color-accent"
	);
});

const expanded: Ref<"none" | "questions" | "courses" | "users"> = ref("none");
</script>

<template>
	<div
		class="absolute z-10 w-full max-w-xl mt-1 bg-secondary-bg text-primary-text rounded-lg shadow-lg max-h-[calc(100vh-4rem)] overflow-y-auto text-sm"
		v-if="searchQuery">
		<div class="py-1">
			<a
				:href="`/search?query=${searchQuery}`"
				class="flex items-center px-4 py-2 text-sm leading-5 transition-colors duration-150 hover:bg-tertiary-bg focus:outline-none focus:bg-tertiary-bg text-primary-text">
				<svg
					class="w-4 h-4 mr-3"
					aria-hidden="true"
					fill="currentColor"
					viewBox="0 0 20 20">
					<path
						fill-rule="evenodd"
						d="M8 4a4 4 0 100 8 4 4 0 000-8zM2 8a6 6 0 1110.89 3.476l4.817 4.817a1 1 0 01-1.414 1.414l-4.816-4.816A6 6 0 012 8z"
						clip-rule="evenodd" />
				</svg>
				<span>Advanced search for "{{ searchQuery }}"</span>
				<orbit-spinner
					class="ml-auto"
					v-show="loading"
					:animation-duration="1200"
					:size="24"
					:color="accentColor" />
			</a>

			<!-- Search results -->
			<div v-if="searchResults">
				<!-- courses -->
				<div
					v-if="
						courses?.length > 0 &&
						(expanded === 'none' || expanded == 'courses')
					">
					<div
						class="px-4 py-2 text-xs font-semibold text-primary-text uppercase flex flex-row items-center">
						<button
							class="mr-2"
							v-show="expanded === 'courses'"
							@click="expanded = 'none'">
							<arrow-back width="16" height="16" />
						</button>
						Courses ({{ searchResults.courses.length }})
					</div>
					<div
						v-for="course in courses"
						:key="`${course.obj.id}${searchQuery}`">
						<!-- Routerlink for when the user is on the dashboard -->
						<RouterLink
							v-if="dashboard"
							:to="{
								name: 'dashboard.course.show',
								params: {
									id: course.obj.id,
								},
							}"
							@click="emit('close')"
							class="flex items-center justify-between px-4 py-2 text-sm leading-5 transition-colors duration-150 text-primary-text hover:text-primary-text hover:bg-tertiary-bg focus:outline-none focus:bg-tertiary-bg relative">
							<HighlightResult
								:result="course[0]"
								:fallback="course.obj.name"
								highlight-class="font-bold" />
							<span
								v-if="course.obj.questions_count > 0"
								class="hidden sm:block text-xs text-on-accent-text bg-accent-clr rounded-full px-2"
								>{{
									course.obj.questions_count
								}}
								Questions</span
							>
						</RouterLink>

						<!-- Using an anchor tag until the entire app is converted to vue + vue-router -->
						<a
							v-else
							:href="`/q/${course.obj.course_level.code}/${course.obj.code}`"
							@click="emit('close')"
							class="flex items-center justify-between px-4 py-2 text-sm leading-5 transition-colors duration-150 hover:text-primary-text hover:bg-tertiary-bg focus:outline-none focus:bg-tertiary-bg relative">
							<HighlightResult
								:result="course[0]"
								:fallback="course.obj.name"
								highlight-class="font-bold" />
							<span
								v-if="course.obj.questions_count > 0"
								class="hidden sm:block text-xs text-on-accent-text bg-accent-clr rounded-full px-2"
								>{{
									course.obj.questions_count
								}}
								Questions</span
							>
						</a>
					</div>

					<button
						class="flex flex-col w-full items-center justify-center px-4 py-2 text-sm leading-5 transition-colors duration-150 hover:text-primary-text hover:bg-tertiary-bg focus:outline-none focus:bg-tertiary-bg relative"
						v-show="
							searchResults.courses?.length > 3 &&
							expanded === 'none'
							// use v-show so the button stays in the dom for vClickOutside
						"
						@click="expanded = 'courses'">
						Show all courses
					</button>
				</div>

				<!-- questions -->
				<div
					v-if="
						questions?.length > 0 &&
						(expanded === 'none' || expanded == 'questions')
					">
					<div
						class="px-4 py-2 text-xs font-semibold text-primary-text uppercase flex flex-row items-center">
						<button
							class="mr-2"
							v-show="expanded === 'questions'"
							@click="expanded = 'none'">
							<arrow-back width="16" height="16" />
						</button>
						Questions ({{ searchResults.questions?.length }})
					</div>
					<div
						v-for="question in questions"
						:key="`${question.obj.id}${searchQuery}`">
						<a
							:href="question.obj.url"
							@click="emit('close')"
							class="flex items-center justify-between px-4 py-2 text-sm leading-5 transition-colors duration-150 hover:text-primary-text hover:bg-tertiary-bg focus:outline-none focus:bg-tertiary-bg relative">
							<div class="flex flex-col w-full">
								<div
									class="flex flex-row justify-between items-center">
									<HighlightResult
										:result="question[0]"
										:fallback="question.obj.title"
										highlight-class="font-bold" />

									<span
										v-if="question.obj.course"
										class="hidden sm:block text-xs text-on-primary-text bg-primary-clr rounded-full px-2"
										>{{ question.obj.course.name }}</span
									>
								</div>

								<div class="flex flex-row">
									<span
										v-if="
											question.obj.subject_tags?.length >
											0
										"
										class="text-xs text-on-accent-text bg-accent-clr rounded-full px-2 mr-4 overflow-hidden max-w-32 whitespace-nowrap"
										v-for="tag in question.obj.subject_tags"
										:key="tag.id"
										>{{ tag.name }}</span
									>
								</div>
							</div>
						</a>
					</div>

					<button
						class="flex flex-col w-full items-center justify-center px-4 py-2 text-sm leading-5 transition-colors duration-150 hover:text-primary-text hover:bg-tertiary-bg focus:outline-none focus:bg-tertiary-bg relative"
						v-show="
							searchResults.courses?.length > 3 &&
							expanded === 'none'
							// use v-show so the button stays in the dom for vClickOutside
						"
						@click="expanded = 'questions'">
						Show all questions
					</button>
				</div>

				<!-- users -->
				<div
					v-if="
						users?.length > 0 &&
						(expanded === 'none' || expanded == 'users')
					">
					<div
						class="px-4 py-2 text-xs font-semibold text-primary-text uppercase flex flex-row items-center">
						<button
							class="mr-2"
							v-show="expanded === 'users'"
							@click="expanded = 'none'">
							<arrow-back width="16" height="16" />
						</button>
						Users ({{ searchResults.users.length }})
					</div>
					<div
						v-for="user in users"
						:key="`${user.obj.id}${searchQuery}`">
						<RouterLink
							:to="{
								name: 'dashboard.user.show',
								params: { id: user.obj.id },
							}"
							@click="emit('close')"
							class="flex items-center justify-between px-4 py-2 text-sm leading-5 transition-colors duration-150 hover:text-primary-text hover:bg-tertiary-bg focus:outline-none focus:bg-tertiary-bg relative">
							<div class="flex flex-col w-full">
								<div
									class="flex flex-row justify-between items-center">
									<HighlightResult
										:result="user[0]"
										:fallback="user.obj.name"
										highlight-class="font-bold" />

									<HighlightResult
										v-if="user.obj.email"
										class="text-sm"
										:result="user[1]"
										:fallback="user.obj.email"
										highlight-class="font-bold" />
								</div>
							</div>
						</RouterLink>
					</div>

					<button
						class="flex flex-col w-full items-center justify-center px-4 py-2 text-sm leading-5 transition-colors duration-150 hover:text-primary-text hover:bg-tertiary-bg focus:outline-none focus:bg-tertiary-bg relative"
						v-show="
							searchResults.users?.length > 3 &&
							expanded === 'none'
							// use v-show so the button stays in the dom for vClickOutside
						"
						@click="expanded = 'users'">
						Show all users
					</button>
				</div>
			</div>
		</div>
	</div>
</template>

<style lang="scss" scoped></style>
