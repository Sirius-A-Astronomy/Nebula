<script setup lang="ts">
import useFlash from "@stores/flashStore";

const flash = useFlash();
</script>

<template>
    <Transition name="fade">
        <template v-if="flash.messages.value.length">
            <div class="absolute top-10 right-0 z-50 m-4 flex flex-col gap-4">
                <transition-group name="fade">
                    <div
                        v-for="flashMessage in flash.messages.value"
                        :key="flashMessage.id"
                        class="flex flex-row items-center justify-between gap-2 rounded-md p-4 font-bold"
                        :class="{
                            'bg-alert-error text-alert-error-text':
                                flashMessage.type === 'error',
                            'text-alert-succes-text bg-alert-success':
                                flashMessage.type === 'success',
                            'bg-alert-warning text-alert-warning-text':
                                flashMessage.type === 'warning',
                            'bg-alert-info text-alert-info-text':
                                flashMessage.type === 'info',
                        }"
                    >
                        <span>{{ flashMessage.message }}</span>
                        <button @click="flash.remove(flashMessage.id)">
                            <svg
                                xmlns="http://www.w3.org/2000/svg"
                                height="24"
                                width="24"
                                fill="currentcolor"
                            >
                                <path
                                    d="M6.4 19 5 17.6l5.6-5.6L5 6.4 6.4 5l5.6 5.6L17.6 5 19 6.4 13.4 12l5.6 5.6-1.4 1.4-5.6-5.6Z"
                                />
                            </svg>
                        </button>
                    </div>
                </transition-group>
            </div>
        </template>
    </Transition>
</template>

<style lang="scss" scoped>
.fade-enter-active,
.fade-move,
.fade-leave-active {
    transition: all 0.5s;
}

.fade-enter-from,
.fade-leave-to {
    opacity: 0;
}

.fade-enter-from {
    transform: translateY(10px);
}

.fade-leave-to {
    transform: translateY(-10px);
}

.fade-leave-active {
    position: absolute;
}

.fade-enter-to,
.fade-leave-from {
    opacity: 1;
}
</style>
