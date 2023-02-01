<script setup lang="ts">
export type BreadCrumb = {
    name: string;
    to: RouteLocationRaw;
};
import type { RouteLocationRaw } from "vue-router";
import { RouterLink } from "vue-router";

defineProps<{
    breadcrumbs: BreadCrumb[];
}>();
</script>

<template>
    <div>
        <div class="path-container">
            <RouterLink
                v-for="breadcrumb in breadcrumbs"
                :key="breadcrumb.name"
                class="path-container__link"
                :to="breadcrumb.to"
                active-class="path-container__link--active"
                >{{ breadcrumb.name }}</RouterLink
            >
        </div>
    </div>
</template>

<style lang="scss" scoped>
.path-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    margin-bottom: 1rem;

    justify-content: flex-start;
    flex-wrap: wrap;
    gap: 0.125rem;

    @media screen and (min-width: 768px) {
        flex-direction: row;
        justify-content: flex-start;
    }

    &__link {
        color: var(--color-text-secondary);
        font-family: "Poppins", "Open Sans", "Arial", sans-serif;
        font-style: normal;
        font-weight: 600;
        font-size: var(--font-size-h4);
        flex: 0 0 content;
        text-align: center;

        &:hover {
            color: var(--color-text-primary);
        }

        &::after {
            content: ">";
            font-family: "Poppins", "Open Sans", "Arial", sans-serif;
            font-style: normal;
            font-weight: 600;
            font-size: var(--font-size-h4);
            margin-inline: 0.0625rem;
        }
        &:last-child {
            color: var(--color-primary-active);
            &::after {
                content: "";
            }
        }
    }
}
</style>
