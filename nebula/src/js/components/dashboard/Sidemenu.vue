<script setup lang="ts">
import { RouterLink } from "vue-router";
import { closeSideMenu } from "@/stores/dashboardStore";

import { useRoute } from "vue-router";

const route = useRoute();

const menuLinks = [
	{
		name: "Courses",
		path: { name: "dashboard.course.index" },
		active: {
			startsWith: "dashboard.course",
		},
	},
	{
		name: "Users",
		path: { name: "dashboard.user.index" },
		active: {
			startsWith: "dashboard.user",
		},
	},

	{
		name: "Questions",
		path: { name: "dashboard.question.index" },
		active: {
			startsWith: "dashboard.question",
		},
	},
];
</script>

<template>
	<div class="py-2 text-primary-text">
		<RouterLink class="flex flex-row items-center px-4 py-2" :to="{
            name: 'home'
        }">
			<span class="text-primary-active text-4xl tracking-wide"
				>Nebula</span
			>
		</RouterLink>

		<nav class="flex flex-col items-start">
			<RouterLink
				v-for="link in menuLinks"
				:to="link.path"
				class="px-4 py-2 nav-link relative text-2xl font-medium hover:text-primary-active tracking-wide"
				active-class="active text-primary-active"
				:class="{
                    'active text-primary-active': (route?.name as string)?.startsWith(link.active.startsWith)
                }"
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
