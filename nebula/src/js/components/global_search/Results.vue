<script setup lang="ts">
import type { SearchResults } from "./Search.vue";
import { ref, type Ref, computed } from "vue";
import { OrbitSpinner } from "epic-spinners";

const props = defineProps<{
	searchQuery: string;
	loading: boolean;
	searchResults: SearchResults;
}>();

const courses = computed(() => {
	if (expanded.value === "courses") {
		return props.searchResults.courses;
	}

	return props.searchResults.courses.slice(0, 3);
});

const questions = computed(() => {
	if (expanded.value === "questions") {
		return props.searchResults.questions;
	}

	return props.searchResults.questions.slice(0, 3);
});

const accentColor = computed(() => {
	return getComputedStyle(document.documentElement).getPropertyValue(
		"--color-accent"
	);
});

const expanded: Ref<"none" | "questions" | "courses"> = ref("none");
</script>

<template>
	<div
		class="absolute z-10 w-full max-w-xl mt-1 bg-secondary-bg text-primary-text rounded-lg shadow-lg max-h-[calc(100vh-16rem)] overflow-hidden"
		v-if="searchQuery">
		<div class="py-1 overflow-y-scroll">
			<a
				:href="`/search?query=${searchQuery}`"
				class="flex items-center px-4 py-2 text-sm leading-5 transition-colors duration-150 hover:bg-tertiary-bg focus:outline-none focus:bg-tertiary-bg">
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
				<span>Search for "{{ searchQuery }}"</span>
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
						class="px-4 py-2 text-xs font-semibold text-primary-text uppercase">
						Courses ({{ searchResults.courses.length }})
					</div>
					<div v-for="course in courses" :key="course.id">
						<a
							:href="course.url"
							class="flex items-center justify-between px-4 py-2 text-sm leading-5 transition-colors duration-150 hover:text-primary-text hover:bg-tertiary-bg focus:outline-none focus:bg-tertiary-bg relative">
							<span>{{ course.name }}</span>
							<span
								v-if="course.questions_count > 0"
								class="hidden sm:block text-xs text-on-accent-text bg-accent-clr rounded-full px-2"
								>{{ course.questions_count }} Questions</span
							>
						</a>
					</div>

					<div
						v-if="
							searchResults.courses.length > 3 &&
							expanded !== 'courses'
						"
						class="flex items-center justify-center px-4 py-2 text-sm leading-5 transition-colors duration-150 hover:text-primary-text hover:bg-tertiary-bg focus:outline-none focus:bg-tertiary-bg relative">
						<button
							@click="expanded = 'courses'"
							class="text-xs text-primary-text uppercase">
							Show all
						</button>
					</div>
				</div>

				<!-- questions -->
				<div
					v-if="
						questions?.length > 0 &&
						(expanded === 'none' || expanded == 'questions')
					">
					<div
						class="px-4 py-2 text-xs font-semibold text-primary-text uppercase">
						Questions ({{ searchResults.questions.length }})
					</div>
					<div v-for="question in questions" :key="question.id">
						<a
							:href="question.url"
							class="flex items-center justify-between px-4 py-2 text-sm leading-5 transition-colors duration-150 hover:text-primary-text hover:bg-tertiary-bg focus:outline-none focus:bg-tertiary-bg relative">
							<div class="flex flex-col w-full">
								<div
									class="flex flex-row justify-between items-center">
									<span>{{ question.title }}</span>

									<span
										v-if="question.course"
										class="hidden sm:block text-xs text-on-primary-text bg-primary-clr rounded-full px-2"
										>{{ question.course.name }}</span
									>
								</div>

								<div class="flex flex-row">
									<span
										v-if="question.subject_tags.length > 0"
										class="text-xs text-on-accent-text bg-accent-clr rounded-full px-2 mr-4"
										v-for="tag in question.subject_tags"
										:key="tag.id"
										>{{ tag.name }}</span
									>
								</div>
							</div>
						</a>
					</div>

					<div
						v-if="searchResults.questions.length > 3"
						class="px-4 py-2 text-sm leading-5 transition-colors duration-150 hover:text-primary-text hover:bg-tertiary-bg focus:outline-none focus:bg-tertiary-bg relative">
						<button
							@click="expanded = 'questions'"
							class="cursor-pointer">
							See all
							{{ searchResults.questions.length }} questions
						</button>
					</div>
				</div>
			</div>
		</div>
	</div>
</template>

<style lang="scss" scoped></style>
