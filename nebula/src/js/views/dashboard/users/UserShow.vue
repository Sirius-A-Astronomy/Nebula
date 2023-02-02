<script setup lang="ts">
import { ref, onMounted, watch, computed } from "vue";
import {
    userStore,
    accessLevels,
    getAccessLevelValue,
} from "@stores/userStore";
import type { User } from "@stores/userStore";
import UserForm from "@/components/user/UserForm.vue";

import type { Updatable } from "@stores/factory/storeFactory";
import useFlashStore from "@stores/flashStore";

import { useRouter } from "vue-router";
import api from "@/http/api";
import useModalStore from "@/stores/modalStore";
import { authenticatedUser } from "@/stores/sessionStore";

const flash = useFlashStore();
const modal = useModalStore();

const props = defineProps<{
    id: string;
}>();

const user = computed(() => userStore.getters.byId(props.id).value);

const router = useRouter();

watch(props, () => {
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
            `Failed to delete user '${user.value.first_name} ${user.value.last_name}': ${response.message}`,
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

const canEdit = computed(() => {
    if (!user.value) {
        return false;
    }

    if (!authenticatedUser.value) {
        return false;
    }

    const isMaintainer =
        authenticatedUser.value.access_level ===
        getAccessLevelValue("maintainer");

    const hasHigherAccessLevel =
        authenticatedUser.value.access_level > user.value.access_level;

    const isSameUser = authenticatedUser.value.id === user.value.id;

    return isMaintainer || hasHigherAccessLevel || isSameUser;
});

onMounted(loadData);
</script>

<template>
    <div v-if="loading">Loading...</div>

    <template v-else>
        <template v-if="!editting">
            <div class="flex flex-row items-baseline justify-between">
                <h1 class="text-3xl">
                    {{ user.first_name }} {{ user.last_name }}
                </h1>

                <div class="flex flex-row gap-1">
                    <button
                        v-if="canEdit"
                        @click="editting = true"
                        class="rounded-md bg-primary-active px-4 py-2 font-bold text-primary-bg"
                    >
                        Edit
                    </button>

                    <button
                        v-if="
                            canEdit &&
                            user.access_level >= getAccessLevelValue('admin')
                        "
                        @click="onDeleteClicked"
                        class="rounded-md bg-alert-warning px-4 py-2 font-bold text-alert-warning-text"
                    >
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
                v-if="
                    canEdit && user.access_level >= getAccessLevelValue('admin')
                "
                @click="onResetPasswordClicked"
                class="rounded-md bg-alert-warning px-4 py-2 text-alert-warning-text"
            >
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
            @submit="updateUser"
        />
    </template>
</template>

<style lang="scss" scoped></style>
