<script setup lang="ts">
import { onMounted } from "vue";

import { courseStore } from "@stores/courseStore";
import { courseLevelStore } from "@stores/courseLevelStore";
import { computed, ref } from "@vue/reactivity";
import type { Ref } from "vue";
import Dropdown from "./Dropdown.vue";
import { useRoute } from "vue-router";
import NavDropdown from "./NavDropdown.vue";
import { isSideMenuOpen, toggleSideMenu } from "@/stores/appState";
import type { MenuItem } from "@/BaseLayout.vue";

defineProps<{
  menuItems?: MenuItem[];
}>();
</script>

<template>
  <div class="navbar-wrapper bg-primary-bg shadow-md">
    <div class="nebula-nav container flex items-center justify-between py-4">
      <RouterLink to="/" class="flex items-center justify-center gap-2 py-2">
        <div class="logo h-8 w-8"></div>
        <span class="site-name text-3xl text-primary-active">Nebula</span>
      </RouterLink>
      <nav class="nebula-nav__links hidden items-center justify-center md:flex">
        <NavDropdown
          v-for="item in menuItems"
          :key="item.name"
          :menu-item="item"
          align="end"
        />
      </nav>

      <div class="nebula-nav__links items-center justify-center md:hidden">
        <button @click="toggleSideMenu" id="nav-mobile-hamburger">
          <svg
            v-show="!isSideMenuOpen"
            xmlns="http://www.w3.org/2000/svg"
            class="h-6 w-6"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M4 6h16M4 12h16M4 18h16"
            />
          </svg>

          <svg
            v-show="isSideMenuOpen"
            xmlns="http://www.w3.org/2000/svg"
            class="h-6 w-6"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M6 18L18 6M6 6l12 12"
            />
          </svg>
        </button>
      </div>
    </div>
  </div>
</template>

<style scoped lang="scss">
.logo {
  background-image: url("/images/mark.svg");
  background-size: cover;
  background-repeat: no-repeat;
  background-position: center;
}
</style>
