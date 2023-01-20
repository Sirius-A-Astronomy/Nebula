<script setup lang="ts">
import UserForm from "@components/user/UserForm.vue";
import { ref } from "vue";

import { useRouter } from "vue-router";
import useFlash from "@stores/flashStore";

import { userStore } from "@stores/userStore";
import type { User, NewUser } from "@stores/userStore";
import type { Updatable, New } from "@/stores/factory/storeFactory";

const router = useRouter();
const flash = useFlash();

const awaitingResponse = ref(false);

const submitUser = async (user: NewUser) => {
	awaitingResponse.value = true;
	const response = await userStore.actions.create(user);
	awaitingResponse.value = false;

	if (response.status !== 201) {
		flash.add(`Failed to create user: ${response.message}`, "error");
		return;
	}
	const data = response.data as User;

	router.push({
		name: "dashboard.user.show",
		params: { id: data.id },
	});

	flash.add(
		`User '${data.first_name} ${data.last_name}' created successfully`,
		"success"
	);
	return;
};
</script>

<template>
	<div>
		<UserForm
			submitText="Create"
			@submit="submitUser"
			:awaiting-response="awaitingResponse"
			@cancel="$router.back()" />
	</div>
</template>

<style lang="scss" scoped></style>
