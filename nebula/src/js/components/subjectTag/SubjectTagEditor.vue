<script setup lang="ts">
import subjectTagStore from "@stores/subjectTagStore";
import { onMounted, ref, computed, nextTick } from "vue";
import RemovableSubjectTag from "@components/subjectTag/RemovableSubjectTag.vue";
import fuzzysort from "fuzzysort";
import useFlashStore from "@stores/flashStore";

const flash = useFlashStore();

const props = defineProps<{
    modelValue: string[];
    options?: {
        placeholder?: string;
    };
}>();

const existingTags = subjectTagStore.getters.all;

const inputValue = ref("");

const emit = defineEmits<{
    (event: "update:modelValue", value: string[]): void;
}>();

const suggestions = computed(() => {
    const tagsToSearch = existingTags.value
        .filter((tag) => !props.modelValue.includes(tag.name))
        .map((tag) => tag.name);

    const results = fuzzysort.go(inputValue.value, tagsToSearch, {});
    return results.map((result) => result.target);
});

const selectedSuggestion = ref("");

const moveSuggestionSelection = (n = 1) => {
    const index = suggestions.value.indexOf(selectedSuggestion.value);
    if (index === -1) {
        selectedSuggestion.value = suggestions.value[0];
    } else {
        selectedSuggestion.value =
            suggestions.value[
                (index + n + suggestions.value.length) %
                    suggestions.value.length
            ];
    }

    nextTick(() => {
        const suggestion = document.querySelector(
            ".selectedSuggestion"
        ) as HTMLElement;
        suggestion.scrollIntoView({
            behavior: "smooth",
            block: "center",
        });
    });
};

const addTagFromSelectedSuggestion = () => {
    if (!props.modelValue.includes(selectedSuggestion.value)) {
        emit("update:modelValue", [
            ...props.modelValue,
            selectedSuggestion.value,
        ]);
        inputValue.value = "";
        selectedSuggestion.value = "";
    } else {
        flash.add("Tag already added", "warning");
    }
};

const addTagFromInput = () => {
    const tag = inputValue.value.toLowerCase().trim();
    if (tag.length > 0) {
        if (!props.modelValue.includes(tag)) {
            emit("update:modelValue", [...props.modelValue, tag]);
            inputValue.value = "";
        } else {
            flash.add("Tag already added", "warning");
        }
    }
};

const onKeyDown = (event: KeyboardEvent) => {
    if (event.key === "ArrowDown") {
        moveSuggestionSelection(1);
        return;
    }
    if (event.key === "ArrowUp") {
        moveSuggestionSelection(-1);
        return;
    }
    if (event.key === "Tab") {
        if (selectedSuggestion.value) {
            event.preventDefault();
            addTagFromSelectedSuggestion();
        }
        return;
    }
    if (event.key === "Enter") {
        event.preventDefault();
        if (selectedSuggestion.value) {
            addTagFromSelectedSuggestion();
            return;
        }
        addTagFromInput();
    }
};

const removeTag = (tag: string) => {
    emit(
        "update:modelValue",
        props.modelValue.filter((t) => t !== tag)
    );
};

onMounted(() => {
    if (subjectTagStore.state.shouldLoadAll()) {
        subjectTagStore.actions.getAll();
    }
});
</script>

<template>
    <TransitionGroup
        name="fade"
        tag="div"
        class="relative flex flex-col gap-1 rounded-lg py-2 focus-within:outline-1 focus-within:outline-blue-500"
    >
        <label for="subjectTagInput" key="label">Subject Tags</label>

        <TransitionGroup
            name="fade"
            class="relative flex flex-row flex-wrap gap-2 pt-2"
            v-if="modelValue.length"
            key="tags"
            tag="div"
        >
            <RemovableSubjectTag
                v-for="tag in modelValue"
                :key="tag"
                :subject-tag="{ name: tag, id: '' }"
                @remove="(tag) => removeTag(tag.name)"
            />

            <button
                v-if="modelValue.length > 2"
                key="remove-all"
                @click="emit('update:modelValue', [])"
            >
                Remove all
            </button>
        </TransitionGroup>
        <input
            class="rounded-lg border-secondary-bg bg-transparent text-primary-text"
            type="text"
            name="subjectTag"
            id="subjectTagInput"
            :placeholder="
                options?.placeholder ?? 'Start typing to add a subject tag'
            "
            @keydown="onKeyDown"
            @input="selectedSuggestion = ''"
            v-model="inputValue"
            key="input"
        />

        <div
            class="flex max-h-60 flex-col gap-1 overflow-auto"
            v-if="suggestions.length"
            key="suggestions"
        >
            <TransitionGroup name="fade">
                <div
                    class="subject-tag cursor-pointer rounded-lg px-2 lowercase text-primary-text"
                    :class="{
                        'selectedSuggestion bg-primary-clr':
                            tag === selectedSuggestion,
                    }"
                    v-for="tag in suggestions"
                    :key="tag"
                    @click="
                        () => {
                            if (!modelValue.includes(tag)) {
                                emit('update:modelValue', [...modelValue, tag]);
                            }
                        }
                    "
                >
                    {{ tag }}
                </div>
            </TransitionGroup>
        </div>

        <div class="text-sm text-secondary-text" key="help-text">
            Start typing to search existing tags. Press
            <kbd class="font-mono rounded-sm bg-secondary-bg px-1">Enter</kbd>
            to add a new tag.
        </div>
    </TransitionGroup>
</template>

<style lang="scss" scoped>
.fade-enter-active,
.fade-move,
.fade-leave-active {
    transition: all 0.5s cubic-bezier(0.55, 0, 0.1, 1);
}

.fade-enter-from {
    opacity: 0;
}
.fade-leave-active {
    position: absolute;
    @apply sr-only;
}
</style>
