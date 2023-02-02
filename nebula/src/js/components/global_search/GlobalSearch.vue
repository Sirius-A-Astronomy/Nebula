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
        id: string;
        code: string;
        name: string;
        study_type: string;
    };
    url: string;
    questions_count: number;
};

export type SearchUser = {
    id: string;
    name: string;
    email: string;
};

export type SearchResults = {
    questions: SearchQuestion[];
    users: SearchUser[];
    courses: SearchCourse[];
};

import { ref, type Ref } from "vue";
import { throttle } from "throttle-debounce";
import api from "@http/api";

import GlobalSearchResults from "@/components/global_search/GlobalSearchResults.vue";
import { vClickOutside } from "@/vue-services/directives/clickOutside";
import { vKeydownEscape } from "@/vue-services/directives/keydownEscape";

const searchQuery = ref("");
const loading = ref(false);

const search = () => {
    loading.value = true;
    getSearchResults();
};

const searchInputElement = ref<HTMLElement | null>(null);

defineProps<{
    placeholder?: string;
    dashboard: boolean;
}>();

const getSearchResults = throttle(1000, async () => {
    if (searchQuery.value.length === 0) {
        loading.value = false;
        return;
    }
    try {
        const searchResponse = await api.get("/search", {
            query: searchQuery.value,
        });

        searchResults.value = searchResponse.data as SearchResults;
        openResults.value = true;
    } catch (error) {
        console.error(error);
    }
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
    searchInputElement.value?.blur();
};
</script>

<template>
    <div
        class="flex flex-1 justify-center"
        v-click-outside="{
            handler: close,
            exclude: ['search'],
        }"
        @click="searchInputElement?.focus()"
        id="search"
        v-keydown-escape="close"
    >
        <div class="relative mr-6 w-full max-w-xl">
            <div class="absolute inset-y-0 flex items-center pl-2">
                <svg
                    class="h-4 w-4"
                    aria-hidden="true"
                    fill="currentColor"
                    viewBox="0 0 20 20"
                >
                    <path
                        fill-rule="evenodd"
                        d="M8 4a4 4 0 100 8 4 4 0 000-8zM2 8a6 6 0 1110.89 3.476l4.817 4.817a1 1 0 01-1.414 1.414l-4.816-4.816A6 6 0 012 8z"
                        clip-rule="evenodd"
                    />
                </svg>
            </div>
            <input
                class="w-full rounded-md border-0 bg-primary-bg py-2 pl-8 pr-2 text-sm focus:bg-tertiary-bg focus:ring-primary-active"
                type="text"
                :placeholder="placeholder ?? 'Search through Nebula...'"
                v-model="searchQuery"
                @focus="openResults = true"
                @input="search"
                ref="searchInputElement"
                aria-label="Search"
            />

            <!-- Clear button -->
            <button
                class="absolute inset-y-0 right-0 flex items-center pr-2"
                v-if="searchQuery.length > 0"
                @click="searchQuery = ''"
            >
                <svg
                    class="h-4 w-4 hover:text-accent-focus"
                    aria-hidden="true"
                    fill="currentColor"
                    viewBox="0 0 20 20"
                >
                    <path
                        fill-rule="evenodd"
                        d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.536-11.464a1 1 0 00-1.414 0L10 8.586 8.464 7.05a1 1 0 00-1.414 1.414l1.536 1.536-1.536 1.536a1 1 0 101.414 1.414L10 11.414l1.536 1.536a1 1 0 001.414-1.414L11.414 10l1.536-1.536a1 1 0 000-1.414z"
                        clip-rule="evenodd"
                    />
                </svg>
            </button>

            <!-- Show search results in a dropdown -->
            <Transition name="fade">
                <GlobalSearchResults
                    v-if="openResults"
                    :loading="loading"
                    :search-results="searchResults"
                    :dashboard="dashboard"
                    @close="close"
                    :search-query="searchQuery"
                />
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
