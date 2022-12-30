<script setup lang="ts">
import { RouterLink, RouterView } from "vue-router";
import { isSideMenuOpen, closeSideMenu } from "@/stores/dashboardStore";
import { vClickOutside } from "@/vue-services/directives/clickOutside";
import { vKeydownEscape } from "@/vue-services/directives/keydownEscape";

import useFlash from "@stores/flashStore";

import "@scss/views/dashboard.scss";
import "@scss/main.scss";

import Header from "@components/dashboard/Header.vue";
import Sidemenu from "@components/dashboard/Sidemenu.vue";

const flash = useFlash();
</script>

<template>
	<div class="w-full min-h-screen flex flex-col">
		<template v-if="flash.messages.value.length">
			<div class="absolute top-0 right-0 m-4 flex flex-col gap-4 z-50">
				<div
					v-for="flashMessage in flash.messages.value"
					:key="flashMessage.id"
					class="p-4 rounded-md font-bold flex flex-row justify-between items-center gap-2"
					:class="{
						'bg-alert-error text-alert-error-text':
							flashMessage.type === 'error',
						'bg-alert-success text-alert-succes-text':
							flashMessage.type === 'success',
						'bg-alert-warning text-alert-warning-text':
							flashMessage.type === 'warning',
						'bg-alert-info text-alert-info-text':
							flashMessage.type === 'info',
					}">
					<span>{{ flashMessage.message }}</span>
					<button @click="flash.remove(flashMessage.id)">
						<svg
							xmlns="http://www.w3.org/2000/svg"
							height="24"
							width="24"
							fill="currentcolor">
							<path
								d="M6.4 19 5 17.6l5.6-5.6L5 6.4 6.4 5l5.6 5.6L17.6 5 19 6.4 13.4 12l5.6 5.6-1.4 1.4-5.6-5.6Z" />
						</svg>
					</button>
				</div>
			</div>
		</template>

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
