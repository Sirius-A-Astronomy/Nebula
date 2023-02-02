<script setup lang="ts">
import DropdownMenu from "@components/baseLayout/DropdownMenu.vue";

import type { MenuItem } from "@/BaseLayout.vue";
import { useRoute, useRouter } from "vue-router";

const route = useRoute();
const router = useRouter();

const isActiveOrHasAciveSubItem = (item: MenuItem): boolean => {
  if (item.to && router.resolve(item.to).href === route.fullPath) return true;
  if (item.items) {
    return item.items.some((subItem) => isActiveOrHasAciveSubItem(subItem));
  }
  return false;
};

const emit = defineEmits<{
  (event: "close", ...args: any[]): void;
}>();

defineProps<{
  menuItem: MenuItem;
  direction?: "left" | "right" | "above" | "below";
  align?: "start" | "end" | "center";
  type?: "major" | "minor";
}>();
</script>

<template>
  <RouterLink
    :to="menuItem.to ?? ''"
    v-if="!menuItem.items"
    @click="(e: Event) => {
      if (menuItem.to) {
              emit('close');
                return
            }

            if (menuItem.action) {
              menuItem.action();
              emit('close');
            }
            e.preventDefault();
        }"
    class="flex"
    :class="{
      'cursor-default': !menuItem.to && !menuItem.action,
      'hover:text-primary-text': menuItem.to || menuItem.action,
      'text-2xl': type === 'major',
    }"
    :active-class="menuItem.to ? '!text-primary-active' : ''"
  >
    <span class="py-1">{{ menuItem.name }}</span>
  </RouterLink>
  <DropdownMenu
    v-if="menuItem.items"
    :direction="direction ?? 'below'"
    :align="align ?? 'start'"
    @close="emit('close')"
  >
    <template #button-content>
      <span
        class="py-1 hover:text-primary-text"
        :class="{
          '!text-primary-active': isActiveOrHasAciveSubItem(menuItem),
        }"
        >{{ menuItem.name }}</span
      >
    </template>

    <template #dropdown-content="{ closeParent }">
      <div class="flex flex-col">
        <NavDropdown
          v-for="item in menuItem.items"
          :key="item.name"
          :menu-item="item"
          :direction="type !== 'major' ? 'right' : 'left'"
          @close="closeParent"
          align="start"
        />
      </div>
    </template>
  </DropdownMenu>
</template>

<style lang="scss" scoped></style>
