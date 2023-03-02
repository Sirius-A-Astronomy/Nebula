<script setup lang="ts">
import { reactive, ref } from "vue";

import { authenticatedUser } from "@stores/sessionStore";

import useFlashStore from "@stores/flashStore";
import { useRouter } from "vue-router";

import { debounce } from "throttle-debounce";

import {
    validatePassword,
    validateEmail,
    validateFirstName,
    validateLastName,
    validatePasswordConfirmation,
} from "@components/user/userValidation";
import { userStore } from "@/stores/userStore";

const flash = useFlashStore();
const router = useRouter();

const user = authenticatedUser;

const values = ref({
    first_name: user.value?.first_name ?? "",
    last_name: user.value?.last_name ?? "",
    email: user.value?.email ?? "",
    current_password: "",
    new_password: "",
    new_password_confirmation: "",
});

const errors: Record<string, string[]> = reactive({
    first_name: [],
    last_name: [],
    email: [],
    access_level: [],
    current_password: [],
    new_password: [],
    new_password_confirmation: [],
});

const validateNewPasswordInput = debounce(500, () => {
    const validPasswordConfirmation = validatePassword(
        values.value.new_password,
        values.value.new_password_confirmation
    );

    if (!validPasswordConfirmation.valid) {
        errors.new_password = [validPasswordConfirmation.message];
        return;
    }

    if (!values.value.current_password) {
        errors.current_password = ["Current password is required"];
    }
    errors.new_password = [];
    errors.new_password_confirmation = [];
});

const validateNewPasswordConfirmationInput = debounce(500, () => {
    const validPasswordConfirmation = validatePasswordConfirmation(
        values.value.new_password,
        values.value.new_password_confirmation
    );

    if (!validPasswordConfirmation.valid) {
        errors.new_password_confirmation = [validPasswordConfirmation.message];
        return;
    }

    if (!values.value.current_password) {
        errors.current_password = ["Current password is required"];
        return;
    }
    errors.new_password_confirmation = [];
});

const validateEmailInput = debounce(500, async () => {
    const validEmail = await validateEmail(values.value.email);

    if (!validEmail.valid) errors.email = [validEmail.message];
    else errors.email = [];
});

const validateFirstNameInput = debounce(500, () => {
    const validFirstName = validateFirstName(values.value.first_name);

    if (!validFirstName.valid) errors.first_name = [validFirstName.message];
    else errors.first_name = [];
});

const validateLastNameInput = debounce(500, () => {
    const validLastName = validateLastName(values.value.last_name);

    errors.last_name = [validLastName.message];
});

const awaitingResponse = ref(false);

const submit = async () => {
    awaitingResponse.value = true;
    const response = await userStore.actions.update({
        ...values.value,
        id: user.value?.id,
    });
    awaitingResponse.value = false;

    if (!response.ok) {
        flash.add(
            `Failed to update user '${user.value?.first_name} ${user.value?.last_name}': ${response.message}`,
            "error"
        );

        const data = response.data as { errors: Record<string, string[]> };

        if (data.errors) {
            for (const [key, value] of Object.entries(data.errors)) {
                errors[key] = value;
            }
        }
        return;
    }

    const updatedUser = response.data;

    flash.add(`Profile updated successfully`, "success");

    authenticatedUser.value = updatedUser;

    router.push({ name: "user.profile" });
};
</script>

