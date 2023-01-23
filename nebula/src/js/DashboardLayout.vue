<script setup lang="ts">
import { RouterView } from "vue-router";
import { isSideMenuOpen, closeSideMenu } from "@/stores/dashboardStore";
import { vClickOutside } from "@/vue-services/directives/clickOutside";
import { vKeydownEscape } from "@/vue-services/directives/keydownEscape";

import useFlash from "@stores/flashStore";

import Header from "@components/dashboard/Header.vue";
import Sidemenu from "@components/dashboard/Sidemenu.vue";
import ModalContainer from "@components/ui/modals/ModalContainer.vue";

const flash = useFlash();
</script>

<template>
  <div class="flex min-h-screen w-full flex-col">
    <template v-if="flash.messages.value.length">
      <div class="absolute top-0 right-0 z-50 m-4 flex flex-col gap-4">
        <div
          v-for="flashMessage in flash.messages.value"
          :key="flashMessage.id"
          class="flex flex-row items-center justify-between gap-2 rounded-md p-4 font-bold"
          :class="{
            'bg-alert-error text-alert-error-text':
              flashMessage.type === 'error',
            'text-alert-succes-text bg-alert-success':
              flashMessage.type === 'success',
            'bg-alert-warning text-alert-warning-text':
              flashMessage.type === 'warning',
            'bg-alert-info text-alert-info-text': flashMessage.type === 'info',
          }"
        >
          <span>{{ flashMessage.message }}</span>
          <button @click="flash.remove(flashMessage.id)">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              height="24"
              width="24"
              fill="currentcolor"
            >
              <path
                d="M6.4 19 5 17.6l5.6-5.6L5 6.4 6.4 5l5.6 5.6L17.6 5 19 6.4 13.4 12l5.6 5.6-1.4 1.4-5.6-5.6Z"
              />
            </svg>
          </button>
        </div>
      </div>
    </template>

    <aside
      class="fixed z-20 hidden h-screen w-64 flex-shrink-0 flex-grow overflow-y-auto bg-secondary-bg md:block"
    >
      <Sidemenu />
    </aside>

    <!-- Mobile SideMenu -->
    <!-- Backdrop -->
    <template v-if="isSideMenuOpen">
      <div
        class="fixed inset-0 z-10 flex h-screen items-end bg-black bg-opacity-50 sm:items-center sm:justify-center"
      />
      <aside
        class="fixed inset-y-0 z-20 mt-16 w-64 flex-shrink-0 overflow-y-auto bg-secondary-bg md:hidden"
        v-click-outside="{
          handler: closeSideMenu,
          exclude: ['nav-mobile-hamburger'],
        }"
        v-keydown-escape="closeSideMenu"
      >
        <Sidemenu />
      </aside>
    </template>

    <div class="relative overflow-hidden">
      <Header />
      <div
        class="fixed inset-x-0 top-20 bottom-0 overflow-auto px-4 py-4 md:left-64"
        id="content"
      >
        <div class="container">
          <RouterView />
        </div>
      </div>
    </div>
  </div>
</template>
