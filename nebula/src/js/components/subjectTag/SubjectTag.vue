<script setup lang="ts">
import type { SubjectTag } from "@stores/subjectTagStore";
defineProps<{
    subjectTag: SubjectTag;
}>();
</script>

<template>
    <span class="subject-tag">{{ subjectTag.name }}</span>
</template>

<style lang="scss" scoped>
.subject-tag {
    display: inline-block;
    padding: 0.2rem 0.5rem;
    border-radius: 0.3rem;
    font-size: 0.75rem;
    color: var(--color-text-on-accent);
    background-color: var(--color-accent);

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

    &:hover {
        background-color: var(--color-accent-focus);
        color: var(--color-text-on-accent);
    }
}
</style>
