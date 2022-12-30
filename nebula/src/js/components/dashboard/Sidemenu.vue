<script setup lang="ts">
import { RouterLink } from "vue-router";
import { closeSideMenu } from "@/stores/dashboardStore";

import router from "@/router";

const menuLinks = [
	{
		name: "Courses",
		path: { name: "dashboard-course-index" },
	},
];
</script>

<template>
	<div class="py-2 text-primary-text">
		<a class="flex flex-row items-center navbar-brand px-4" href="/">
			<span class="site-name">Nebula</span>
		</a>

		<nav class="flex flex-col items-start">
			<RouterLink
				v-for="link in menuLinks"
				:to="link.path"
				class="px-4 py-2 nav-link relative"
				active-class="active"
				@click="closeSideMenu">
				<span class="active-indicator"></span>
				{{ link.name }}
			</RouterLink>
		</nav>
	</div>
</template>

<style lang="scss" scoped>
.active-indicator {
	position: absolute;
	top: 50%;
	left: -4px;
	width: 0;
	height: 80%;
	transform: translateY(-50%);
	border-radius: 0 0.25rem 0.25rem 0;
	background-color: var(--color-primary-active);
	transition: all 0.3s ease-in-out;
}
.active > .active-indicator {
	top: 50%;
	left: 0;
	width: 3px;
	height: 80%;
	transform: translateY(-50%);
}
</style>
