<script setup lang="ts">
import type { RouteLocationRaw } from "vue-router";
import Dropdown from "@components/baseLayout/Dropdown.vue";

export type MenuItem = {
	name: string;
	to?: RouteLocationRaw;
	items?: MenuItem[];
	active?: boolean;
};

defineProps<{
	items: MenuItem[];
	direction?: "left" | "right" | "above" | "below";
}>();
</script>

<template>
	<div class="flex flex-col" v-for="item in items" :key="item.name">
		<span v-if="!item.to && !item.items" class="text-tertiary-text">{{
			item.name
		}}</span>

		<RouterLink
			v-if="!item.items && item.to"
			:to="item.to"
			class="flex items-center text-primary-text">
			<span class="py-1">{{ item.name }}</span>
		</RouterLink>

		<Dropdown
			v-if="item.items"
			:direction="direction ?? 'below'"
			align="start">
			<template #button-content>
				<span class="text-primary-text py-1">{{ item.name }}</span>
			</template>

			<template #dropdown-content>
				<div class="flex flex-col">
					<NavDropdown :items="item.items" direction="left" />
				</div>
			</template>
		</Dropdown>
	</div>
</template>

<style lang="scss" scoped></style>
