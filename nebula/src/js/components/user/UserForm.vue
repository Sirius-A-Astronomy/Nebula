<script setup lang="ts">
import { ref, type Ref, onMounted, watch, computed, reactive } from "vue";

import type { User } from "@stores/userStore";

import {
	validateUsername,
	validatePassword,
	validatePasswordConfirmation,
	validateEmail,
} from "@components/user/userValidation";

import { accessLevels } from "@stores/userStore";
import { authenticatedUser } from "@/stores/sessionStore";

import type { Updatable } from "@stores/factory/storeFactory";

import useFlashStore from "@/stores/flashStore";

const props = defineProps<{
	user?: User;
	loading?: boolean;
	awaitingResponse?: boolean;
	submitText?: string;
}>();

const emit = defineEmits<{
	(event: "cancel"): void;
	(event: "submit", user: Updatable<User>): void;
}>();

const values: Updatable<User> = reactive(
	props.user || {
		first_name: "",
		last_name: "",
		username: "",
		email: "",
		access_level: 0,
	}
);

const password = reactive({
	value: "",
	confirmation: "",
});

const errors = reactive({
	first_name: "",
	last_name: "",
	username: "",
	email: "",
	access_level: "",
	password: "",
	password_confirmation: "",
});

const validatePasswordInput = () => {
	const validPassword = validatePassword(
		password.value,
		password.confirmation
	);
	console.log(validPassword);

	errors.password = validPassword.message;
};

const validatePasswordConfirmationInput = () => {
	const validPasswordConfirmation = validatePasswordConfirmation(
		password.value,
		password.confirmation
	);

	errors.password_confirmation = validPasswordConfirmation.message;
};

const submit = () => {
	if (!props.user) {
		const validPassword = validatePassword(
			password.value,
			password.confirmation
		);

		if (!validPassword.valid) {
			errors.password = validPassword.message;
		}
	}

	emit("submit", values);
};
</script>

<template>
	<div class="flex flex-row justify-between items-center">
		<h1 class="text-3xl">{{ props.user ? "Edit" : "Create" }} User</h1>

		<button
			@click="emit('cancel')"
			class="px-4 py-2 bg-primary-active text-primary-bg rounded-md font-bold hover:text-primary-text">
			Cancel
		</button>
	</div>

	<form class="flex flex-col gap-2" @submit.prevent="submit">
		<div class="flex flex-row gap-1">
			<div class="flex flex-col gap-2">
				<label for="first_name" class="text-xl font-bold"
					>First Name</label
				>
				<input
					type="text"
					name="first_name"
					id="first_name"
					autocomplete="given-name"
					class="border-2 focus:border-primary-active border-primary-bg px-2 py-1 rounded-md focus:outline-none transition-colors bg-secondary-bg focus:bg-tertiary-bg focus:ring-primary-active"
					v-model="values.first_name" />
				<p v-if="errors.first_name" class="text-red-500 text-sm">
					{{ errors.first_name }}
				</p>
			</div>

			<div class="flex flex-col gap-2">
				<label for="last_name" class="text-xl font-bold"
					>Last Name</label
				>
				<input
					type="text"
					name="last_name"
					id="last_name"
					autocomplete="family-name"
					class="border-2 focus:border-primary-active border-primary-bg px-2 py-1 rounded-md focus:outline-none transition-colors bg-secondary-bg focus:bg-tertiary-bg focus:ring-primary-active"
					v-model="values.last_name" />
				<p v-if="errors.last_name" class="text-red-500 text-sm">
					{{ errors.last_name }}
				</p>
			</div>
		</div>

		<div class="flex flex-col gap-2">
			<label for="username" class="text-xl font-bold">Username</label>
			<input
				type="text"
				name="username"
				id="username"
				autocomplete="username"
				class="border-2 focus:border-primary-active border-primary-bg px-2 py-1 rounded-md focus:outline-none transition-colors bg-secondary-bg focus:bg-tertiary-bg focus:ring-primary-active"
				v-model="values.username" />
			<p v-if="errors.username" class="text-red-500 text-sm">
				{{ errors.username }}
			</p>
		</div>

		<!-- Password and password confirmation -->

		<div class="flex flex-col gap-2" v-if="!user">
			<label for="password" class="text-xl font-bold">Password</label>
			<input
				type="password"
				name="password"
				id="password"
				class="border-2 focus:border-primary-active border-primary-bg px-2 py-1 rounded-md focus:outline-none transition-colors bg-secondary-bg focus:bg-tertiary-bg focus:ring-primary-active"
				autocomplete="new-password"
				v-model="password.value"
				@input="validatePasswordInput" />
			<p v-if="errors.password" class="text-red-500 text-sm">
				{{ errors.password }}
			</p>

			<label for="password_confirmation" class="text-xl font-bold"
				>Password Confirmation</label
			>
			<input
				type="password"
				name="password_confirmation"
				id="password_confirmation"
				class="border-2 focus:border-primary-active border-primary-bg px-2 py-1 rounded-md focus:outline-none transition-colors bg-secondary-bg focus:bg-tertiary-bg focus:ring-primary-active"
				autocomplete="new-password"
				v-model="password.confirmation"
				@input="validatePasswordConfirmationInput" />
			<p v-if="errors.password_confirmation" class="text-red-500 text-sm">
				{{ errors.password_confirmation }}
			</p>
		</div>

		<div class="flex flex-col gap-2">
			<label for="email" class="text-xl font-bold">Email</label>
			<input
				type="email"
				name="email"
				id="email"
				class="border-2 focus:border-primary-active border-primary-bg px-2 py-1 rounded-md focus:outline-none transition-colors bg-secondary-bg focus:bg-tertiary-bg focus:ring-primary-active"
				v-model="values.email" />
			<p v-if="errors.email" class="text-red-500 text-sm">
				{{ errors.email }}
			</p>
		</div>

		<div class="flex flex-col gap-2">
			<label for="access_level" class="text-xl font-bold"
				>Access Level</label
			>
			<div>
				<select
					name="access_level"
					id="access_level"
					class="border-2 focus:border-primary-active border-primary-bg px-2 py-1 rounded-md focus:outline-none transition-colors bg-secondary-bg focus:bg-tertiary-bg focus:ring-primary-active"
					v-model="values.access_level">
					<option value="" disabled selected>
						Select an access level
					</option>
					<option
						v-for="accessLevel in accessLevels"
						:value="accessLevel.value"
						:disabled="
							(accessLevel.value >=
								authenticatedUser.access_level &&
								authenticatedUser.access_level !==
									accessLevels.find(
										(accessLevel) =>
											accessLevel.name === 'Maintainer'
									)?.value) ||
							user?.id === authenticatedUser.id
						"
						:key="accessLevel.value">
						{{ accessLevel.name }}
					</option>
				</select>

				<p
					v-if="user?.id === authenticatedUser.id"
					class="text-tertiary-text text-sm">
					Note: You cannot change your own access level.
				</p>
			</div>
		</div>

		<button
			type="submit"
			class="px-4 py-2 bg-primary-clr text-on-primary-text rounded-md font-bold hover:bg-primary-active hover:text-primary-bg transition-colors"
			:disabled="loading || awaitingResponse">
			{{
				awaitingResponse
					? "Loading..."
					: props.submitText
					? props.submitText
					: "Submit"
			}}
		</button>
	</form>
</template>

<style lang="scss" scoped></style>
