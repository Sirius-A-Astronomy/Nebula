<script setup lang="ts">
import Dropdown from "@components/baseLayout/Dropdown.vue";

import type { MenuItem } from "@/BaseLayout.vue";

defineProps<{
  menuItem: MenuItem;
  direction?: "left" | "right" | "above" | "below";
  align?: "start" | "end" | "center";
}>();
</script>

<template>
  <RouterLink
    :to="menuItem.to ?? ''"
    v-if="!menuItem.items"
    @click="(e: Event) => {
            if (menuItem.to) {
                return
            }

            if (menuItem.action)
                menuItem.action();
            e.preventDefault();
        }"
    class="flex text-primary-text"
    :class="{
      'cursor-default': !menuItem.to && !menuItem.action,
    }"
  >
    <span class="py-1">{{ menuItem.name }}</span>
  </RouterLink>
  <Dropdown
    v-if="menuItem.items"
    :direction="direction ?? 'below'"
    :align="align ?? 'start'"
  >
    <template #button-content>
      <span class="py-1 text-primary-text">{{ menuItem.name }}</span>
    </template>

    <template #dropdown-content>
      <div class="flex flex-col">
        <NavDropdown
          v-for="item in menuItem.items"
          :key="item.name"
          :menu-item="item"
          direction="left"
          align="start"
        />
      </div>
    </template>
  </Dropdown>
</template>

<style lang="scss" scoped></style>