<template>
    <main id="content" class="mx-auto max-w-xl py-4">
        <h1 class="text-3xl font-bold">Edit Profile</h1>
        <form class="flex flex-col gap-2" @submit.prevent="submit">
            <div class="grid grid-cols-2 gap-1">
                <div class="flex flex-col gap-2">
                    <label for="first_name" class="text-xl font-bold"
                        >First Name</label
                    >
                    <input
                        type="text"
                        name="first_name"
                        id="first_name"
                        autocomplete="given-name"
                        @input="validateFirstNameInput"
                        class="rounded-md border-2 border-primary-bg bg-secondary-bg px-2 py-1 transition-colors focus:border-primary-active focus:bg-tertiary-bg focus:outline-none focus:ring-primary-active"
                        v-model="values.first_name"
                    />
                    <ul v-if="errors.first_name" class="text-sm text-red-500">
                        <li v-for="error in errors.first_name" :key="error">
                            {{ error }}
                        </li>
                    </ul>
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
                        @input="validateLastNameInput"
                        class="rounded-md border-2 border-primary-bg bg-secondary-bg px-2 py-1 transition-colors focus:border-primary-active focus:bg-tertiary-bg focus:outline-none focus:ring-primary-active"
                        v-model="values.last_name"
                    />
                    <ul v-if="errors.last_name" class="text-sm text-red-500">
                        <li v-for="error in errors.last_name" :key="error">
                            {{ error }}
                        </li>
                    </ul>
                </div>
            </div>

            <div class="flex flex-col gap-2">
                <label for="email" class="text-xl font-bold">Email</label>
                <input
                    type="email"
                    name="email"
                    id="email"
                    autocomplete="email"
                    @input="validateEmailInput"
                    class="rounded-md border-2 border-primary-bg bg-secondary-bg px-2 py-1 transition-colors focus:border-primary-active focus:bg-tertiary-bg focus:outline-none focus:ring-primary-active"
                    v-model="values.email"
                />
                <ul v-if="errors.email" class="text-sm text-red-500">
                    <li v-for="error in errors.email" :key="error">
                        {{ error }}
                    </li>
                </ul>

                <p class="text-sm">
                    Note: Changing your email address will require you to verify
                    your current password.
                </p>
            </div>

            <!-- Password and password confirmation -->

            <!-- Hidden username field for autocomplete and password managers -->
            <input
                type="hidden"
                name="username"
                :value="user.email"
                autocomplete="username"
            />

            <div class="flex flex-col gap-2">
                <label for="password" class="text-xl font-bold"
                    >Current Password</label
                >
                <input
                    type="password"
                    name="password"
                    id="password"
                    class="rounded-md border-2 border-primary-bg bg-secondary-bg px-2 py-1 transition-colors focus:border-primary-active focus:bg-tertiary-bg focus:outline-none focus:ring-primary-active"
                    autocomplete="current-password"
                    v-model="values.current_password"
                />
                <ul v-if="errors.current_password" class="text-sm text-red-500">
                    <li v-for="error in errors.current_password" :key="error">
                        {{ error }}
                    </li>
                </ul>

                <label for="new_password" class="text-xl font-bold"
                    >New Password</label
                >
                <input
                    type="password"
                    name="new_password"
                    id="new_password"
                    class="rounded-md border-2 border-primary-bg bg-secondary-bg px-2 py-1 transition-colors focus:border-primary-active focus:bg-tertiary-bg focus:outline-none focus:ring-primary-active"
                    autocomplete="new-password"
                    v-model="values.new_password"
                    @input="validateNewPasswordInput"
                />
                <ul v-if="errors.new_password" class="text-sm text-red-500">
                    <li v-for="error in errors.new_password" :key="error">
                        {{ error }}
                    </li>
                </ul>
            </div>

            <div class="flex flex-col gap-2" v-if="values.new_password">
                <label for="new_password_confirmation" class="text-xl font-bold"
                    >New Password Confirmation</label
                >
                <input
                    type="password"
                    name="new_password_confirmation"
                    id="new_password_confirmation"
                    class="rounded-md border-2 border-primary-bg bg-secondary-bg px-2 py-1 transition-colors focus:border-primary-active focus:bg-tertiary-bg focus:outline-none focus:ring-primary-active"
                    autocomplete="new-password"
                    v-model="values.new_password_confirmation"
                    @input="validateNewPasswordConfirmationInput"
                />
                <ul
                    v-if="errors.new_password_confirmation"
                    class="text-sm text-red-500"
                >
                    <li
                        v-for="error in errors.new_password_confirmation"
                        :key="error"
                    >
                        {{ error }}
                    </li>
                </ul>
            </div>

            <button
                type="submit"
                class="rounded-md bg-primary-clr px-4 py-2 font-bold text-on-primary-text transition-colors hover:bg-primary-active hover:text-primary-bg"
                :disabled="awaitingResponse"
            >
                {{ awaitingResponse ? "Loading..." : "Submit" }}
            </button>
        </form>
    </main>
</template>

<style lang="scss" scoped></style>
