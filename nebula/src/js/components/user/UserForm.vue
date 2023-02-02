<script setup lang="ts">
import { reactive } from "vue";

import {
    type User,
    type NewUser,
    getAccessLevelValue,
} from "@stores/userStore";

import {
    validatePassword,
    validatePasswordConfirmation,
} from "@components/user/userValidation";

import { accessLevels } from "@stores/userStore";
import { authenticatedUser } from "@/stores/sessionStore";

import type { New, Updatable } from "@stores/factory/storeFactory";

const props = defineProps<{
    user?: User;
    loading?: boolean;
    awaitingResponse?: boolean;
    submitText?: string;
}>();

const emit = defineEmits<{
    (event: "cancel"): void;
    (event: "submitNewUser", user: NewUser): void;
    (event: "submitUpdateUser", user: Updatable<User>): void;
}>();

const values = reactive({
    first_name: props.user?.first_name ?? "",
    last_name: props.user?.last_name ?? "",
    username: props.user?.username ?? "",
    email: props.user?.email ?? "",
    access_level: props.user?.access_level ?? 0,
});

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

        emit("submitNewUser", {
            ...(values as New<User>),
            password: password.value,
            password_confirmation: password.confirmation,
        });

        return;
    }

    emit("submitUpdateUser", values);
};
</script>

<template>
    <div class="flex flex-row items-center justify-between">
        <h1 class="text-3xl">{{ props.user ? "Edit" : "Create" }} User</h1>

        <button
            @click="emit('cancel')"
            class="rounded-md bg-primary-active px-4 py-2 font-bold text-primary-bg hover:text-primary-text"
        >
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
                    class="rounded-md border-2 border-primary-bg bg-secondary-bg px-2 py-1 transition-colors focus:border-primary-active focus:bg-tertiary-bg focus:outline-none focus:ring-primary-active"
                    v-model="values.first_name"
                />
                <p v-if="errors.first_name" class="text-sm text-red-500">
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
                    class="rounded-md border-2 border-primary-bg bg-secondary-bg px-2 py-1 transition-colors focus:border-primary-active focus:bg-tertiary-bg focus:outline-none focus:ring-primary-active"
                    v-model="values.last_name"
                />
                <p v-if="errors.last_name" class="text-sm text-red-500">
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
                class="rounded-md border-2 border-primary-bg bg-secondary-bg px-2 py-1 transition-colors focus:border-primary-active focus:bg-tertiary-bg focus:outline-none focus:ring-primary-active"
                v-model="values.username"
            />
            <p v-if="errors.username" class="text-sm text-red-500">
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
                class="rounded-md border-2 border-primary-bg bg-secondary-bg px-2 py-1 transition-colors focus:border-primary-active focus:bg-tertiary-bg focus:outline-none focus:ring-primary-active"
                autocomplete="new-password"
                v-model="password.value"
                @input="validatePasswordInput"
            />
            <p v-if="errors.password" class="text-sm text-red-500">
                {{ errors.password }}
            </p>

            <label for="password_confirmation" class="text-xl font-bold"
                >Password Confirmation</label
            >
            <input
                type="password"
                name="password_confirmation"
                id="password_confirmation"
                class="rounded-md border-2 border-primary-bg bg-secondary-bg px-2 py-1 transition-colors focus:border-primary-active focus:bg-tertiary-bg focus:outline-none focus:ring-primary-active"
                autocomplete="new-password"
                v-model="password.confirmation"
                @input="validatePasswordConfirmationInput"
            />
            <p v-if="errors.password_confirmation" class="text-sm text-red-500">
                {{ errors.password_confirmation }}
            </p>
        </div>

        <div class="flex flex-col gap-2">
            <label for="email" class="text-xl font-bold">Email</label>
            <input
                type="email"
                name="email"
                id="email"
                class="rounded-md border-2 border-primary-bg bg-secondary-bg px-2 py-1 transition-colors focus:border-primary-active focus:bg-tertiary-bg focus:outline-none focus:ring-primary-active"
                v-model="values.email"
            />
            <p v-if="errors.email" class="text-sm text-red-500">
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
                    class="rounded-md border-2 border-primary-bg bg-secondary-bg px-2 py-1 transition-colors focus:border-primary-active focus:bg-tertiary-bg focus:outline-none focus:ring-primary-active"
                    :disabled="
                        (user?.access_level ?? 0) >=
                            authenticatedUser.access_level &&
                        authenticatedUser.access_level !==
                            getAccessLevelValue('maintainer')
                    "
                    v-model="values.access_level"
                >
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
                                    getAccessLevelValue('maintainer')) ||
                            user?.id === authenticatedUser.id
                        "
                        :key="accessLevel.value"
                    >
                        {{ accessLevel.name }}
                    </option>
                </select>

                <p
                    v-if="user?.id === authenticatedUser.id"
                    class="text-sm text-tertiary-text"
                >
                    Note: You cannot change your own access level.
                </p>
                <p
                    v-else-if="
                        (user?.access_level ?? 0) >=
                            authenticatedUser.access_level &&
                        authenticatedUser.access_level !==
                            getAccessLevelValue('maintainer')
                    "
                    class="text-sm text-tertiary-text"
                >
                    Note: You cannot change the access level of a user with an
                    access level equal to or higher than your own.
                </p>
            </div>
        </div>

        <button
            type="submit"
            class="rounded-md bg-primary-clr px-4 py-2 font-bold text-on-primary-text transition-colors hover:bg-primary-active hover:text-primary-bg"
            :disabled="loading || awaitingResponse"
        >
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
