<script setup lang="ts">
import type { SubjectTag } from "@stores/subjectTagStore";
import { faClose } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";
const props = defineProps<{
    subjectTag: SubjectTag;
}>();

const emit = defineEmits<{
    (event: "remove", subjectTag: SubjectTag): void;
}>();

const onRemove = () => {
    emit("remove", props.subjectTag);
};
</script>

<template>
    <div class="subject-tag flex flex-row gap-2">
        <span class="subject-tag__text">
            {{ subjectTag.name }}
        </span>
        <button
            class="flex flex-row items-center gap-1 text-sm text-on-accent-text"
            :aria-label="`Remove subject tag: '${subjectTag.name}'`"
            @click="onRemove"
            :title="`Remove subject tag: '${subjectTag.name}'`"
        >
            <font-awesome-icon :icon="faClose" class="text-on-accent-text" />
        </button>
    </div>
</template>

<style lang="scss" scoped>
.subject-tag {
    display: flex;
    padding: 0.2rem 0.5rem;
    border-radius: 0.3rem;
    font-size: 0.75rem;
    color: var(--color-text-on-accent);
    background-color: var(--color-accent);
    align-items: center;
    justify-content: center;

    .subject-tag__text {
        font-style: normal;
        font-weight: 400;
        line-height: 0.875rem;
        text-align: center;
        letter-spacing: 0.095em;
        text-transform: lowercase;

        max-width: 200px;
        text-overflow: ellipsis;
        white-space: nowrap;
        overflow: hidden;
    }

    &:has(button:hover) {
        background-color: var(--color-accent-focus);
        color: var(--color-text-on-accent);
    }
}
</style>
