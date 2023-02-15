<script setup lang="ts">
import useFlash from "@stores/flashStore";

const flash = useFlash();
</script>

<template>
    <Transition name="fade">
        <template v-if="flash.messages.value.length">
            <div class="pointer-events-none fixed inset-0 z-50 overflow-hidden">
                <TransitionGroup
                    name="fade"
                    class="container relative flex flex-col items-end justify-end gap-4 pt-20"
                    tag="div"
                >
                    <div
                        v-for="flashMessage in flash.messages.value"
                        :key="flashMessage.id"
                        class="pointer-events-auto left-3 right-3 top-20 flex flex-row items-center justify-between gap-2 overflow-hidden rounded-md p-4 font-bold sm:left-auto"
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
                </TransitionGroup>
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
