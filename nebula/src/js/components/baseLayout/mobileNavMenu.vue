<script setup lang="ts">
import { vKeydownEscape } from "@/vue-services/directives/keydownEscape";
import { vClickOutside } from "@/vue-services/directives/clickOutside";
import type { MenuItem } from "@/BaseLayout.vue";

import recursiveMobileNavDropdown from "@components/baseLayout/recursiveMobileNavDropdown.vue";

import {
  isSideMenuOpen,
  closeSideMenu,
  toggleSideMenu,
} from "@stores/appState";
import { onMounted } from "vue";

defineProps<{
  menuItems: Array<MenuItem & { expanded?: boolean }>;
}>();
</script>

<template>
  <Transition name="fade">
    <div
      v-if="isSideMenuOpen"
      class="fixed inset-0 top-20 z-10 -mt-1 flex h-screen bg-primary-bg sm:items-center sm:justify-center md:hidden"
    />
  </Transition>
  <Transition name="fade">
    <nav
      v-if="isSideMenuOpen"
      class="container fixed inset-0 top-20 z-20 w-full max-w-[288px] flex-shrink-0 overflow-y-auto md:hidden"
      id="mobile-nav"
      v-click-outside="{
        handler: closeSideMenu,
        exclude: ['nav-mobile-hamburger', 'mobile-nav'],
      }"
      v-keydown-escape="closeSideMenu"
    >
      <div class="flex h-full flex-col">
        <ul>
          <li v-for="item in menuItems" :key="item.name">
            <recursive-mobile-nav-dropdown :item="item" />
          </li>
        </ul>
      </div>
    </nav>
  </Transition>
</template>

<style lang="scss" scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.1s ease-in-out;
}

.fade-enter,
.fade-leave-to {
  opacity: 0;
}

.fade-enter-to,
.fade-leave {
  opacity: 1;
}
</style>
