<script setup lang="ts">
import { ref, type Ref, onMounted, watch, computed } from "vue";
import { userStore, type User, accessLevels } from "@/stores/userStore";
import UserForm from "@/components/user/UserForm.vue";

import type { Updatable } from "@stores/factory/storeFactory";
import useFlashStore from "@/stores/flashStore";

import { useRouter } from "vue-router";
import api from "@/http/api";
import useModalStore from "@/stores/modalStore";

const flash = useFlashStore();
const modal = useModalStore();

const props = defineProps<{
	id: string;
}>();

const user = computed(() => userStore.getters.byId(props.id).value);

const router = useRouter();

watch(props, (value) => {
	loading.value = true;
	loadData();
});

const loading = ref(true);

const loadData = async () => {
	if (!user.value) {
		await userStore.actions.getById(props.id);
	}

	loading.value = false;
};

const awaitingResponse = ref(false);

const updateUser = async (user: Updatable<User>) => {
	awaitingResponse.value = true;
	const response = await userStore.actions.update(user);
	awaitingResponse.value = false;

	if (response.status !== 200) {
		flash.add(
			`Failed to update user '${user.first_name} ${user.last_name}': ${response.message}`,
			"error"
		);
		return;
	}
	flash.add(
		`User '${user.first_name} ${user.last_name}' updated successfully`,
		"success"
	);
	editting.value = false;
};

const confirmDelete = ref(false);

const onDeleteClicked = () => {
	modal.add({
		title: "Delete User",
		body: `Are you sure you want to delete user '${user.value?.first_name} ${user.value?.last_name}'?`,
		actions: [
			{
				text: "Cancel",
				type: "neutral",
			},
			{
				text: "Delete User",
				action: deleteUser,
				type: "danger",
			},
		],
	});
};

const deleteUser = async () => {
	awaitingResponse.value = true;
	const response = await userStore.actions.delete(props.id);
	awaitingResponse.value = false;

	if (response.status !== 200) {
		flash.add(
			`Failed to delete uesr '${user.value.first_name} ${user.value.last_name}': ${response.message}`,
			"error"
		);
		return;
	}
	router.push({ name: "dashboard.user.index" });
	const data = response.data as User;
	flash.add(
		`Course '${data.first_name} ${data.last_name}' deleted successfully`,
		"success"
	);
};

const onResetPasswordClicked = () => {
	modal.add({
		title: "Reset Password",
		body: `Are you sure you want to reset ${user.value.first_name}'s password?`,
		actions: [
			{
				text: "Cancel",
				type: "neutral",
			},
			{
				text: "Reset Password",
				action: resetPassword,
				type: "danger",
			},
		],
	});
};

const resetPassword = async () => {
	awaitingResponse.value = true;
	const response = await api.post(`/users/reset_password`, {
		uuid: props.id,
	});
	awaitingResponse.value = false;

	if (response.status !== 200) {
		flash.add(
			`Failed to reset password for user '${user.value.first_name} ${user.value.last_name}': ${response.message}`,
			"error"
		);
		return;
	}

	const data = response.data as { password: string };

	flash.add(
		`Password for user '${user.value.first_name} ${user.value.last_name}' reset successfully`,
		"success"
	);

	modal.add({
		title: "Password Reset",
		body: `The new password for ${user.value.first_name} is "${data.password}". 
        Please note that this password is only shown once.`,
		actions: [
			{
				text: "Close",
				type: "positive",
			},
		],
	});
};

const editting = ref(false);

onMounted(loadData);
</script>

<template>
	<div v-if="loading">Loading...</div>

	<template v-else>
		<template v-if="!editting">
			<div class="flex flex-row justify-between items-baseline">
				<h1 class="text-3xl">
					{{ user.first_name }} {{ user.last_name }}
				</h1>

				<div class="flex flex-row gap-1">
					<button
						@click="editting = true"
						class="px-4 py-2 bg-primary-active text-primary-bg rounded-md font-bold">
						Edit
					</button>

					<button
						@click="onDeleteClicked"
						class="px-4 py-2 bg-alert-warning text-alert-warning-text rounded-md font-bold">
						Delete
					</button>
				</div>
			</div>

			<div class="flex flex-col">
				<div class="flex flex-row items-center gap-1">
					<span class="font-bold">Username: </span>
					<span>{{ user.username }}</span>
				</div>
				<div class="flex flex-row items-center gap-1">
					<span class="font-bold">Email: </span>
					<span>{{ user.email }}</span>
				</div>

				<div class="flex flex-row items-center gap-1">
					<span class="font-bold">Access Level: </span>
					<span>{{ accessLevels[user.access_level]?.name }}</span>
				</div>

				<div class="flex flex-row items-center gap-1">
					<span class="font-bold">Account created</span>
					<span>{{ user.created_at }}</span>
				</div>
			</div>

			<button
				@click="onResetPasswordClicked"
				class="rounded-md bg-alert-warning text-alert-warning-text px-4 py-2">
				Reset Password
			</button>

			<!-- show new password -->
		</template>

		<UserForm
			v-if="editting"
			:user="user"
			submitText="Update"
			@cancel="editting = false"
			:awaiting-response="awaitingResponse"
			@submit="updateUser" />
	</template>
</template>

<style lang="scss" scoped></style>