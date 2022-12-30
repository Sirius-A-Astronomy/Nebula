<script setup lang="ts">
import api from "@/http/api";
import { throttle } from "throttle-debounce";
import {
	toggleSideMenu,
	isProfileMenuOpen,
	toggleProfileMenu,
	closeProfileMenu,
} from "@/stores/dashboardStore";

import { authenticatedUser } from "@/stores/sessionStore";

import { vClickOutside } from "@/vue-services/directives/clickOutside";
import { vKeydownEscape } from "@/vue-services/directives/keydownEscape";

import Search from "@components/global_search/Search.vue";

const user = authenticatedUser;

const withSearch = true;
</script>

<template>
	<div class="w-full bg-secondary-bg shadow-md z-10 relative">
		<div class="container flex flex-row justify-between items-center py-4">
			<button
				id="nav-mobile-hamburger"
				class="p-1 mr-5 -ml-1 rounded-md md:hidden text-accent"
				@click="toggleSideMenu"
				aria-label="Menu">
				<svg
					class="w-6 h-6"
					aria-hidden="true"
					fill="currentColor"
					viewBox="0 0 20 20">
					<path
						fill-rule="evenodd"
						d="M3 5a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zM3 10a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zM3 15a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1z"
						clip-rule="evenodd" />
				</svg>
			</button>

			<Search v-if="withSearch" :dashboard="true" />

			<div
				class="flex flex-row justify-end ml-auto items-center"
				:class="withSearch ? '' : 'w-full ml-auto'">
				<ul>
					<li class="relative">
						<button
							id="nav-profile-photo"
							class="align-middle rounded-full focus:shadow-outline-purple focus:outline-none flex flex-row gap-1"
							@click="toggleProfileMenu"
							v-keydown-escape="closeProfileMenu"
							aria-label="Account"
							aria-haspopup="true">
							<svg
								xmlns="http://www.w3.org/2000/svg"
								height="24"
								width="24"
								fill="currentColor">
								<path
									d="M5.85 17.1q1.275-.975 2.85-1.538Q10.275 15 12 15q1.725 0 3.3.562 1.575.563 2.85 1.538.875-1.025 1.363-2.325Q20 13.475 20 12q0-3.325-2.337-5.663Q15.325 4 12 4T6.338 6.337Q4 8.675 4 12q0 1.475.488 2.775.487 1.3 1.362 2.325ZM12 13q-1.475 0-2.488-1.012Q8.5 10.975 8.5 9.5t1.012-2.488Q10.525 6 12 6t2.488 1.012Q15.5 8.025 15.5 9.5t-1.012 2.488Q13.475 13 12 13Zm0 9q-2.075 0-3.9-.788-1.825-.787-3.175-2.137-1.35-1.35-2.137-3.175Q2 14.075 2 12t.788-3.9q.787-1.825 2.137-3.175 1.35-1.35 3.175-2.138Q9.925 2 12 2t3.9.787q1.825.788 3.175 2.138 1.35 1.35 2.137 3.175Q22 9.925 22 12t-.788 3.9q-.787 1.825-2.137 3.175-1.35 1.35-3.175 2.137Q14.075 22 12 22Zm0-2q1.325 0 2.5-.387 1.175-.388 2.15-1.113-.975-.725-2.15-1.113Q13.325 17 12 17t-2.5.387q-1.175.388-2.15 1.113.975.725 2.15 1.113Q10.675 20 12 20Zm0-9q.65 0 1.075-.425.425-.425.425-1.075 0-.65-.425-1.075Q12.65 8 12 8q-.65 0-1.075.425Q10.5 8.85 10.5 9.5q0 .65.425 1.075Q11.35 11 12 11Zm0-1.5Zm0 9Z" />
							</svg>
							<span class="md:inline hidden" v-if="user">
								{{ user.name }}
							</span>
						</button>
						<ul
							v-if="isProfileMenuOpen"
							v-clickOutside="{
								handler: closeProfileMenu,
								exclude: ['nav-profile-photo'],
							}"
							v-keydown-escape="closeProfileMenu"
							class="absolute right-0 w-56 p-2 mt-2 space-y-2 text-slate-600 bg-white border border-slate-100 rounded-md shadow-md dark:border-slate-700 dark:text-slate-300 dark:bg-slate-700"
							aria-label="submenu">
							<li class="flex">
								<a
									class="inline-flex items-center w-full px-2 py-1 text-sm font-semibold transition-colors duration-150 rounded-md hover:bg-slate-100 hover:text-slate-800 dark:hover:bg-slate-800 dark:hover:text-slate-200"
									href="#">
									<svg
										class="w-4 h-4 mr-3"
										aria-hidden="true"
										fill="none"
										stroke-linecap="round"
										stroke-linejoin="round"
										stroke-width="2"
										viewBox="0 0 24 24"
										stroke="currentColor">
										<path
											d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
									</svg>
									<span>Profile</span>
								</a>
							</li>
							<li class="flex">
								<a
									class="inline-flex items-center w-full px-2 py-1 text-sm font-semibold transition-colors duration-150 rounded-md hover:bg-slate-100 hover:text-slate-800 dark:hover:bg-slate-800 dark:hover:text-slate-200"
									href="#">
									<svg
										class="w-4 h-4 mr-3"
										aria-hidden="true"
										fill="none"
										stroke-linecap="round"
										stroke-linejoin="round"
										stroke-width="2"
										viewBox="0 0 24 24"
										stroke="currentColor">
										<path
											d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
										<path
											d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
									</svg>
									<span>Settings</span>
								</a>
							</li>
							<li class="flex">
								<button
									class="inline-flex items-center w-full px-2 py-1 text-sm font-semibold transition-colors duration-150 rounded-md hover:bg-slate-100 hover:text-slate-800 dark:hover:bg-slate-800 dark:hover:text-slate-200">
									<svg
										class="w-4 h-4 mr-3"
										aria-hidden="true"
										fill="none"
										stroke-linecap="round"
										stroke-linejoin="round"
										stroke-width="2"
										viewBox="0 0 24 24"
										stroke="currentColor">
										<path
											d="M11 16l-4-4m0 0l4-4m-4 4h14m-5 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h7a3 3 0 013 3v1" />
									</svg>
									<span>Log out</span>
								</button>
							</li>
						</ul>
					</li>
				</ul>
			</div>
		</div>
	</div>
</template>

<style lang="scss" scoped></style>
