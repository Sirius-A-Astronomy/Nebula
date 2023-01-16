<script setup lang="ts">
import type { RouteLocationRaw } from "vue-router";
import Dropdown from "@components/baseLayout/Dropdown.vue";

export type MenuItem = {
	label: string;
	to?: RouteLocationRaw;
	items?: MenuItem[];
	active?: boolean;
};

defineProps<{
	items: MenuItem[];
}>();
</script>

<template>
	<Dropdown direction="below" align="end">
		<template #button-content>
			<div class="flex items-center">
				<div class="w-8 h-8 rounded-full bg-primary-active"></div>
				<span class="text-primary-active">User</span>
			</div>
		</template>

		<template #dropdown-content>
			<div class="flex flex-col">
				<div
					v-for="item in items"
					:key="item.label"
					class="flex items-center px-2">
					<Router
						:is="item.to ? 'RouterLink' : 'div'"
						v-bind="{
							to: item.to,
							class: 'flex items-center',
						}">
						<span v-if="!item.items" class="py-1">{{
							item.label
						}}</span>

						<Dropdown
							v-if="item.items"
							direction="left"
							align="start">
							<template #button-content>
								<span class="text-primary-text py-1">{{
									item.label
								}}</span>
							</template>

							<template #dropdown-content>
								<div class="flex flex-col">
									<div
										v-for="nestedItem in item.items"
										:key="nestedItem.label"
										class="flex items-center px-2">
										<RouterLink
											:to="nestedItem.to"
											class="flex items-center">
											<span class="py-1">{{
												nestedItem.label
											}}</span>
										</RouterLink>
									</div>
								</div>
							</template>
						</Dropdown>
					</Router>
				</div>
			</div>
		</template>
	</Dropdown>
</template>

<style lang="scss" scoped></style>
