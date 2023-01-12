<script setup lang="ts">
import { userStore, accessLevels } from "@stores/userStore";

import { ref, onMounted } from "vue";

const users = ref(userStore.getters.all);
const loading = ref(true);

const loadData = async () => {
	if (userStore.state.shouldLoadAll()) {
		await userStore.actions.getAll();
	}
	loading.value = false;
};

onMounted(loadData);
</script>

<template>
	<div>
		<div class="flex flex-row justify-between items-center">
			<h1 class="text-3xl">Users</h1>
			<RouterLink
				to="/dashboard/users/create"
				class="px-4 py-2 bg-primary-active text-primary-bg rounded-md font-bold hover:text-primary-text"
				>Create</RouterLink
			>
		</div>

		<div class="flex flex-col gap-2">
			<RouterLink
				v-for="user in users.sort(
					(a, b) => b.access_level - a.access_level
				)"
				:key="user.id"
				class="flex flex-col text-primary-text"
				:to="{
					name: 'dashboard.user.show',
					params: { id: user.id },
				}">
				<div class="flex flex-row gap-2 justify-between">
					<div class="flex flex-col">
						<div class="text-lg font-bold">
							{{ user.first_name }} {{ user.last_name }}
						</div>
						<div
							class="text-base text-secondary-text flex items-baseline gap-2">
							<span>
								{{ user.username }}
							</span>
							<span class="text-sm">
								{{ user.email }}
							</span>
						</div>
					</div>
					<div class="flex flex-row gap-1">
						<span class="text-sm text-gray-500">Access Level:</span>
						<span class="text-sm font-bold">{{
							accessLevels[user.access_level]?.name
						}}</span>
					</div>
				</div>
			</RouterLink>
		</div>
	</div>
</template>

<style lang="scss" scoped></style>
