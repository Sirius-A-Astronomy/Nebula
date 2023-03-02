<script setup lang="ts">
import { computed } from "vue";
import useModalStore from "@stores/modalStore";
import CloseIcon from "@/components/icons/CloseIcon.vue";

const modal = useModalStore();

const currentModal = computed(() => {
    if (modal.modals.value.length === 0) return null;
    return modal.modals.value[0];
});

const executeAction = (action: any) => {
    const actionModal = currentModal.value;
    if (!actionModal) return;
    modal.remove({ id: actionModal.id });
    action.action?.();
};
</script>

<template>
    <div
        class="fixed z-50 h-screen w-screen bg-black bg-opacity-20"
        v-if="currentModal"
    >
        <div class="flex h-full w-full items-center justify-center">
            <div
                class="relative flex w-96 flex-col gap-2 rounded-md bg-primary-bg px-4 py-2 shadow-lg"
                v-if="currentModal"
            >
                <div class="flex w-full flex-row items-start justify-between">
                    <h1 class="text-2xl">{{ currentModal.title }}</h1>
                    <button
                        class="flex items-center justify-center rounded-sm bg-secondary-bg font-bold text-primary-text shadow-sm hover:text-primary-text"
                        @click="modal.remove({ id: currentModal!.id })"
                    >
                        <CloseIcon height="20" width="20" />
                    </button>
                </div>
                <p>{{ currentModal.body }}</p>
                <div class="flex flex-row justify-between gap-4">
                    <div class="positive-actions">
                        <button
                            v-for="action in currentModal.actions?.filter(
                                (action) =>
                                    ['positive', 'danger', 'warning'].includes(
                                        action.type ?? ''
                                    )
                            )"
                            :key="action.text"
                            class="rounded-md px-4 py-2 font-bold hover:font-bold"
                            :class="{
                                'bg-alert-warning text-alert-warning-text':
                                    action.type === 'warning' ||
                                    action.type === 'danger',
                                'bg-alert-success text-alert-success-text':
                                    action.type === 'positive',
                            }"
                            @click="executeAction(action)"
                        >
                            {{ action.text }}
                        </button>
                    </div>

                    <div>
                        <button
                            v-for="action in currentModal.actions?.filter(
                                (action) =>
                                    ['negative', 'neutral'].includes(
                                        action.type ?? 'neutral'
                                    )
                            )"
                            :key="action.text"
                            class="rounded-md px-4 py-2 font-bold hover:shadow-md"
                            :class="{
                                'bg-alert-warning text-alert-warning-text':
                                    action.type === 'negative',
                                'bg-alert-info text-alert-info-text':
                                    action.type === 'neutral',
                            }"
                            @click="executeAction(action)"
                        >
                            {{ action.text }}
                        </button>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<style lang="scss" scoped></style>
