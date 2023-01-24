<script setup lang="ts">
import { closeSideMenu } from "@/stores/appState";
import type { MenuItem } from "@/BaseLayout.vue";
import { ref } from "vue";
defineProps<{
  item: MenuItem;
}>();

const expanded = ref(false);
</script>

<template>
  <RouterLink
    :to="item.to ?? ''"
    @click="
            (e: Event) => {
                if (item.to) {
                    expanded= false;
                    closeSideMenu();
                    return
                }
                if (item.items) {
                    expanded= !expanded;
                }
                if (item.action)
                    item.action();
                e.preventDefault();
            }
        "
    class="flex items-center text-primary-text"
  >
    <span
      class="flex-shrink flex-grow-0 py-1"
      :class="{
        'font-bold': expanded,
        'font-normal': !expanded,
        'cursor-default text-tertiary-text':
          !item.to && !item.items && !item.action,
      }"
      >{{ item.name }}</span
    >
    <svg
      xmlns="http://www.w3.org/2000/svg"
      height="24"
      fill="currentColor"
      class="icon ml-auto flex items-center justify-center transition-transform"
      v-if="item.items"
      :class="{
        'rotate-180': !expanded,
        'rotate-0': expanded,
      }"
      width="24"
    >
      <path d="m12 15.375-6-6 1.4-1.4 4.6 4.6 4.6-4.6 1.4 1.4Z" />
    </svg>
  </RouterLink>
  <ul
    class="recursive-item-list border-l border-secondary-bg pl-2"
    v-if="expanded"
  >
    <li v-for="nestedItem in item.items" :key="nestedItem.name">
      <recursive-mobile-nav-dropdown :item="nestedItem" />
    </li>
  </ul>
</template>

<style lang="scss" scoped>
.recursive-item-list {
  font-size: 0.96em;
  li {
    list-style: none;
  }
}
</style>
