<script setup lang="ts">
import { RouterLink, RouterView } from "vue-router";
import { isSideMenuOpen, closeSideMenu } from "@/stores/dashboardStore";
import { vClickOutside } from "@/vue-services/directives/clickOutside";
import { vKeydownEscape } from "@/vue-services/directives/keydownEscape";

import "@scss/views/dashboard.scss";
import "@scss/main.scss";

import Header from "@components/dashboard/Header.vue";
import Sidemenu from "@components/dashboard/Sidemenu.vue";
</script>

<template>
	<div class="w-full min-h-screen flex flex-col">
		<aside
			class="z-20 hidden w-64 overflow-y-auto bg-secondary-bg md:block flex-shrink-0 flex-grow h-screen fixed">
			<Sidemenu />
		</aside>

		<!-- Mobile SideMenu -->
		<!-- Backdrop -->
		<template v-if="isSideMenuOpen">
			<div
				class="fixed inset-0 z-10 flex items-end bg-black bg-opacity-50 sm:items-center sm:justify-center h-screen" />
			<aside
				class="fixed inset-y-0 z-20 flex-shrink-0 w-64 mt-16 overflow-y-auto bg-secondary-bg md:hidden"
				v-click-outside="{
					handler: closeSideMenu,
					exclude: ['nav-mobile-hamburger'],
				}"
				v-keydown-escape="closeSideMenu">
				<Sidemenu />
			</aside>
		</template>

		<div class="md:ml-64">
			<Header />
			<div class="container">
				<RouterView />
			</div>
		</div>
	</div>
</template>

<style lang="scss" scoped></style>
