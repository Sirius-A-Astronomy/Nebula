<script setup lang="ts">
export type SearchQuestion = {
	id: string;
	title: string;
	content: string;
	created_at: string;
	url: string;
	user: {
		id: string;
		name: string;
	};
	course: {
		id: string;
		name: string;
		code: string;
	};
	subject_tags: {
		id: string;
		name: string;
	}[];
};

export type SearchCourse = {
	id: string;
	name: string;
	code: string;
	description: string;
	semester: string;
	course_level: {
		code: string;
		name: string;
		study_type: string;
	};
	url: string;
	questions_count: number;
};

export type SearchResults = {
	questions: SearchQuestion[];
	users: {
		id: string;
		name: string;
	}[];
	courses: SearchCourse[];
};

import { ref, type Ref } from "vue";
import { throttle } from "throttle-debounce";
import api from "@http/api";

import Results from "@components/global_search/Results.vue";
import { vClickOutside } from "@/vue-services/directives/clickOutside";
import { vKeydownEscape } from "@/vue-services/directives/keydownEscape";

const searchQuery = ref("");
const loading = ref(false);

const search = () => {
	loading.value = true;
	getSearchResults();
};

const getSearchResults = throttle(1000, async () => {
	const searchResponse = await api.get("/search", {
		query: searchQuery.value,
	});

	searchResults.value = searchResponse.data as SearchResults;
	openResults.value = true;
	loading.value = false;
});

const searchResults: Ref<SearchResults> = ref({
	questions: [],
	users: [],
	tags: [],
	courses: [],
});
const openResults = ref(false);

const close = () => {
	openResults.value = false;
};
</script>

<template>
	<div
		class="flex justify-center flex-1"
		v-click-outside="close"
		v-keydown-escape="close">
		<div class="relative w-full max-w-xl mr-6">
			<div class="absolute inset-y-0 flex items-center pl-2">
				<svg
					class="w-4 h-4"
					aria-hidden="true"
					fill="currentColor"
					viewBox="0 0 20 20">
					<path
						fill-rule="evenodd"
						d="M8 4a4 4 0 100 8 4 4 0 000-8zM2 8a6 6 0 1110.89 3.476l4.817 4.817a1 1 0 01-1.414 1.414l-4.816-4.816A6 6 0 012 8z"
						clip-rule="evenodd" />
				</svg>
			</div>
			<input
				class="w-full pl-8 pr-2 py-2 text-sm border-0 rounded-md input"
				type="text"
				placeholder="Search through Nebula..."
				v-model="searchQuery"
				@input="search"
				aria-label="Search" />

			<!-- Show search results in a dropdown -->
			<Transition name="fade">
				<Results
					v-if="openResults"
					:loading="loading"
					:search-results="searchResults"
					:search-query="searchQuery" />
			</Transition>
		</div>
	</div>
</template>

<style lang="scss">
.fade-enter-active,
.fade-leave-active {
	transition: opacity 0.1s ease;
}

.fade-enter-from,
.fade-leave-to {
	opacity: 0;
}
</style>
