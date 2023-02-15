<script setup lang="ts">
import { RouterView } from "vue-router";
import { isSideMenuOpen, closeSideMenu } from "@/stores/dashboardStore";
import { vClickOutside } from "@/vue-services/directives/clickOutside";
import { vKeydownEscape } from "@/vue-services/directives/keydownEscape";

import useFlash from "@stores/flashStore";

import Header from "@/components/dashboard/DashboardHeader.vue";
import Sidemenu from "@/components/dashboard/DashboardSidemenu.vue";

const flash = useFlash();
</script>

<template>
    <div class="flex min-h-screen w-full flex-col">
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
